# Utilities

Run `ollama`:

```bash
podman run -it --rm --pull=always --name ollama --device nvidia.com/gpu=all --network host --userns=keep-id -v $HOME/.ollama:/home/ubuntu/.ollama:U -e OLLAMA_HOME=/ollama ollama/ollama
```

Download `qwen3.5:35b`:

```bash
podman exec -it ollama ollama pull qwen3.5:35b
```

Run utilities container use [run.sh](./run.sh)
