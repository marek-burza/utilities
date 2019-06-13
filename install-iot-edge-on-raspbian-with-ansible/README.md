# Introduction

This is a set of Ansible scripts which automate installation of Azure IoT Edge on Raspbian.

The scripts are based on the original guide [here](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge-linux-arm).


# Assumptions

It is assumed that:
* The IP address of the Raspberry Pi is placed in the file `inventory` in the main directory of this cloned repository
* The Raspberry Pi is running Raspbian (the scripts were tested with Stretch)
* SSH is installed and accessible from outside of the Raspberry Pi
* Your public SSH key was copied to the Raspberry Pi
  (see [here](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md) for details)


# Installation

First, register an Azure IoT Edge Device ([here](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-register-device-portal) are details).

**Caution:** For a Raspberry Pi remember to set _OptimizeForPerformance_ to _false_ (see [here](https://docs.microsoft.com/en-us/azure/iot-edge/troubleshoot#stability-issues-on-resource-constrained-devices) for more details; see [here](./iot_edge.deployment.json) for an example)

An example script to automate the above steps can be found [here](./iot_edge.creation.sh).

Then, once you have connection string, run these commands:

```shell
read -s -p "Please enter IoT Edge Device connection string: " IOTEDGE_CONNECTION_STRING
cd ansible
export ANSIBLE_ROLES_PATH=$(pwd)/roles
ansible-playbook -u pi -i ../inventory --extra-vars "ansible_dir=$(pwd) ansible_ssh_user=pi iotedge_connection_string=$IOTEDGE_CONNECTION_STRING" books/provision.yml
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
