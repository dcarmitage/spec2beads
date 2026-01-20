---
name: spec-to-beads
description: Transform vague product specs into well-structured agile beads (issues) for AI agent and human collaboration. Use when a user provides a feature request, PRD, idea, or any vague requirement that needs to be decomposed into actionable tasks. Outputs beads_rust (br) compatible issues with dependencies, priorities, types, and acceptance criteria. Designed for Linear-style workflows where AI agents and humans collaborate on product development.
---

# Spec to Beads

Transform vague specs into structured, actionable beads for AI/human team collaboration.

## Quick Start

```bash
# 1. Ensure br is initialized
br init

# 2. Analyze the spec (Claude does this)
# 3. Generate beads with proper structure
br create "Epic: User Authentication" --type epic --priority 1
br create "Design auth flow" --type task --priority 1 --parent bd-epic-id
br dep add bd-child bd-blocker  # Set dependencies
```

## Workflow

### 1. Analyze the Spec

Extract from the user's input:
- **Goal**: What are we ultimately trying to achieve?
- **Users**: Who benefits? What are their needs?
- **Scope signals**: MVP vs full-featured, time constraints, technical constraints
- **Implicit requirements**: Security, error handling, edge cases
- **Unknowns**: What needs investigation before implementation?

### 2. Decompose into Beads

Apply the **INVEST** criteria for each bead:
- **I**ndependent: Minimize dependencies where possible
- **N**egotiable: Leave implementation details flexible
- **V**aluable: Each delivers user/business value
- **E**stimable: Clear enough to estimate effort
- **S**mall: Completable in one work session (for agents: < 1 context window)
- **T**estable: Has clear acceptance criteria

### 3. Structure the Hierarchy

```
Epic (P1-P2)
├── Feature (P1-P2)
│   ├── Task (P1-P3) - atomic work unit
│   └── Task
├── Feature
│   ├── Task
│   └── Bug (if discovered)
└── Spike (P2-P3) - investigation/research
```

### 4. Set Dependencies

Model the DAG (Directed Acyclic Graph):
- `br dep add <child> <parent>` — child is blocked by parent
- Identify critical path (longest chain of dependencies)
- Parallelize independent work tracks

### 5. Output Format

For each bead, generate:

```bash
br create "TITLE" \
  --type TYPE \
  --priority PRIORITY \
  --description "DESCRIPTION" \
  --acceptance "ACCEPTANCE_CRITERIA" \
  --labels "LABELS"
```

## Bead Types

| Type | Use For | Who Typically Handles |
|------|---------|----------------------|
| `epic` | Large initiative spanning multiple features | Human sets direction, agents execute |
| `feature` | User-facing capability | Collaborative |
| `task` | Atomic implementation work | Agent-optimal |
| `bug` | Defect fix | Agent-optimal |
| `spike` | Research/investigation | Either; agent reports findings |
| `chore` | Maintenance, refactoring | Agent-optimal |

## Priority Levels

| Priority | Meaning | Timeline |
|----------|---------|----------|
| P0 | Critical/blocking | Immediate |
| P1 | High - core functionality | This sprint |
| P2 | Medium - important | Next sprint |
| P3 | Low - nice to have | Backlog |
| P4 | Someday/maybe | Icebox |

## Agent Collaboration Patterns

### Assigning Work
```bash
# Assign to specific agent
br update bd-xxx --assignee "agent:cursor"
br update bd-xxx --assignee "agent:claude-code"

# Assign to human (you)
br update bd-xxx --assignee "human"

# Or leave unassigned - agents pick from br ready
```

### Agent Handoff Protocol
When an agent completes work:
```bash
br update bd-xxx --status done
br close bd-xxx --reason "Implemented in commit abc123"
br sync --flush-only  # Export for git
```

### Multi-Agent Coordination
- Use `br ready --json` to find unblocked work
- Agents claim via `br update bd-xxx --status in_progress`
- Dependencies prevent collision on blocked work

## Decomposition Templates

### API Endpoint
```
1. [spike] Design API contract (OpenAPI/schema)
2. [task] Implement endpoint handler
3. [task] Add input validation
4. [task] Add authentication/authorization
5. [task] Write integration tests
6. [task] Add documentation
Dependencies: 2→1, 3→2, 4→2, 5→2, 6→2
```

### UI Feature
```
1. [spike] Design mockups/wireframes
2. [task] Create component skeleton
3. [task] Implement core UI logic
4. [task] Add state management
5. [task] Connect to API
6. [task] Add loading/error states
7. [task] Write tests
Dependencies: 2→1, 3→2, 4→3, 5→4, 6→5, 7→5
```

### Database Migration
```
1. [spike] Design schema changes
2. [task] Write migration script
3. [task] Update ORM/models
4. [task] Update queries/repositories
5. [task] Add rollback procedure
6. [task] Test on staging data
Dependencies: 2→1, 3→2, 4→3, 5→2, 6→4,5
```

## Acceptance Criteria Format

Use Given/When/Then for testable criteria:

```
Given [precondition]
When [action]
Then [expected result]
```

Or checklist format:
```
- [ ] User can perform X
- [ ] Error Y shows message Z
- [ ] Performance: < 200ms response
- [ ] Security: validates input against schema
```

## Labels for Organization

Standard labels:
- `backend`, `frontend`, `infra`, `docs`
- `security`, `performance`, `ux`
- `blocked:external`, `needs-review`, `needs-decision`
- `quick-win`, `complex`

```bash
br label add bd-xxx backend security
```

## Example: Vague Spec → Beads

**Input**: "We need user authentication"

**Output**:
```bash
# Epic
br create "Epic: User Authentication System" --type epic --priority 1 \
  --description "Implement secure user authentication with email/password and OAuth"

# Spike - resolve unknowns first
br create "Spike: Auth architecture decision" --type spike --priority 1 \
  --description "Decide JWT vs sessions, OAuth providers, password requirements" \
  --acceptance "ADR document with chosen approach"

# Core features (depend on spike)
br create "Implement password auth flow" --type feature --priority 1 \
  --description "Email/password registration and login" \
  --acceptance "User can register, login, logout; passwords hashed with bcrypt"

br create "Implement OAuth login" --type feature --priority 2 \
  --description "Google and GitHub OAuth integration" \
  --acceptance "User can login via Google/GitHub; accounts linked correctly"

# Tasks under password auth feature
br create "Create users table migration" --type task --priority 1 \
  --labels "backend database"
  
br create "Implement registration endpoint" --type task --priority 1 \
  --labels "backend api" \
  --acceptance "POST /auth/register validates input, hashes password, returns JWT"

br create "Implement login endpoint" --type task --priority 1 \
  --labels "backend api"

br create "Add email verification flow" --type task --priority 2 \
  --labels "backend email"

br create "Build registration form UI" --type task --priority 1 \
  --labels "frontend"

br create "Build login form UI" --type task --priority 1 \
  --labels "frontend"

# Set dependencies
br dep add bd-registration-endpoint bd-users-migration
br dep add bd-login-endpoint bd-users-migration
br dep add bd-password-feature bd-auth-spike
br dep add bd-oauth-feature bd-auth-spike
```

## Critical Rules

1. **Never create beads larger than one agent work session** — if it can't be done in one context window, split it
2. **Always include acceptance criteria** — agents need clear "done" definitions
3. **Model dependencies explicitly** — enables `br ready` to show unblocked work
4. **Use spikes for unknowns** — don't let agents guess at architecture decisions
5. **Label for decisions** — use `needs-decision` when human judgment required

## See Also

- `references/decomposition-patterns.md` — More decomposition templates
- `references/agent-workflows.md` — Multi-agent coordination patterns
