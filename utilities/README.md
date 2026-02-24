# Utilities

```bash
docker run -it -e TERM=xterm-256color --rm --cap-drop=ALL --security-opt=no-new-privileges:true --network host --user $(id -u):$(id -g) -e PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native -e PIPEWIRE_REMOTE=/run/user/$(id -u)/pipewire-0 -v /run/user/$(id -u)/pulse/native:/run/user/$(id -u)/pulse/native -v /run/user/$(id -u)/pipewire-0:/run/user/$(id -u)/pipewire-0 -v $HOME/.claude.json:/home/user/.claude.json -v $HOME/.claude:/home/user/.claude -v $HOME/.gemini:/home/user/.gemini -v $PWD:/home/user/workspace -w /home/user/workspace ghcr.io/altermarkive/utilities
```
