FROM python:3.7.4-alpine3.10

COPY shared/requirements/numpy_pandas_matplotlib.requirements.txt /tmp/requirements.txt

RUN apk add --update --no-cache build-base freetype-dev && \
    pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY plot-heatmap/plot_heatmap.py /app/plot_heatmap.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/plot_heatmap.py" ]
