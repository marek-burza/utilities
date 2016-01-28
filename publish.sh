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
if [ "$#" -ne 3 ]; then
    echo "Usage: ./publish.sh REGION NAME URL"
    echo "Builds and publishes a Docker image to Amazon ECR"
    echo "Arguments:"
    echo "    REGION - AWS region to be used (e.g. us-west-1)"
    echo "    NAME   - Repository name (tag) to be used"
    echo "    URL    - Repository URL to publish the image to"
    echo "Example:"
    echo "./publish.sh us-west-1 altermarkive/simple-collector 012345678900.dkr.ecr.us-west-1.amazonaws.com"
    exit 1
else
    REGION=$1
    NAME=$2
    URL=$3
fi

# Move to the base directory
SELF=$0
BASE=`dirname "$0"`
cd $BASE

# Build docker image
docker build --rm -t $NAME .

# Tag the docker image
docker tag -f $NAME:latest $URL/$NAME:latest

# Login to Docker Hub
`aws ecr get-login --region $REGION`

# Publish the docker image
docker push $URL/$NAME:latest
