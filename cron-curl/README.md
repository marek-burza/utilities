# Cron schedules &amp; curl commands

This Docker image allows to run `curl` commands on a schedule. For example,
to download content from `http://from.a.com/download` and upload it to
`http://to.b.com/upload` every hour create the following `crontab` file:

    0 * * * * curl --silent http://from.a.com/download | curl --silent -X POST --data-binary @- http://to.b.com/upload

Then, run the following command:

    docker run -it -e CRONTAB="$(cat crontab)" altermarkive/cron-curl
