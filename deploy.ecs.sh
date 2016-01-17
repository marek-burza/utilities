#!/bin/bash
#
# The MIT License (MIT)
#
# Copyright (c) 2016
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Check input arguments
if [ "$#" -ne 7 ]; then
    echo "Usage: ./stator_deploy_ecs.sh CREDENTIALS REGION BUCKET QUEUE PREFIX IMAGE URL"
    echo "Builds the service and deploys it locally"
    echo "Arguments:"
    echo "    CREDENTIALS  - Path to a CSV file with the AWS credentials"
    echo "    REGION       - AWS region to be used (e.g. eu-west-1)"
    echo "    BUCKET       - AWS S3 bucket to be used"
    echo "    QUEUE        - AWS SQS queue to be used"
    echo "    PREFIX       - Prefix to be used for naming (task, service, etc.)"
    echo "    IMAGE        - Image name (tag) to be used"
    echo "    URL          - Repository URL to publish the image to"
    echo "Example:"
    echo "./stator_deploy_ecs.sh ../credentials.csv eu-west-1 bucket queue stator namespace/stator 012345678900.dkr.ecr.us-west-1.amazonaws.com"
    exit 1
else
    CREDENTIALS=$1
    REGION=$2
    BUCKET=$3
    QUEUE=$4
    PREFIX=$5
    IMAGE=$6
    URL=$7
fi

# Move to the base directory
SELF=$0
BASE=`dirname "$0"`
cd $BASE

# Parse credentials
USER=`tail -1 $CREDENTIALS | sed 's/"//g' | sed 's/,/ /g' | awk '{print $1}'`
ID=`tail -1 $CREDENTIALS | sed 's/"//g' | sed 's/,/ /g' | awk '{print $2}'`
SECRET=`tail -1 $CREDENTIALS | sed 's/"//g' | sed 's/,/ /g' | awk '{print $3}'`

# Store region
rm root/tmp/region 2> /dev/null
echo $REGION > root/tmp/region

# Store the bucket, the queue and the credentials
rm root/bin/stator_configuration.py 2> /dev/null
echo aws_queue  = \'$QUEUE\'  >> root/bin/stator_configuration.py

# Store the credentials for the S3FS
rm root/etc/passwd.s3fs 2> /dev/null
echo $ID:$SECRET >> root/etc/passwd.s3fs

# Store the bucket for the S3FS
rm root/etc/bucket.s3fs 2> /dev/null
echo $BUCKET >> root/etc/bucket.s3fs

# Store the config & credentials for the AWS logs and the stator.py
rm -r root/root 2> /dev/null
mkdir -p root/root/.aws
echo [default]                       >> root/root/.aws/config
echo region = $REGION                >> root/root/.aws/config
echo [default]                       >> root/root/.aws/credentials
echo aws_access_key_id = $ID         >> root/root/.aws/credentials
echo aws_secret_access_key = $SECRET >> root/root/.aws/credentials

# Build docker image
docker build --rm -t $IMAGE .

# Tag the docker image
docker tag $IMAGE:latest $URL/$IMAGE:latest

# Login to Docker Hub
`aws ecr get-login --region $REGION`

# Publish the docker image
docker push $URL/$IMAGE:latest

# Create container definition
DEF=name=$PREFIX-container
DEF=$DEF,image=$IMAGE
DEF=$DEF,cpu=1024,memory=6144
DEF=$DEF,essential=true
DEF=$DEF,mountPoints=[{sourceVolume=logs,containerPath=/mnt/logs,readOnly=false}]
DEF=$DEF,privileged=true

# Register task definition
TASK=$PREFIX-task
VOLUMES=name=logs,host={sourcePath=/var/log}
aws ecs register-task-definition --family $TASK --container-definitions $DEF --volumes $VOLUMES

# Create service
SERVICE=$PREFIX-service
aws ecs create-service --service-name $SERVICE --task-definition $TASK --desired-count 1

# Clean-up
rm root/tmp/region 2> /dev/null
rm root/bin/stator_configuration.py 2> /dev/null
rm root/etc/passwd.s3fs 2> /dev/null
rm root/etc/bucket.s3fs 2> /dev/null
rm -rf root/root
