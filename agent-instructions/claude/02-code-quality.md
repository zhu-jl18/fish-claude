# Code Quality

## Change Scope

- Prefer clean rewrites over incremental patches when modifying a cohesive unit.
- For targeted fixes (single bug, small feature), change only what's necessary — but leave no dead code or orphaned remnants behind.

## Error Handling

<important if="you are modifying critical paths, failure behavior, or retry logic">
- Critical paths must have explicit error handling.
</important>

## Red Lines

- No copy-paste duplication.
- Do not proceed with a known-wrong approach.

## Security

- Never hardcode secrets (keys/passwords/tokens).
- Never commit `.env` files or any credentials.

<important if="you are handling user input, APIs, CLIs, or external data sources">
- Validate user input at trust boundaries (APIs, CLIs, external data sources).
</important>

## Cleanup

- After changes, update related docs (`README.md`, `CLAUDE.md`, `AGENTS.md`, etc.).
- Remove temporary files and debug logging that is no longer needed.
