FROM python:3.10.0-alpine3.15

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install --disable-pip-version-check -r /tmp/requirements.txt && rm /tmp/requirements.txt

ADD app /app

WORKDIR /app

ENTRYPOINT [ "/usr/local/bin/python", "/app/app.py" ]
