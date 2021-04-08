#!/bin/sh

if [ ! -f "/var/lib/tailscale/tailscaled.state" -a ! -z "$TAILSCALE_AUTH_KEY" ]; then
    if [ -z "$TAILSCALE_AUTH_DELAY" ]; then
        TAILSCALE_AUTH_DELAY=5
    fi
    ( sleep $TAILSCALE_AUTH_DELAY; /usr/local/bin/tailscale up --authkey=$TAILSCALE_AUTH_KEY ) &
fi

if [ ! -f "/dev/net/tun" ]; then
    mknod /dev/net/tun c 10 200
fi

/usr/local/bin/tailscaled
