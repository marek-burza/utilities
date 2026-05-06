# Plan: `--solve-mode` with RAG retrieval

Adds a retrieval path to `souffleur.py` so that, instead of asking an LLM to *generate* a solution, the solver can *look up* a pre-written solution from a corpus of text files. Useful when the assignments are drawn from a known question bank (interviews, exam prep, FAQ).

## 1. CLI surface

Two new options on `main()`:

```python
class SolveMode(str, enum.Enum):
    LLM = 'llm'
    RAG = 'rag'

solve_mode: SolveMode = typer.Option(SolveMode.LLM, '--solve-mode',
    help='How the solver produces a solution: "llm" (generate via LLM) or "rag" (retrieve from --solve-content).')

solve_content: list[str] = typer.Option([], '--solve-content',
    help='Paths to text files used as the RAG corpus. Required when --solve-mode=rag. Repeatable.')
```

Validation in `main()`: if `solve_mode == RAG` and `solve_content` is empty, raise `typer.BadParameter`. When `solve_mode == RAG`, skip launching the solve `llama-server` (drop `solve_model` from `unique_models`).

Dispatch the solver via `match`:

```python
match solve_mode:
    case SolveMode.LLM:
        target = solver_worker_llm   # current solver_worker, renamed
        args = (state, exit, solve_client)
    case SolveMode.RAG:
        target = solver_worker_rag
        args = (state, exit, retriever)
```

## 2. Corpus format and parsing

Each file is split on lines that are exactly `---` (allowing trailing whitespace). Within a chunk:
- `chunk_title`: the first line starting with `# ` (the `# ` is stripped). If missing, the chunk is skipped with a warning.
- `chunk_content`: everything in the chunk except the title line, stripped.

```python
@dataclasses.dataclass
class Chunk:
    title: str
    content: str
    source: str          # file path, for debugging

def load_chunks(paths: list[str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in paths:
        text = pathlib.Path(path).read_text()
        for raw in re.split(r'(?m)^---\s*$', text):
            lines = raw.strip().splitlines()
            title_idx = next((i for i, l in enumerate(lines) if l.startswith('# ')), None)
            if title_idx is None:
                continue
            title = lines[title_idx][2:].strip()
            content = '\n'.join(lines[:title_idx] + lines[title_idx+1:]).strip()
            if title and content:
                chunks.append(Chunk(title, content, path))
    return chunks
```

(Note: the `Chunk` audio dataclass already in the file should be renamed to `AudioChunk` to avoid the name collision.)

## 3. Embedder: which model

All three candidates fit on a small GPU and produce 768-1024-dim vectors. MTEB v2 retrieval scores (higher = better) and approximate CPU/GPU latency for a single short query:

| Model | Dim | MTEB retrieval (approx) | Notes |
|---|---|---|---|
| `intfloat/e5-base-v2` (the released base; "instruct" only exists at `large`) | 768 | ~50 | Mature, requires `query: ` / `passage: ` prefixes. Smallest and fastest. |
| `Qwen/Qwen3-Embedding-0.6B` | 1024 | ~64 (top of leaderboard for <1B) | Best quality by a wide margin. Supports task instructions. ~600M params, needs GPU for snappy latency. |
| `google/embeddinggemma-300m-qat-q8` | 768 | ~58 | Quantized, very small (~300MB on disk), CPU-friendly. Quality between e5-base and Qwen3-0.6B. |

**Recommendation: `Qwen/Qwen3-Embedding-0.6B`.** The corpus is tiny (embed-once at startup), so embedding cost is irrelevant; per-query embedding is one forward pass on a 0.6B model: ~10-20 ms on the same GPU already running `llama-server`. The quality gap over e5-base on technical Q&A retrieval is large enough to matter. If the user is CPU-only, fall back to `embeddinggemma-300m-qat-q8`. Make this configurable:

```python
embed_model: str = typer.Option('Qwen/Qwen3-Embedding-0.6B', '--embed-model', ...)
```

## 4. Embeddings: `sentence-transformers` direct vs `HuggingFaceEmbeddings`

`langchain_huggingface.HuggingFaceEmbeddings` is a thin wrapper around `sentence-transformers`. Pros/cons:

- **Direct `sentence-transformers`**: one fewer dependency, fewer abstraction layers, exact control over `prompt_name` / instruction prefixes (Qwen3 and e5 both need them). Code is shorter.
- **`HuggingFaceEmbeddings`**: integrates with LangChain's `VectorStore` interface (`FAISS.from_texts(...)`), but the project does not otherwise need a `VectorStore` and the corpus is small enough that a dot-product over a numpy matrix is simpler than FAISS.

**Recommendation: use `sentence-transformers` directly, no FAISS.** With <10k chunks (likely <1000), a numpy dot-product is microseconds and avoids two heavy deps. FAISS / `faiss-gpu` would only make sense at >100k vectors.

```python
from sentence_transformers import SentenceTransformer

class DenseIndex:
    def __init__(self, model_id: str, chunks: list[Chunk]) -> None:
        self.model = SentenceTransformer(model_id)
        # Qwen3-Embedding uses an instruction prompt for queries; passages use no prompt.
        self.embeddings = self.model.encode(
            [c.title for c in chunks], normalize_embeddings=True, convert_to_numpy=True,
        )

    def rank(self, query: str) -> np.ndarray:  # returns indices sorted best-first
        q = self.model.encode(
            [query], prompt_name='query', normalize_embeddings=True, convert_to_numpy=True,
        )
        scores = self.embeddings @ q[0]
        return np.argsort(-scores)
```

The embedding key is `chunk_title` (per spec). `chunk_content` is what gets returned, never embedded.

## 5. BM25 lexical index

Use `rank_bm25` (pure Python, ~200 LOC, no native deps). Tokenize with a simple regex: `re.findall(r'\w+', text.lower())`. Index over `chunk_title` (consistent with the dense side: both score against the title, so RRF is comparing like to like).

```python
from rank_bm25 import BM25Okapi

class BM25Index:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.bm25 = BM25Okapi([self._tok(c.title) for c in chunks])

    @staticmethod
    def _tok(s: str) -> list[str]:
        return re.findall(r'\w+', s.lower())

    def rank(self, query: str) -> np.ndarray:
        scores = self.bm25.get_scores(self._tok(query))
        return np.argsort(-scores)
```

## 6. Fusion: RRF vs cross-encoder reranker

Two options:

**(a) Reciprocal Rank Fusion (RRF):** trivially cheap, parameter-free (the standard `k=60`). Combines the two rank lists:
```
score(i) = 1/(k + rank_dense(i)) + 1/(k + rank_bm25(i))
```
Per-query cost: ~zero on top of the two retrievals. This is what the Anthropic course recommends for hybrid retrieval and what production systems mostly use.

**(b) Cross-encoder reranker (`BAAI/bge-reranker-v2-m3`):** take the top-N (say 20) from RRF, then re-score with a cross-encoder that sees `(query, chunk_title)` jointly. Cross-encoders generally lift recall@1 by 5-15 points on hard retrieval but cost one full forward pass per candidate (~568M params, ~50 ms total for N=20 on GPU).

**Recommendation: start with RRF only.** Reasons:
1. The retrieval target is `chunk_title`, which is a short, focused string. Cross-encoders shine when re-ranking long passages where dense embeddings lose detail; for short titles the dense+BM25 hybrid is usually already saturated.
2. Adds a third large model to load, plus the `top-N` plumbing.
3. RRF is one dozen lines of code and trivially debuggable.

Keep the door open: structure `Retriever.search()` so a reranker can be slotted in later behind a `--rerank/--no-rerank` flag without rewriting callers. Do not implement it in v1.

```python
def rrf(rank_lists: list[np.ndarray], k: int = 60) -> np.ndarray:
    n = len(rank_lists[0])
    scores = np.zeros(n)
    for ranks in rank_lists:
        for r, idx in enumerate(ranks):
            scores[idx] += 1.0 / (k + r)
    return np.argsort(-scores)
```

## 7. Retriever wrapper and solver worker

```python
class Retriever:
    def __init__(self, chunks: list[Chunk], embed_model: str) -> None:
        self.chunks = chunks
        self.dense = DenseIndex(embed_model, chunks)
        self.bm25 = BM25Index(chunks)

    def top1(self, query: str) -> Chunk:
        fused = rrf([self.dense.rank(query), self.bm25.rank(query)])
        return self.chunks[fused[0]]


def solver_worker_rag(state, exit, retriever, interval=0.5):
    previous_assignment = ''
    while not exit.is_set():
        _, _, assignment = state.snapshot()
        if assignment == previous_assignment or not assignment:
            time.sleep(interval); continue
        previous_assignment = assignment
        try:
            chunk = retriever.top1(assignment)
            state.update_solution(chunk.content)
            print('\n===\n'); print(state.assignment)
            print('\n--- (matched: ' + chunk.title + ') ---\n')
            print(state.solution); print('\n---\n')
        except Exception as e:
            print(f'RAG solver error: {e}')
```

Build the retriever in `main()` before threads start (so corpus errors fail fast):

```python
retriever = None
if solve_mode == SolveMode.RAG:
    print('Loading embedder and indexing corpus...')
    chunks = load_chunks(solve_content)
    if not chunks:
        raise typer.BadParameter('No valid chunks found in --solve-content files.')
    retriever = Retriever(chunks, embed_model)
    print(f'Indexed {len(chunks)} chunks.')
```

## 8. Dependency additions

Append to the script header `dependencies` block:
- `sentence-transformers`
- `rank-bm25`

Both are pure-Python (sentence-transformers pulls torch, already present). No FAISS.

## 9. Changes summary (files touched)

Only `utilities/scripts/souffleur.py`:
1. Add `SolveMode` enum, rename existing audio `Chunk` to `AudioChunk` (1 line + 4 references).
2. Add new `Chunk`, `load_chunks`, `DenseIndex`, `BM25Index`, `rrf`, `Retriever` (~80 LOC).
3. Rename `solver_worker` → `solver_worker_llm`; add `solver_worker_rag`.
4. Add `--solve-mode`, `--solve-content`, `--embed-model` CLI options.
5. Conditional retriever construction + conditional skip of solve `llama-server` in `main()`.
6. Append two deps to the script header.

## 10. Open questions for the user

- Is the corpus likely to grow past ~10k chunks? If yes, switch the dense side to FAISS (`IndexFlatIP`, still in-memory, still trivial).
- Is the BM25 side meant to also score against `chunk_content` (richer signal, more false positives) instead of `chunk_title`? Default in this plan: title only, matching the dense side.
- Should the matched chunk be reported as-is, or wrapped (e.g. `TL;DR: ...`) so downstream consumers see the same shape as the LLM solver's output? Default: as-is.
