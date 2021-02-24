# Tools

Note: When using docker commands in git bash on Windows prefix them with `MSYS_NO_PATHCONV=1` and wrap environment variables like so `$(cygpath -w $HOME)`.


## Workspace

Workspace for Python 3, Azure, AWS, format conversions, etc.:

    docker run --rm --name workspace -it -v $HOME/.ssh:/root/.ssh -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/shared -w /shared -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro --user=$(id -u) altermarkive/workspace


## autossh

Can be used to forward a service on a local port to an SSH jump server:

    docker run --restart always -d --network host -v $HOME/.ssh:/ssh:ro altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /ssh/id_rsa -R ${JUMP_SERVER_PORT}:127.0.0.1:${LOCAL_PORT_FORWARDED} -N ${JUMP_SERVER_USER}@${JUMP_SERVER_HOST}


## ffmpeg

Can be used for AV conversion between formats:

    docker run --rm -it -v $PWD:/w -w /w altermarkive/ffmpeg -i example.avi -c:a aac -c:v libx264 example.mp4


## imagemagick

Can be used for conversion between formats:

    docker run --rm -it -v $PWD:/w -w /w altermarkive/imagemagick example.png example.pdf
    docker run --rm -it -v $PWD:/w -w /w altermarkive/imagemagick -density 600 example.pdf example.png


## svetovid

If you want to automatically become a watcher of Atlassian Jira issues (and are not the owner/administrator) then you can use this service to accomplish this (with suitable email client rules it creates an office experience by revealing what is generally happening without the necessity of acting upon it):

    docker run --restart always -d --name svetovid -e ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" -e ATLASSIAN_USER="$ATLASSIAN_USER" -e ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" -e ATLASSIAN_QUERY="$ATLASSIAN_QUERY" -e ATLASSIAN_WATCHER="$ATLASSIAN_WATCHER" -e SVETOVID_SLEEP="$SVETOVID_SLEEP" altermarkive/svetovid


## xpstopdf

Can be used for conversion from XPS to PDF:

    docker run -it -v $PWD:/w -w /w xpstopdf example.xps example.pdf
