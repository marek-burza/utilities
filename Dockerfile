FROM ubuntu:xenial-20170619

ADD install.sh /install.sh
ADD requirements*.txt /

RUN /bin/bash /install.sh && rm -rf /install.sh /requirements*.txt

CMD ["/bin/bash"]
