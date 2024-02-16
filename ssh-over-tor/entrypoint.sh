#!/bin/sh

if [ "$#" -eq 0 ]; then
  mkdir -p /var/lib/tor/service
  chmod 700 /var/lib/tor/service
  chown -R tor:nogroup /var/lib/tor
  if [ -n "$ADDRESS" -a -n "$USER" ]; then
    su -s /bin/sh -c '/usr/bin/tor -f /etc/tor/torrc --runasdaemon 0 2>&1 | tee /var/log/tor/notices.log' tor &
    while ! grep "Bootstrapped 100" "/var/log/tor/notices.log"; do
      sleep 1
    done
    torify ssh $USER@$ADDRESS -oStrictHostKeyChecking=no
  else
    su -s /bin/sh -c '/usr/bin/tor -f /etc/tor/torrc --runasdaemon 0' tor
    sleep 2
  fi
else
  exec "$@"
fi
