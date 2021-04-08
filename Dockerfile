FROM ubuntu:20.04 AS Build

ARG VERSION
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && apt-get -yq install curl

COPY architecture.sh /tmp/architecture.sh

RUN dpkg --print-architecture && mkdir -p /tmp/tailscale && \
    cd /tmp/tailscale && \
    curl -fsSL https://pkgs.tailscale.com/stable/tailscale_${VERSION}_$(/bin/sh /tmp/architecture.sh).tgz -o tailscale.tar.gz && \
	tar --strip-components=1 -xzf tailscale.tar.gz && \
	cp tailscale tailscaled /usr/local/bin/ && \
	rm -rf /tmp/tailscale /tmp/architecture.sh

FROM alpine:3.13

RUN apk add --no-cache ca-certificates iptables iproute2

COPY --from=Build /usr/local/bin/tailscale* /usr/local/bin/

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
