# Automating Workspace

## Workspace

Workspace for Python 3, Azure, AWS, format conversions, etc.:

    docker run --rm --name workspace -it -v $HOME/.ssh:/root/.ssh -v $PWD:/shared -w /shared -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro --user=$(id -u) ghcr.io/altermarkive/workspace

## Svetovid

If you want to automatically become a watcher of Atlassian Jira issues (and are not the owner/administrator) then you can use this service to accomplish this:

    docker run --restart always -d --name svetovid -e ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" -e ATLASSIAN_USER="$ATLASSIAN_USER" -e ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" -e ATLASSIAN_QUERY="$ATLASSIAN_QUERY" -e ATLASSIAN_WATCHER="$ATLASSIAN_WATCHER" -e SVETOVID_SLEEP="$SVETOVID_SLEEP" altermarkive/svetovid
