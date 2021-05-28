FROM httpd:${VERSION:-alpine}

ADD apache-graceful-reload.sh /usr/local/apache2/bin/apache-graceful-reload.sh

RUN chmod 0111 /usr/local/apache2/bin/apache-graceful-reload.sh && \
    apk add --update --no-cache sudo && \
    echo "ALL ALL=(root) NOPASSWD: /usr/local/apache2/bin/apache-graceful-reload.sh" >> /etc/sudoers
