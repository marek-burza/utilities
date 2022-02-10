# Tailscale as a sidecar

Given that [Tailscale](https://tailscale.com/) finally published their own Docker image it is no longer necessary to put together own one.

To run the Tailscale daemon as a "sidecar" on Kubernetes start reading [here](https://tailscale.com/blog/kubecon-21/).

To run the Tailscale daemon as a "sidecar" to the services bound to the Docker host run the following command:

```bash
docker run -d --name tailscaled --hostname $HOSTNAME -e TAILSCALE_AUTH_KEY=$TAILSCALE_AUTH_KEY -v $HOME/.tailscale:/var/lib/tailscale --device /dev/net/tun --network host --cap-add=NET_ADMIN --restart unless-stopped --entrypoint /bin/sh -e TAILSCALE_AUTH_KEY=$TAILSCALE_AUTH_KEY tailscale/tailscale:latest -c '(([ ! -f "/var/lib/tailscale/tailscaled.state" ] && ( sleep 3; /usr/local/bin/tailscale up --authkey=$TAILSCALE_AUTH_KEY)) &); /usr/local/bin/tailscaled'
```
