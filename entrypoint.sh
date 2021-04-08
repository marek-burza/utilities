#!/bin/sh

if [ ! -f "$FILE" -a ! -z "$TAILSCALE_AUTH_KEY" ]; then
    if [ -z "$TAILSCALE_AUTH_DELAY" ]; then
        TAILSCALE_AUTH_DELAY=5
    fi
    ( sleep $TAILSCALE_AUTH_DELAY; /usr/local/bin/tailscale up --authkey=$TAILSCALE_AUTH_KEY ) &
fi

/usr/local/bin/tailscaled
