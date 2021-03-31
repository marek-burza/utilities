FROM ubuntu:focal-20210119

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && \
    apt-get -yq install curl jq && \
    (curl -sL https://aka.ms/InstallAzureCLIDeb | /bin/bash) && \
    az aks install-cli --install-location /usr/bin/kubectl && \
    curl -fsSL https://get.helm.sh/helm-v3.5.3-linux-amd64.tar.gz -o /tmp/helm-linux-amd64.tar.gz && \
    tar -zxvf /tmp/helm-linux-amd64.tar.gz && \
    mv linux-amd64/helm /usr/bin/helm && \
    rm -rf /tmp/helm-linux-amd64.tar.gz linux-amd64 && \
    curl -fsSL https://github.com/mikefarah/yq/releases/download/4.6.3/yq_linux_amd64 -o /usr/bin/yq && \
    chmod +x /usr/bin/yq
