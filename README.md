# Minimalistic Tools

- [Static Topographic Map](https://altermarkive.github.io/altermarkive/web/topography.html)
- [Development Environment](sovereign)

# New Mac Quick Start

Scheduled git prefetch:

```bash
git maintenance start
```

Accelerate git status:

```bash
git config --global core.fsmonitor true
git config --global core.untrackedcache true
```

Disable sleep on macOS to avoid interrupting background network tasks with screen lock:

```bash
sudo pmset -a sleep 0
sudo pmset -a hibernatemode 0
sudo pmset -a disablesleep 1
```

# To Do

- Possibly, rework the HTML + JS tool to: https://github.com/pyscript/pyscript

# Other

- Disable all AI in Firefox by going to `about:config` and setting `browser.ml.enable` to `false`
