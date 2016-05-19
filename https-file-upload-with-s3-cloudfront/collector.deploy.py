#!/usr/bin/env python
#
# This script creates an upload-only CloudFront Distribution behind a WAF and
# bound to a supplied S3 bucket.
# With the created CloudFront Distribution it is then possible to upload a file
# like so:
#   curl -v -F "key=file.bz2" -F "Content-Type=application/x-bzip2" \
#           -F "file=@file.bz2" https://h72j8rnthsgg5j.cloudfront.net/
# Note that the content has to be uploaded over HTTPS with a multipart POST.
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
import json
import sys
import time
import uuid

if len(sys.argv) < 3:
    print('Usage: ./collector.deploy.py BUCKET DISTRIBUTION')
    print('Deploys an upload-only CloudFront Distribution for an S3 bucket')
    print('Arguments:')
    print('    BUCKET       - Name of the (existing) S3 bucket to upload to')
    print('    DISTRIBUTION - Name to for the CloudFront Distribution')
    print('Example:')
    print('./collector.deploy.py s3-bucket-name cloudfront-tag')
    sys.exit()
else:
    s3_bucket = sys.argv[1]
    cloudfront_name = sys.argv[2]

#-------------------------------------------------------------------------------
print('Setting up the configuration')

cloudfront_metric_name = filter(str.isalnum, cloudfront_name).upper()
waf_condition_name = '%s-waf-condition-push-only' % cloudfront_name
waf_rule_name = '%s-waf-rule-push-only' % cloudfront_name
waf_rule_metric_name = '%sWAFRulePushOnly' % cloudfront_metric_name
waf_acl_name = '%s-waf-acl-push-only' % cloudfront_name
waf_acl_metric_name = '%sWAFACLPushOnly' % cloudfront_metric_name
cloudfront_config = {
    'CallerReference': None,
    'Aliases': {'Quantity': 0},
    'DefaultRootObject': '',
    'Origins': {
        'Quantity': 1,
        'Items': [
            {
                'Id': s3_bucket,
                'DomainName': '%s.s3.amazonaws.com' % s3_bucket,
                'OriginPath': '',
                'CustomHeaders': {'Quantity': 0},
                'S3OriginConfig': {'OriginAccessIdentity': ''},
            }
        ]
    },
    'DefaultCacheBehavior': {
        'TargetOriginId': s3_bucket,
        'ForwardedValues': {
            'QueryString': False,
            'Cookies': {'Forward': 'none'},
            'Headers': {'Quantity': 0},
        },
        'TrustedSigners': {'Enabled': False, 'Quantity': 0},
        'ViewerProtocolPolicy': 'https-only',
        'MinTTL': 0,
        'AllowedMethods': {
            'Quantity': 7,
            'Items': [
                'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'
            ],
            'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
        },
        'SmoothStreaming': False,
        'DefaultTTL': 0, 'MaxTTL': 0,
        'Compress': False
    },
    'CacheBehaviors': {'Quantity': 0},
    'CustomErrorResponses': {'Quantity': 0},
    'Comment': cloudfront_name,
    'Logging': {
        'Enabled': False,
        'IncludeCookies': True,
        'Bucket': '',
        'Prefix': ''
    },
    'PriceClass': 'PriceClass_All',
    'Enabled': True,
    'ViewerCertificate': {
        'CloudFrontDefaultCertificate': True,
        'MinimumProtocolVersion': 'SSLv3'
    },
    'Restrictions': {
        'GeoRestriction': {'RestrictionType': 'none', 'Quantity': 0}
    },
    'WebACLId': ''
}
s3_statement = {
    'Sid': cloudfront_name,
		'Effect': 'Allow',
		'Principal': {'AWS': None},
		'Action': ['s3:PutObject'],
		'Resource': 'arn:aws:s3:::%s/*' % s3_bucket
}
s3_arn = 'arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity %s'

#-------------------------------------------------------------------------------
print('Accessing the WAF, the CloudFront and the S3')

waf = boto3.client('waf')
cloudfront = boto3.client('cloudfront')
s3 = boto3.client('s3')

#-------------------------------------------------------------------------------
print('Deleting the CloudFront Distribution')

marker = None
while marker != '':
    if marker == None:
        part = cloudfront.list_distributions(MaxItems='100')
    else:
        part = cloudfront.list_distributions(MaxItems='100', NextMarker=marker)
    part = part['DistributionList']
    if part['Quantity'] == 0:
        break
    marker = part['Marker']
    for distro in part['Items']:
        if distro['Comment'] == cloudfront_name:
            reply = cloudfront.get_distribution(Id=distro['Id'])
            config = reply['Distribution']['DistributionConfig']
            tag = reply['ETag']
            if config['Enabled']:
                config['Enabled'] = False
                cloudfront.update_distribution(
                    DistributionConfig=config, Id=distro['Id'], IfMatch=tag)
                while True:
                    reply = cloudfront.get_distribution(Id=distro['Id'])
                    tag = reply['ETag']
                    if reply['Distribution']['Status'] == 'Deployed':
                        break
                    else:
                        time.sleep(60)
            cloudfront.delete_distribution(Id=distro['Id'], IfMatch=tag)

#-------------------------------------------------------------------------------
print('Deleting the CloudFront Origin Access Identity')

marker = None
while marker != '':
    if marker == None:
        part = cloudfront.list_cloud_front_origin_access_identities(
            MaxItems='100')
    else:
        part = cloudfront.list_cloud_front_origin_access_identities(
            MaxItems='100', Marker=marker)
    part = part['CloudFrontOriginAccessIdentityList']
    if part['Quantity'] == 0:
        break
    marker = part['Marker']
    for identity in part['Items']:
        it = identity['Id']
        if identity['Comment'] == cloudfront_name:
            reply = cloudfront.get_cloud_front_origin_access_identity(Id=it)
            tag = reply['ETag']
            cloudfront.delete_cloud_front_origin_access_identity(
                 Id=it, IfMatch=tag)

#-------------------------------------------------------------------------------
print('Cleaning up the WAF')

def check(call, marker, key):
    if marker == None:
        result = call(Limit=100)
    else:
        result = call(Limit=100, NextMarker=marker)
    if result.has_key('NextMarker'):
        marker = result['NextMarker']
    result = result[key]
    return (result, marker)

def derive(key, value):
    result = {'Action': 'DELETE'}
    result[key] = value
    return result

def delete(lister, getter, updater, deleter, many, single, name, it, link, key):
    marker = None
    while True:
        (items, marker) = check(lister, marker, many)
        if len(items) == 0:
            break
        for item in items:
            if item['Name'] == name:
                it = item[it]
                item = getter(it)
                others = item[single][link]
                if len(others) > 0:
                    token = waf.get_change_token()['ChangeToken']
                    updates = [derive(key, other) for other in others]
                    updater(it, token, updates)
                token = waf.get_change_token()['ChangeToken']
                deleter(it, token)

#-------------------------------------------------------------------------------
print('Deleting the WAF ACL')

lister = waf.list_web_acls
getter = lambda it: waf.get_web_acl(WebACLId=it)
updater = lambda it, token, updates: waf.update_web_acl(
    WebACLId=it, ChangeToken=token, Updates=updates)
deleter = lambda it, token: waf.delete_web_acl(WebACLId=it, ChangeToken=token)
many = 'WebACLs'
single = 'WebACL'
name = waf_acl_name
it = 'WebACLId'
link = 'Rules'
key = 'ActivatedRule'
delete(lister, getter, updater, deleter, many, single, name, it, link, key)

#-------------------------------------------------------------------------------
print('Deleting the WAF Rule')

lister = waf.list_rules
getter = lambda it: waf.get_rule(RuleId=it)
updater = lambda it, token, updates: waf.update_rule(
    RuleId=it, ChangeToken=token, Updates=updates)
deleter = lambda it, token: waf.delete_rule(RuleId=it, ChangeToken=token)
many = 'Rules'
single = 'Rule'
name = waf_rule_name
it = 'RuleId'
link = 'Predicates'
key = 'Predicate'
delete(lister, getter, updater, deleter, many, single, name, it, link, key)

#-------------------------------------------------------------------------------
print('Deleting the WAF Condition')

lister = waf.list_byte_match_sets
getter = lambda it: waf.get_byte_match_set(ByteMatchSetId=it)
updater = lambda it, token, updates: waf.update_byte_match_set(
    ByteMatchSetId=it, ChangeToken=token, Updates=updates)
deleter = lambda it, token: waf.delete_byte_match_set(
    ByteMatchSetId=it, ChangeToken=token)
many = 'ByteMatchSets'
single = 'ByteMatchSet'
name = waf_condition_name
it = 'ByteMatchSetId'
link = 'ByteMatchTuples'
key = 'ByteMatchTuple'
delete(lister, getter, updater, deleter, many, single, name, it, link, key)

#-------------------------------------------------------------------------------
print('Creating the WAF String Match Condition')

token = waf.get_change_token()['ChangeToken']
result = waf.create_byte_match_set(Name=waf_condition_name, ChangeToken=token)
waf_condition_id = result['ByteMatchSet']['ByteMatchSetId']

#-------------------------------------------------------------------------------
print('Defining the WAF String Match Condition')

updates = [
    {
        'Action': 'INSERT',
        'ByteMatchTuple': {
            'FieldToMatch': {'Type': 'METHOD'},
            'TargetString': 'POST',
            'TextTransformation': 'NONE',
            'PositionalConstraint': 'EXACTLY'
        }
    }
]
token = waf.get_change_token()['ChangeToken']
waf.update_byte_match_set(
    ByteMatchSetId=waf_condition_id, ChangeToken=token, Updates=updates)

#-------------------------------------------------------------------------------
print('Creating the WAF Rule')

token = waf.get_change_token()['ChangeToken']
reply = waf.create_rule(
    Name=waf_rule_name, MetricName=waf_rule_metric_name, ChangeToken=token)
waf_rule_id = reply['Rule']['RuleId']

#-------------------------------------------------------------------------------
print('Associating the WAF Rule with the WAF String Match Condition')

updates = [
    {
        'Action': 'INSERT',
        'Predicate': {
            'Negated': False, 'Type': 'ByteMatch', 'DataId': waf_condition_id
        }
    }
]
token = waf.get_change_token()['ChangeToken']
waf.update_rule(RuleId=waf_rule_id, ChangeToken=token, Updates=updates)

#-------------------------------------------------------------------------------
print('Creating the WAF ACL')

token = waf.get_change_token()['ChangeToken']
reply = waf.create_web_acl(
   Name=waf_acl_name, MetricName=waf_acl_metric_name,
   DefaultAction={'Type': 'BLOCK'}, ChangeToken=token)
waf_acl_id = reply['WebACL']['WebACLId']

#-------------------------------------------------------------------------------
print('Associating the WAF ACL with the WAF Rule')

updates = [
    {
        'Action': 'INSERT',
        'ActivatedRule': {
            'Priority': 0, 'RuleId': waf_rule_id, 'Action': {'Type': 'ALLOW'}
        }
    }
]
token = waf.get_change_token()['ChangeToken']
waf.update_web_acl(WebACLId=waf_acl_id, ChangeToken=token, Updates=updates)

#-------------------------------------------------------------------------------
print('Creating the CloudFront Origin Access Identity')

config = {'CallerReference': uuid.uuid1().hex, 'Comment': cloudfront_name}
reply = cloudfront.create_cloud_front_origin_access_identity(
    CloudFrontOriginAccessIdentityConfig=config)
cloudfront_access = reply['CloudFrontOriginAccessIdentity']['Id']

#-------------------------------------------------------------------------------
print('Creating the CloudFront Distribution')

cloudfront_config['CallerReference'] = uuid.uuid1().hex
cloudfront_config['WebACLId'] = waf_acl_id
cloudfront_config['Enabled'] = True
origin = cloudfront_config['Origins']['Items'][0]['S3OriginConfig']
template = 'origin-access-identity/cloudfront/%s'
origin['OriginAccessIdentity'] = template % cloudfront_access
distro = cloudfront.create_distribution(DistributionConfig=cloudfront_config)
while True:
    reply = cloudfront.get_distribution(Id=distro['Distribution']['Id'])
    if reply['Distribution']['Status'] == 'Deployed':
        break
    else:
        time.sleep(60)

#-------------------------------------------------------------------------------
print('Editing the S3 Bucket Policy')

policy = json.loads(s3.get_bucket_policy(Bucket=s3_bucket)['Policy'])
found = None
for statement in policy['Statement']:
    if statement['Sid'] == cloudfront_name:
        found = statement
if found == None:
    policy['Statement'].append(s3_statement)
    found = s3_statement
found['Principal']['AWS'] = s3_arn % cloudfront_access
s3.put_bucket_policy(Bucket=s3_bucket, Policy=json.dumps(policy))

#-------------------------------------------------------------------------------
print('Done')
