# Chrome

* To enable password import got to `chrome://flags/`

# Bash

* Tutorial about [Bash history](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps)

# Wireshark

To filter for UDP, a particular MAC and broadcast use this filter:

    udp && (eth.addr == 00:11:22:33:44:55 || eth.addr == FF:FF:FF:FF:FF:FF)