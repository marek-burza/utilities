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
if [ "$#" -ne 1 ]; then
    echo "Usage: ./observer.deploy.sh BUCKET"
    echo "Installs the observer service"
    echo "Arguments:"
    echo "    BUCKET - The S3 bucket where the data arrives"
    echo "Example:"
    echo "./observer.deploy.sh bucket"
    exit 1
else
    export BUCKET_NAME=$1
fi

# Delete previously created items
aws lambda delete-function --function-name observer-lambda
aws iam delete-role-policy --role-name observer-role --policy-name observer-policy
aws iam delete-role --role-name observer-role

# Create the role
aws iam create-role --role-name observer-role --assume-role-policy-document file://observer.role.json

# Generate the policy
cat observer.template.json | envsubst > observer.policy.json

# Attach the policy
aws iam put-role-policy --role-name observer-role --policy-name observer-policy --policy-document file://observer.policy.json

# Obtain the role ARN
ROLE_ARN=`aws iam get-role --role-name observer-role | grep "Arn" | sed 's/[",]//g' | awk '{print $2}'`

# Configure the bucket names
rm configuration.py 2> /dev/null
echo bucket = \'$BUCKET_NAME\' >> configuration.py

# Create the archive
zip -r observer.zip observer.py configuration.py

# IAM profiles can take ~10 seconds to propagate in AWS:
# http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#launch-instance-with-role-console
# A client error (InvalidParameterValueException) occurred when calling the CreateFunction operation: The role defined for the function cannot be assumed by Lambda.
sleep 11

# Create the function
aws lambda create-function --function-name observer-lambda --runtime python2.7 --role $ROLE_ARN --handler observer.lambda_handler --timeout 10 --memory-size 128 --zip-file fileb://observer.zip

# Publish the function
aws lambda publish-version --function-name observer-lambda

# Obtain the function ARN
FUNCTION_ARN=`aws lambda get-function --function-name observer-lambda | grep "FunctionArn" | sed 's/[",]//g' | awk '{print $2}'`

# Permit the S3 to call the function
aws lambda add-permission --function-name observer-lambda --principal s3.amazonaws.com --action lambda:InvokeFunction --source-arn arn:aws:s3:::$BUCKET_NAME --statement-id `date "+%Y%m%d%H%M%S"`

# Put a bucket event notification
NOTIFICATION="{\"LambdaFunctionConfigurations\":[{\"Events\":[\"s3:ObjectCreated:*\"],\"LambdaFunctionArn\":\"$FUNCTION_ARN\"}]}"
aws s3api put-bucket-notification-configuration --bucket $BUCKET_NAME --notification-configuration $NOTIFICATION

# Clean-up
rm observer.zip
rm observer.policy.json
rm configuration.py
