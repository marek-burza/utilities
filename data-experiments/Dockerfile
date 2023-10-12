FROM python:3.10.13-slim-bookworm

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && \
    apt-get -yq install \
        build-essential=12.9 \
        cmake=3.25.1-1 \
        libfreetype-dev=2.12.1+dfsg-5 \
        libjpeg-dev=1:2.1.5-2 \
        pkg-config=1.8.1-1 \
        swig=4.1.0-0.2 \
        zlib1g-dev=1:1.2.13.dfsg-1
# build-essential - tornado
# cmake - lightgbm (older, non-wheel version)
# libfreetype-dev - matplotlib (older, non-wheel version)
# libjpeg-dev - Pillow (older, non-wheel version)
# pkg-config - matplotlib (older, non-wheel version)
# swig - auto-sklearn
# zlib - Pillow (older, non-wheel version)

# TODO:
# * libopenblas-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
