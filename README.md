![languages](https://github-readme-stats.vercel.app/api/top-langs/?username=altermarkive&hide=html,tex,roff,hcl,jinja,matlab&langs_count=10&layout=compact&hide_border=true&theme=dark)

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
