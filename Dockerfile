FROM alpine:latest

RUN apk add --update nginx supervisor uwsgi uwsgi-python3

RUN chmod 777 /run/ -R

ADD root /

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
