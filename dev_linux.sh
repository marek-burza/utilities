#!/bin/bash
#
# This script helps to set up the development environment on Xubuntu (in VirtualBox)
#
# The MIT License (MIT)
#
# Copyright (c) 2016
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

export USER_NAME=ubuntu

echo
echo "Updating the system"
apt-get update
apt-get upgrade

echo
echo "Installing Xubuntu desktop"
apt-get install -y xubuntu-desktop

echo
echo "Enabling auto-login"
echo "[SeatDefaults]" >> /etc/lightdm/lightdm.conf.d/10-autologin.conf
echo "autologin-user=$USER_NAME" >> /etc/lightdm/lightdm.conf.d/10-autologin.conf

echo
echo "Starting X11"
startx &
sleep 10

echo
echo "Disabling the screen lock"
gsettings set apps.light-locker lock-on-suspend false
gsettings set org.gnome.settings-daemon.plugins.power active false
gsettings set org.gnome.desktop.screensaver lock-enabled false

echo
echo "Removing the bloat"
apt-get remove abiword gnumeric gmusicbrowser parole pidgin xchat firefox thunderbird gimp simple-scan gnome-mines gnome-sudoku

echo
echo "Cleaning-up"
apt-get autoremove -y

echo
echo "Installing utilities"
apt-get install -y mc imagemagick

echo
echo "Installing essential build environment, Java, Python 3, git & meld"
apt-get install -y build-essential default-jdk python-pip python3-pip subversion git meld xclip

echo
echo "Enabling dynamic display resolution (assuming VirtualBox environment)"
apt-get install -y dkms

echo
echo "Installing VirtualBox guest additions for X11"
apt-get install -y virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11

echo
echo "Installing Atom editor"
wget -q -O /tmp/atom.deb https://atom.io/download/deb
dpkg -i /tmp/atom.deb

echo
echo "Installing Chrome"
apt-get install -y libindicator7 libappindicator1
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb
apt-get -yf install

echo
echo "Installing Docker"
apt-get install -y apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo deb https://apt.dockerproject.org/repo ubuntu-xenial main | sudo tee /etc/apt/sources.list.d/docker.list 2> /dev/null
apt-get update
apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-get install -y docker-engine
service docker start
groupadd docker 2> /dev/null
usermod -aG docker $USER_NAME

echo
echo "Instaling AWS Python module"
pip3 install boto3
pip3 install awscli

echo
echo "Installation ready - rebooting!"
reboot
