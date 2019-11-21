# Workspace

Workspace for Python 3, Docker, AWS, ML, etc.

## Docker

Linux:

    docker run --rm --name workspace -it -v $HOME/.ssh:/root/.ssh -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/shared -w /shared -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro --user=$(id -u) altermarkive/workspace

Windows (with git bash):

    MSYS_NO_PATHCONV=1 docker run --rm --name workspace -it -v $(cygpath -w $HOME)/.ssh:/root/.ssh.shadow -v /var/run/docker.sock:/var/run/docker.sock -v $(cygpath -w $PWD):/shared -w /shared altermarkive/workspace

## Vagrant

    vagrant plugin install vagrant-disksize
    vagrant up
    vagrant ssh
