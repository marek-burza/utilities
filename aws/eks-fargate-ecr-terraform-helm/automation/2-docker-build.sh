#!/bin/sh
# Build and Push Docker Container Image
# image: python:3.10.0
# environment:
#   - AWS_DEFAULT_REGION
#   - AWS_ACCESS_KEY_ID
#   - AWS_SECRET_ACCESS_KEY
#   - IMAGE_NAME
#   - IMAGE_VERSION

set -e

pip3 install --disable-pip-version-check --no-cache-dir awscli==1.22.16
eval $(aws ecr get-login --region ${AWS_DEFAULT_REGION} --no-include-email)
export AWS_REGISTRY_URL=$(aws ecr describe-repositories | python -c 'import sys, json; print(next(item for item in json.load(sys.stdin)["repositories"] if item["repositoryName"] == "'$IMAGE_NAME'")["repositoryUri"])')
docker build -t ${IMAGE_NAME} .
docker tag ${IMAGE_NAME}:latest ${AWS_REGISTRY_URL}:latest
docker tag ${IMAGE_NAME}:latest ${AWS_REGISTRY_URL}:${IMAGE_VERSION}
docker push ${AWS_REGISTRY_URL}:latest
docker push ${AWS_REGISTRY_URL}:${IMAGE_VERSION}
