# Research (No Guessing)

If something is unfamiliar or version-sensitive, look it up — never guess.

## Library Docs

<important if="you need current docs for a library, framework, SDK, API, CLI tool, or cloud service">
- Use `Context7` (`resolve-library-id` → `query-docs`).
</important>

## General Web Search Priority

<important if="you need general web search or non-library information">
- Prefer the `grok-search` skill for general / non-library queries.
- If `grok-search` is unavailable or not usable, fall back to `exa` MCP when available.
- Use the built-in `Web Search` tool only as the last fallback.
</important>

## Version and Source Checks

<important if="behaviour may differ across versions">
- First identify the project's version (lockfile/config), then query docs for that version.
- Source priority: official docs > changelog > upstream repo > community posts.
</important>
