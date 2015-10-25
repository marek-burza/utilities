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

# Move to the base directory
SELF=$0
BASE=`dirname "$0"`
cd $BASE

# Build docker image
docker build --rm -t service .

# Tag the docker image
docker tag -f service altermarkive/http-post-to-s3-in-python

# Login to Docker Hub
docker login

# Publish the docker image
docker push altermarkive/http-post-to-s3-in-python
