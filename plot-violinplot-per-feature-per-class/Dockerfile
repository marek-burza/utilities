FROM python:3.7.4-alpine3.10

COPY shared/requirements/numpy_pandas.requirements.txt /tmp/numpy_pandas.requirements.txt

RUN apk add --update --no-cache build-base && \
    pip3 --disable-pip-version-check install -r /tmp/numpy_pandas.requirements.txt && \
    rm /tmp/numpy_pandas.requirements.txt

COPY shared/requirements/matplotlib.requirements.txt /tmp/matplotlib.requirements.txt

RUN apk add --update --no-cache freetype-dev && \
    pip3 --disable-pip-version-check install -r /tmp/matplotlib.requirements.txt && \
    rm /tmp/matplotlib.requirements.txt

COPY plot-violinplot-per-feature-per-class/plot_violinplot_per_feature_per_class.py /app/plot_violinplot_per_feature_per_class.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/plot_violinplot_per_feature_per_class.py" ]
