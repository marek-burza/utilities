#!/usr/bin/env python

import boto3
import json
import os
import time
import zipfile

aws_iam = boto3.client('iam')
aws_apigateway = boto3.client('apigateway')
aws_lambda = boto3.client('lambda')

print('Preparing the constants')
bucket_name = 'gate-bucket'
lambda_name = 'gate-lambda'
role_name = 'gate-role'
policy_name = 'gate-policy'
api_name = 'gate-api'
key = 'index.html'

print('Deleting past stack')
raw_input('You must delete the %s API manually. Press ENTER when ready' % api_name)
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
            'Action': ['s3:ListBucket'],
            'Resource': 'arn:aws:s3:::%s' % bucket_name
        },
        {
            'Effect': 'Allow',
            'Action': ['s3:GetObject'],
            'Resource': 'arn:aws:s3:::%s/*' % bucket_name
        }
    ]
}
policy = json.dumps(policy)
aws_iam.put_role_policy(
    RoleName=role_name, PolicyName=policy_name, PolicyDocument=policy)

print('Obtaining the ARN of the role')
response = aws_iam.get_role(RoleName=role_name)
role_arn = response['Role']['Arn']

print('Storing the bucket and key')
with open('config.py', 'w') as handle:
    handle.write('bucket = \'%s\'\n' % bucket_name)
    handle.write('key = \'%s\'\n' % key)

print('Creating the archive')
with zipfile.ZipFile('gate.zip', 'w', zipfile.ZIP_DEFLATED) as zipped:
    zipped.write('gate.py')
    zipped.write('config.py')

print('Waiting for the role to propagate')
# If a client error (InvalidParameterValueException) occurs when calling
# the CreateFunction operation that means that the role defined for the function
# cannot be assumed by Lambda yet.
# That is because the IAM profiles can take ~10 seconds to propagate in AWS,
# for more details see: http://amzn.to/28KFJu6
time.sleep(15)

print('Creating the Lanbda function')
with open('gate.zip', 'rb') as zipped:
    aws_lambda.create_function(
        FunctionName=lambda_name, Runtime='python2.7', Role=role_arn,
        Handler='gate.lambda_handler', Timeout=120, MemorySize=128,
        Code={'ZipFile': zipped.read()})

print('Publishing the Lambda function')
aws_lambda.publish_version(FunctionName=lambda_name)

print('Obtaining the ARN of the Lambda function ARN and its region')
lambda_json = aws_lambda.get_function(FunctionName=lambda_name)
lambda_arn = lambda_json['Configuration']['FunctionArn']
region = lambda_arn.split(':')[3]

print('Importing the API Gateway specification')
swagger = {
    'swagger': '2.0',
    'info': {
        'version': '1.0.0',
        'title': api_name,
        'description': 'This is the specification of the gate'
    },
    'schemes': ['https'],
    'paths': {
        '/': {
        'get': {
            'produces': ['text/html'],
            'parameters': [
                {
                    'name': 'query',
                    'in': 'query',
                    'required': False,
                    'type': 'string'
                }
            ],
            'responses': {
                '200': {
                    'description': '200 response',
                    'schema': {'$ref': '#/definitions/Empty'}
                }
            },
            'x-amazon-apigateway-integration': {
                'responses': {
                    'default': {
                        'statusCode': '200',
                        'responseTemplates': {'text/html': '$input.path(\'$\')'}
                    }
                },
                'requestTemplates': {
                    'application/json': '{"query": "$input.params(\'query\')"}'
                },
                'httpMethod': 'POST',
                    'uri': 'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/%s/invocations' % lambda_arn,
                    'type': 'aws'
                }
            }
        }
    },
    'definitions': {'Empty': {'type': 'object'}}
}
swagger = json.dumps(swagger)
api_id = aws_apigateway.import_rest_api(
    failOnWarnings=False, parameters={}, body=swagger)['id']

print('Creating the API Gateway deployment')
aws_apigateway.create_deployment(restApiId=api_id, stageName='gate')

print('Granting the rights to invoke the function by the API Gateway')
account_id = aws_iam.get_user()['User']['Arn'].split(':')[4]
api_arn = 'arn:aws:execute-api:%s:%s:%s/gate/GET/'
api_arn = api_arn % (region, account_id, api_id)
aws_lambda.add_permission(
    FunctionName=lambda_name, StatementId='gate-api',
    Action='lambda:InvokeFunction', Principal='apigateway.amazonaws.com',
    SourceArn=api_arn)

print('Creating the URL to be used')
url = 'https://%s.execute-api.%s.amazonaws.com/gate' % (api_id, region)
print('The gate can be reached at: %s' % url)

print('Cleaning up')
os.remove('gate.zip')
os.remove('config.py')

print('Done')
