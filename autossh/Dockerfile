FROM alpine:3.13.5

RUN apk add --no-cache autossh

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
CMD [ "/usr/bin/autossh" ]
