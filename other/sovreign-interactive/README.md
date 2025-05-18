# Sovreign Interactive

## Introduction

This is a set of Ansible scripts to install local-hosted set of utilities I frequently use.

## Prerequisites

```shell
sudo apt-get -yq update
sudo apt-get -yq install ansible-core
install -m 0700 -d $HOME/.ansible/tmp
```

## Installation

```shell
ansible-playbook -i "localhost," --connection=local --ask-become-pass --extra-vars "tailscale_auth_key=$TS_AUTHKEY utilities_password=$UTILITIES_PASSWORD" playbook.yml
```

## Future

- Install OpenVPN or Wireguard for secure localaccess
