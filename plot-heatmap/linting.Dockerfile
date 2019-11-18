FROM plot-heatmap

COPY shared/automation/lint.here.sh /app/lint.here.sh

WORKDIR /app

RUN /bin/sh /app/lint.here.sh
