## cron-curl

This Docker image allows to run `curl` commands on a schedule. For example,
to download content from `http://from.a.com/download` and upload it to
`http://to.b.com/upload` every hour create the following `crontab` file:

```
0 * * * * curl --silent http://from.a.com/download | curl --silent -X POST --data-binary @- http://to.b.com/upload
```

Then, run the following command:

```bash
docker run --restart always -d -e CRONTAB="$(cat crontab)" ghcr.io/altermarkive/cron-curl
```

`Dockerfile`:

```dockerfile
FROM alpine:3.13.5

RUN apk add --update --no-cache curl

ADD run.sh /

CMD ["/bin/sh", "/run.sh"]
```

`run.sh`:

```bash
#!/bin/sh

echo "$CRONTAB" > /tmp/crontab
crontab /tmp/crontab
crond -f
```