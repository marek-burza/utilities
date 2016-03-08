#!/bin/bash

# This code is free software: you can redistribute it and/or modify it under the
# terms  of  the  GNU Lesser General Public License  as published  by  the  Free
# Software Foundation,  either version 3 of the License, or (at your option) any
# later version.
#
# This code is distributed in the hope that it will be useful,  but  WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A  PARTICULAR  PURPOSE.  See  the  GNU Lesser General Public License  for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with code. If not, see http://www.gnu.org/licenses/.

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
DEF=$DEF,cpu=32,memory=128
DEF=$DEF,portMappings=[$MAPPING]
DEF=$DEF,essential=true
DEF=$DEF,environment=[$ENVIRONMENT_REGION,$ENVIRONMENT_ID,$ENVIRONMENT_SECRET]
DEF=$DEF,privileged=true

# Register task definition
TASK=$PREFIX-task
aws ecs register-task-definition --family $TASK --container-definitions $DEF

# Create service
SERVICE=$PREFIX-service
aws ecs create-service --service-name $SERVICE --task-definition $TASK --desired-count 1
