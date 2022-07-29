FROM alpine:latest

RUN apk add --no-cache imagemagick && \
    sed -i '/PDF/d' /etc/ImageMagick-7/policy.xml
