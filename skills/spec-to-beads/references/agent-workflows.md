# Agent Workflows

Coordination patterns for AI agents and human collaboration using beads.

## Team Model

**One human (you)** directing multiple AI agents. Work is specialized, not people.

### Work Categories Requiring Human Input
- **Architecture decisions**: Major tech choices, tradeoffs
- **Product direction**: What to build, priorities, scope
- **External coordination**: API keys, third-party accounts, purchases
- **Judgment calls**: Ambiguous requirements, edge case decisions
- **Review/approval**: Final sign-off on significant changes

### Work Categories Agents Handle Well
- **Implementation**: Writing code to spec
- **Testing**: Creating and running tests
- **Refactoring**: Improving existing code
- **Documentation**: Writing docs from code
- **Bug fixes**: Fixing well-defined issues
- **Research**: Investigating options, reporting findings

## Session Patterns

### Agent Boot-Up Protocol

Every agent session should start with:

```bash
# 1. Sync latest state
br sync --import-only

# 2. Find actionable work
br ready --json

# 3. Check for assigned work
br list --assignee "agent:$(whoami)" --status open --json

# 4. Claim a task
br update bd-xxx --status in_progress --assignee "agent:$(whoami)"

# 5. Show task details
br show bd-xxx --json
```

### Agent Landing Protocol

Every agent session should end with:

```bash
# 1. Update task with progress
br update bd-xxx --notes "Completed X, Y remains"

# 2. If complete, close
br close bd-xxx --reason "Implemented in commit abc123"

# 3. File any discovered work
br create "Discovered: edge case in validation" --type bug --priority 2

# 4. Sync to JSONL
br sync --flush-only

# 5. Commit
git add . && git commit -m "feat: implement X (bd-xxx)"
```

## Coordination Patterns

### Pipeline Pattern

Sequential handoff between specialized agents:

```
Agent A (Design) → Agent B (Implement) → Agent C (Test)

# Agent A creates, Agent B waits
br create "Design: API schema" --type spike --assignee "agent:claude"
# Agent A completes
br close bd-design --reason "Schema in api.yaml"

# Agent B auto-picks up (dependency now resolved)
br ready --json  # Shows implementation task
```

### Swarm Pattern

Multiple agents work independently on parallel tracks:

```
           ┌─ Agent A: Backend Track
Epic ──────┼─ Agent B: Frontend Track  
           └─ Agent C: Infrastructure Track

# Each track has independent tasks
br list --labels backend --status open
br list --labels frontend --status open
br list --labels infra --status open
```

### Supervisor Pattern

You coordinate multiple agents working in parallel:

```
You (Human)
    │
    ├── Agent A (Cursor) - frontend tasks
    ├── Agent B (Claude Code) - backend tasks
    └── Agent C (Codex) - test tasks

# Assign work
br update bd-ui-task --assignee "agent:cursor"
br update bd-api-task --assignee "agent:claude-code"

# Agents report back via notes
br update bd-ui-task --notes "Blocked on API contract"
```

### Review Pattern

Work requires your approval before proceeding:

```bash
# Agent completes implementation
br update bd-xxx --status review --notes "Ready for review"
br label add bd-xxx needs-review

# You review
br show bd-xxx
br comments add bd-xxx "LGTM, minor: add error handling for X"
br label remove bd-xxx needs-review

# Agent picks up feedback and continues
br list --status review --json
```

## Multi-Agent Safety Rules

### Claiming Work

```bash
# ALWAYS claim before starting
br update bd-xxx --status in_progress --assignee "agent:$(whoami)"

# Check claim succeeded (handle race conditions)
OWNER=$(br show bd-xxx --json | jq -r '.assignee')
if [ "$OWNER" != "agent:$(whoami)" ]; then
    echo "Task claimed by $OWNER, finding alternate work"
    br ready --json | jq '.[1]'  # Get next task
fi
```

### Conflict Prevention

```bash
# Before editing a file, check no other agent has related in-progress tasks
br list --status in_progress --json | jq '.[] | select(.labels | contains(["backend"]))'

# Use file-level locks if needed (in notes)
br update bd-xxx --notes "LOCK: editing src/auth/*.rs"
```

### Dependency Awareness

```bash
# NEVER work on blocked tasks
br show bd-xxx --json | jq '.blocked_by'

# If you discover a blocker, file it
br create "Blocker: need OAuth credentials" --type task --priority 0
br dep add bd-current-task bd-new-blocker
```

## Communication Patterns

### Via Bead Notes

```bash
# Progress update
br update bd-xxx --notes "$(date): Completed steps 1-3, step 4 in progress"

# Handoff note
br update bd-xxx --notes "HANDOFF: API complete, frontend can proceed"

# Blocker note
br update bd-xxx --notes "BLOCKED: waiting on external API key from ops"
```

### Via Comments

```bash
# Agent asks a question (for you)
br comments add bd-xxx "QUESTION: Should this support batch operations?"

# You answer
br comments add bd-xxx "Yes, add batch endpoint as follow-up task"

# Code review feedback
br comments add bd-xxx "Edge case: what if user_id is null? Add validation."
```

### Via Labels

```bash
# Signal state
br label add bd-xxx blocked:external
br label add bd-xxx needs-review
br label add bd-xxx needs-decision
br label add bd-xxx wip

# Signal ownership
br label add bd-xxx agent:cursor
```

## Escalation Patterns

### Stuck Agent

```bash
# Agent recognizes it's stuck
br update bd-xxx --notes "STUCK: tried X, Y, Z - need guidance"
br label add bd-xxx needs-decision
br update bd-xxx --assignee "human"
```

### Scope Creep

```bash
# Agent discovers task is larger than expected
br update bd-xxx --notes "SCOPE: this requires 5 subtasks, not 1"

# File the subtasks
br create "Subtask 1 of: original title" --type task --priority 1
br create "Subtask 2 of: original title" --type task --priority 1
# ... etc

# Link them
br dep add bd-original bd-subtask1
br dep add bd-original bd-subtask2
```

### Quality Gate Failure

```bash
# Tests fail
br update bd-xxx --notes "FAILED: tests fail on edge case X"
br label add bd-xxx test-failure

# Create fix task
br create "Fix: test failure in auth module" --type bug --priority 0
br dep add bd-xxx bd-fix-task
```

## Metrics and Observability

### Task Timing

```bash
# Start time (in notes)
br update bd-xxx --notes "STARTED: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# End time (in close reason)
br close bd-xxx --reason "COMPLETED: $(date -u +%Y-%m-%dT%H:%M:%SZ) | duration: 45min"
```

### Velocity Tracking

```bash
# Count completed this week
br list --status closed --json | jq 'length'

# Points completed (if using story points in labels)
br list --status closed --labels "points:3" --json | jq 'length'
```

### Agent Performance

```bash
# Tasks by agent
br list --assignee "agent:cursor" --status closed --json | jq 'length'

# Blocked time (parse from notes)
br list --labels blocked --json | jq '.[].notes'
```
