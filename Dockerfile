# The MIT License (MIT)
#
# Copyright (c) 2016
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

FROM ubuntu:14.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq       \
    python python-pip automake autotools-dev g++ git libcurl4-gnutls-dev       \
    libfuse-dev libssl-dev libxml2-dev make pkg-config rsyslog                 \
    python-setuptools curl unzip xorg-dev

RUN sed -i "s/#\$ModLoad imudp/\$ModLoad imudp/" /etc/rsyslog.conf &&          \
    sed -i "s/#\$UDPServerRun/\$UDPServerRun/" /etc/rsyslog.conf &&            \
    sed -i "s/#\$ModLoad imtcp/\$ModLoad imtcp/" /etc/rsyslog.conf &&          \
    sed -i "s/#\$InputTCPServerRun/\$InputTCPServerRun/" /etc/rsyslog.conf

RUN curl http://www.mathworks.com/supportfiles/downloads/R2013b/deployment_files/R2013b/installers/glnxa64/MCR_R2013b_glnxa64_installer.zip -s -o /tmp/MCR_R2013b_glnxa64_installer.zip && \
    unzip /tmp/MCR_R2013b_glnxa64_installer.zip -d /tmp/MCR &&                 \
    rm /tmp/MCR_R2013b_glnxa64_installer.zip &&                                \
    cd /tmp/MCR && ./install -mode silent -agreeToLicense yes                  \
    cd / && rm -rf /tmp/MCR

RUN cd /tmp && git clone https://github.com/s3fs-fuse/s3fs-fuse.git &&         \
    cd s3fs-fuse && ./autogen.sh && ./configure && make && make install &&     \
    cd / && rm -rf /tmp/s3fs-fuse && chmod 400 /etc/*.s3fs && mkdir -p /mnt/s3

ADD root /

RUN curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -s -o /tmp/awslogs-agent-setup.py && \
    python /tmp/awslogs-agent-setup.py -n -r `cat /tmp/region` -c /tmp/logs && \
    rm /tmp/awslogs-agent-setup.py /tmp/region /tmp/logs

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN chmod +x /bin/stator.sh

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
