Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true

    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end

  # Install development environment
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    export USER_NAME=ubuntu

    echo "--- Installing ---"
    /bin/bash /vagrant/install.sh

    echo "--- Installing UI with utilities ---"
    apt-get -yq install ubuntu-desktop meld xclip dkms virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11

    echo "--- Removing the bloat ---"
    apt-get -yq remove abiword gnumeric gmusicbrowser parole pidgin xchat thunderbird gimp gnome-mines gnome-sudoku

    echo "--- Cleaning-up ---"
    apt-get -yq autoremove

    echo "--- Installing Atom editor ---"
    wget -q -O /tmp/atom.deb https://atom.io/download/deb
    dpkg -i /tmp/atom.deb
    apt-get -yf install

    echo "--- Installing Docker ---"
    apt-get -yq install apt-transport-https ca-certificates software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get -yq update
    apt-get -yq install docker-ce
    groupadd docker 2> /dev/null
    usermod -aG docker $USER_NAME

    echo "--- Rebooting ---"
    reboot

  SHELL
end
