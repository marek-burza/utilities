FROM ubuntu:artful-20171019

ADD install.sh /tmp/install.sh
ADD requirements.txt /tmp/requirements.txt

RUN /bin/bash /tmp/install.sh && rm -rf /tmp/*

CMD ["/bin/bash"]
