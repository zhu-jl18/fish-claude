# Git

GitHub CLI (`gh`) is installed.

## Commit and Push Rules

- Do not commit unless the user explicitly asks.
- Do not push unless the user explicitly asks.
- Before writing a commit message, glance at a few recent commits
  and match the repo's style:
  - `git log -n 5 --oneline`
- If there is no obvious existing style, use this default format:
  - `<type>(<scope>): <description>`
- Before any commit: run `git diff` and confirm the exact scope of changes.
- Never force-push to `main` / `master` unless the user approves.
