FROM python:3.7.5-slim-buster

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yq update

COPY shared/requirements/numpy_pandas.requirements.txt /tmp/numpy_pandas.requirements.txt

RUN apt-get -yq install build-essential && \
    pip3 --disable-pip-version-check install -r /tmp/numpy_pandas.requirements.txt && \
    rm /tmp/numpy_pandas.requirements.txt

COPY csv-split-by-time-of-day/csv_split_by_time_of_day.py /app/csv_split_by_time_of_day.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/csv_split_by_time_of_day.py" ]
