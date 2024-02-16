#!/bin/sh

if [ ! -z "$AUTOSSH_ID_KEY" ]
then
  mkdir -p /root/.ssh
  echo $AUTOSSH_ID_KEY > /root/.ssh/id_key
fi

/usr/bin/autossh "$@"
