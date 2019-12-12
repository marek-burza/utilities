FROM python:3.7.5-slim-buster

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yq update

COPY shared/requirements/numpy_pandas.requirements.txt /tmp/numpy_pandas.requirements.txt

RUN apt-get -yq install build-essential && \
    pip3 --disable-pip-version-check install -r /tmp/numpy_pandas.requirements.txt && \
    rm /tmp/numpy_pandas.requirements.txt

COPY shared/requirements/matplotlib.requirements.txt /tmp/matplotlib.requirements.txt

RUN apt-get -yq install libfreetype6-dev && \
    pip3 --disable-pip-version-check install -r /tmp/matplotlib.requirements.txt && \
    rm /tmp/matplotlib.requirements.txt

COPY plot-scatterplot/plot_scatterplot.py /app/plot_scatterplot.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/plot_scatterplot.py" ]
