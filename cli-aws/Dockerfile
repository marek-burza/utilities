FROM python:3.9.2-alpine3.13

RUN apk add --no-cache bash

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

ENTRYPOINT [ "/bin/bash" ]
