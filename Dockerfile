FROM golang:1.16-alpine3.13 AS Build

ARG VERSION
ARG COMMIT_HASH

WORKDIR /go/src/tailscale

RUN apk add --no-cache git

RUN git clone https://github.com/tailscale/tailscale.git . && \
    git checkout v${VERSION}

RUN go mod download

RUN go install -tags=xversion -ldflags="-X tailscale.com/version.Long=$VERSION -X tailscale.com/version.Short=$VERSION -X tailscale.com/version.GitCommit=$COMMIT_HASH" -v ./cmd/...

FROM alpine:3.13

RUN apk add --no-cache ca-certificates iptables iproute2

COPY --from=Build /go/bin/tailscale* /usr/local/bin/

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
