#!/bin/sh

if [ ! -f "/etc/ssh/ssh_host_rsa_key" ]; then
	ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa &> /dev/null
fi
if [ ! -f "/etc/ssh/ssh_host_ecdsa_key" ]; then
	ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa &> /dev/null
fi
if [ ! -f "/etc/ssh/ssh_host_ed25519_key" ]; then
	ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519 &> /dev/null
fi

cp /config/authorized_keys /home/user/.ssh/authorized_keys
chmod 0600 /home/user/.ssh/authorized_keys
chown 1000.100 /home/user/.ssh/authorized_keys

exec "$@"
