# Code Quality

## Rules

- **Thorough changes only**: Whether maintaining, adding features, or refactoring —
  do a **clean, full rewrite** of all related code. No patch stacking,
  no remnants left behind.
- Critical paths must have explicit error handling.

## Red Lines

- No copy-paste duplication.
- Do not proceed with a known-wrong approach.

## Security

- Never hardcode secrets (keys/passwords/tokens).
- Never commit `.env` files or any credentials.
- Validate user input at trust boundaries (APIs, CLIs, external data sources).

## Cleanup

- After changes, update related docs (`README.md`, `CLAUDE.md`, `AGENTS.md`, etc.).
- Remove temporary files and debug logging that is no longer needed.
