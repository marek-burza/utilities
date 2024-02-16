# SSH Jump Server

Prepare the SSH keys:

```bash
mkdir computer
ssh-keygen -t rsa -b 4096 -C "nobody@nowhere" -f computer/id_rsa
touch authorized_keys
cat computer/id_rsa.pub >> authorized_keys
ssh user@computer mkdir /home/user/.jump
scp computer/id_rsa user@computer:/home/user/.jump/id_rsa
scp computer/id_rsa.pub user@computer:/home/user/.jump/id_rsa.pub
kubectl create secret generic authorized-keys --from-file=authorized_keys=authorized_keys
```

Create `ssh-jump-server.yml` file:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ssh-jump-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ssh-jump-server
  template:
    metadata:
      labels:
        app: ssh-jump-server
    spec:
      nodeSelector:
        "beta.kubernetes.io/os": linux
      restartPolicy: Always
      containers:
      - name: ssh-jump-server
        image: altermarkive/ssh-jump-server
        ports:
        - containerPort: 22
        - containerPort: 22000
        volumeMounts:
          - name: authorized-keys-volume
            readOnly: true
            mountPath: "/home/user/.ssh"
      volumes:
      - name: authorized-keys-volume
        secret:
          secretName: authorized-keys
---
apiVersion: v1
kind: Service
metadata:
  name: ssh-jump-server
spec:
  type: LoadBalancer
  ports:
  - port: 22
    targetPort: 22
    name: ssh
    protocol: TCP
  - port: 22000
    targetPort: 22000
    name: ssh0
    protocol: TCP
  selector:
    app: ssh-jump-server
```

Deploy the jump server to Kubernetes cluster:

```bash
kubectl apply -f ssh-jump-server.yml
kubectl describe services
```

Forward the SSH:

```bash
docker run --restart always -d --name forward22 --network host --add-host=host.docker.internal:host-gateway alpine/socat TCP4-LISTEN:10022,fork,reuseaddr 
TCP4:host.docker.internal:22
docker run --restart always -d --name autossh22 --network host -v $HOME/.jump:/keys:ro ghcr.io/altermarkive/autossh -M 0 -o "PubkeyAuthentication=yes" -o 
"PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /keys/id_rsa -R 22002:127.0.0.1:10022 -N user@${JUMP_SERVER_HOST}
```

or shorter:

```bash
docker run --restart always -d --name autossh22 -v $HOME/.jump:/keys:ro --add-host=host.docker.internal:host-gateway ghcr.io/altermarkive/autossh -M 0 -o 
"PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -o "StrictHostKeyChecking no" -i /keys/id_rsa -R 22002:host.docker.internal:22 -N user@${JUMP_SERVER_HOST}
```

Additional materials:

* [How to SSH Into a Kubernetes Pod From Outside the Cluster](https://betterprogramming.pub/how-to-ssh-into-a-kubernetes-pod-from-outside-the-cluster-354b4056c42b)
* [Kubernetes - Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [Kubernetes - Get a Shell to a Running Container](https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/)
* [Kubernetes - Create an External Load Balancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)
