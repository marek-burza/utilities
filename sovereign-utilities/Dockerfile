FROM debian:latest

COPY *.py /usr/local/bin/

ENV HOME=/root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -yq && \
    apt-get install -yq \
      build-essential \
      curl \
      enscript \
      fzf \
      git \
      imagemagick \
      jq \
      nano \
      poppler-utils \
      procps \
      qpdf \
      ripgrep \
      sudo \
      supervisor \
      tmux \
      vim && \
    curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.noarmor.gpg -o /usr/share/keyrings/tailscale-archive-keyring.gpg && \
    curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.tailscale-keyring.list -o /etc/apt/sources.list.d/tailscale.list && \
    apt-get update -yq && \
    apt-get install -yq tailscale && \
    curl -fsSL https://go.dev/dl/$(curl -sL https://golang.org/dl/ | grep -oP 'go[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n 1).linux-amd64.tar.gz -o /tmp/go.linux-amd64.tar.gz && \
    rm -rf /usr/local/go && \
    tar -C /usr/local -xzf /tmp/go.linux-amd64.tar.gz && \
    rm /tmp/go.linux-amd64.tar.gz && \
    /bin/sh -c "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y" && \
    /bin/sh -c "curl -LsSf https://astral.sh/uv/install.sh | sh" && \
    /usr/local/go/bin/go install github.com/sorenisanerd/gotty@latest && \
    /bin/sh -c "curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash" && \
    curl https://raw.githubusercontent.com/hackerb9/lsix/refs/heads/master/lsix -o /usr/local/bin/lsix && \
    chmod +x /usr/local/bin/lsix

ENV PATH="/usr/local/go/bin:${HOME}/.cargo/bin:source:${HOME}/.local/bin:${PATH}"
