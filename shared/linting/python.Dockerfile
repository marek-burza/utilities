FROM python:3.7.4-alpine3.10

RUN apk add --update --no-cache build-base && \
    pip3 install bandit==1.6.2 flake8==3.7.8 pylint==2.3.1 pycodestyle==2.5.0

WORKDIR /app

COPY shared/requirements /app

RUN find /app -name "*requirements.txt" -exec pip3 install -r {} \;

CMD (find . -iname "*.py" | xargs pylint --disable=R0801) && \
    pycodestyle . && \
    flake8 *.py && \
    bandit -r .
