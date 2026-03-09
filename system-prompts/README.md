# system-prompts

## Codex CLI

- file: `codex-cli.md`
- source remote: `https://github.com/openai/codex.git`
- local mirror: `X:\Toys\codex`
- source prompt path: `codex-rs/core/prompt.md`
- synced date: `2026-03-09`
- note: Codex CLI currently uses a mostly static primary system prompt file, so this copy is close to a direct source sync

## Gemini CLI

- file: `gemini-cli.md`
- source remote: `https://github.com/google-gemini/gemini-cli.git`
- local mirror: `X:\Toys\gemini-cli`
- source commit: `ca7ac0003`
- source prompt path: `packages/core/src/prompts/snippets.ts`
- synced date: `2026-03-09`
- note: Gemini CLI does not use one static system prompt file like Codex
- note: Gemini CLI composes the final prompt dynamically from `snippets.ts`
- note: `gemini-cli.md` records the Gemini 3 / modern / interactive baseline plus the major conditional sections injected at runtime
