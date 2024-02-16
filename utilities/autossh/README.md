# autossh

Can be used to forward a service on a local port to an SSH jump server:

```bash
docker run --restart always -d --network host -v $HOME/.ssh:/keys:ro ghcr.io/altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o 
"StrictHostKeyChecking no" -i /keys/id_rsa -R ${JUMP_SERVER_PORT}:127.0.0.1:${LOCAL_PORT_FORWARDED} -N ${JUMP_SERVER_USER}@${JUMP_SERVER_HOST}
```

The SSH key can be also passed via an environment variable:

```bash
docker run --restart always -d --network host -e AUTOSSH_ID_KEY=$(cat $HOME/.ssh/id_key) ghcr.io/altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o 
"PasswordAuthentication=no" -o "StrictHostKeyChecking no" -R ${JUMP_SERVER_PORT}:127.0.0.1:${LOCAL_PORT_FORWARDED} -N ${JUMP_SERVER_USER}@${JUMP_SERVER_HOST}
```

When using `autossh` remember to include the following line in /etc/ssh/sshd_config file on the SSH jump server:

```
GatewayPorts yes
```

