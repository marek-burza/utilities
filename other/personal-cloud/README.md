# Introduction

This is a set of Ansible scripts to:

- Automate installation of Docker on Ubuntu. The scripts are based on the original guide [here](https://docs.docker.com/engine/install/ubuntu/).


# Prerequisites

```shell
sudo apt-get -yq update
sudo apt-get -yq install ansible-core openssh-server
test -f ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519 -C "$USER@localhost"
ssh-copy-id -i ~/.ssh/id_ed25519.pub $USER@localhost
echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers.d/$USER
install 0700 -d $HOME/.ansible/tmp
```

# Installation

```shell
cd ansible
ANSIBLE_ROLES_PATH=$PWD/roles ansible-playbook -u $USER -i ../inventory --extra-vars "ansible_dir=$PWD ansible_ssh_user=$USER" books/provision.yml
```
