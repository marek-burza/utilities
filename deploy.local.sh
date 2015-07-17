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
if [ "$#" -ne 4 ]; then
    echo "Usage: ./stator_deploy_local.sh CREDENTIALS REGION BUCKET QUEUE"
    echo "Builds the service and deploys it locally"
    echo "Arguments:"
    echo "    CREDENTIALS - Path to a CSV file with the AWS credentials"
    echo "    REGION      - AWS region to be used (e.g. eu-west-1)"
    echo "    BUCKET      - AWS S3 bucket to be used"
    echo "    QUEUE       - AWS SQS queue to be used"
    echo "Example:"
    echo "./stator_deploy_local.sh ../credentials.csv eu-west-1 bucket queue"
    exit 1
else
    CREDENTIALS=$1
    REGION=$2
    BUCKET=$3
    QUEUE=$4
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
docker build --rm -t stator .

# Launch docker image
docker run -dt --privileged -v /var/log:/mnt/logs stator

# Clean-up
rm root/tmp/region 2> /dev/null
rm root/bin/stator_configuration.py 2> /dev/null
rm root/etc/passwd.s3fs 2> /dev/null
rm root/etc/bucket.s3fs 2> /dev/null
rm -rf root/root
