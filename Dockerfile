# This code is free software: you can redistribute it and/or modify it under the
# terms  of  the  GNU Lesser General Public License  as published  by  the  Free
# Software Foundation,  either version 3 of the License, or (at your option) any
# later version.
#
# This code is distributed in the hope that it will be useful,  but  WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A  PARTICULAR  PURPOSE.  See  the  GNU Lesser General Public License  for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with code. If not, see http://www.gnu.org/licenses/.

FROM ubuntu:14.04

ADD root /

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq python python-dev python-pip automake autotools-dev g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config rsyslog python-setuptools curl

RUN curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -s -o /tmp/awslogs-agent-setup.py

RUN python /tmp/awslogs-agent-setup.py -n -r `cat /etc/region.conf` -c /etc/awslogs.conf

RUN sed -i "s/#\$ModLoad imudp/\$ModLoad imudp/" /etc/rsyslog.conf && \
    sed -i "s/#\$UDPServerRun 514/\$UDPServerRun 514/" /etc/rsyslog.conf && \
    sed -i "s/#\$ModLoad imtcp/\$ModLoad imtcp/" /etc/rsyslog.conf && \
    sed -i "s/#\$InputTCPServerRun 514/\$InputTCPServerRun 514/" /etc/rsyslog.conf

RUN pip install -r /etc/simple-collector.requirements.txt

RUN chmod +x /bin/simple-collector.py

EXPOSE 5000

RUN git clone https://github.com/s3fs-fuse/s3fs-fuse.git && cd s3fs-fuse && ./autogen.sh && ./configure && make && make install

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
