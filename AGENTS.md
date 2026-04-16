# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

## What This Repo Is

An **AI coding assistant configuration sharing repository** — NOT a business application.
Contains reusable rule fragments for project docs, baseline CLI config references, pack references, MCP setup guides, skills, and output styles for Claude Code, Codex, Gemini CLI, etc.

**There is no build system, no test suite, no `src/` directory.** Do not look for or create them.

## Architecture

### Composable Module System

Each `.md` file in `agent-instructions/general/`, `agent-instructions/claude/`, `agent-instructions/codex/`, and `agent-instructions/oh-my-pi/` is an **independent, composable rule fragment**. Users browse, pick what they need, and concatenate modules into their own global config:

```bash
# Claude Code
cat general/01-no-extra-notes.md claude/01-defaults.md claude/02-code-quality.md ... > CLAUDE.md

# Codex
cat general/01-no-extra-notes.md codex/01-basic-rules.md codex/02-text-editing-tool.md ... > AGENTS.md

# Oh My Pi
cat general/01-no-extra-notes.md oh-my-pi/01-defaults.md oh-my-pi/03-code-style.md ... > AGENTS.md
```

For Codex, `config.toml` provides a `developer_instructions` field as a high-priority override slot — modules that Codex follows poorly can be moved from `AGENTS.md` into `developer_instructions` for stronger enforcement.

Module details and dependency info are documented in `agent-instructions/README.md`. Baseline CLI config references live under `config-files/`.

### Directory Layout

| Directory                        | Purpose                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------------ |
| `agent-instructions/general/`    | Shared cross-CLI rule modules                                                              |
| `agent-instructions/claude/`     | Claude Code rule modules (composable fragments)                                            |
| `agent-instructions/codex/`      | Codex rule modules                                                                         |
| `agent-instructions/oh-my-pi/`   | Oh My Pi rule modules                                                                      |
| `config-files/`                  | Baseline CLI config references (`settings.json`, `config.toml`, etc.)                      |
| `system-prompts/`                | Upstream system prompt references                                                          |
| `mcp/`                           | MCP server installation & usage guides                                                     |
| `skills/`                        | Custom skill definitions                                                                   |
| `output-styles/`                 | Personality/style presets for AI output                                                    |
| `slash-commands/`                | Slash command prompt templates                                                             |
| `sub-agents/`                    | Sub-agent role layers and related examples                                                 |
| `packs/`                         | Composite packages (commands + skills + hooks + subagents) and external toolkit references |

## Rules for Editing This Repo

1. **Not a business code repo.** No builds, deploys, or `src/` assumptions.
2. **Do NOT rewrite rule fragments into tutorials or monolithic docs.**
3. **Do NOT force optional modules into default configurations.**
4. **Keep modules composable**: one file = one responsibility; edits must preserve copy-paste assembly.
5. **Minimal changes only**: small, focused edits scoped to the user's request; do not modify unrelated modules.
6. **If file structure changes**, update index docs (`agent-instructions/README.md`, `system-prompts/README.md`, `mcp/README.md`, `packs/README.md`).

# Git Commit Message Format

Use conventional commits format:

```
<type>(<scope>): <subject>
<body>
<footer>
```

<type> and <subject> are required; <body> and <footer> are optional.

## Local Repo Clones

If you are on my WSL2 environment:
- `codex`、`oh-my-pi`、`gemini-cli`、`rtk` → `~/01-workspace/`
- `code-dispatcher-toolkit` → `~/personal-workspace/`
