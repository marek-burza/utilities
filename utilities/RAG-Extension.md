# Extension: LLM fallback when the RAG match is weak

RRF scores are uncalibrated (just `1/(k+rank)` sums), so the fused score itself is useless as a confidence threshold. To recognize a weak top match you have to look at the underlying signals before fusion. Options, roughly in order of robustness:

## 1. Cosine similarity floor on the dense side
With normalized embeddings, dense cosine is in `[-1, 1]` and has a roughly stable meaning per embedder. For Qwen3-Embedding on short titles, "clearly relevant" is typically >0.55, "clearly off-topic" <0.35, with a fuzzy band in between. Pick a floor empirically (one afternoon of eyeballing 20-30 assignments against the corpus) and fall back to LLM if `top_dense_score < floor`. Simplest, most reliable single signal.

## 2. Margin between top-1 and top-2
If the best match is much better than the runner-up, the retriever is confident; if they're tied, it's guessing. Compute `dense[top1] - dense[top2]`; require >0.05. Catches the case where the corpus has nothing relevant and several irrelevant chunks score similarly.

## 3. Agreement between dense and BM25
If both rankers put the same chunk at #1 (or both put it in their top-3), trust it. If their #1s disagree entirely, that's a strong "neither is confident" signal. Cheap and parameter-light.

## 4. Cross-encoder as a gate, not a reranker
The only option that gives a *calibrated* relevance score. `bge-reranker-v2-m3` outputs a logit you can sigmoid into a 0-1 probability; >0.5 is the standard threshold. Most reliable signal but adds the 568M model the base plan was trying to avoid. If a real confidence number is ever needed, this is how to get it.

## 5. Ask the LLM to judge
Send `(assignment, chunk_title, chunk_content)` to the solver LLM with "does this chunk answer the assignment? yes/no", fall back to generation on no. Adds latency but reuses infrastructure already running. Reasonable when adding a second model class is undesirable.

## Recommendation for v1: combine (1) and (2)

```python
def top1_with_confidence(self, query):
    dense_scores = self.dense.scores(query)   # cosine, normalized
    fused = rrf([np.argsort(-dense_scores), self.bm25.rank(query)])
    top, second = fused[0], fused[1]
    confident = (
        dense_scores[top] >= 0.55 and
        dense_scores[top] - dense_scores[second] >= 0.05
    )
    return self.chunks[top], confident
```

Then in `solver_worker_rag`, if `not confident` and an LLM client was also configured, hand off to the LLM path. Surface the thresholds as `--rag-min-score` / `--rag-min-margin` flags so they can be tuned without code changes.

If this turns out to be flaky in practice, escalate to (4): the cross-encoder is the only path to a *principled* threshold.

## CLI implications

- `--solve-mode=rag` becomes "RAG with LLM fallback" rather than "RAG only" when a `--solve-model` is also specified. If only RAG is wanted, the user can pass `--solve-model ''` (or a new `--no-solve-fallback` flag) to disable the fallback and accept whatever RAG returns.
- The solve `llama-server` must then be launched even in RAG mode (revert that part of the base plan's section 1) whenever the fallback is enabled.
- Log which path served each assignment (`[rag]` vs `[llm fallback: low score 0.42]`) so threshold tuning has a paper trail.
