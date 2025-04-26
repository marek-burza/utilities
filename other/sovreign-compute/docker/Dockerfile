FROM debian:latest

ARG DEBIAN_FRONTEND=noninteractive

COPY *.sh /tmp/sovreign/
COPY tools/* /usr/local/bin/

ENV HOME=/root

RUN /bin/sh /tmp/sovreign/install_utilities.sh && \
    /bin/sh /tmp/sovreign/install_tailscale.sh && \
    /bin/sh /tmp/sovreign/install_go.sh && \
    /bin/sh /tmp/sovreign/install_rust.sh && \
    /bin/sh /tmp/sovreign/install_uv.sh && \
    /bin/sh /tmp/sovreign/install_gotty.sh && \
    rm -rf /tmp/sovreign

ENV PATH="/usr/local/go/bin:${HOME}/.cargo/bin:source:${HOME}/.local/bin:${PATH}"