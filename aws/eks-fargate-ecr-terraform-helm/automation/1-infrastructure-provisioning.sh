#!/bin/sh
# Provision Infrastructure with Terraform
# image: hashicorp/terraform:1.0.11
# environment:
#   - AWS_DEFAULT_REGION
#   - AWS_ACCESS_KEY_ID
#   - AWS_SECRET_ACCESS_KEY
# artifacts:
#   - terraform/aws-logging-cloudwatch-configmap.yaml
#   - terraform/aws-load-balancer-controller-service-account.yaml

set -e

apk add --no-cache python3 py3-pip
pip3 install --disable-pip-version-check --no-cache-dir awscli==1.22.16
rm -rf /var/cache/apk/*
cd terraform
terraform init
terraform validate
terraform refresh
terraform show
terraform plan
terraform apply -auto-approve
terraform show
