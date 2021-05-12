#!/bin/sh

echo "$CRONTAB" > /tmp/crontab
crontab /tmp/crontab
crond -f
