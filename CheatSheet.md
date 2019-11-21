# Chrome

* To enable password import got to `chrome://flags/`


# Bash

* Tutorial about [Bash history](https://www.digitalocean.com/community/tutorials/how-to-use-bash-history-commands-and-expansions-on-a-linux-vps)


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


# Wireshark

To filter for UDP, a particular MAC and broadcast use this filter:

    udp && (eth.addr == 00:11:22:33:44:55 || eth.addr == FF:FF:FF:FF:FF:FF)
