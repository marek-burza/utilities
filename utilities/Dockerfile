# Sync with NVIDIA Driver & CUDA versions (`nvidia-smi`)
FROM nvidia/cuda:13.1.1-runtime-ubuntu24.04

# 1. NVIDIA CUDA Installation Guide for Linux (Ubuntu): https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu
# 2. Installing the NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt

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
    libnvidia-compute-580-server \
    libopenblas-dev \
    ncurses-bin \
    pipewire-bin \
    pkg-config \
    poppler-utils \
    python3 \
    python3-pip \
    python3-venv \
    qpdf \
    ripgrep \
    software-properties-common \
    unzip \
    zlib1g-dev
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
# libnvidia-compute-580-server - lightgbm
# libopenblas-dev - N/A
# ncurses-bin - Claude Code
# pipewire-bin - Claude Code
# pkg-config - matplotlib (older, non-wheel version)
# poppler-utils - N/A
# python3 - N/A
# python3-pip - N/A
# python3-venv - N/A
# qpdf - N/A
# ripgrep - Claude Code
# software-properties-common - Python
# unzip - N/A
# zlib - Pillow (older, non-wheel version)

ADD scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/pdf_*.py

ENV USER=user
ENV HOME=/home/$USER
WORKDIR $HOME
RUN userdel -r ubuntu 2> /dev/null || true
RUN useradd -m -s /bin/bash -u 1000 $USER && \
    chown -R $USER:$USER $HOME
USER $USER

RUN (curl --proto '=https' --tlsv1.2 -fsSL https://claude.ai/install.sh | /bin/bash) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://astral.sh/uv/install.sh | /bin/sh) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://go.dev/dl/$(curl -sL https://golang.org/dl/ | grep -oP 'go[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n 1).linux-amd64.tar.gz | /usr/bin/tar -C $HOME/.local -xzf -) && \
    (curl --proto '=https' --tlsv1.2 -fsSL https://sh.rustup.rs | /bin/sh -s -- -y)
ENV PATH="$PATH:$HOME/.local/bin:$HOME/.local/go/bin:$HOME/go/bin:$HOME/.cargo/bin"

ENTRYPOINT [ "/bin/bash" ]

# TODO: Follow the best practices listed at https://docs.astral.sh/uv/guides/integration/docker/ and switch to regular user
