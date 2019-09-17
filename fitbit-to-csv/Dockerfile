FROM python:3.7.4-alpine3.10 AS Core

COPY fitbit-to-csv/fitbit_to_csv.py /app/fitbit_to_csv.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/fitbit_to_csv.py" ]


FROM Core

WORKDIR /app

RUN apk add --update --no-cache build-base && \
    pip3 install bandit==1.6.2 flake8==3.7.8 pylint==2.3.1 pycodestyle==2.5.0 && \
    (find . -iname "*.py" | xargs pylint --disable=R0801) && \
    pycodestyle . && \
    flake8 *.py && \
    bandit -r .


FROM Core