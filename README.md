# Workspace

Workspace for Python 3, Docker, AWS, Azure, ML, etc.

## Docker

    docker build -t workspace .
    docker run -it --rm -v $HOME/.ssh:/root/.ssh -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/shared -w /shared workspace

## Vagrant

    vagrant plugin install vagrant-disksize
    vagrant up
    vagrant ssh
