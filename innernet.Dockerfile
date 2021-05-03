FROM rust:1.51.0-bullseye AS BuildInnernet

ARG VERSION

WORKDIR /innernet

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && \
    apt-get -yq install git build-essential musl-tools musl-dev clang libclang-dev libsqlite3-dev && \
    update-ca-certificates

RUN git clone https://github.com/tonarino/innernet.git . && \
    git checkout -q v${VERSION}

RUN cargo build --release --bin innernet

FROM golang:1.16.3-buster AS BuildWireGuard

WORKDIR /wireguard-go

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && \
    apt-get -yq install git

RUN git clone https://git.zx2c4.com/wireguard-go . && \
    git checkout -q 0.0.20210424 && \
    make

FROM debian:bullseye-20210408-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -yq update && \
    apt-get -yq install libsqlite3-0

COPY --from=BuildInnernet /innernet/target/release/innernet /usr/local/bin/
COPY --from=BuildWireGuard /wireguard-go/wireguard-go /usr/local/bin/

RUN mkdir /var/run/wireguard

ENTRYPOINT [ "/usr/local/bin/innernet" ]
