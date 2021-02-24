FROM alpine:3.13.2

RUN apk add --no-cache git build-base bash && \
    git clone --branch v0.9.8 https://github.com/wolfcw/libfaketime.git /tmp/libfaketime && \
    cd /tmp/libfaketime && \
    make install && \
    cd - && \
    rm -rf /tmp/libfaketime

ENTRYPOINT [ "/bin/bash" ]
