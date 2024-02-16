Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  gitlab_ci_runner_url = ENV["GITLAB_CI_RUNNER_URL"]
  gitlab_ci_runner_token = ENV["GITLAB_CI_RUNNER_TOKEN"]

  config.vm.hostname = SecureRandom.hex(16)

  base = File.dirname(__FILE__)
  ENV['ANSIBLE_ROLES_PATH'] = "#{base}/ansible/roles"

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
      "gitlab_ci_runner_url" => gitlab_ci_runner_url,
      "gitlab_ci_runner_token" => gitlab_ci_runner_token
    }
  end
end
