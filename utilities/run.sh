#!/bin/sh

podman run \
  -it \
  --rm \
  --pull=always \
  -e ANTHROPIC_API_KEY \
  -e HF_TOKEN \
  -e DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --network host \
  --userns=keep-id \
  --device nvidia.com/gpu=all \
  -e PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
  -e PIPEWIRE_REMOTE=/run/user/$(id -u)/pipewire-0 \
  -v /run/user/$(id -u)/pulse/native:/run/user/$(id -u)/pulse/native \
  -v /run/user/$(id -u)/pipewire-0:/run/user/$(id -u)/pipewire-0 \
  -v $HOME/.claude.json:/home/user/.claude.json \
  -v $HOME/.claude:/home/user/.claude \
  -v $HOME/.cache/huggingface:/home/user/.cache/huggingface \
  -v $PWD:/home/user/workspace \
  -w /home/user/workspace \
  ghcr.io/marek-burza/utilities:latest
