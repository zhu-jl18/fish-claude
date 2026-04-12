# Git Commit / Push

- Do not commit unless the user explicitly asks.
- Do not push unless the user explicitly asks.
- Before any commit, inspect the exact change scope first:
  - `git diff`
- Before writing a commit message, glance at a few recent commits and match the repo's style:
  - `git log -n 5 --oneline`
- If there is no obvious existing style, use conventional commits by default:
  - `<type>(<scope>): <description>`
- Never force-push to `main` / `master` unless the user explicitly approves.