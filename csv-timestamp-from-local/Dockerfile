FROM python:3.7.4-alpine3.10 AS Core

COPY csv-timestamp-from-local/requirements.txt /tmp/requirements.txt

RUN apk add --update --no-cache build-base && \
    pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY csv-timestamp-from-local/csv_timestamp_from_local.py /app/csv_timestamp_from_local.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/csv_timestamp_from_local.py" ]


FROM Core

WORKDIR /app

RUN apk add --update --no-cache build-base && \
    pip3 install bandit==1.6.2 flake8==3.7.8 pylint==2.3.1 pycodestyle==2.5.0 && \
    (find . -iname "*.py" | xargs pylint --disable=R0801) && \
    pycodestyle . && \
    flake8 *.py && \
    bandit -r .


FROM Core
