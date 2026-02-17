FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

ENV HOME=/home/sandbox
ENV USER=sandbox
WORKDIR $HOME

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    ncurses-bin \
    ripgrep \
    pipewire-bin \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for security
# Remove default 'ubuntu' user (UID 1000) so sandbox can use that UID,
# matching the host user when running with --user $(id -u):$(id -g)
RUN userdel -r ubuntu 2>/dev/null || true
RUN useradd -m -s /bin/bash -u 1000 sandbox && \
    mkdir -p $HOME/.npm-global $HOME/.npm && \
    chown -R sandbox:sandbox $HOME
USER sandbox

ENV NODE_OPTIONS="--max-old-space-size=2048"
RUN npm config set prefix "$HOME/.npm-global"

RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="$HOME/.local/bin:$PATH"

CMD ["/bin/bash"]

# Build instructions:
# docker build -t sandbox .
#
# Run instructions:
# docker run -it -e TERM=xterm-256color --rm --cap-drop=ALL --security-opt=no-new-privileges:true --network host --user $(id -u):$(id -g) -e PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native -e PIPEWIRE_REMOTE=/run/user/$(id -u)/pipewire-0 -v /run/user/$(id -u)/pulse/native:/run/user/$(id -u)/pulse/native -v /run/user/$(id -u)/pipewire-0:/run/user/$(id -u)/pipewire-0 -v $HOME/.claude.json:/home/sandbox/.claude.json -v $HOME/.claude:/home/sandbox/.claude -v $PWD:/home/sandbox/workspace -w /home/sandbox/workspace sandbox
