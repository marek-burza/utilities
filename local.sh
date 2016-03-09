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
