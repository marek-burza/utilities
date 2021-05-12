#!/usr/bin/env python
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

import boto3
import os
import sys
import time
import zipfile

aws_lambda = boto3.client('lambda')
aws_iam = boto3.client('iam')
aws_apigateway = boto3.client('apigateway')

print('Checking input arguments')
if len(sys.argv) < 2:
    print('Usage: ./bouncer.deploy.sh BUCKET')
    print('Installs the bouncer service')
    print('Arguments:')
    print('    BUCKET - The S3 bucket to sign upload URLs for')
    print('Example:')
    print('./bouncer.deploy.sh bucket')
    sys.exit()
else:
    bucket_name = sys.argv[1]

print('Preparing names')
lambda_name = bucket_name + '-bouncer-lambda'
role_name = bucket_name + '-bouncer-role'
policy_name = bucket_name + '-bouncer-policy'
api_name = bucket_name + '-bouncer-api'

print('Deleting previously created items')
raw_input('Please delete %s API and press ENTER' % api_name)
try:
    aws_lambda.delete_function(FunctionName=lambda_name)
except:
    pass
try:
    aws_iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
except:
    pass
try:
    aws_iam.delete_role(RoleName=role_name)
except:
    pass

print('Creating the role')
with open('bouncer.role.json', 'rb') as document:
    policy = document.read()
    aws_iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=policy)

print('Generating the policy')
with open('bouncer.template.policy.json', 'rb') as template:
    with open('bouncer.policy.json', 'wb') as document:
        document.write(template.read() % bucket_name)

print('Attaching the policy')
with open('bouncer.policy.json', 'rb') as document:
    policy = document.read()
    aws_iam.put_role_policy(
        RoleName=role_name, PolicyName=policy_name, PolicyDocument=policy)

print('Obtaining the role ARN')
role_json = aws_iam.get_role(RoleName=role_name)
role_arn = role_json['Role']['Arn']

print('Configuring the bucket names')
with open('configuration.py', 'wb') as configuration:
    configuration.write('bucket = \'%s\'' % bucket_name)

print('Creating the archive')
with zipfile.ZipFile('bouncer.zip', 'w', zipfile.ZIP_DEFLATED) as zipped:
    zipped.write('bouncer.py')
    zipped.write('configuration.py')

print('Waiting for the role to propagate')
# IAM profiles can take ~10 seconds to propagate in AWS: http://amzn.to/28KFJu6
# A client error (InvalidParameterValueException) occurred when calling
# the CreateFunction operation: The role defined for the function cannot be
# assumed by Lambda.
time.sleep(14)

print('Creating the function')
with open('bouncer.zip', 'rb') as zipped:
    aws_lambda.create_function(
        FunctionName=lambda_name, Runtime='python2.7', Role=role_arn,
        Handler='bouncer.lambda_handler', Timeout=10, MemorySize=128,
        Code={'ZipFile': zipped.read()})

print('Publishing the function')
aws_lambda.publish_version(FunctionName=lambda_name)

print('Obtaining the function ARN and the region it is in')
lambda_json = aws_lambda.get_function(FunctionName=lambda_name)
lambda_arn = lambda_json['Configuration']['FunctionArn']
region = lambda_arn.split(':')[3]

print('Generating the API specification')
with open('bouncer.template.api.json', 'rb') as template:
    with open('bouncer.api.json', 'wb') as policy:
        policy.write(template.read() % (api_name, lambda_arn))

print('Importing the API specification')
with open('bouncer.api.json', 'rb') as swagger:
    api_id = aws_apigateway.import_rest_api(
        failOnWarnings=False, parameters={}, body=swagger.read())['id']

print('Creating the API deployment')
aws_apigateway.create_deployment(restApiId=api_id, stageName='bouncer')

print('Granting the rights to invoke the function by the API')
account_id = aws_iam.get_user()['User']['Arn'].split(':')[4]
api_arn = 'arn:aws:execute-api:%s:%s:%s/bouncer/GET/'
api_arn = api_arn % (region, account_id, api_id)
aws_lambda.add_permission(
    FunctionName=lambda_name, StatementId='bouncer-api',
    Action='lambda:InvokeFunction', Principal='apigateway.amazonaws.com',
    SourceArn=api_arn)

print('Creating the URL to be used')
url = 'https://%s.execute-api.%s.amazonaws.com/bouncer' % (api_id, region)
print('The bouncer is avilable at: %s' % url)

print('Cleaning up')
os.remove('bouncer.zip')
os.remove('bouncer.api.json')
os.remove('bouncer.policy.json')
os.remove('configuration.py')

print('Done')
