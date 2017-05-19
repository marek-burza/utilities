FROM ubuntu:xenial-20170510

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -yq mc imagemagick python3 python3-pip python3-dev python3-tk build-essential subversion git libfreetype6-dev libpng-dev libopenblas-dev

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip -r /tmp/requirements.txt && rm -rf /tmp/requirements.txt

CMD ["/bin/bash"]
