#!/bin/sh

ORIGINAL_LOCATION=$(curl http://ip-api.com/json/)
/usr/sbin/openvpn --config /etc/openvpn/config.conf &
OTHER_LOCATION=$(curl -s http://ip-api.com/json/)
while [ "$ORIGINAL_LOCATION" = "$OTHER_LOCATION" ]
do
  OTHER_LOCATION=$(curl -s http://ip-api.com/json/)
  echo $OTHER_LOCATION
  sleep 10
done
curl -s http://ip-api.com/json/
/usr/bin/transmission-cli $@
