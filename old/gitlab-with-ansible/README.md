# Introduction

## Server

To bring the server up (Vagrant + Ansible):

```shell
cd server
GITLAB_SERVER_EMAIL=support@example.com GITLAB_SERVER_FQDN=example.com vagrant up
```

To bring the server up (Ansible):

```shell
cd server/ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u centos --key-file=key.pem -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=centos gitlab_server_fqdn=example.com gitlab_server_email=support@example.com" books/provision.yml
```

## Runner

To bring the runner up (Vagrant + Ansible):

```shell
cd runner
GITLAB_CI_RUNNER_URL=https://example.com/ci GITLAB_CI_RUNNER_TOKEN=a1B2c3D4e5F6g7H8i9J vagrant up
```

To bring the runner up (Ansible):

```shell
cd runner/ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u centos --key-file=key.pem -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=centos gitlab_ci_runner_url=https://example.com/ci gitlab_ci_runner_token=a1B2c3D4e5F6g7H8i9J" books/provision.yml
```

## Quick'n'dirty Gitlab CI runner

```shell
/usr/bin/docker run \
    -d \
    --rm \
    --name gitlab-ci-runner \
    -v /var/run/docker.sock:/var/run/docker.sock \
    gitlab/gitlab-runner:alpine

/usr/bin/docker exec gitlab-ci-runner \
    gitlab-runner register \
    --non-interactive \
    --url https://gitlab.com/ \
    --registration-token $1 \
    --description 'runner' \
    --tag-list 'docker' \
    --executor 'docker' \
    --run-untagged=True \
    --docker-image 'docker:latest' \
    --docker-volumes /var/run/docker.sock:/var/run/docker.sock
```
