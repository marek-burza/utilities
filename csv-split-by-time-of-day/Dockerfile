FROM python:3.7.4-alpine3.10

COPY shared/requirements/numpy_pandas.requirements.txt /tmp/requirements.txt

RUN apk add --update --no-cache build-base && \
    pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY csv-split-by-time-of-day/csv_split_by_time_of_day.py /app/csv_split_by_time_of_day.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/csv_split_by_time_of_day.py" ]
