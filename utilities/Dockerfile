# Sync NVIDIA Driver & CUDA versions (`nvidia-smi`)
FROM nvidia/cuda:13.3.0-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && \
    apt-get -yq remove python && \
    apt-get -yyq install \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
        build-essential \
        cmake \
        curl \
        ffmpeg \
        git \
        git-lfs \
        jq \
        libatlas3-base \
        libblas-dev \
        libasound2-plugins \
        libnvidia-compute-595-server \
        libopenblas-dev \
        ncurses-bin \
        pipewire-bin \
        npm \
        ripgrep \
        software-properties-common \
        sudo \
        unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# build-essential - N/A
# cmake - lightgbm (older, non-wheel version)
# curl - N/A
# ffmpeg - N/A
# git - N/A
# git-lfs - N/A
# jq - N/A
# libatlas3-base - N/A
# libblas-dev - N/A
# libasound2-plugins - Claude Code voice (ALSA → PulseAudio routing)
# libnvidia-compute-595-server - lightgbm
# libopenblas-dev - N/A
# ncurses-bin - Claude Code
# pipewire-bin - Claude Code
# npm - MCP (provides node, npx)
# ripgrep - Claude Code
# software-properties-common - Python
# unzip - N/A

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_HTTP_TIMEOUT=60 \
    UV_PYTHON=python3.13 \
    UV_PYTHON_INSTALL_DIR=/app/python \
    VIRTUAL_ENV=/app/venv
# Initiate Virtual Environment
RUN /bin/uv venv $VIRTUAL_ENV
# Install utilities
ADD scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/*.py

ENV USER=user
ENV HOME=/home/$USER
RUN userdel -r ubuntu 2> /dev/null || true
RUN getent group 1000 > /dev/null 2>&1 || groupadd -g 1000 user
RUN useradd -m -s /bin/bash -u 1000 -g 1000 $USER && \
    chown -R $USER:$USER $HOME /app && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER $USER

ENV TERM=xterm-256color
# Route ALSA default device through PulseAudio (Claude Code voice mode)
RUN /bin/bash -c "echo -e 'pcm.!default pulse\nctl.!default pulse' > $HOME/.asoundrc"

RUN curl --proto '=https' --tlsv1.2 -fsSL https://claude.ai/install.sh | /bin/bash
ENV PATH="$PATH:$VIRTUAL_ENV/bin:$HOME/.local/bin"
