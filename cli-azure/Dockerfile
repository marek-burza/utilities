FROM ubuntu:focal-20210119

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && \
    apt-get -yq install curl && \
    (curl -sL https://aka.ms/InstallAzureCLIDeb | /bin/bash) && \
    az aks install-cli --install-location /usr/bin/kubectl && \
    curl -fsSL https://get.helm.sh/helm-v3.5.3-linux-amd64.tar.gz -o /tmp/helm-linux-amd64.tar.gz && \
    tar -zxvf /tmp/helm-linux-amd64.tar.gz && \
    rm /tmp/helm-linux-amd64.tar.gz && \
    mv linux-amd64/helm /usr/bin/helm && \
    rm -rf linux-amd64
