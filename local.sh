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
if [ "$#" -ne 2 ]; then
    echo "Usage: ./launch.sh CREDENTIALS REGION"
    echo "Builds the service and launches it locally"
    echo "Arguments:"
    echo "    CREDENTIALS - Path to a CSV file with the AWS credentials"
    echo "    REGION      - AWS region to be used (e.g. eu-west-1)"
    echo "Example:"
    echo "./launch.sh ../credentials.csv eu-west-1"
    exit 1
else
    CREDENTIALS=$1
    REGION=$2
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
echo $REGION > root/etc/region.conf

# Build docker image
docker build --rm -t simple-collector .

# Launch docker image
docker run -e AWS_ACCESS_KEY_ID=$ID -e AWS_SECRET_ACCESS_KEY=$SECRET -e AWS_DEFAULT_REGION=$REGION -dt --privileged -v /var/log:/mnt/logs -p 80:5000 simple-collector
