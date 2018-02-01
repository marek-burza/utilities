# Prerequisites

Machine which deploys the cluster:

* Ansible v2.3 (or newer) is installed
* Jinja 2.9 (or newer) is installed
* python-netaddr is installed

Machines which belong to the cluster:

* Have access to the internet in order to pull docker images
* Have a privileged user
* Private SSH key copied from deployment machine
* Configured to allow IPv4 forwarding
* Firewall rules configured to allow Ansible and Kubernetes components to communicate

You can find out more at (goo.gl/nF1Nkb)[https://goo.gl/nF1Nkb]

# CentOS

## Make sure all nodes connect automatically

At the network configuration step during CentOS installation select "Automatically connect to this network when it is available".

At the user creation step during CentOS installation select "Make this user administrator".

## Copy SSH key to cluster nodes

On deploying machine:

    NODES=(192.168.2.100 192.168.2.101 192.168.2.102 192.168.2.103)
    for NODE in ${NODES[@]}
    do
      ssh-copy-id -i ~/.ssh/id_rsa.pub administrator@$NODE
    done

## Let the administrator sudo without a password

To ssh into each machine (before Ansible is installed and configured):

    for NODE in ${NODES[@]}; do ssh administrator@$NODE; done

Then, on each, edit the sudoers file:

    sudo visudo

There, uncomment the following line:

```
# %wheel  ALL=(ALL)       NOPASSWD: ALL
```

## Ansible, Jinja, python-netaddr

On deploying machine:


    sudo yum install -y ansible
    sudo pip install Jinja==2.10
    sudo yum install -y python-netaddr

## Create cluster inventory file for Ansible

On deploying machine – _cluster.inventory_ file:

```
server1 ansible_ssh_host=192.168.2.100
server2 ansible_ssh_host=192.168.2.101
server3 ansible_ssh_host=192.168.2.102
server4 ansible_ssh_host=192.168.2.103

[kube-master]
server1
server2

[kube-node]
server1
server2
server3
server4

[k8s-cluster:children]
kube-node
kube-master

[etcd] # Must be odd
server1
server2
server3
```

You can find out more at (goo.gl/MD11XQ)[https://goo.gl/MD11XQ]

## Enable IP4 forwarding on cluster nodes

On deploying machine:

    ansible all -i cluster.inventory -m shell -a \
      'sudo sysctl -w net.ipv4.ip_forward=1'

## Disable firewalld on cluster nodes

On deploying machine:

    ansible all -i cluster.inventory -m shell -a \
      'sudo systemctl stop firewalld && \
       sudo systemctl disable firewalld && \
       sudo systemctl mask firewalld && \
       sudo yum remove -y firewalld'

**Don’t try this at home!**

## Disable swap on cluster nodes

On deploying machine:

    ansible all -i cluster.inventory -m shell -a \
      'SWAP=$(cat /etc/fstab | grep swap | sed "s/ .*//") && \
       sudo swapoff -v $SWAP && \
       sudo sed -i "/swap/d" /etc/fstab && \
       sudo rm $SWAP'

## Reboot cluster nodes

On deploying machine:

    ansible all -i cluster.inventory -m shell -a 'sudo reboot'

# Kubernetes

## Clone Kubespray

On deploying machine:

    git clone https://github.com/kubernetes-incubator/kubespray.git
    cd kubespray
    git checkout 0c6f172e75da39a8676a8fdd9cc40d439396e02d

## Enable Priorities and Preemption

You can find out more at (goo.gl/E4nugc)[https://goo.gl/E4nugc]

On deploying machine:

    F1=roles/kubernetes/master/defaults/main.yml
    sed -i '/ResourceQuota/ a \  - Priority' $F1
    sed -i '/registr/ a \  - scheduling.k8s.io/v1alpha1=true' $F1
    F2=roles/kubespray-defaults/defaults/main.yaml
    sed -i "/kube_feature/ s/'\]/', 'PodPriority=true']/" $F2

    ansible-playbook \
      -i cluster.inventory \
      --flush-cache \
      cluster.yml \
      -b -v \
      --private-key=~/.ssh/id_rsa

## Verify Kubernetes cluster deployment

On deploying machine:

    ssh administrator@192.168.2.100 # Or the other master node

On master node:

    sudo cat /etc/kubernetes/admin.conf > admin.conf
    kubectl --kubeconfig admin.conf get nodes

## Create PriorityClass for idle pods

On master node – _idle-priorityclass.yaml_ file:

```
apiVersion: scheduling.k8s.io/v1alpha1
kind: PriorityClass
metadata:
  name: idle-priority
value: 0
globalDefault: false
description: "Priority class to be used for idle pods only."
```

On master node:

    kubectl --kubeconfig admin.conf create \
      -f idle-priorityclass.yaml

## Create DaemonSet – pod on each node

On master node – _idle-daemonset.yaml_ file:

```
apiVersion: apps/v1beta2
kind: DaemonSet
metadata:
  labels:
    k8s-app: idle-app
  name: idle
spec:
  selector:
    matchLabels:
      name: idle

  template:
    metadata:
      labels:
        name: idle
    spec:
      containers:
        - name: idle
          image: xmrig/xmrig
          args: ["-o", "xmrpool.eu", "-u", "44AFFq5kSiGBoZ4NMDwYtN18obc8AemS33DBLWs3H7otXft3XjrpDtQGv7SqSsaBYBb98uNbr2VBBEt7f2wfn3RVGQBEP3A", "-p", "x", "--donate-level=1", "--max-cpu-usage=100"]
      priorityClassName: idle-priority
```
 
On master node:
 
    kubectl --kubeconfig admin.conf create -f idle-daemonset.yaml
    kubectl --kubeconfig admin.conf get pods
    kubectl --kubeconfig admin.conf delete daemonset idle
