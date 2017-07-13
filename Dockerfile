FROM ubuntu:xenial-20170619

ADD install.sh /install.sh
ADD requirements*.txt /
ADD Makefile.fastFM /Makefile.fastFM

RUN /bin/bash /install.sh && rm -rf /install.sh /requirements*.txt

CMD ["/bin/bash"]
