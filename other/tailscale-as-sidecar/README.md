# Tailscale as a sidecar

Given that [Tailscale](https://tailscale.com/) finally published their own Docker image it is no longer necessary to put together own one.

To run the Tailscale daemon as a "sidecar" on Kubernetes start reading [here](https://tailscale.com/blog/kubecon-21/).

To run the Tailscale daemon as a "sidecar" to the services bound to the Docker host run the following command:

```bash
docker run -d --name tailscaled --hostname $HOSTNAME -e TS_AUTHKEY=$TS_AUTHKEY -v /var/lib:/var/lib -v /dev/net/tun:/dev/net/tun --network host --cap-add=NET_ADMIN --cap-add=NET_RAW --restart unless-stopped tailscale/tailscale
```
