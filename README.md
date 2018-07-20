# Introduction

This is a set of Ansible scripts which automates installation of Docker CE on Raspbian.

The scripts are based on the original guide [here](https://docs.docker.com/install/linux/docker-ce/debian/).


# Assumptions

It is assumed that:
* The IP address of the Raspberry Pi is placed in the file `inventory` in the main directory of this cloned repository
* The Raspberry Pi is running Raspbian (the scripts were tested with Stretch)
* SSH is installed and accessible from outside of the Raspberry Pi
* Your public SSH key was copied to the Raspberry Pi
  (see [here](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md) for details)

# Installation

```shell
cd ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u pi -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=pi" books/provision.yml
```
