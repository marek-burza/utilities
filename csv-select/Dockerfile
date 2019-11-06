FROM python:3.7.4-alpine3.10

COPY shared/requirements/numpy_pandas.requirements.txt /tmp/numpy_pandas.requirements.txt

RUN apk add --update --no-cache build-base && \
    pip3 --disable-pip-version-check install -r /tmp/numpy_pandas.requirements.txt && \
    rm /tmp/numpy_pandas.requirements.txt

COPY csv-select/csv_select.py /app/csv_select.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/csv_select.py" ]
