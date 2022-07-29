# Atlassian

## svetovid

If you want to automatically become a watcher of Atlassian Jira issues (and are not the owner/administrator) then you can use this service to accomplish this (with suitable email client rules it creates an office experience by revealing what is generally happening without the necessity of acting upon it):

```bash
ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" ATLASSIAN_USER="$ATLASSIAN_USER" ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" ATLASSIAN_QUERY="$ATLASSIAN_QUERY" ATLASSIAN_WATCHER="$ATLASSIAN_WATCHER" SVETOVID_SLEEP="$SVETOVID_SLEEP" python svetovid.py
```


## veles

If you want to prefix Atlassian Jira issues with [...] and have it automatically carried over into labels then you can use this service to accomplish this:

```bash
ATLASSIAN_INSTANCE="$ATLASSIAN_INSTANCE" ATLASSIAN_USER="$ATLASSIAN_USER" ATLASSIAN_TOKEN="$ATLASSIAN_TOKEN" ATLASSIAN_QUERY="$ATLASSIAN_QUERY" VELES_SLEEP="$VELES_SLEEP" python veles.py
```
