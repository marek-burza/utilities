#!/usr/bin/env python3

import boto3
import glob
import json
import os
import shutil
import sys
import time
import zipfile

if len(sys.argv) < 3:
    print('Usage: ./cthulhu.deploy.py API_KEY PRIVATE_KEY')
    print('Deploys the Cthulhu')
    print('Arguments:')
    print('    API_KEY     - Kraken\'s API key')
    print('    PRIVATE_KEY - Kraken\'s private key')
    print('Example:')
    print('./cthulhu.deploy.py a1b2c3d4e5f6e7f8g9 9z8y7x6w5v4u3t2s1q0p')
    sys.exit()
else:
    kraken_api_key = sys.argv[1]
    kraken_private_key = sys.argv[2]

print('Moving to the base directory')
base_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(base_path)

print('Preparing the constants')
lambda_name = 'cthulhu-lambda'
role_name = 'cthulhu-role'
policy_name = 'cthulhu-policy'
zip_name = 'cthulhu.zip'

print('Initiating AWS clients')
aws_iam = boto3.client('iam')
aws_lambda = boto3.client('lambda')

print('Deleting past stack')
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

print('Creating the role for the service')
policy = {
    'Version': '2012-10-17',
    'Statement': [
        {
            'Sid': '',
            'Effect': 'Allow',
            'Principal': {'Service': 'lambda.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }
    ]
}
policy = json.dumps(policy)
aws_iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=policy)

print('Identifying the account ID')
account_id = aws_iam.get_user()['User']['Arn'].split(':')[4]

print('Attaching the policy for the service')
policy = {
    'Version': '2012-10-17',
    'Statement': [
        {
            'Effect': 'Allow',
            'Action': [
                'logs:CreateLogGroup',
                'logs:CreateLogStream',
                'logs:PutLogEvents'
            ],
            'Resource': 'arn:aws:logs:*:*:*'
        },
        {
            'Effect': 'Allow',
            'Action': 'dynamodb:PutItem',
            'Resource': 'arn:aws:dynamodb:eu-west-1:%s:table/cthulhu' % account_id
        }
    ]
}
policy = json.dumps(policy)
aws_iam.put_role_policy(
    RoleName=role_name, PolicyName=policy_name, PolicyDocument=policy)

print('Obtaining the ARN of the role')
response = aws_iam.get_role(RoleName=role_name)
role_arn = response['Role']['Arn']

print('Fetching the krakenex Python module')
os.system('pip3 install krakenex -t %s' % base_path)

print('Creating the archive')
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipped:
    zipped.write('cthulhu.py')
    for directory in glob.glob('krakenex*'):
        for root, directories, files in os.walk(directory):
            for target in files:
                zipped.write(os.path.join(root, target))

print('Waiting for the role to propagate')
# If a client error (InvalidParameterValueException) occurs when calling
# the CreateFunction operation that means that the role defined for the function
# cannot be assumed by Lambda yet.
# That is because the IAM profiles can take ~10 seconds to propagate in AWS,
# for more details see: http://amzn.to/28KFJu6
time.sleep(15)

print('Creating the Lanbda function')
environment = {
    'Variables': {
        'KRAKEN_API_KEY': kraken_api_key,
        'KRAKEN_PRIVATE_KEY': kraken_private_key
    }
}
with open(zip_name, 'rb') as zipped:
    aws_lambda.create_function(
        FunctionName=lambda_name, Runtime='python3.6', Role=role_arn,
        Handler='cthulhu.lambda_handler', Timeout=120, MemorySize=128,
        Code={'ZipFile': zipped.read()}, Environment=environment)

print('Publishing the Lambda function')
aws_lambda.publish_version(FunctionName=lambda_name)

print('Cleaning up')
os.remove(zip_name)
for directory in glob.glob('krakenex*'):
    shutil.rmtree(directory)

print('Done')
