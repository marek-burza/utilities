# Introduction

To bring the server up (Vagrant + Ansible):

```shell
GITLAB_SERVER_EMAIL=support@example.com GITLAB_SERVER_FQDN=example.com vagrant up
```

To bring the server up (Ansible):

```shell
cd ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u centos --key-file=key.pem -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=centos gitlab_server_fqdn=example.com gitlab_server_email=support@example.com" books/provision.yml
```
