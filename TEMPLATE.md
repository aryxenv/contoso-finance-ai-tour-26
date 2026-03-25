# Template Usage

This is a template repository, however the template does not transfer issues. Here is how to transfer it:

## Pre-requisites

- Copilot CLI (https://github.com/features/copilot/cli)
- Github CLI (https://cli.github.com/)
- Authenticated through Github CLI (`gh auth login`)

## Get started

1. Use repository as a template.
2. Copy the link to the repository you made (e.g. https://github.com/aryxenv/contoso-finance-ai-tour-26)
3. Clone your repo

```bash
git clone <YOUR_REPO_URL> # replace with your repo url (e.g. https://github.com/aryxenv/contoso-finance-ai-tour-26)
```

4. Clone the template repo & navigate to it

```bash
git clone https://github.com/aryxenv/contoso-finance
cd contoso-finance
```

5. Start Copilot CLI

```bash
copilot
```

6. Transfer prompt (on Plan Mode - `shift+tab` to switch) -> NOTE: REPLACE `<USER>` AND `<YOUR_REPO_NAME>`

```txt
Read all open issues from this repo (aryxenv/contoso-finance) using the GitHub CLI.
Create them as new issues in https://github.com/<USER>/<YOUR_REPO_NAME> (I own this repo).

The source repo has gaps in issue numbers (e.g. #9, #11, #12, …, #35). In the target repo,
issues must be created sequentially so they are numbered #1 through #22 with no gaps.
Create them in ascending order of their source issue number so the relative order is preserved.

For each issue, copy the title, full body, and labels. Do NOT include any reference back to
the source repo or original issue number. Update any cross-references in issue bodies
(e.g. "depends on #35") to use the new sequential number from the target repo.

Try to do as much in parallel as possible, where safe.
```

7. (optional) It may ask you some questions, select what you believe is best.
8. Select `autopilot + /fleet` option.
9. Let Copilot CLI do it's magic!

> [!TIP]
> To reduce agent hallucination, delete this file when doing the demo.
