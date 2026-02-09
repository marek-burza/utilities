FROM python:3.14.3-alpine3.23

RUN apk add --no-cache bash build-base curl enscript ffmpeg git imagemagick jq poppler-utils qpdf && \
    sed -i '/PDF/d' /etc/ImageMagick-7/policy.xml && \
    /bin/sh -c "((curl -LsSf https://astral.sh/uv/install.sh | sh); uv self update) || true"

ENV PATH=$PATH:/root/.local/bin/

ADD scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/pdf_*.py

ENTRYPOINT [ "/bin/bash" ]
