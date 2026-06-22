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
        enscript \
        ffmpeg \
        gh \
        ghostscript \
        git \
        git-lfs \
        imagemagick \
        jq \
        libatlas3-base \
        libblas-dev \
        libfreetype-dev \
        libhdf5-dev \
        libjpeg-dev \
        libasound2-plugins \
        libnvidia-compute-595-server \
        libopenblas-dev \
        ncurses-bin \
        pipewire-bin \
        pkg-config \
        poppler-utils \
        qpdf \
        npm \
        ripgrep \
        software-properties-common \
        sudo \
        unzip \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# build-essential - N/A
# cmake - lightgbm (older, non-wheel version)
# curl - N/A
# enscript - N/A
# ffmpeg - N/A
# gh - N/A
# ghostscript - pdf_optimize
# git - N/A
# git-lfs - N/A
# imagemagick - N/A
# jq - N/A
# libatlas3-base - N/A
# libblas-dev - N/A
# libfreetype-dev - matplotlib (older, non-wheel version)
# libhdf5-dev - Keras
# libjpeg-dev - Pillow (older, non-wheel version)
# libasound2-plugins - Claude Code voice (ALSA → PulseAudio routing)
# libnvidia-compute-595-server - lightgbm
# libopenblas-dev - N/A
# ncurses-bin - Claude Code
# pipewire-bin - Claude Code
# pkg-config - matplotlib (older, non-wheel version)
# poppler-utils - N/A
# qpdf - N/A
# npm - MCP (provides node, npx)
# ripgrep - Claude Code
# software-properties-common - Python
# unzip - N/A
# zlib - Pillow (older, non-wheel version)

RUN TAG=$(curl -fsSL https://api.github.com/repos/dejavu-fonts/dejavu-fonts/releases/latest | jq -r '.tag_name') && \
    VER=$(echo "$TAG" | sed 's/version_//' | tr '_' '.') && \
    curl -fsSL "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/${TAG}/dejavu-fonts-ttf-${VER}.tar.bz2" \
    | tar -xj -C /usr/share/fonts/truetype/dejavu --strip-components=2 \
        "dejavu-fonts-ttf-${VER}/ttf/DejaVuSans-Oblique.ttf" \
        "dejavu-fonts-ttf-${VER}/ttf/DejaVuSans-BoldOblique.ttf" && \
    fc-cache -f

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_HTTP_TIMEOUT=60 \
    UV_PYTHON=python3.13 \
    UV_PYTHON_INSTALL_DIR=/app/python \
    VIRTUAL_ENV=/app/venv
# TensorRT is quite noisy
ENV PYTHONWARNINGS="ignore::SyntaxWarning"
# Initiate Virtual Environment
# Install an extension of Python debugger & deep inspection of Python objects
RUN /bin/uv venv && /bin/uv pip install pdbpp wat
# Install utilities
ADD scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/*.py

RUN git clone --depth 1 https://github.com/ggml-org/llama.cpp.git /tmp/llama.cpp && \
    cd /tmp/llama.cpp && \
    cmake -B . . -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86 -DLLAMA_BUILD_UI=OFF && \
    cmake --build . --config Release -j$(nproc) && \
    cmake --install . --config Release && \
    rm -rf /tmp/llama.cpp

ENV USER=user
ENV HOME=/home/$USER
RUN userdel -r ubuntu 2> /dev/null || true
RUN getent group 1000 > /dev/null 2>&1 || groupadd -g 1000 user
RUN useradd -m -s /bin/bash -u 1000 -g 1000 $USER && \
    chown -R $USER:$USER $HOME /app && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER $USER

# Route ALSA default device through PulseAudio (Claude Code voice mode)
RUN /bin/bash -c "echo -e 'pcm.!default pulse\nctl.!default pulse' > $HOME/.asoundrc"

RUN (curl --proto '=https' --tlsv1.2 -fsSL https://claude.ai/install.sh | /bin/bash) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://antigravity.google/cli/install.sh | /bin/bash) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://opencode.ai/install | /bin/bash) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://go.dev/dl/$(curl -sL https://golang.org/dl/ | grep -oP 'go[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n 1).linux-amd64.tar.gz | /usr/bin/tar -C $HOME/.local -xzf -) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://sh.rustup.rs | /bin/sh -s -- -y) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://tailscale.com/install.sh | /bin/sh -s)
ENV PATH="$PATH:$VIRTUAL_ENV/bin:$HOME/.local/bin:$HOME/.opencode/bin:$HOME/.local/go/bin:$HOME/go/bin:$HOME/.cargo/bin"
