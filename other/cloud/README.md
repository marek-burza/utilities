# Introduction

This is a set of Ansible scripts to automate installation of Docker on Ubuntu.

The scripts are based on the original guide [here](https://docs.docker.com/install/linux/docker-ce/debian/).


# Prerequisites

```shell
sudo apt-get -yq update
sudo apt-get -yq install ansible-core openssh-server
test -f ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519 -C "$USER@localhost"
ssh-copy-id -i ~/.ssh/id_ed25519.pub $USER@localhost
```

# Installation

```shell
cd ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u pi -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=pi" books/provision.yml
```
