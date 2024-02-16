# socat

To expose Docker host ports on Docker networks it is often enough to use [`qoomon/docker-host`](https://github.com/qoomon/docker-host) (and it may be necessary to add `--network host`):

```bash
docker run --restart always -d --name forwarder --cap-add=NET_ADMIN --cap-add=NET_RAW qoomon/docker-host
```

However, if an another image is interfering with firewall rules (or cannot grant `NET_ADMIN` or `NET_RAW` cabilities)
it may be necessary to tunnel the traffic with [`socat`](https://www.redhat.com/sysadmin/getting-started-socat),
here an example for `ssh`:

```bash
docker run --restart always -d --name forwarder alpine/socat TCP4-LISTEN:22,fork,reuseaddr TCP4:host.docker.internal:22
```

Note: On Linux, the following option might be necessary to be added to the command above: `--add-host=host.docker.internal:host-gateway`

