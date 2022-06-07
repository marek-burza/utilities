FROM alpine:3.16.0

RUN apk add --no-cache imagemagick && \
    sed -i '/PDF/d' /etc/ImageMagick-7/policy.xml

ENTRYPOINT [ "convert" ]
