# Utilities

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


## PDF Image Conversion (imagemagick)

Can be used for conversion between formats:

```bash
convert example.png example.pdf
convert -density 600 example.pdf example.png
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

## PDF Encryption

Use this command to encrypt a PDF file:

```bash
qpdf --encrypt $PASSWORD $PASSWORD 256 -- $PDF_FILE _$PDF_FILE
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

## Links

### Science

* [SciHub](https://sci-hub.se/)

### Cloud

* [Google Cloud Shell](https://shell.cloud.google.com/)

### Commute Time Map - Isochrones

* [Smappen](https://www.smappen.com/)
* [OpenRouteService](https://maps.openrouteservice.org/)

### Static Topographic Map with GPX

* [gpx2png](https://altermarkive.github.io/altermarkive/gpx2png.html) - upload a GPX file and download a PNG file

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

# Linux

- Disable CUPS: https://securityonline.info/severe-unauthenticated-rce-flaw-cvss-9-9-in-gnu-linux-systems-awaiting-full-disclosure/
