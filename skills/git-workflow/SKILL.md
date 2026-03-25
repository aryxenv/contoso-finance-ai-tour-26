---
name: git-workflow
description: Enforces the project's Git branching model, conventional commits, PR workflow, and commit granularity rules. Use this when creating branches, writing commit messages, opening PRs, or performing any Git operations.
---

# Git Workflow — Special Olympics Data Dashboard

## Tooling — Always use `gh` CLI

**All Git operations MUST use the `gh` CLI** (GitHub CLI). This includes creating branches, pushing, creating PRs, viewing PR status, and merging.

- Do **not** fall back to raw `git` commands when `gh` provides the same functionality.
- Do **not** use the GitHub MCP API for operations `gh` can handle.
- `gh` is installed at `C:\Program Files\GitHub CLI\gh.exe` — add it to PATH if needed.

### Common `gh` commands

```bash
# Create and switch to a new branch
git checkout -b feat/my-feature

# Stage, commit, push, and create PR in one flow
git add src/extract.py
git commit -m "feat(etl): add extraction class"
gh pr create --title "feat(etl): add extraction class" --body "Description" --base main

# Check PR status
gh pr status
gh pr view 1

# List open PRs
gh pr list
```

## Branching Model

`main` is the single production + development branch.

- **Never commit directly to `main`.** All changes (features, fixes, docs, etc.) must go through a dedicated branch + pull request.
- Create a branch from `main` for each unit of work, then open a PR back to `main`.
- PRs require approval before merging — reviewers may request changes.
- Do **not** merge your own PR without approval.

## Branch Naming

Use the conventional commit type as a prefix:

```
feat/short-description     → new feature
fix/short-description      → bug fix
docs/short-description     → documentation only
refactor/short-description → code restructure (no behaviour change)
chore/short-description    → tooling, deps, CI, config
test/short-description     → adding or updating tests
```

### Steps to create a branch

```bash
git checkout main
git pull origin main
git checkout -b feat/my-new-feature
```

## Commit Granularity

Split work into **logical, atomic commits** — never lump all changes into a single commit per branch/PR.

- Each commit should represent one self-contained change (e.g., one function, one fix, one file group).
- If a feature touches extract + transform + tests, that is at least 3 separate commits.
- Keep commits reviewable: a reviewer should understand each commit on its own.

### How to stage logical groups

```bash
# Stage only related files for one logical commit
git add src/extract.py
git commit -m "feat(etl): add Excel extraction class"

# Then stage the next logical group
git add src/transform.py
git commit -m "feat(etl): add score normalization in transform"

# Then tests
git add tests/test_extract.py
git commit -m "test(etl): add unit tests for extraction"
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <short summary>

[optional body]
```

### Types

| Type       | When to use                                    |
| ---------- | ---------------------------------------------- |
| `feat`     | New feature or capability                      |
| `fix`      | Bug fix                                        |
| `docs`     | Documentation only                             |
| `refactor` | Code restructure with no behaviour change      |
| `chore`    | Tooling, deps, CI, config                      |
| `test`     | Adding or updating tests                       |
| `style`    | Formatting, whitespace (no logic change)       |
| `perf`     | Performance improvement                        |
| `ci`       | CI/CD pipeline changes                         |
| `build`    | Build system or external dependency changes    |

### Examples

```
feat(etl): add score normalization for time-based results
fix(transform): handle DQ entries in rank parsing
docs: update data requirements with medal logic
chore: add openpyxl to requirements.txt
refactor(extract): simplify multi-sheet reading logic
test(transform): add edge cases for ordinal rank parsing
```

## Pre-Push Verification

**Before pushing a branch, always run the linter against the directories you changed.** This catches lint failures locally instead of waiting for CI to fail — a very common pain point.

### How to determine what to lint

Check which top-level areas you touched, then run the appropriate linter:

```bash
# See which files changed on your branch
git diff --name-only main

# If you changed files in apps/server/ — run ruff
cd apps/server && uv run ruff check src/ tests/

# If you changed files in apps/client/ or packages/shared-types/ — run eslint / tsc
cd apps/client && npm run lint
cd packages/shared-types && npm run build
```

### Rules

- **Always lint before pushing.** If lint fails, fix the issues and amend or add a commit before pushing.
- Only lint the directories you actually changed — no need to lint the entire repo.
- If you changed both `apps/server/` and `apps/client/`, run both linters.
- This applies to every push, not just the final one before a PR.

### Full CI check — before creating a PR

Before opening a pull request, run the **full CI pipeline locally** for every area you changed. Do not rely on remote CI to catch failures — fix them before the PR exists.

**If CI is configured in the workspace** (e.g., `.github/workflows/` exists), mirror its checks locally:

1. Identify which CI jobs cover the areas you changed.
2. Run those checks locally (lint + build + test).
3. If anything fails, fix it and re-run until all checks pass.
4. Only then create the PR.

**Contoso Finance CI commands by area:**

```bash
# Server (apps/server/) — lint + tests
cd apps/server
uv run ruff check src/ tests/
uv run pytest tests/ -v

# Client (apps/client/) — lint + build + tests
cd apps/client
npm run lint
npm run build
npm run test

# Shared types (packages/shared-types/) — type check
cd packages/shared-types
npm run build
```

**Rules:**

- This applies before PR creation — not every intermediate push. (Linting still applies to every push.)
- If a test failure is pre-existing and unrelated to your changes, note it in the PR description — don't silently ignore it.
- If the project has no CI configured, this step is skipped. Linting before push still applies.

## Pull Requests

### PR titles

PR titles follow the same conventional commit format:

```
feat(etl): implement athlete dimension extraction
fix(transform): correct fuzzy club matching threshold
docs: add star schema diagram to README
```

### PR granularity — one logical change per PR

Each pull request should represent **one logical, reviewable unit of work**. If a reviewer needs to context-switch between unrelated changes while reading your PR, it's too broad.

**Principles:**

- A PR addresses one concern: a feature, a bug fix, a refactor, or a docs update — not several at once.
- Drive-by fixes (unrelated cleanups spotted during development) get their own separate PR.
- If a PR grows beyond ~400 lines of meaningful change, consider splitting it. This is a reviewability signal, not a hard rule — a 500-line migration file is fine; a 400-line PR touching 8 unrelated modules is not.

**Decomposing large features into sequential PRs:**

If a feature spans multiple layers or domains, break it into a chain of small PRs that each land independently and leave `main` in a working state.

Example — adding a new "Notifications" domain to Contoso Finance:

| PR | Branch | What it delivers |
|----|--------|-----------------|
| 1  | `feat/notifications-model` | Data model + Alembic migration — the table exists but nothing uses it yet |
| 2  | `feat/notifications-api` | Repository, service, and router (CRUD endpoints) — backend is functional, no UI yet |
| 3  | `feat/notifications-ui` | React components + API integration — feature is user-visible |

Each PR is independently reviewable, testable, and mergeable. Reviewers see focused diffs instead of a wall of cross-cutting changes.

**When one PR is acceptable for a multi-layer change:**

- The total change is small (e.g., under ~200 lines across all layers)
- The layers are tightly coupled for this specific change and splitting would make review harder
- It's a bug fix that necessarily touches model + service + test

### PR workflow

1. Push your branch and create a PR with `gh`:
   ```bash
   gh pr create --title "feat(etl): my feature" --body "Description" --base main
   ```
2. Use a conventional commit-style title for the PR.
3. Check PR status:
   ```bash
   gh pr status
   ```
4. Wait for review and approval — do **not** merge without it.
5. Address any requested changes with additional commits on the same branch.
6. Once approved, the reviewer (or you, after approval) merges the PR.

### What NOT to do

- ❌ Push directly to `main`
- ❌ Merge your own PR without approval
- ❌ Squash an entire feature into one giant commit
- ❌ Use vague commit messages like `"update files"` or `"WIP"`
- ❌ Use raw `git push` + GitHub web UI when `gh pr create` can do it
- ❌ Push without running the linter on changed directories first
- ❌ Mix unrelated concerns in a single PR (e.g., a feature + an unrelated refactor)
- ❌ Open mega-PRs that require reviewers to context-switch across domains
- ❌ Bundle drive-by fixes with the main feature — give them their own PR
- ❌ Create a PR when local builds or tests are failing
- ❌ Rely on remote CI as your first line of defense — run checks locally first
