FROM golang:1.17.2-alpine3.14 AS build-env

ARG VERSION_LONG=""
ENV VERSION_LONG=$VERSION_LONG
ARG VERSION_SHORT=""
ENV VERSION_SHORT=$VERSION_SHORT
ARG VERSION_GIT_HASH=""
ENV VERSION_GIT_HASH=$VERSION_GIT_HASH

WORKDIR /go/src/tailscale

RUN apk add --no-cache git

RUN git clone https://github.com/tailscale/tailscale.git . && \
    git checkout v${VERSION_SHORT}

RUN go mod download

RUN go install -tags=xversion -ldflags="\
    -X tailscale.com/version.Long=$VERSION_LONG
    -X tailscale.com/version.Short=$VERSION_SHORT
    -X tailscale.com/version.GitCommit=$VERSION_GIT_HASH"
    -v ./cmd/tailscale ./cmd/tailscaled

FROM alpine:3.14

RUN apk add --no-cache ca-certificates iptables iproute2 ip6tables
COPY --from=build-env /go/bin/* /usr/local/bin/
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
