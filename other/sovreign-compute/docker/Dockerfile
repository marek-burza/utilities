FROM debian:latest

ARG DEBIAN_FRONTEND=noninteractive

COPY *.sh /sovreign/

RUN ls /sovreign/ && /bin/sh /sovreign/install_utilities.sh && \
    /bin/sh /sovreign/install_tailscale.sh && \
    /bin/sh /sovreign/install_go.sh && \
    /bin/sh /sovreign/install_rust.sh && \
    /bin/sh /sovreign/install_uv.sh && \
    /bin/sh /sovreign/install_gotty.sh && \
    rm /sovreign/install*.sh

ENV PATH="/usr/local/go/bin:${HOME}/.cargo/bin:source:${HOME}/.local/bin:${PATH}"