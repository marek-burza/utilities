# Tools

Note: When using docker commands in git bash on Windows prefix them with `MSYS_NO_PATHCONV=1` and wrap environment variables like so `$(cygpath -w $HOME)`.


## autossh

Can be used to forward a service on a local port to an SSH jump server:

```bash
docker run --restart always -d --network host -v $HOME/.ssh:/keys:ro altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /keys/id_rsa -R ${JUMP_SERVER_PORT}:127.0.0.1:${LOCAL_PORT_FORWARDED} -N ${JUMP_SERVER_USER}@${JUMP_SERVER_HOST}
```

The SSH key can be also passed via an environment variable:

```bash
docker run --restart always -d --network host -e AUTOSSH_ID_KEY=$(cat $HOME/.ssh/id_key) altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -R ${JUMP_SERVER_PORT}:127.0.0.1:${LOCAL_PORT_FORWARDED} -N ${JUMP_SERVER_USER}@${JUMP_SERVER_HOST}
```

When using `autossh` remember to include the following line in /etc/ssh/sshd_config file on the SSH jump server:

```
GatewayPorts yes
```


## cron-curl

This Docker image allows to run `curl` commands on a schedule. For example,
to download content from `http://from.a.com/download` and upload it to
`http://to.b.com/upload` every hour create the following `crontab` file:

```
0 * * * * curl --silent http://from.a.com/download | curl --silent -X POST --data-binary @- http://to.b.com/upload
```

Then, run the following command:

```bash
docker run --restart always -d -e CRONTAB="$(cat crontab)" altermarkive/cron-curl
```


## exif

To run the tools included in exif image use these commands:

```bash
docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/jhead altermarkive/exif ...
docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/exiftime altermarkive/exif ...
docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/exiftool altermarkive/exif ...
```

To add EXIF:

```bash
jhead -mkexif IMG_0000.jpg
```

To shift the date:

```bash
exiftime -v-55M -fw -ta *.JPG
```

Rename photos to feature album name and creation date:

```bash
find -type f -printf "mv %p \$ALBUM.\$(exiftool -CreateDate %p | cut -c 35- | sed 's/[ :]//g').jpg\n" | sh
```


## ffmpeg

Can be used for AV conversion between formats:

```bash
docker run --rm -it -v $PWD:/w -w /w altermarkive/ffmpeg -i example.avi -c:a aac -c:v libx264 example.mp4
```

To encode H.265:

```bash
ffmpeg -i input.mp4 -metadata creation_time="1970-01-10T00:00:00Z" -c:v libx265 -c:a aac output.hevc.mp4
```

To transcode from DVD:

```bash
ffmpeg -i dvd.vob -f mp4 -vcodec libx264 -profile:v main -level 4.0 -s 480x384 -b:v 500k -maxrate 500k -bufsize 1000k -c:a aac -strict experimental -ac 2 -ar 48000 -ab 192k -threads 0 video.mp4
```

To scale:

```bash
ffmpeg -i video.mp4 -vf scale=540:960 scaled.mp4
```

To convert video to individual frames:

```bash
ffmpeg -i video.mp4 frame.%08d.png
```

To create a silent audio file:

```bash
ffmpeg -f s16le -ac 1 -t 1 -i /dev/zero -ar 22050 -y silence.mp3
```

To concatenate files:

```bash
ffmpeg -i concat:"one.mp3|two.mp3" -strict -2 -y three.aac
```

To combine video frames with audio:

```bash
for ENTRY in $(ls -1 *.jpg | sed -e 's/\.jpg//g')
do
    ffmpeg -loop 1 -i ${ENTRY}.jpg -i ${ENTRY}.aac -strict -2 -crf 25 -c:v libx264 -tune stillimage -pix_fmt yuv420p -shortest -y ${ENTRY}.mp4
done
```


## imagemagick

Can be used for conversion between formats:

```bash
docker run --rm -it -v $PWD:/w -w /w altermarkive/imagemagick example.png example.pdf
docker run --rm -it -v $PWD:/w -w /w altermarkive/imagemagick -density 600 example.pdf example.png
```

Or, in combination with the `altermarkive/exif` utility, one can run the following `compact.sh` (for example with this command - `find . -name "*.JPG" -exec /bin/sh compact.sh {} \;`):

```bash
#!/bin/sh
export FILE_IN=$1
export FILE_OUT=$PREFIX.$(docker run --rm -v $PWD:/w -w /w --entrypoint /usr/bin/exiftool altermarkive/exif -CreateDate $1 | sed 's/[^0-9]*//g').heic
docker run --rm -v $PWD:/w -w /w altermarkive/imagemagick $FILE_IN $FILE_OUT
```


## networking

Contains nmap, netcat & tcpdump available for bash shell:

```bash
docker run --rm -it --network host altermarkive/networking
```

Here is the [link to ncat man page](http://man7.org/linux/man-pages/man1/ncat.1.html).

Example 1: Send text "test" in a UDP packet over IPv4 with a connection time of 1 second from port 5000 to a broadcast address 172.17.255.255 and port 10000:

```bash
echo test | netcat -4u -w1 -p 5000 -b 172.17.255.255 10000
```


## pillow

Can be used like this:

```bash
docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/local/bin/python altermarkive/pillow example.py
```

Where the `example.py` could look like this:

```python
from PIL import Image, ImageDraw

image = Image.new('RGB', (128, 128))
draw = ImageDraw.Draw(image)
draw.text((10,10), 'Hello', fill=(255,255,255))
image.save('example.png')
```


## poppler

Can be used to extract pages from a PDF file:

```bash
docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/pdfseparate altermarkive/poppler -f 1 -l 1 example.pdf %d.pdf
```

Or to join PDF files:

```bash
docker run --rm -it -v $PWD:/w -w /w --entrypoint /usr/bin/pdfunite altermarkive/poppler 0.pdf 1.pdf result.pdf
```


## python-linters

Can be used for thorough Python linting of the current directory like this:

```bash
docker run -it -v $PWD:/w -w /w --entrypoint /bin/lint.sh altermarkive/python-linters
```


## retroactive-git

Can be used in the following way:

```bash
docker run --rm -it -v $PWD:/w -w /w altermarkive/retroactive-git
LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1 FAKETIME_NO_CACHE=1 FAKETIME='1970-01-01 00:00:00' date
LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1 FAKETIME_NO_CACHE=1 FAKETIME='+365d' date
```


## socat

To expose Docker host ports on Docker networks it is often enough to use [`qoomon/docker-host`](https://github.com/qoomon/docker-host) (and it may be necessary to add `--network host`):

```bash
docker run --restart always -d --name forwarder --cap-add=NET_ADMIN --cap-add=NET_RAW qoomon/docker-host
```

However, if an another image is interfering with firewall rules (or cannot grant `NET_ADMIN` or `NET_RAW` cabilities)
it may be necessary to tunnel the traffic with [`socat`](https://www.redhat.com/sysadmin/getting-started-socat),
here an example for `ssh`:

```bash
docker run --restart always -d --name forwarder altermarkive/socat TCP4-LISTEN:22,fork,reuseaddr TCP4:host.docker.internal:22
```

Note: On Linux, the following option might be necessary to be added to the command above: `--add-host=host.docker.internal:host-gateway`


## ssh-jump-server

Prepare the SSH keys:

```bash
mkdir computer
ssh-keygen -t rsa -b 4096 -C "nobody@nowhere" -f computer/id_rsa
touch authorized_keys
cat computer/id_rsa.pub >> authorized_keys
ssh user@computer mkdir /home/user/.jump
scp computer/id_rsa user@computer:/home/user/.jump/id_rsa
scp computer/id_rsa.pub user@computer:/home/user/.jump/id_rsa.pub
kubectl create secret generic authorized-keys --from-file=authorized_keys=authorized_keys
```

Create `ssh-jump-server.yml` file:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ssh-jump-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ssh-jump-server
  template:
    metadata:
      labels:
        app: ssh-jump-server
    spec:
      nodeSelector:
        "beta.kubernetes.io/os": linux
      restartPolicy: Always
      containers:
      - name: ssh-jump-server
        image: altermarkive/ssh-jump-server
        ports:
        - containerPort: 22
        - containerPort: 22000
        volumeMounts:
          - name: authorized-keys-volume
            readOnly: true
            mountPath: "/home/user/.ssh"
      volumes:
      - name: authorized-keys-volume
        secret:
          secretName: authorized-keys
---
apiVersion: v1
kind: Service
metadata:
  name: ssh-jump-server
spec:
  type: LoadBalancer
  ports:
  - port: 22
    targetPort: 22
    name: ssh
    protocol: TCP
  - port: 22000
    targetPort: 22000
    name: ssh0
    protocol: TCP
  selector:
    app: ssh-jump-server
```

Deploy the jump server to Kubernetes cluster:

```bash
kubectl apply -f ssh-jump-server.yml
kubectl describe services
```

Forward the SSH:

```bash
docker run --restart always -d --name forward22 --network host --add-host=host.docker.internal:host-gateway altermarkive/socat TCP4-LISTEN:10022,fork,reuseaddr TCP4:host.docker.internal:22
docker run --restart always -d --name autossh22 --network host -v $HOME/.jump:/keys:ro altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /keys/id_rsa -R 22002:127.0.0.1:10022 -N user@${JUMP_SERVER_HOST}
```

or shorter:

```bash
docker run --restart always -d --name autossh22 -v $HOME/.jump:/keys:ro --add-host=host.docker.internal:host-gateway altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /keys/id_rsa -R 22002:host.docker.internal:22 -N user@${JUMP_SERVER_HOST}
```

Additional materials:

* [How to SSH Into a Kubernetes Pod From Outside the Cluster](https://betterprogramming.pub/how-to-ssh-into-a-kubernetes-pod-from-outside-the-cluster-354b4056c42b)
* [Kubernetes - Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [Kubernetes - Get a Shell to a Running Container](https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/)
* [Kubernetes - Create an External Load Balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)


## svetovid

If you want to automatically become a watcher of Atlassian Jira issues (and are not the owner/administrator) then you can use this service to accomplish this (with suitable email client rules it creates an office experience by revealing what is generally happening without the necessity of acting upon it):

```bash
docker run --restart always -d --name svetovid -e ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" -e ATLASSIAN_USER="$ATLASSIAN_USER" -e ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" -e ATLASSIAN_QUERY="$ATLASSIAN_QUERY" -e ATLASSIAN_WATCHER="$ATLASSIAN_WATCHER" -e SVETOVID_SLEEP="$SVETOVID_SLEEP" altermarkive/svetovid
```


## veles

If you want to prefix Atlassian Jira issues with [...] and have it automatically carried over into labels then you can use this service to accomplish this:

```bash
docker run --restart always -d --name veles -e ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" -e ATLASSIAN_USER="$ATLASSIAN_USER" -e ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" -e ATLASSIAN_QUERY="$ATLASSIAN_QUERY" -e VELES_SLEEP="$VELES_SLEEP" altermarkive/veles
```


# Cheat Sheet

## Keyboard Shortcuts

| Shortcut           | Function                                                         |
| ------------------ | ---------------------------------------------------------------- |
| Ctrl + Shift + Esc | Windows: Open Task Manager                                       |
| Win + B            | Windows: Go to System Tray                                       |
| Shift + F10        | Windows: Right-click in System Tray                              |
| Win + V            | Windows: Paste from Clipboard history                            |
| Win + H            | Windows: Start dictation                                         |
| Win + I            | Windows: System settings                                         |
| Alt + P            | Windows Explorer: Toggle preview panel                           |
| Ctrl + Shift + E   | Visual Studio Code: Navigate between editor and file tree panels |
| Ctrl + \[          | Visual Studio Code: Unindent selection                           |
| Ctrl + \]          | Visual Studio Code: Indent selection                             |
| Ctrl + Shift + L   | Visual Studio Code: Select all occurences                        |
| Alt + D            | Edge: Select the URL in the address bar to edit                  |
| Ctrl + W           | Edge: Close tab                                                  |
| Ctrl + Shift + L   | Visual Studio Code: Select all occurences                        |

## git

### Get latest tag with current "distance"

```bash
git describe --tags --dirty
```

### Re-commit a particular branch / commit/ tag

```bash
git rm -r .
git checkout <branch/tag/commit> .
git commit
```

### Undo local uncommited changes on a specific file

```bash
git checkout -- <file>
```

### Delete remote branch

```bash
git push origin :<branch>
```

### Merging branch as one commit

```bash
git merge --squash <branch> -m <message>
```

### Make the current commit the only commit

```bash
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin <uri>
git push -u --force origin master
```

### Merging repository into another under a subdirectory

```bash
git clone $A_URL $A_NAME
cd $A_NAME
git remote add -f $B_NAME $B_URL
git merge --allow-unrelated-histories -s ours --no-commit $B_NAME/master
git read-tree --prefix=$SUBDIRECTORY -u $B_NAME/master
git commit -m "Merged $B_NAME into $A_NAME under $SUBDIRECTORY"
```

### Print all files ever committed

```bash
git log --abbrev-commit --pretty=oneline | cut -d ' ' -f 1 | xargs -L1 git diff-tree --no-commit-id --name-only -r | sort | uniq
```

### Correcting author for selected commits

See details [here](https://stackoverflow.com/questions/3042437/how-to-change-the-commit-author-for-one-specific-commit).


## Docker

### Nexus 3

Quick start with Nexus 3:

```bash
mkdir /tmp/nexus-data && sudo chown -R 200 /tmp/nexus-data
docker run -p 8081:8081 -p 8082:8082 --name nexus -v /tmp/nexus-data:/nexus-data -it sonatype/nexus3:3.4.0
```


## Bash

* Tutorial about [Bash history](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps)

* Check if the script was called with root privileges:
```bash
if [ "$(id -u)" != "0" ]; then
    echo "This must be run as root!"
    exit 1
fi
```


## Network Troubleshooting

### Wireshark

To filter for UDP, a particular MAC and broadcast use this filter:

```
udp && (eth.addr == 00:11:22:33:44:55 || eth.addr == FF:FF:FF:FF:FF:FF)
```

For more see [this link](https://wiki.wireshark.org/DisplayFilters).

### HTTP

Headers to prevent browsers from caching:

```
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
```


## Links

### Science

* [SciHub](https://sci-hub.se/)

### Cloud

* [Google Cloud Shell](https://shell.cloud.google.com/)

### Other

* [Import from CSV to draw.io](https://drawio-app.com/import-from-csv-to-drawio/)


## OS, web browser, etc.

### Windows

Beep

```bash
powershell -c (New-Object Media.SoundPlayer "C:\beep.wav").PlaySync();
```

Lock the screen

```bash
rundll32 user32.dll, LockWorkStation
```

A command to set the default printer on Windows

```bash
cscript C:\Windows\System32\Printing_Admin_Scripts\en-US\prnmngr.vbs -t -p "\\host\printer"
```

Run Edge as an administrator (or any other user)

```bash
runas /user:"%ADMINISTRATOR%" /savecred "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

Removing Dead Icons From Taskbar

* See: https://www.tenforums.com/tutorials/3151-reset-clear-taskbar-pinned-apps-windows-10-a-3.html

List the password of a WiFi network:

```bash
netsh wlan show profile name=$SSID key=clear
```

File encryption/decryption with GPG

```bash
gpg --cipher-algo AES256 -c filename.tar.gz
gpg -o filename.tar.gz -d filename.tar.gz.gpg
```

### Mac

Basic tools:

```bash
brew install bash git jq yq p7zip python@3.10 meld
```

Completely disable sleep on any Mac:

```bash
sudo pmset -a sleep 0; sudo pmset -a hibernatemode 0; sudo pmset -a disablesleep 1;
```

List partition and format a USB stick:

```bash
diskutil list disk2
diskutil partitionDisk disk2 1 MBR MS-DOS STICK R
```

To make sure that fonts render well on the terminal:

```bash
defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO
defaults -currentHost write -globalDomain AppleFontSmoothing -int 2
```

### Raspberry Pi

Quick and dirty script to expose USB disk from Raspberry Pi over a web server:

```bash
sudo apt-get install apache2 -y
sudo rm -R /var/www
sudo ln -s /mnt /var/www
echo "/dev/sda1 /mnt ntfs ro,user,umask=000 0 0" | sudo tee --append /etc/fstab
sudo reboot
```

### Chrome

* To enable password import got to `chrome://flags/`

### Visual Studio Code

Extensions:

* Docker, docs-markdown, docs-preview, docs-yaml, Pylance, Python, Remote - Containers, Remote - SSH, XML (RedHat), YAML (RedHat)

### Alacritty

`$HOME/.alacritty.yml`:

```yaml
window:
  padding:
    x: 6
    y: 0
  dynamic_padding: true
  decorations: full
  dynamic_title: true
  startup_mode: Maximized

scrolling:
  history: 100000
  multiplier: 1

font:
  normal:
    family: JetBrains Mono
    style: Regular
  bold:
    family: JetBrains Mono
    style: Bold
  italic:
    family: JetBrains Mono
    style: Italic
  bold_italic:
    family: JetBrains Mono
    style: Bold Italic
  size: 14.0
  use_thin_strokes: true

colors:
  primary:
    background: '#0C0C0C'
    foreground: '#CCCCCC'
  cursor:
    cursor: '#FFFFFF'
  selection:
    background: '#FFFFFF'
  normal:
    black:   '#0C0C0C'
    red:     '#C50F1F'
    green:   '#13A10E'
    yellow:  '#C19C00'
    blue:    '#0037DA'
    magenta: '#881798'
    cyan:    '#3A96DD'
    white:   '#CCCCCC'
  bright:
    black:   '#767676'
    red:     '#E74856'
    green:   '#16C60C'
    yellow:  '#F9F1A5'
    blue:    '#3B78FF'
    magenta: '#B4009E'
    cyan:    '#61D6D6'
    white:   '#F2F2F2'

selection:
  save_to_clipboard: true

cursor:
  style:
    shape: Beam
    blinking: On

shell:
  program: '/usr/local/bin/bash'
  args:
    - -i
    - -l

mouse_bindings:
  - { mouse: Middle, action: PasteSelection }
```
