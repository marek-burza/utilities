# Sync NVIDIA Driver & CUDA versions (`nvidia-smi`)
FROM nvidia/cuda:13.2.0-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && \
    apt-get -yq remove python && \
    apt-get -yq install \
    build-essential \
    cmake \
    curl \
    enscript \
    ffmpeg \
    git \
    git-lfs \
    imagemagick \
    jq \
    libatlas3-base \
    libblas-dev \
    libfreetype-dev \
    libhdf5-dev \
    libjpeg-dev \
    libnvidia-compute-590-server \
    libopenblas-dev \
    ncurses-bin \
    pipewire-bin \
    pkg-config \
    poppler-utils \
    qpdf \
    ripgrep \
    software-properties-common \
    sudo \
    unzip \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*
# build-essential - N/A
# cmake - lightgbm (older, non-wheel version)
# curl - N/A
# enscript - N/A
# ffmpeg - N/A
# git - N/A
# git-lfs - N/A
# imagemagick - N/A
# jq - N/A
# libatlas3-base - N/A
# libblas-dev - N/A
# libfreetype-dev - matplotlib (older, non-wheel version)
# libhdf5-dev - Keras
# libjpeg-dev - Pillow (older, non-wheel version)
# libnvidia-compute-590-server - lightgbm
# libopenblas-dev - N/A
# ncurses-bin - Claude Code
# pipewire-bin - Claude Code
# pkg-config - matplotlib (older, non-wheel version)
# poppler-utils - N/A
# qpdf - N/A
# ripgrep - Claude Code
# software-properties-common - Python
# unzip - N/A
# zlib - Pillow (older, non-wheel version)

RUN curl -fsSL https://deb.nodesource.com/setup_24.x | /bin/bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

ADD scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/pdf_*.py

RUN git clone --depth 1 https://github.com/ggml-org/llama.cpp.git /tmp/llama.cpp && \
    cd /tmp/llama.cpp && \
    cmake -B . . -DLLAMA_CUDA=ON && \
    cmake --build . --config Release -j$(nproc) && \
    cmake --install . --config Release && \
    rm -rf /tmp/llama.cpp

ENV USER=user
ENV HOME=/home/$USER
WORKDIR $HOME
RUN userdel -r ubuntu 2> /dev/null || true
RUN useradd -m -s /bin/bash -u 1000 $USER && \
    chown -R $USER:$USER $HOME && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER $USER

ENV NODE_OPTIONS="--max-old-space-size=2048"
RUN npm config set prefix "$HOME/.npm-global"
ENV PATH="$PATH:$HOME/.npm-global/bin"
RUN npm install -g @google/gemini-cli

RUN (curl --proto '=https' --tlsv1.2 -fsSL https://claude.ai/install.sh | /bin/bash) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://astral.sh/uv/install.sh | /bin/sh) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://go.dev/dl/$(curl -sL https://golang.org/dl/ | grep -oP 'go[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n 1).linux-amd64.tar.gz | /usr/bin/tar -C $HOME/.local -xzf -) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://sh.rustup.rs | /bin/sh -s -- -y)
ENV PATH="$PATH:$HOME/.local/bin:$HOME/.local/go/bin:$HOME/go/bin:$HOME/.cargo/bin"
# Install an extension of Python debugger & deep inspection of Python objects
RUN uv tool install pdbpp && uv tool install wat

ENTRYPOINT [ "/bin/bash" ]

# TODO: Follow the best practices listed at https://docs.astral.sh/uv/guides/integration/docker/ and switch to regular user
