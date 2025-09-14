FROM debian:latest

COPY *.py /usr/local/bin/

ENV HOME=/root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -yq && \
    apt-get install -yq build-essential curl enscript ffmpeg git imagemagick jq poppler-utils qpdf && \
    /bin/sh -c "curl -LsSf https://astral.sh/uv/install.sh | sh" && \
    curl https://raw.githubusercontent.com/hackerb9/lsix/refs/heads/master/lsix -o /usr/local/bin/lsix && \
    chmod +x /usr/local/bin/lsix

ENV PATH="${HOME}/.local/bin:${PATH}"
