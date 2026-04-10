# Utilities

Run `ollama`:

```bash
podman run -it --rm --pull=always --name ollama --device nvidia.com/gpu=all --network host --userns=keep-id -v $HOME/.ollama:$HOME/.ollama:U ollama/ollama
```

Download `qwen3.5:35b`:

```bash
podman exec -it ollama ollama pull qwen3.5:35b
```

Run utilities container:

```bash
podman run -it --rm --pull=always -e TERM=xterm-256color -e HF_TOKEN -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --network host --add-host=host.docker.internal:host-gateway --userns=keep-id --user $(id -u):$(id -g) --device nvidia.com/gpu=all -e PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native -e PIPEWIRE_REMOTE=/run/user/$(id -u)/pipewire-0 -v /run/user/$(id -u)/pulse/native:/run/user/$(id -u)/pulse/native:U -v /run/user/$(id -u)/pipewire-0:/run/user/$(id -u)/pipewire-0:U -v $HOME/.claude.json:/home/user/.claude.json:U -v $HOME/.claude:/home/user/.claude:U -v $HOME/.gemini:/home/user/.gemini:U -v $HOME/.cache/huggingface:/home/user/.cache/huggingface:U -v $PWD:/home/user/workspace:U -w /home/user/workspace ghcr.io/altermarkive/utilities:latest
```
