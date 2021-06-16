FROM ubuntu:focal-20210416

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && \
    apt-get -yq install exiftags jhead libimage-exiftool-perl

ENTRYPOINT [ "/bin/bash" ]
