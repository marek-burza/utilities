# Svetovit

With suitable email client rules it creates an office experience by revealing what is generally happening without the necessity of acting upon it.

## Atlassian

If you want to automatically become a watcher of Atlassian Jira issues (and are not the owner/administrator) then you can use this service to accomplish this:

```shell
SVETOVIT_ATLASSIAN_INSTANCE="$SVETOVIT_ATLASSIAN_INSTANCE" SVETOVIT_ATLASSIAN_USER="$SVETOVIT_ATLASSIAN_USER" SVETOVIT_ATLASSIAN_TOKEN="$SVETOVIT_ATLASSIAN_TOKEN" SVETOVIT_ATLASSIAN_QUERY="$SVETOVIT_ATLASSIAN_QUERY" SVETOVIT_ATLASSIAN_WATCHER="$SVETOVIT_ATLASSIAN_WATCHER" python svetovit_atlassian.py
```


## GitLab

If you want to automatically subscribe to merge requests on GitLab you can use this service to accomplish this:

```shell
SVETOVIT_GITLAB_URL="$SVETOVIT_GITLAB_URL" SVETOVIT_GITLAB_TOKEN="$SVETOVIT_GITLAB_TOKEN" SVETOVIT_GITLAB_GROUPS="$SVETOVIT_GITLAB_GROUPS" SVETOVIT_GITLAB_USERS="$SVETOVIT_GITLAB_USERS" SVETOVIT_GITLAB_SPAN="$SVETOVIT_GITLAB_SPAN" SVETOVIT_GITLAB_SKIP="$SVETOVIT_GITLAB_SKIP" python svetovit_gitlab.py
```
