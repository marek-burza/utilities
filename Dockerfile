FROM ubuntu:bionic-20190718

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y transmission-cli openvpn curl && \
    sed -i '/\=\"all\"/s/^#//g' /etc/default/openvpn

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
