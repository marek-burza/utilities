FROM httpd:${VERSION:-alpine}

ADD apache-graceful-reload.sh /usr/local/apache2/bin/apache-graceful-reload.sh

RUN chmod 0111 /usr/local/apache2/bin/apache-graceful-reload.sh && \
    apk add --update --no-cache sudo && \
    echo "ALL ALL=(root) NOPASSWD: /usr/local/apache2/bin/apache-graceful-reload.sh" >> /etc/sudoers

ENV MOD_AUTH_OPENIDC_REPOSITORY https://github.com/zmartzone/mod_auth_openidc.git

ENV MOD_AUTH_OPENIDC_VERSION v2.4.8.4

ENV BUILD_DIRECTORY /tmp/mod_auth_openidc

RUN mkdir ${BUILD_DIRECTORY} && mkdir /usr/lib/apache2

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && apk add --no-cache wget jansson hiredis cjose cjose-dev git autoconf build-base automake curl apache2-dev curl-dev pcre-dev libtool && \
  cd ${BUILD_DIRECTORY} && \
  git clone -b ${MOD_AUTH_OPENIDC_VERSION} ${MOD_AUTH_OPENIDC_REPOSITORY} && \
  cd mod_auth_openidc && \
  ./autogen.sh && \
  ./configure CFLAGS="-g -O0" LDFLAGS="-lrt" && \
  make test && \
  make install && \
  cd / && \
  rm -fr ${BUILD_DIRECTORY} && \
  apk del git cjose-dev apache2-dev autoconf automake build-base wget curl-dev pcre-dev libtool
