#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Periodically checks if user is a watcher of queried Jira issues
and adds the user if not watching.
"""

import base64
import json
import logging
import os
import re
import time
import urllib.parse
import urllib.request


def init_logging():
    """
    Initiates logging
    """
    pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.INFO)
    return logging.getLogger('svetovid')


def http(logger, url, method, headers, data=None):
    """
    Fetches the given URL (with reply caching & optional authorization)
    """
    result = '{}'
    while True:
        if headers is None:
            request = urllib.request.Request(url, method=method, data=data)
        else:
            request = urllib.request.Request(
                url, method=method, data=data, headers=headers)
        try:
            reply = urllib.request.urlopen(request)  # nosec
            if reply.getcode() in [200, 204]:
                result = reply.read().decode('utf-8')
                break
        except urllib.error.HTTPError as exception:
            logger.exception(exception)
            break
    return result


def authorization_credentials():
    """
    Reads authorization credentials from environment variables
    """
    user = os.environ.get('ATLASSIAN_USER')
    token = os.environ.get('ATLASSIAN_TOKEN')
    return (user, token)


def authorization_headers(user, token):
    """
    Prepares authorization header for an API request
    """
    if None in [user, token]:
        return None
    credentials = '%s:%s' % (user, token)
    auth = base64.b64encode(credentials.encode('utf-8'))
    headers = {'Authorization': 'Basic %s' % auth.decode('utf-8')}
    return headers


def prepare_headers():
    """
    Prepares headers for Atlassian API
    """
    credentials = authorization_credentials()
    headers = authorization_headers(*credentials)
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    return headers


def prepare_parameters():
    """
    Prepare the operational parameters
    """
    instance = os.environ.get('ATLASSIAN_INSTANCE')
    query = urllib.parse.quote(os.environ.get('ATLASSIAN_QUERY'))
    sleep = int(os.environ.get('VELES_SLEEP'))
    return (instance, query, sleep)


def query_issues(instance, query, headers, logger):
    """
    Queries for issues and aggregates over paging
    """
    template = 'https://%s.atlassian.net/rest/api/2/search?&jql=%s&startAt=%d'
    issues = []
    index = 0
    while True:
        url = template % (instance, query, index)
        reply = http(logger, url, 'GET', headers)
        reply = json.loads(reply)
        if 'issues' not in reply:
            break
        issues.extend(reply['issues'])
        if reply['total'] == len(issues):
            break
        index += len(reply['issues'])
    return issues


def add_issue_labels(instance, issue_key, labels, headers, logger):
    """
    Adds issue labels
    """
    template = 'https://%s.atlassian.net/rest/api/2/issue/%s'
    url = template % (instance, issue_key)
    addition = [{'add': label} for label in labels]
    payload = {'update': {'labels': addition}}
    payload = json.dumps(payload).encode('utf-8')
    http(logger, url, 'PUT', headers, payload)
    labels = ', '.join(labels)
    logger.info(f'{issue_key} - {labels}')


def find_missing_labels(issue_summary, issue_labels):
    """
    Returns the list of strings in square brackets from summary
    filtered to feature only the strings not found among labels
    """
    found = re.findall(r'\[.*?\]', issue_summary)
    found = [item.replace('[', '').replace(']', '') for item in found]
    found = [item.replace(' ', '_') for item in found]
    found = [item.upper() for item in found]
    return [item for item in found if item not in issue_labels]


def main():
    """
    Main function of the script
    """
    logger = init_logging()
    headers = prepare_headers()
    instance, query, sleep = prepare_parameters()
    while True:
        issues = query_issues(instance, query, headers, logger)
        for issue in issues:
            issue_key = issue['key']
            issue_summary = issue['fields']['summary']
            issue_labels = issue['fields']['labels']
            missing = find_missing_labels(issue_summary, issue_labels)
            if missing:
                add_issue_labels(
                    instance, issue_key, missing, headers, logger)
        time.sleep(sleep)


if __name__ == '__main__':
    main()
