FROM nvidia/cuda:12.6.2-devel-ubuntu24.04

# 1. NVIDIA CUDA Installation Guide for Linux (Ubuntu): https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu
# 2. Installing the NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt

ENV DEBIAN_FRONTEND=noninteractive

# Docker in Docker
RUN apt-get update -qqy && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables
RUN curl -sSL https://get.docker.com/ | sh

# Python package dependencies
RUN apt-get -yq update && \
    apt-get -yq install \
        build-essential \
        cmake \
        curl \
        default-jdk \
        git-lfs \
        libatlas3-base \
        libblas-dev \
        libfreetype-dev \
        libhdf5-dev \
        libjpeg-dev \
        libopenblas-dev \
        pkg-config \
        python3 \
        python3-dev \
        python3-pip \
        swig \
        unzip \
        zlib1g-dev
# build-essential - tornado
# cmake - lightgbm (older, non-wheel version)
# curl - Auto-WEKA
# default-jdk - Auto-WEKA
# libatlas3-base - Auto-WEKA
# libblas-dev - N/A
# libfreetype-dev - matplotlib (older, non-wheel version)
# libhdf5-dev - Keras
# libjpeg-dev - Pillow (older, non-wheel version)
# libopenblas-dev - Auto-WEKA
# pkg-config - matplotlib (older, non-wheel version)
# swig - auto-sklearn
# unzip - Auto-WEKA
# zlib - Pillow (older, non-wheel version)

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Auto-WEKA
ARG TARGETARCH
RUN useradd -s /bin/bash -m -d /home/user user
USER user
WORKDIR /home/user

RUN curl -L -O http://prdownloads.sourceforge.net/weka/weka-3-9-6.zip && \
    unzip weka-3-9-6.zip && \
    rm weka-3-9-6.zip && \
    unzip /home/user/weka-3-9-6/weka.jar arpack_combined.jar core.jar mtj.jar
ENV CLASSPATH="${CLASSPATH}:/home/user/weka-3-9-6/weka.jar:/home/user/arpack_combined.jar:/home/user/core.jar:/home/user/mtj.jar"

RUN java weka.core.WekaPackageManager -install-package netlibNativeLinux
RUN find /home/user/wekafiles/packages/netlibNativeLinux/lib/ && \
    (find /home/user/wekafiles/packages/netlibNativeLinux/lib/ -name "*aarch64*" -print0 | xargs -0 -I {} /bin/bash -c 'cp "{}" "$(echo "{}" | sed "s/aarch64/arm64/")"') && \
    (find /home/user/wekafiles/packages/netlibNativeLinux/lib/ -name "*x86_64*" -print0 | xargs -0 -I {} /bin/bash -c 'cp "{}" "$(echo "{}" | sed "s/x86_64/amd64/")"') && \
    (find /home/user/wekafiles/packages/netlibNativeLinux/lib/ -name "*i686*" -print0 | xargs -0 -I {} /bin/bash -c 'cp "{}" "$(echo "{}" | sed "s/i686/386/")"') && \
    find /home/user/wekafiles/packages/netlibNativeLinux/lib/ 
ENV CLASSPATH="${CLASSPATH}:/home/user/wekafiles/packages/netlibNativeLinux/lib/jniloader-1.2.jar:/home/user/wekafiles/packages/netlibNativeLinux/lib/native_system-java-1.2.jar:/home/user/wekafiles/packages/netlibNativeLinux/lib/netlib-native_system-linux-${TARGETARCH}-1.2-natives.jar:/home/user/wekafiles/packages/netlibNativeLinux/lib/native_ref-java-1.2.jar:/home/user/wekafiles/packages/netlibNativeLinux/lib/netlib-native_ref-linux-${TARGETARCH}-1.2-natives.jar"

RUN java weka.core.WekaPackageManager -install-package Auto-WEKA
ENV CLASSPATH="${CLASSPATH}:/home/user/wekafiles/packages/Auto-WEKA/autoweka.jar"

USER root
