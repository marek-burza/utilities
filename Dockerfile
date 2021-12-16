FROM golang:1.17.5-alpine3.15 AS MeekBuild

RUN apk add --update-cache git

RUN git clone --quiet -c advice.detachedHead=false --depth 1 --branch v0.37.0 https://git.torproject.org/pluggable-transports/meek.git && \
    cd meek/meek-client && \
    go get && \
    go build


FROM alpine:3.15.0

RUN apk add --update-cache tor torsocks openssh-client

ADD torrc /etc/tor/torrc
ADD entrypoint.sh /entrypoint.sh
COPY --from=MeekBuild /go/meek/meek-client/meek-client /usr/bin/meek-client

VOLUME ["/var/lib/tor"]

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
