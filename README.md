# Automating Workspace

## Workspace

Workspace for Python 3, Docker, AWS, ML, etc.:

    docker run --rm --name workspace -it -v $HOME/.ssh:/root/.ssh -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/shared -w /shared -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro --user=$(id -u) ghcr.io/altermarkive/workspace
