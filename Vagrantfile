Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_version = "20190409.1.0"
  config.vm.synced_folder "../", "/vagrant"
  config.disksize.size = "40GB"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end

  config.vm.network :forwarded_port, guest: 50000, host: 50000
  config.vm.network :forwarded_port, guest: 50001, host: 50001
  config.vm.network :forwarded_port, guest: 50002, host: 50002
  config.vm.network :forwarded_port, guest: 50003, host: 50003
  config.vm.network :forwarded_port, guest: 50004, host: 50004
  config.vm.network :forwarded_port, guest: 50005, host: 50005
  config.vm.network :forwarded_port, guest: 50006, host: 50006
  config.vm.network :forwarded_port, guest: 50007, host: 50007
  config.vm.network :forwarded_port, guest: 50008, host: 50008
  config.vm.network :forwarded_port, guest: 50009, host: 50009

  config.vm.provision "file", source: "~/.ssh", destination: "$HOME/.ssh"
  config.vm.provision "shell", inline: <<-SHELL
    /bin/sh /vagrant/workspace/install.sh
  SHELL
end
