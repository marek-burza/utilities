# Tools

Note: When using docker commands in git bash on Windows prefix them with `MSYS_NO_PATHCONV=1` and wrap environment variables like so `$(cygpath -w $HOME)`.


## autossh

Can be used to forward a service on a local port to an SSH jump server:

    docker run --restart always -d --network host -v $HOME/.ssh:/ssh:ro altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /ssh/id_rsa -R ${JUMP_SERVER_PORT}:127.0.0.1:${LOCAL_PORT_FORWARDED} -N ${JUMP_SERVER_USER}@${JUMP_SERVER_HOST}


## cli-azure

Can be used to run Azure CLI in a bash shell like this:

    docker run --rm -it -v $HOME/.azure:/root/.azure -v $PWD:/w -w /w altermarkive/cli-azure


## cli-azure

Can be used to run AWS CLI in a bash shell like this:

    docker run --rm -it -v $HOME/.azure:/root/.azure -v $PWD:/w -w /w altermarkive/cli-aws


## ffmpeg

Can be used for AV conversion between formats:

    docker run --rm -it -v $PWD:/w -w /w altermarkive/ffmpeg -i example.avi -c:a aac -c:v libx264 example.mp4


## imagemagick

Can be used for conversion between formats:

    docker run --rm -it -v $PWD:/w -w /w altermarkive/imagemagick example.png example.pdf
    docker run --rm -it -v $PWD:/w -w /w altermarkive/imagemagick -density 600 example.pdf example.png


## networking

Contains nmap, netcat & tcpdump available for bash shell:

    docker run --rm -it --network host altermarkive/networking


## pillow

Can be used like this:

    docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/local/bin/python altermarkive/pillow example.py

Where the `example.py` could look like this:

```python
from PIL import Image, ImageDraw

image = Image.new('RGB', (128, 128))
draw = ImageDraw.Draw(image)
draw.text((10,10), 'Hello', fill=(255,255,255))
image.save('example.png')
```


## poppler

Can be used to extract pages from a PDF file and to join PDF files:

    docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/pdfseparate altermarkive/poppler -f 1 -l 1 example.pdf %d.pdf
    docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/pdfunite altermarkive/poppler example.pdf 1.pdf result.pdf


## python-linters

Can be used for thorough Python linting of the current directory like this:

    docker run -it -v $PWD:/w -w /w --entrypoint /bin/lint.sh altermarkive/python-linters


## retroactive-git

Can be used in the following way:

    docker run --rm -it -v $PWD:/w -w /w altermarkive/retroactive-git
    LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1 FAKETIME_NO_CACHE=1 FAKETIME='1970-01-01 00:00:00' date
    LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1 FAKETIME_NO_CACHE=1 FAKETIME='+365d' date


## svetovid

If you want to automatically become a watcher of Atlassian Jira issues (and are not the owner/administrator) then you can use this service to accomplish this (with suitable email client rules it creates an office experience by revealing what is generally happening without the necessity of acting upon it):

    docker run --restart always -d --name svetovid -e ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" -e ATLASSIAN_USER="$ATLASSIAN_USER" -e ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" -e ATLASSIAN_QUERY="$ATLASSIAN_QUERY" -e ATLASSIAN_WATCHER="$ATLASSIAN_WATCHER" -e SVETOVID_SLEEP="$SVETOVID_SLEEP" altermarkive/svetovid


## veles

If you want to prefix Atlassian Jira issues with [...] and have it automatically carried over into labels then you can use this service to accomplish this:

    docker run --restart always -d --name veles -e ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" -e ATLASSIAN_USER="$ATLASSIAN_USER" -e ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" -e ATLASSIAN_QUERY="$ATLASSIAN_QUERY" -e VELES_SLEEP="$VELES_SLEEP" altermarkive/veles


## xpstopdf

Can be used for conversion from XPS to PDF:

    docker run --rm -it -v $PWD:/w -w /w altermarkive/xpstopdf example.xps example.pdf
