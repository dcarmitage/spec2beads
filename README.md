# spec-to-beads

A Claude Code skill that transforms vague product specs into well-structured agile beads (issues) for AI agent and human collaboration.

## What it does

Takes inputs like "we need user authentication" and decomposes them into a proper DAG of:
- Epics, features, tasks, spikes, bugs, chores
- Dependencies between beads
- Acceptance criteria
- Priority levels (P0-P4)
- Labels for organization

Designed for [beads_rust (br)](https://github.com/Dicklesworthstone/beads_rust) - a local-first, non-invasive issue tracker.

## Installation

### Via Claude Code Plugin Marketplace

```bash
# In Claude Code
/plugin marketplace add dcarmitage/spec-to-beads

# Then install the skill
/plugin install spec-to-beads@spec-to-beads
```

### Manual Installation

Clone to your Claude Code skills directory:

```bash
# Personal skill (available in all projects)
git clone https://github.com/dcarmitage/spec2beads ~/.claude/skills/spec-to-beads

# Or project skill (shared with team via git)
git clone https://github.com/dcarmitage/spec2beads .claude/skills/spec-to-beads
```

## Usage

Just describe what you want to build:

```
"We need user authentication with email/password and OAuth"
```

Claude will:
1. Analyze the spec for goals, scope, and unknowns
2. Decompose into INVEST-compliant beads
3. Generate `br create` commands with proper types, priorities, and acceptance criteria
4. Set up the dependency DAG

## Team Model

This skill assumes:
- **One human (you)** directing multiple AI agents
- Work is specialized, not people
- Tasks requiring your input get `needs-decision` label and `human` assignee
- Everything else agents can pick up from `br ready`

## Included Files

- `SKILL.md` - Main instructions
- `references/decomposition-patterns.md` - Templates for common features (auth, CRUD, payments, etc.)
- `references/agent-workflows.md` - Multi-agent coordination patterns
- `scripts/generate_beads.py` - Generate bash scripts from JSON plans
- `assets/example-auth-plan.json` - Example plan you can use as a template

## Requirements

- [beads_rust (br)](https://github.com/Dicklesworthstone/beads_rust) installed
- A git repository with `br init` run

## License

MIT
