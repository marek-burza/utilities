# Introduction

To bring the runner up (Vagrant + Ansible):

```shell
GITLAB_CI_RUNNER_URL=https://example.com/ci GITLAB_CI_RUNNER_TOKEN=a1B2c3D4e5F6g7H8i9J vagrant up
```

To bring the runner up (Ansible):

```shell
cd ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u centos --key-file=key.pem -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=centos gitlab_ci_runner_url=https://example.com/ci gitlab_ci_runner_token=a1B2c3D4e5F6g7H8i9J" books/provision.yml
```
