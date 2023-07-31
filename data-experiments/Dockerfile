FROM python:3.10.7-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && \
    apt-get -yq install \
        build-essential=12.9 \
        cmake=3.18.4-2+deb11u1 \
        libfreetype-dev=2.10.4+dfsg-1+deb11u1 \
        libjpeg-dev=1:2.0.6-4 \
        pkg-config=0.29.2-1 \
        zlib1g-dev=1:1.2.11.dfsg-2+deb11u2
# build-essential - tornado
# cmake - lightgbm (older, non-wheel version)
# libfreetype-dev - matplotlib (older, non-wheel version)
# libjpeg-dev - Pillow (older, non-wheel version)
# pkg-config - matplotlib (older, non-wheel version)
# zlib - Pillow (older, non-wheel version)

# TODO:
# * libopenblas-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
