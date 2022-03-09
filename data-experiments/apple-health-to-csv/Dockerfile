FROM python:3.9.5-alpine3.13 AS core

RUN pip3 install defusedxml==0.7.1

COPY apple_health_to_csv.py /app/apple_health_to_csv.py

ENTRYPOINT [ "/usr/local/bin/python3", "/app/apple_health_to_csv.py" ]


FROM core

WORKDIR /app

RUN apk add --update --no-cache build-base && \
    pip3 install bandit==1.7.0 flake8==3.9.2 pylint==2.8.2 pycodestyle==2.7.0 && \
    (find . -iname "*.py" | xargs pylint --disable=R0801) && \
    pycodestyle . && \
    flake8 *.py && \
    bandit -r .


FROM core