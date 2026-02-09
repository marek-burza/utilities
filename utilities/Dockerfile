FROM python:3.14.3-alpine3.23

RUN apk add --no-cache bash build-base curl enscript ffmpeg git imagemagick jq poppler-utils qpdf && \
    sed -i '/PDF/d' /etc/ImageMagick-7/policy.xml && \
    curl -sL -o /usr/local/bin/lsix https://raw.githubusercontent.com/hackerb9/lsix/refs/heads/master/lsix && \
    chmod +x /usr/local/bin/lsix && \
    /bin/sh -c "((curl -LsSf https://astral.sh/uv/install.sh | sh); uv self update) || true"

ENV PATH=$PATH:/root/.local/bin/

ADD scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/pdf_*.py

ENTRYPOINT [ "/bin/bash" ]
