Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  gitlab_server_fqdn = ENV["GITLAB_SERVER_FQDN"]
  gitlab_server_email = ENV["GITLAB_SERVER_EMAIL"]

  config.vm.hostname = gitlab_server_fqdn
  config.vm.network :forwarded_port, guest: 80, host: 8880
  config.vm.network :forwarded_port, guest: 443, host: 8443
  config.vm.network :forwarded_port, guest: 8822, host: 8822

  base = File.dirname(__FILE__)
  ENV['ANSIBLE_ROLES_PATH'] = "#{base}/ansible/roles"

  config.vm.synced_folder "#{base}/gitlab", "/srv/gitlab", create: true, type: "rsync"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.ssh.insert_key = false
  config.vbguest.auto_update = true

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "#{base}/ansible/books/provision.yml"
    ansible.config_file = "#{base}/ansible/ansible.cfg"
    ansible.raw_arguments = ["-u", "vagrant", "--private-key=~/.vagrant.d/insecure_private_key"]
    ansible.extra_vars = {
      "ansible_dir" => "#{base}/ansible",
      "ansible_ssh_user" => "vagrant",
      "gitlab_server_fqdn" => gitlab_server_fqdn,
      "gitlab_server_email" => gitlab_server_email
    }
  end
end
