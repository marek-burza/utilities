# Azure IoT Edge: Virtual Kubelet & AKS

Source materials:

* https://github.com/azure/iot-edge-virtual-kubelet-provider
* https://tsmatz.wordpress.com/2020/04/06/azure-iot-edge-connector-kubernetes-virtual-kubelet/
* https://thenewstack.io/tutorial-kubernetes-for-orchestrating-iot-edge-deployments/

## Step 1: Provision an Azure IoT Hub, an Azure IoT Edge device instance & Azure Kubernetes Service cluster

To accomplish this step, run:

```bash
./provisioning1.create.sh $PREFIX $LOCATION
```

## Step 2: Provision an edge device

See [here](../iot-edge-with-ansible) for details.

## Step 3: Provision Virtual Kubelet

To accomplish this step, run:

```bash
./provisioning2.create.sh $PREFIX
```

## Step 3: Experiment

Tag the device:

```bash
az iot hub device-twin update --device-id ${PREFIX}prototype --hub-name ${PREFIX}hub --set tags='{"device":"'${PREFIX}'prototype"}'
sed 's/DEVICE_TAG/'${PREFIX}prototype'/g' prototype-deployment.yaml.template > prototype-deployment.yaml
```

```bash
kubectl apply -f prototype-deployment.yaml
```
