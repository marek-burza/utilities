# Unofficial Docker image for Tailscale ![Build status](https://github.com/altermarkive/tailscale/workflows/Automation/badge.svg)

Given that [Tailscale](https://tailscale.com/) does not yet publish their own Docker image (see [this issue](https://github.com/tailscale/tailscale/issues/504) for details) I decided to put together my own (and the outcome is partially inspired by https://github.com/function61/tailscale-dockerimage).

To run the Tailscale daemon and join it to your network run the following command:

```bash
docker run -d --name tailscaled --hostname $HOSTNAME -e TAILSCALE_AUTH_KEY=$TAILSCALE_AUTH_KEY -v $PWD/tailscale:/var/lib/tailscale --device /dev/net/tun --network host --cap-add=NET_ADMIN --restart unless-stopped altermarkive/tailscale
```
