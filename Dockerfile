FROM python:2.7-alpine

RUN apk add --update nginx supervisor uwsgi-python && rm -rf /var/cache/apk/*

ADD root /

RUN chown -R nginx:nginx /app && chmod 777 /run/ -R

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
