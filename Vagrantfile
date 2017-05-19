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
    /bin/bash /vagrant/dev_linux.sh
  SHELL
end
