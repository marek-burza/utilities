# BitTorrent over VPN

This repository implements a Docker container simplifying BitTorrent downloads over a VPN.

It is assumed that one has an `.ovpn` configuration file (here: `config.ovpn`) and the associated credentials file (here: `credentials.txt`), coupled together by a following example entry in the `.ovpn` file:

    auth-user-pass /etc/openvpn/credentials.txt

With these assumptions, download of a magnet link can be accomplished with the following command (`--privileged` enables creation of a tunnel device and `--dns=1.1.1.1` redirects your DNS query to a privacy-oriented service of CloudFlare):

    docker run --rm --privileged --dns=1.1.1.1 -it -v ${PWD}/config.ovpn:/etc/openvpn/config.conf -v ${PWD}/credentials.txt:/etc/openvpn/credentials.txt -v ${PWD}/downloads:/downloads altermarkive/bittorrent-over-vpn --download-dir /downloads 'magnet:...'
