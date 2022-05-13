FROM ubuntu:jammy-20220428

RUN apt-get -yq update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -yq install mc=3:4.8.27-1

CMD ["/usr/bin/mc"]
