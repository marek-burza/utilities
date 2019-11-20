FROM ubuntu:bionic-20191029

ADD install.sh /tmp/install.sh
ADD requirements.txt /tmp/requirements.txt

RUN /bin/sh /tmp/install.sh && rm -rf /tmp/*

CMD ["/bin/bash"]
