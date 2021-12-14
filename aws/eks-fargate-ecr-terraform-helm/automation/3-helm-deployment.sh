#!/bin/sh
# Deploy Docker Container Image
# image: python:3.10.0
# environment:
#   - AWS_DEFAULT_REGION
#   - AWS_ACCESS_KEY_ID
#   - AWS_SECRET_ACCESS_KEY
#   - IMAGE_NAME
#   - IMAGE_VERSION
# artifacts:
#   - terraform/aws-logging-cloudwatch-configmap.yaml
#   - terraform/aws-load-balancer-controller-service-account.yaml

set -e

# Install AWS CLI
pip3 install --disable-pip-version-check --no-cache-dir awscli==1.22.16

# https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
curl -o /usr/local/bin/kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.21.2/2021-07-05/bin/linux/amd64/kubectl
chmod +x /usr/local/bin/kubectl

# https://helm.sh/docs/intro/install/
curl -o helm-linux-amd64.tar.gz https://get.helm.sh/helm-v3.7.1-linux-amd64.tar.gz
tar -zxvf helm-linux-amd64.tar.gz
cp linux-amd64/helm /usr/local/bin/helm
chmod +x /usr/local/bin/helm
rm -rf helm-linux-amd64.tar.gz linux-amd64

# Print cluster status and configure kubectl
aws eks describe-cluster --name examplecluster --query cluster.status
aws eks update-kubeconfig --name examplecluster

# https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html
kubectl apply -f kubectl/aws-observability-namespace.yaml
kubectl apply -f terraform/aws-logging-cloudwatch-configmap.yaml

# https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html
kubectl patch deployment coredns -n kube-system --type json -p='[{"op":"remove", "path":"/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]' || true

# https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
kubectl apply -f terraform/aws-load-balancer-controller-service-account.yaml

# https://www.eksworkshop.com/beginner/180_fargate/prerequisites-for-alb/
# https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
# https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/2071
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=v0.0.50"
helm repo add eks https://aws.github.io/eks-charts
helm repo update
export VPC_ID=$(aws eks describe-cluster --name examplecluster --query "cluster.resourcesVpcConfig.vpcId" --output text)
helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=examplecluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller --set image.repository=602401143452.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/amazon/aws-load-balancer-controller --version "1.1.6" --set image.tag="v2.1.3" --set region=${AWS_DEFAULT_REGION} --set vpcId=${VPC_ID}

# https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/examples/2048/2048_full.yaml
export AWS_REGISTRY_URL=$(aws ecr describe-repositories | python -c 'import sys, json; print(next(item for item in json.load(sys.stdin)["repositories"] if item["repositoryName"] == "'$IMAGE_NAME'")["repositoryUri"])')
helm upgrade -i --set image_uri="$AWS_REGISTRY_URL" --set image_tag="$IMAGE_VERSION" --set aws_secret_access_key="$(echo -n $AWS_SECRET_ACCESS_KEY | base64 -w 0)" --set aws_access_key_id="$(echo -n $AWS_ACCESS_KEY_ID | base64 -w 0)" --set aws_default_region="$AWS_DEFAULT_REGION" example-chart ./helm

# Diagnostics
kubectl get all
kubectl get svc
kubectl describe po
kubectl get all -n kube-system
kubectl get svc -n kube-system
kubectl describe po -n kube-system
kubectl get all -n examplefargatenamespace
kubectl get svc -n examplefargatenamespace
kubectl describe po -n examplefargatenamespace
kubectl get ingress/exampleingress -n examplefargatenamespace
