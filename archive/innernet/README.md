# Unofficial Docker image for Innernet

CAUTION: The work in this repository is not finished, do not use!
(the service tries to bind to the external IP rather than 0.0.0.0 which does not cooperate with Docker)

See more info about `innernet` at:
[https://blog.tonari.no/introducing-innernet](https://blog.tonari.no/introducing-innernet) and
[https://github.com/tonarino/innernet](https://github.com/tonarino/innernet)

To run the container:

```bash
docker run -it --name innernet -v $HOME/.innernet/db/:/var/lib/innernet-server -v $HOME/.innernet/conf/:/etc/innernet-server --cap-add NET_ADMIN altermarkive/innernet-server ...
```
