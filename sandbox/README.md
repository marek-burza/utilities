# Claude Code Sandbox

- `Shift + TAB, Shift TAB` - cycle through modes to enter planning mode
- `/memory` - with this prefix, the instruction will be memorized in `CLAUDE.md` ([AGENTS.md](https://agents.md))
- `/init` - to create `CLAUDE.md` (optionally, append and provide more instructions and request it to "ultrathink")
- `Esc, Esc` - to rewind the conversation to before an unrelated side-quest or a mistake in instruction
- `/compact` - to retain knowledge gathered but not the minutia (e.g. to start on a similar task)
- Create `.claude/commands/[name].md` with instructions for a new `/name` command (use `$ARGUMENTS` to insert subject into generic instruction)
- `claude mcp add ...` - MCP!
- `/install-github-app` - ability to: mention `@claude` from an issue or a PR to interact there, have Claude Code review your PR
- Use `--teleport` to move cession between web and terminal
- Turn every (repeated) Claude mistake into a rule in `CLAUDE.md`, same with PR/MR ("review and extractnew desirable patterns/conventions, and preventable anti-patterns")
- Use smartest model to reduce mistakes/churn/dead-ends
- Plan (interactively), then execute (automatically)
- Consider [sub-agents](https://code.claude.com/docs/en/sub-agents) for specific domain/expertise/tool and to avoid poluting main context window
- Automate everything with hooks to reduce interruptions / defend flow
- Use "Stop" hook for long-running tasks to verify work delivered
- Tests / verification are crucial
