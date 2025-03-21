# Favorites

## Favorite git Commands

Print all files ever committed:

```bash
git log --abbrev-commit --pretty=oneline | cut -d ' ' -f 1 | xargs -L1 git diff-tree --no-commit-id --name-only -r | sort | uniq
```

Scheduled prefetch:

```bash
git maintenance start
```

Accelerate status:

```bash
git config core.fsmonitor true
git config core.untrackedcache true
```

## Favorite Mapping Tools

- Isochrones - [Smappen](https://www.smappen.com/), [OpenRouteService](https://maps.openrouteservice.org/)
- Static Topographic Map - [GPX2PNG](https://altermarkive.github.io/altermarkive/gpx2png.html)

## Favorite macOS Commands

Disable sleep on macOS to avoid interrupting background network tasks with screen lock:

```bash
sudo pmset -a sleep 0; sudo pmset -a hibernatemode 0; sudo pmset -a disablesleep 1
```

## Favorite Visual Studio Code Extensions

- [GitLens (GitKraken)](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
- [learn-markdown (Microsoft)](https://marketplace.visualstudio.com/items?itemName=docsmsft.docs-markdown)
- [learn-preview (Microsoft)](https://marketplace.visualstudio.com/items?itemName=docsmsft.docs-preview)
- [Pylance (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [YAML (RedHat)](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

# Linux

- Disable CUPS: https://securityonline.info/severe-unauthenticated-rce-flaw-cvss-9-9-in-gnu-linux-systems-awaiting-full-disclosure/
