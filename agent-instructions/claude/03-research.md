# Research (No Guessing)

If something is unfamiliar or version-sensitive, look it up — never guess.

- **Library docs**: Use `Context7` (`resolve-library-id` → `query-docs`).

## General Web Search Priority

- Prefer the `grok-search` skill for general / non-library queries.
- If `grok-search` is unavailable or not usable, fall back to `exa` MCP when available.
- Use the built-in `Web Search` tool only as the last fallback.

## Version and Source Checks

- When behaviour may differ across versions,
  first identify the project's version (lockfile/config),
  then query docs for that version.
- Source priority: official docs > changelog > upstream repo > community posts.
