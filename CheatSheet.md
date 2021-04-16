# Keyboard Shortcuts

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
| Ctrl + L           | Firefox: Go to address bar                                       |


# Chrome

* To enable password import got to `chrome://flags/`


# Bash

* Tutorial about [Bash history](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps)

* Check if the script was called with root privileges:
```bash
if [ "$(id -u)" != "0" ]; then
    echo "This must be run as root!"
    exit 1
fi
```

# Photos & Videos

To adjust the photo dates install the following packages:

    sudo apt-get install exiftags jhead

To add EXIF:

    jhead -mkexif IMG_0000.jpg

To shift the date:

    exiftime -v-55M -fw -ta *.JPG

To encode H.265:

    ffmpeg -i input.mp4 -metadata creation_time="1970-01-10T00:00:00Z" -c:v libx265 -c:a aac output.hevc.mp4

To transcode from DVD:

    ffmpeg -i dvd.vob -f mp4 -vcodec libx264 -profile:v main -level 4.0 -s 480x384 -b:v 500k -maxrate 500k -bufsize 1000k -c:a aac -strict experimental -ac 2 -ar 48000 -ab 192k -threads 0 video.mp4

To scale:

    ffmpeg -i video.mp4 -vf scale=540:960 scaled.mp4

To convert video to individual frames:

    ffmpeg -i video.mp4 frame.%08d.png

To create a silent audio file:

    ffmpeg -f s16le -ac 1 -t 1 -i /dev/zero -ar 22050 -y silence.mp3

To concatenate files:

    ffmpeg -i concat:"one.mp3|two.mp3" -strict -2 -y three.aac

To combine video frames with audio:

    for ENTRY in $(ls -1 *.jpg | sed -e 's/\.jpg//g')
    do
        ffmpeg -loop 1 -i ${ENTRY}.jpg -i ${ENTRY}.aac -strict -2 -crf 25 -c:v libx264 -tune stillimage -pix_fmt yuv420p -shortest -y ${ENTRY}.mp4
    done


# Windows

Beep

    powershell -c (New-Object Media.SoundPlayer "C:\beep.wav").PlaySync();

Lock the screen

    rundll32 user32.dll, LockWorkStation

A command to set the default printer on Windows

    cscript C:\Windows\System32\Printing_Admin_Scripts\en-US\prnmngr.vbs -t -p "\\host\printer"

Removing Dead Icons From Taskbar

* See: https://www.tenforums.com/tutorials/3151-reset-clear-taskbar-pinned-apps-windows-10-a-3.html

List the password of a WiFi network:

    netsh wlan show profile name=$SSID key=clear


# git

## Get latest tag with current "distance"

    git describe --tags --dirty

## Re-commit a particular branch / commit/ tag

    git rm -r .
    git checkout <branch/tag/commit> .
    git commit

## Undo local uncommited changes on a specific file

    git checkout -- <file>

## Delete remote branch

    git push origin :<branch>

## Merging branch as one commit

    git merge --squash <branch> -m <message>

## Make the current commit the only commit

    rm -rf .git
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin <uri>
    git push -u --force origin master


## Merging repository into another under a subdirectory

    git clone $A_URL $A_NAME
    cd $A_NAME
    git remote add -f $B_NAME $B_URL
    git merge --allow-unrelated-histories -s ours --no-commit $B_NAME/master
    git read-tree --prefix=$SUBDIRECTORY -u $B_NAME/master
    git commit -m "Merged $B_NAME into $A_NAME under $SUBDIRECTORY"


## Print all files ever committed

    git log --abbrev-commit --pretty=oneline | cut -d ' ' -f 1 | xargs -L1 git diff-tree --no-commit-id --name-only -r | sort | uniq


## Correcting author for selected commits

See details [here](https://stackoverflow.com/questions/3042437/how-to-change-the-commit-author-for-one-specific-commit).


# Network Troubleshooting

## Wireshark

To filter for UDP, a particular MAC and broadcast use this filter:

    udp && (eth.addr == 00:11:22:33:44:55 || eth.addr == FF:FF:FF:FF:FF:FF)

For more see [this link](https://wiki.wireshark.org/DisplayFilters).

## ncat

Here is the [link to ncat man page](http://man7.org/linux/man-pages/man1/ncat.1.html).

Send text "test" in a UDP packet over IPv4 with a connection time of 1 second from port 5000 to a broadcast address 172.17.255.255 and port 10000:

    echo test | netcat -4u -w1 -p 5000 -b 172.17.255.255 10000


# Science

* [SciHub](https://sci-hub.se/)


# Cloud

* [Google Cloud Shell](https://shell.cloud.google.com/)


# Mac

Completely disable sleep on any Mac:

    sudo pmset -a sleep 0; sudo pmset -a hibernatemode 0; sudo pmset -a disablesleep 1;

List partition and format a USB stick:

    diskutil list disk2
    diskutil partitionDisk disk2 1 MBR MS-DOS STICK R