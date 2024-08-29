# Utilities

## Editing Photos (jhead, exiftime, exiftool)

To run the tools included install following packages on Ubuntu: `jhead`, `exiftags`, `libimage-exiftool-perl`.

To add EXIF:

```bash
jhead -mkexif IMG_0000.jpg
```

To shift the date:

```bash
exiftime -v-55M -fw -ta *.JPG
```

To set an arbitrary date:

```bash
exiftool "-AllDates=20221131000000" example.jpg
```

Rename photos to feature album name and creation date:

```bash
find -type f -printf "mv %p \$ALBUM.\$(exiftool -CreateDate %p | cut -c 35- | sed 's/[ :]//g').jpg\n" | sh
```


## Editing Videos (ffmpeg)

Can be used for AV conversion between formats ([`linuxserver/ffmpeg`](https://github.com/linuxserver/docker-ffmpeg)):

```bash
docker run --rm -it -v $PWD:/w -w /w linuxserver/ffmpeg -i example.avi -c:a aac -c:v libx264 example.mp4
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


## Image Conversion (imagemagick)

Can be used for conversion between formats:

```bash
convert example.png example.pdf
convert -density 600 example.pdf example.png
```

Or, in combination with the `exif` utility, one can run the following `compact.sh`:

```bash
#!/bin/sh
EXTENSION=$1
PREFIX=$2
TEMPORARY_SCRIPT=./compact.$PREFIX.sh
RENAME="echo -n convert {}; echo -n \ $PREFIX/$PREFIX.; exiftool -CreateDate {} | sed s/[^0-9]*//g | sed -e 's/\$/\.heic/'"
RENAME_ALL="find $PREFIX -name $EXTENSION -exec /bin/sh -c \"$RENAME\" \;"
/bin/sh -c "$RENAME_ALL" | tr -d '\r' > $TEMPORARY_SCRIPT
cat $TEMPORARY_SCRIPT
/bin/sh $TEMPORARY_SCRIPT
rm $TEMPORARY_SCRIPT
```


## PDF Conversion (brew: poppler; Ubuntu: poppler-tools)

Can be used to extract pages from a PDF file:

```bash
pdfseparate -f 1 -l 1 example.pdf %d.pdf
```

Or to join PDF files:

```bash
pdfunite 0.pdf 1.pdf result.pdf
```

## PDF Optimization

Use this command to rescale images in a PDF file (screen = 75dpi, ebook = 150dpi, printer = 300dpi):

```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

## Midnight Commander

Use: `blackvoidclub/midnight-commander`

```bash
docker run -it --name=mc -v $PWD:/w -w /w blackvoidclub/midnight-commander -S dark
```


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

or

```bash
git switch example-branch
git reset --soft $(git merge-base master HEAD)
git commit -m "one commit on example branch"
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

### Correcting author for all commits

```bash
git config user.name "Corrected Name"
git config user.email corrected.name@somewhere.com
git rebase --root --exec 'git commit --amend --no-edit --reset-author'
git push -f
```

### Scheduled Prefetch

```bash
git maintenance start
```

### Accelerate Status

```bash
git config core.fsmonitor true
git config core.untrackedcache true
```


## Ubuntu / Bash

Keyboard shortcuts:

| Shortcut           | Function                                                         |
| ------------------ | ---------------------------------------------------------------- |
| Ctrl + K           | bash: Clear characters in line after cursor                      |

* Tutorial about [Bash history](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps)

* Check if the script was called with root privileges:
```bash
if [ "$(id -u)" != "0" ]; then
    echo "This must be run as root!"
    exit 1
fi
```

* Parameterize successive arguments:
```bash
cp {source,destination}.txt
```


## Network Troubleshooting

### Wireshark

To filter for UDP, a particular MAC and broadcast use this filter:

```
udp && (eth.addr == 00:11:22:33:44:55 || eth.addr == FF:FF:FF:FF:FF:FF)
```

For more see [this link](https://wiki.wireshark.org/DisplayFilters).

### netcat

Send text "test" in a UDP packet over IPv4 with a connection time of 1 second from port 5000 to a broadcast address 172.17.255.255 and port 10000:

```bash
echo test | netcat -4u -w1 -p 5000 -b 172.17.255.255 10000
```

### HTTP

Headers to prevent browsers from caching:

```
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
```


## IMAP Migration

```shell
docker run --rm gilleslamiral/imapsync imapsync --gmail1 --office2 --dry --user1 "$G_USER" --password1 "$G_PASS" --user2 "$M_USER" --password2 "$M_PASS" --exclude 'All Mail|Spam|Drafts|Important|Starred|Trash' --skipemptyfolders
```


## Links

### Science

* [SciHub](https://sci-hub.se/)

### Cloud

* [Google Cloud Shell](https://shell.cloud.google.com/)

### Commute Time Map - Isochrones

* [Smappen](https://www.smappen.com/)
* [OpenRouteService](https://maps.openrouteservice.org/)

### Static Topographic Map with GPX

* [OpenTopoMap](https://opentopomap.org/) - upload a GPX file and take a screen shot

### Other

* [Import from CSV to draw.io](https://drawio-app.com/import-from-csv-to-drawio/)


## Windows

Keyboard shortcuts:

| Shortcut           | Function                                                         |
| ------------------ | ---------------------------------------------------------------- |
| Ctrl + Shift + Esc | Windows: Open Task Manager                                       |
| Win + B            | Windows: Go to System Tray                                       |
| Shift + F10        | Windows: Right-click in System Tray                              |
| Win + V            | Windows: Paste from Clipboard history                            |
| Win + H            | Windows: Start dictation                                         |
| Win + I            | Windows: System settings                                         |

Beep:

```bash
powershell -c (New-Object Media.SoundPlayer "C:\beep.wav").PlaySync();
```

Lock the screen:

```bash
rundll32 user32.dll, LockWorkStation
```

A command to set the default printer on Windows:

```bash
cscript C:\Windows\System32\Printing_Admin_Scripts\en-US\prnmngr.vbs -t -p "\\host\printer"
```

Run Edge as an administrator (or any other user):

```bash
runas /user:"%ADMINISTRATOR%" /savecred "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

Removing Dead Icons From Taskbar:

* See: https://www.tenforums.com/tutorials/3151-reset-clear-taskbar-pinned-apps-windows-10-a-3.html

List the password of a WiFi network:

```bash
netsh wlan show profile name=$SSID key=clear
```

File encryption/decryption with GPG:

```bash
gpg --cipher-algo AES256 -c filename.tar.gz
gpg -o filename.tar.gz -d filename.tar.gz.gpg
```

## Mac

Keyboard shortcuts:

| Shortcut           | Function                                                         |
| ------------------ | ---------------------------------------------------------------- |
| ⌘ + Shift + E      | Visual Studio Code: Navigate between editor and file tree panels |
| ⌘ + \[             | Visual Studio Code: Unindent selection                           |
| ⌘ + \]             | Visual Studio Code: Indent selection                             |
| ⌘ + Shift + L      | Visual Studio Code: Select all occurences                        |
| ⌘ + K, V           | Visual Studio Code: Preview Markdown                             |

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

## Chrome / Edge

Keyboard shortcuts:

| Shortcut           | Function                                                         |
| ------------------ | ---------------------------------------------------------------- |
| ⌘ + L              | Edge: Select the URL in the address bar to edit                  |
| ⌘ + W              | Edge: Close tab                                                  |

* To enable password import got to `chrome://flags/`

## Visual Studio Code

Extensions:

* [Dev Containers (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
* [Docker (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
* [GitLens (GitKraken)](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
* [Prettier (prettier.io)](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
* [learn-markdown (Microsoft)](https://marketplace.visualstudio.com/items?itemName=docsmsft.docs-markdown)
* [learn-preview (Microsoft)](https://marketplace.visualstudio.com/items?itemName=docsmsft.docs-preview)
* [Pylance (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [Python (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [Remote - SSH (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
* [YAML (RedHat)](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
