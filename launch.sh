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
if [ "$#" -ne 5 ]; then
    echo "Usage: ./launch.sh CREDENTIALS REGION"
    echo "Builds the service and launches it locally"
    echo "Arguments:"
    echo "    CREDENTIALS - Path to the AWS credentials (CSV) for the service"
    echo "    REGION      - AWS region for the service (e.g. eu-west-1)"
    echo "    PREFIX      - Prefix to be used for naming (task, service, etc.)"
    echo "    IMAGE       - Image (URL) to be launched"
    echo "    PORT        - Port number to expose the service at"
    echo "Example:"
    echo "./launch.sh ../credentials.csv eu-west-1 simple-collector altermarkive/simple-collector 80"
    exit 1
else
    CREDENTIALS=$1
    REGION=$2
    PREFIX=$3
    IMAGE=$4
    PORT=$5
fi

# Move to the base directory
SELF=$0
BASE=`dirname "$0"`
cd $BASE

# Parse credentials
USER=`tail -1 $CREDENTIALS | sed 's/"//g' | sed 's/,/ /g' | awk '{print $1}'`
ID=`tail -1 $CREDENTIALS | sed 's/"//g' | sed 's/,/ /g' | awk '{print $2}'`
SECRET=`tail -1 $CREDENTIALS | sed 's/"//g' | sed 's/,/ /g' | awk '{print $3}'`

# Create container definition
MAPPING={containerPort=5000,hostPort=$PORT,protocol=tcp}
ENVIRONMENT_REGION={name=AWS_DEFAULT_REGION,value=$REGION}
ENVIRONMENT_ID={name=AWS_ACCESS_KEY_ID,value=$ID}
ENVIRONMENT_SECRET={name=AWS_SECRET_ACCESS_KEY,value=$SECRET}
DEF=name=$PREFIX-container
DEF=$DEF,image=$IMAGE
DEF=$DEF,cpu=32,memory=256
DEF=$DEF,portMappings=[$MAPPING]
DEF=$DEF,essential=true
DEF=$DEF,environment=[$ENVIRONMENT_REGION,$ENVIRONMENT_ID,$ENVIRONMENT_SECRET]
DEF=$DEF,mountPoints=[{sourceVolume=logs,containerPath=/mnt/logs,readOnly=false}]
DEF=$DEF,privileged=true

# Register task definition
TASK=$PREFIX-task
VOLUMES=name=logs,host={sourcePath=/var/log}
aws ecs register-task-definition --family $TASK --container-definitions $DEF --volumes $VOLUMES

# Create service
SERVICE=$PREFIX-service
aws ecs create-service --service-name $SERVICE --task-definition $TASK --desired-count 1
