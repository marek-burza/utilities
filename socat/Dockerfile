FROM alpine:3.13.5

RUN apk add --update --no-cache socat

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
