FROM python:3.9.10-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yq update && \
    apt-get -yq install --no-install-recommends build-essential=12.9 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip3 --disable-pip-version-check install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
