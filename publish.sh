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

# Store region
echo $REGION > root/etc/region.conf

# Build docker image
docker build --rm -t $NAME .

# Tag the docker image
docker tag $NAME:latest $URL/$NAME:latest

# Login to Docker Hub
`aws ecr get-login --region $REGION`

# Publish the docker image
docker push $URL/$NAME:latest
