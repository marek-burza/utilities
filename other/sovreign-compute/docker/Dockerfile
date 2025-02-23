FROM debian:latest

ARG DEBIAN_FRONTEND=noninteractive

COPY *.sh /sovreign/

RUN /bin/sh /sovreign/install_utilities.sh && \
    /bin/sh /sovreign/install_tailscale.sh && \
    /bin/sh /sovreign/install_coder.sh && \
    rm /sovreign/install*.sh
