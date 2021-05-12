# Inspired by https://github.com/WAGO/azure-iot-edge

# Lock versions
ARG DEBIAN_VERSION=stretch-build-20210225
ARG YQ_VERSION=3.4.1
ARG DOCKER_CE_VERSION=5:19.03.15~3-0~debian-stretch
ARG CONTAINERD_VERSION=1.4.3-1
ARG AZURE_IOT_EDGE_VERSION=1.1.1-1

# Based on Debian
FROM balenalib/armv7hf-debian:${DEBIAN_VERSION} as Base

# Use versions
ARG YQ_VERSION
ARG DOCKER_CE_VERSION
ARG CONTAINERD_VERSION
ARG AZURE_IOT_EDGE_VERSION

# Disable interactive configuration prompts
ARG DEBIAN_FRONTEND=noninteractive

# Begin of cross-build
RUN [ "cross-build-start" ]

# Update and install required prerequisites
#  Shared: curl
#  Docker: apt-transport-https ca-certificates gnupg lsb-release
#  Azure IoT Edge: yq
RUN apt-get -yq update && \
    apt-get -yq install curl apt-transport-https ca-certificates gnupg lsb-release && \
    curl -fsSL https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_arm -o /usr/bin/yq && \
    chmod +x /usr/bin/yq

# Install Docker-in-Docker
RUN (curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg) && \
    (echo "deb [arch=armhf signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker-ce.list > /dev/null) && \
    apt-get -yq update && apt-get -yq install docker-ce=${DOCKER_CE_VERSION} docker-ce-cli=${DOCKER_CE_VERSION} containerd.io=${CONTAINERD_VERSION}

# Install Azure IoT Edge
RUN (curl -fsSL https://packages.microsoft.com/config/debian/stretch/multiarch/prod.list > /tmp/microsoft-prod.list) && \
    mv /tmp/microsoft-prod.list /etc/apt/sources.list.d/microsoft-prod.list && \
    (curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/microsoft.gpg) && \
    mv /tmp/microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg && \
    apt-get -yq update && apt-get -yq install libiothsm-std=${AZURE_IOT_EDGE_VERSION} iotedge=${AZURE_IOT_EDGE_VERSION} && \
    cp /etc/iotedge/config.yaml.template /etc/iotedge/config.yaml

# Clean-up
RUN apt-get -y autoremove && apt-get clean && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

# End of cross-build
RUN [ "cross-build-end" ]

# Reduce container image size
FROM scratch as Final
COPY --from=Base / /
WORKDIR /

# Include the start-up script
COPY entrypoint.sh /
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
