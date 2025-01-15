#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks if user is a watcher of queried Jira issues
and adds the user if not watching.
"""

import base64
import fcntl
import json
import logging
import os
import urllib.parse
import urllib.request
import sys


def init_logging():
    """
    Initiates logging
    """
    pattern = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=pattern, level=logging.INFO)


def http(url, method, headers, data=None):
    """
    Fetches the given URL (with reply caching & optional authorization)
    """
    result = "{}"
    while True:
        if headers is None:
            request = urllib.request.Request(url, method=method, data=data)
        else:
            request = urllib.request.Request(
                url, method=method, data=data, headers=headers)
        try:
            reply = urllib.request.urlopen(request)  # nosec
            if reply.getcode() in [200, 204]:
                result = reply.read().decode("utf-8")
                break
        except urllib.error.HTTPError as exception:
            logging.error(f"{method} {url} {data}")
            logging.exception(exception)
            break
    return result


def authorization_credentials():
    """
    Reads authorization credentials from environment variables
    """
    user = os.environ.get("SVETOVIT_ATLASSIAN_USER")
    token = os.environ.get("SVETOVIT_ATLASSIAN_TOKEN")
    return (user, token)


def authorization_headers(user, token):
    """
    Prepares authorization header for an API request
    """
    if None in [user, token]:
        return None
    credentials = f"{user}:{token}"
    auth = base64.b64encode(credentials.encode("utf-8"))
    headers = {"Authorization": "Basic %s" % auth.decode("utf-8")}
    return headers


def prepare_headers():
    """
    Prepares headers for Atlassian API
    """
    credentials = authorization_credentials()
    headers = authorization_headers(*credentials)
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    return headers


def prepare_parameters():
    """
    Prepare the operational parameters
    """
    instance = os.environ.get("SVETOVIT_ATLASSIAN_INSTANCE")
    query = urllib.parse.quote(os.environ.get("SVETOVIT_ATLASSIAN_QUERY"))
    watcher = os.environ.get("SVETOVIT_ATLASSIAN_WATCHER")
    return (instance, query, watcher)


def query_issues(instance, query, headers):
    """
    Queries for issues and aggregates over paging
    """
    template = "https://%s.atlassian.net/rest/api/2/search?&jql=%s&startAt=%d"
    issues = []
    index = 0
    while True:
        url = template % (instance, query, index)
        reply = http(url, "GET", headers)
        reply = json.loads(reply)
        if "issues" not in reply:
            break
        issues.extend(reply["issues"])
        if reply["total"] == len(issues):
            break
        index += len(reply["issues"])
    return issues


def filter_issues(issues):
    """
    Returns only the issues the user is not watching
    """
    not_watching = []
    for issue in issues:
        watching = issue["fields"]["watches"]["isWatching"]
        if not watching:
            not_watching.append(issue)
    return not_watching


def watch_issues(not_watching, instance, watcher, headers):
    """
    Watch the unwatched issues
    """
    template = "https://%s.atlassian.net/rest/api/2/issue/%s/watchers"
    watcher = f"\"{watcher}\"".encode("utf-8")
    for issue in not_watching:
        issue_key = issue["key"]
        issue_summary = issue["fields"]["summary"]
        url = template % (instance, issue_key)
        http(url, "POST", headers, watcher)
        logging.info(f"{issue_key} {issue_summary}")


def main():
    """
    Main function of the script
    """
    with open("/tmp/atlassian.lock", "w") as lock:
        try:
            fcntl.lockf(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            # The task is already running
            sys.exit()
        init_logging()
        headers = prepare_headers()
        instance, query, watcher = prepare_parameters()
        issues = query_issues(instance, query, headers)
        not_watching = filter_issues(issues)
        watch_issues(not_watching, instance, watcher, headers)


if __name__ == "__main__":
    main()
