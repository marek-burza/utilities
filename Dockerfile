FROM ubuntu:xenial-20170619

ADD install.sh /tmp/install.sh
ADD requirements.txt /tmp/requirements.txt

RUN chmod +x /tmp/install.sh && /tmp/install.sh && rm -rf /tmp/install.sh /tmp/requirements.txt

CMD ["/bin/bash"]
