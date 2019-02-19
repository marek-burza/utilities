FROM alpine:3.8

RUN apk add --update-cache tor torsocks openssh-client

ADD torrc /etc/tor/torrc
ADD entrypoint.sh /entrypoint.sh

VOLUME ["/var/lib/tor"]

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
