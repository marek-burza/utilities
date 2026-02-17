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

# AI

- Disable all AI in Firefox by going to `about:config` and setting `browser.ml.enable` to `false`
- [AGENTS.md](https://agents.md)

## Claude Code Cheat Sheet

- `Shift + TAB, Shift TAB` - cycle through modes to enter planning mode
- `#` - with this prefix, the instruction will be memorized in `CLAUDE.md`
- `/init` - to create `CLAUDE.md` (optionally, append and provide more instructions and request it to "ultrathink")
- `Esc, Esc` - to rewind the conversation to before an unrelated side-quest or a mistake in instruction
- `/compact` - to retain knowledge gathered but not the minutia (e.g. to start on a similar task)
- Create `.claude/commands/[name].md` with instructions for a new `/name` command
