FROM python:3.13.1-bookworm

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq cron

ADD *.py crontab requirements.txt /svetovit/

RUN crontab /svetovit/crontab && \
    pip install --no-cache-dir --break-system-packages -r /svetovit/requirements.txt && \
    rm -rf /svetovit/crontab /svetovit/requirements.txt && \
    chmod +x /svetovit/*.py

CMD ["cron", "-f"]
