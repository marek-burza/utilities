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
    echo "Usage: ./bouncer.deploy.sh BUCKET"
    echo "Installs the bouncer service"
    echo "Arguments:"
    echo "    BUCKET - The S3 bucket to sign upload URLs for"
    echo "Example:"
    echo "./bouncer.deploy.sh bucket"
    exit 1
else
    export BUCKET_NAME=$1
fi

# Prepare names
LAMBDA_NAME=$BUCKET_NAME-bouncer-lambda
ROLE_NAME=$BUCKET_NAME-bouncer-role
POLICY_NAME=$BUCKET_NAME-bouncer-policy
API_NAME=$BUCKET_NAME-bouncer-api

# Delete previously created items
echo "Please delete $API_NAME API and press ENTER"
read
aws lambda delete-function --function-name $LAMBDA_NAME 2> /dev/null
aws iam delete-role-policy --role-name $ROLE_NAME --policy-name $POLICY_NAME 2> /dev/null
aws iam delete-role --role-name $ROLE_NAME 2> /dev/null

# Create the role
aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://bouncer.role.json

# Generate the policy
cat bouncer.template.policy.json | sed 's/$BUCKET_NAME/'$BUCKET_NAME'/g' > bouncer.policy.json

# Attach the policy
aws iam put-role-policy --role-name $ROLE_NAME --policy-name $POLICY_NAME --policy-document file://bouncer.policy.json

# Obtain the role ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME | grep "Arn" | tr -d "\"," | awk '{print $2}')

# Configure the bucket names
rm configuration.py 2> /dev/null
echo bucket = \'$BUCKET_NAME\' >> configuration.py

# Create the archive
zip -r bouncer.zip bouncer.py configuration.py

# IAM profiles can take ~10 seconds to propagate in AWS:
# http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#launch-instance-with-role-console
# A client error (InvalidParameterValueException) occurred when calling the CreateFunction operation: The role defined for the function cannot be assumed by Lambda.
sleep 14

# Create the function
aws lambda create-function --function-name $LAMBDA_NAME --runtime python2.7 --role $ROLE_ARN --handler bouncer.lambda_handler --timeout 10 --memory-size 128 --zip-file fileb://bouncer.zip

# Publish the function
aws lambda publish-version --function-name $LAMBDA_NAME

# Obtain the function ARN and the region it is in
LAMBDA_ARN=$(aws lambda get-function --function-name $LAMBDA_NAME | grep "FunctionArn" | tr -d "\"," | awk '{print $2}')
REGION=$(echo $LAMBDA_ARN | tr ":" " " | awk '{print $4}')

# Generate the API specification
cat bouncer.template.api.json | sed 's/$API_NAME/'$API_NAME'/g' | sed 's/$LAMBDA_ARN/'$LAMBDA_ARN'/g' > bouncer.api.json

# Import the API specification
API_ID=$(aws apigateway import-rest-api --body file://bouncer.api.json | grep "id" | tr -d "\"," | awk '{print $2}')

# Create the API deployment
aws apigateway create-deployment --rest-api-id $API_ID --stage-name bouncer

# Grant the rights to invoke the function by the API
ACCOUNT_ID=$(aws iam get-user | grep "Arn" | tr ":" " " | awk '{print $5}')
API_ARN=arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/bouncer/GET/
aws lambda add-permission --function-name $LAMBDA_NAME --statement-id bouncer-api --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn $API_ARN

# Create the URL to be used
URL=https://$API_ID.execute-api.$REGION.amazonaws.com/bouncer
echo "The bouncer is avilable at: $URL"

# Clean-up
rm bouncer.zip
rm bouncer.api.json
rm bouncer.policy.json
rm configuration.py
