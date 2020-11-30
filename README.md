# Automating Workspace

## Workspace

Workspace for Python 3, Azure, AWS, format conversions, etc.:

    docker run --rm --name workspace -it -v $HOME/.ssh:/root/.ssh -v $PWD:/shared -w /shared -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro --user=$(id -u) ghcr.io/altermarkive/workspace
