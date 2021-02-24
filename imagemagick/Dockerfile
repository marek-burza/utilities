FROM alpine:3.13.2

RUN apk add --no-cache imagemagick && \
    sed -i '/PDF/d' /etc/ImageMagick-7/policy.xml

ENTRYPOINT [ "convert" ]
