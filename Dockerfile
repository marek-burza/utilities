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

RUN apt-get update && apt-get install -y python python-dev python-pip automake autotools-dev g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config

RUN pip install -r /etc/simple-collector.requirements.txt

RUN chmod +x /bin/simple-collector.py

EXPOSE 5000

RUN git clone https://github.com/s3fs-fuse/s3fs-fuse.git && cd s3fs-fuse && ./autogen.sh && ./configure && make && make install

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "/bin/simple-collector.py", "--logto", "/tmp/simple-collector.uwsgi.log", "--socket-timeout", "60", "--http-timeout", "60", "--harakiri", "60"]
