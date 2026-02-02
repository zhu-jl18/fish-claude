# CLAUDE.md

## Defaults

- Reply in **Chinese** unless I explicitly ask for English.
- No emojis.
- Do not truncate important outputs (logs, diffs, stack traces, commands,
  or critical reasoning that affects safety/correctness).

## Code Quality Rules

- **No patch stacking**: When code is hard to maintain or badly designed, do a
  **clean, full refactor** — not minimal changes.
- **No backward compatibility**: When the user requests new requirements,
  tear it down and rebuild. Don't carry legacy baggage.
- **Refactor thoroughly**: When refactoring, change **all** related code together.
  Leave no remnants behind.

## Before Touching Code (mandatory)

Find reuse opportunities + Trace the call/dependency chain and impact radius:

- Use semantic code search first via `codebase-retrieval` tool.
- Confirm understanding with LSP: `goToDefinition`, `findReferences`.
- Use Grep/Glob for verifying and understanding additional code snippets.

## Red Lines

- No copy-paste duplication.
- Do not proceed with a known-wrong approach.
- Critical paths must have explicit error handling.
- Never implement "blindly": always confirm understanding via code reading + references.

## Web Research (no guessing)

If something is unfamiliar or likely version-sensitive,
you MUST search the web instead of guessing:

- Use: `WebSearch`
- or Use Exa: `mcp__exa__web_search_exa`.

Source priority:

1. Official docs / API reference.
2. Official changelog / release notes.
3. Upstream GitHub repository docs (README, `/docs`).
4. Community posts only if necessary to fill gaps.

Version rule:

- When behaviour may differ across versions,
  first identify the project's version (lockfile/config),
  then search docs specifically for that version.

## Git

GitHub CLI (`gh`) is installed. Default username: `xxx`. Alternatives: `yyy`, `zzz`.

## Commit and Push Rules

- Do not commit unless I explicitly ask.
- Do not push unless I explicitly ask.
- Before writing a commit message, glance at a few recent commits
  and match the repo's style:
  - `git log -n 5 --oneline`
- If there is no obvious existing style, use this default format:
  - `<type>(<scope>): <description>`
- Before any commit: run `git diff` and confirm the exact scope of changes.
- Never force-push to `main` / `master` unless the user approves.
- Do not add attribution lines in commit messages.

## Security

- Never hardcode secrets (keys/passwords/tokens).
- Never commit `.env` files or any credentials.
- Validate user input at trust boundaries (APIs, CLIs, external data sources).

## Cleanup

- If you change a function signature, update **all** call sites.
- After any changes, check and update all related documentation:
  `README.md`, `CLAUDE.md`, `AGENTS.md`, and any other relevant docs.
- After changes:
  - Remove temporary files.
  - Remove dead/commented-out code.
  - Remove unused imports.
  - Remove debug logging that is no longer needed.

## Environment

When using PowerShell:

- PowerShell does not support `&&`; use `;` to chain commands.
- Quote paths that contain spaces or non-ASCII characters.

When using Git Bash on Windows:

- **NUL file bug**: Claude Code may create actual files named `nul` when commands
  redirect output to `NUL` (e.g., `> NUL`, `2> NUL`). `NUL` is a reserved device
  name on Windows; if a `nul` file is created, delete it via UNC path:
  `del "\\.\<full-path>\nul"`
