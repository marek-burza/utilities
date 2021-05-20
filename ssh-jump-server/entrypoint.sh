#!/bin/sh

if [ ! -f "/etc/ssh/ssh_host_rsa_key" ]; then
	ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
fi
if [ ! -f "/etc/ssh/ssh_host_ecdsa_key" ]; then
	ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa
fi
if [ ! -f "/etc/ssh/ssh_host_ed25519_key" ]; then
	ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519
fi

if [ ! -d "/var/run/sshd" ]; then
    mkdir -p /var/run/sshd
fi

exec "$@"
