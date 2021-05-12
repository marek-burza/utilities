FROM python:3.8.3-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && apt-get -yq install build-essential nginx supervisor curl

COPY requirements.txt /tmp/requirements.txt
RUN pip --disable-pip-version-check install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . /
RUN curl -sL https://unpkg.com/swagger-client@3.10.9/browser/index.js -o /app/wwwroot/swagger-client.js

WORKDIR /app

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

EXPOSE 80
