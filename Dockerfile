FROM python:2.7-slim

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -yq nginx python-dev gcc libpcre3 libpcre3-dev

RUN pip install -r /tmp/requirements.txt && rm -rf /tmp/requirements.txt

RUN chmod 777 /run/ -R

ADD root /

EXPOSE 80

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
