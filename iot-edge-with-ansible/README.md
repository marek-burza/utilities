# Introduction

This is a set of Ansible scripts which automate installation of Azure IoT Edge.

The scripts are based on the original guide [here](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge).


# Assumptions

It is assumed that:

* The IP address of the target machine is placed in the file `inventory` in the main directory of this cloned repository
* SSH server is installed and accessible from outside of the target machine
* Your public SSH key was copied to the target machine
  (see [here](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md) for details)

Here is an example `inventory` file if you decide to use the included `Vagrantfile`:

```
machine ansible_ssh_host=127.0.0.1 ansible_ssh_port=2222 ansible_ssh_user='vagrant' ansible_ssh_private_key_file='~/.vagrant.d/insecure_private_key'
```

# Installation

First, register an Azure IoT Edge Device ([here](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-register-device-portal) are details).

**Caution:** For a Raspberry Pi remember to set _OptimizeForPerformance_ to _false_ (see [here](https://docs.microsoft.com/en-us/azure/iot-edge/troubleshoot#stability-issues-on-resource-constrained-devices) for more details; see [here](./iot_edge.deployment.json) for an example)

An example script to automate the above steps can be found [here](./iot_edge.creation.sh).

Then, once you have connection string, run these commands (here, assuming a Raspberry Pi as the target machine):

```shell
read -s -p "Please enter IoT Edge Device connection string: " AZURE_IOT_EDGE_CONNECTION_STRING
cd ansible
ansible-galaxy install geerlingguy.docker
ansible-galaxy install geerlingguy.docker_arm
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u pi -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=pi azure_iot_edge_connection_string=$AZURE_IOT_EDGE_CONNECTION_STRING" books/provision.yml
```

Here is the variant of the last command for the included `Vagrantfile`:

```shell
ansible-playbook -u vagrant -i ../inventory --key-file=~/.vagrant.d/insecure_private_key --extra-vars "ansible_user=vagrant azure_iot_edge_connection_string=$AZURE_IOT_EDGE_CONNECTION_STRING" books/provision.yml
```


# Notes

If you are working with [Revolution Pi Core 3](https://revolution.kunbus.de/shop/en/revpi-core-3) there are additional steps to take.

1. Download Raspbian Stretch image [here](https://revolution.kunbus.de/shop/en/stretch)
2. Flash the image following the instructions listed [here](https://www.raspberrypi.org/documentation/hardware/computemodule/cm-emmc-flashing.md) (mind that `rpiboot` may have issues running on Windows 7 so it is best to use Linux)
3. The first time you SSH into the device you will have to configure the serial number and MAC - the steps are described [here](https://revolution.kunbus.com/tutorials/images-2/ein-neues-image-sichern-und-installieren-jessie-und-stretch/)
4. The image runs a web-based interface which will conflict with Azure IoT Edge, this can be disabled with the following commands (source information can be found [here](https://revolution.kunbus.de/tutorials/software-2/revolution-pi-dienste-aktivieren-und-deaktivieren/)):
```shell
sudo systemctl stop apache2
sudo systemctl disable apache2
```
5. There is also a firewall in place, to remove all restrictions run the following commands:
```shell
sudo iptables -F
sudo iptables-save | sudo tee /etc/iptables.conf
```
