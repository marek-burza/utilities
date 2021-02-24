FROM ubuntu:focal-20210119

ENV DEBIAN_FRONTEND noninteractive
# ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1

RUN apt-get -yq update && \
    apt-get -yq install curl && \
    (curl -sL https://aka.ms/InstallAzureCLIDeb | /bin/bash)
