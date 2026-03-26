# `.github/agents/`

This directory contains **GitHub Copilot custom agents** (`.agent.md` files) for the Contoso Finance project.

## Conventions

See **`skills/custom-agents/SKILL.md`** for the full authoring guide, including:

- File format and frontmatter reference
- Optimized agent template
- Nested agent / orchestration patterns
- Tool selection by role
- Naming conventions and quality checklist

## Available Agents

### Standalone

| Agent                  | File                          | Tools                                | Purpose                                                                             |
| ---------------------- | ----------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| **backend-developer**  | `backend-developer.agent.md`  | `read, edit, search, terminal`       | Implements server-side domain features (models → schemas → repo → service → router) |
| **frontend-developer** | `frontend-developer.agent.md` | `read, edit, search, terminal`       | Builds Fluent UI v9 pages and components with dark-theme conventions                |
| **test-writer**        | `test-writer.agent.md`        | `read, edit, search, terminal, test` | Writes and runs pytest (server) and vitest (client) tests                           |
| **code-reviewer**      | `code-reviewer.agent.md`      | `read, search`                       | Read-only review for correctness, conventions, security, and architecture           |

### Orchestrator

| Agent               | File                       | Tools                 | Purpose                                                       |
| ------------------- | -------------------------- | --------------------- | ------------------------------------------------------------- |
| **feature-builder** | `feature-builder.agent.md` | `agent, read, search` | Full-stack feature delivery: plan → implement → test → review |

### Subagents (feature-builder)

| Agent               | File                       | Tools                                | Purpose                                                 |
| ------------------- | -------------------------- | ------------------------------------ | ------------------------------------------------------- |
| **fb--planner**     | `fb--planner.agent.md`     | `read, search`                       | Analyzes requirements and produces implementation plans |
| **fb--implementer** | `fb--implementer.agent.md` | `read, edit, search, terminal`       | Writes backend + frontend code per plan                 |
| **fb--tester**      | `fb--tester.agent.md`      | `read, edit, search, terminal, test` | Writes and runs tests for implemented features          |

## Quick start

1. Copy the template from the skill file
2. Save as `<your-agent-name>.agent.md` in this directory
3. Follow the quality checklist before committing
