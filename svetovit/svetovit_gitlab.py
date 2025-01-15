#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks if user is a subscriber to queried GitLab merge requests
and subscribes the user if not subscribed.
"""

import datetime
import fcntl
import logging
import os
import sys
import time

import gitlab


def main() -> None:
    with open("/tmp/gitlab.lock", "w") as lock:
        try:
            fcntl.lockf(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            # The task is already running
            sys.exit()
        pattern = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=pattern, level=logging.INFO)
        gitlab_url = os.environ["SVETOVIT_GITLAB_URL"]
        gitlab_token = os.environ["SVETOVIT_GITLAB_TOKEN"]
        gitlab_groups = os.environ["SVETOVIT_GITLAB_GROUPS"].lower().split(",")
        gitlab_users = os.environ["SVETOVIT_GITLAB_USERS"].lower().split(",")
        gitlab_span = int(os.environ["SVETOVIT_GITLAB_SPAN"]) * 24 * 60 * 60
        gitlab_skip = os.environ["SVETOVIT_GITLAB_SKIP"]
        since = time.time() - gitlab_span
        created_after = datetime.datetime.fromtimestamp(since, datetime.timezone.utc).isoformat() + "Z"
        api = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
        for group in api.groups.list(get_all=True):
            group_name = group.name.lower()
            if group_name not in gitlab_groups:
                logging.info(f"Skipping {group_name}")
                continue
            logging.info(f"Checking {group_name}")
            for mr in api.groups.get(group_name).mergerequests.list(created_after=created_after, get_all=True):
                title = mr.title
                if gitlab_skip in title:
                    continue
                mr_author = mr.author["username"].lower()
                if mr_author not in gitlab_users:
                    continue
                full_mr = api.projects.get(mr.project_id) .mergerequests.get(mr.iid)
                if not full_mr.subscribed:
                    full_mr.subscribe()
                    reference = mr.references["full"]
                    logging.info(f"Subscribed to {reference} - {title}")


if __name__ == "__main__":
    main()
