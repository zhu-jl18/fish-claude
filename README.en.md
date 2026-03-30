<div align="center">

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

English | [中文](README.md)

</div>

## Introduction

This repository shares my personal rule modules, baseline config references, packs, sub-agents, slash commands, and skills for various coding CLIs, including but not limited to:

- Claude Code
- Codex
- Gemini CLI
- Others

opencode is shit.

It also includes a small set of maintenance/migration tools, primarily for cleaning up or repairing local state and history data across these CLIs.

## Directory Structure

```text
.
├── agent-instructions/ # Rule modules for assembling AGENTS.md / CLAUDE.md / GEMINI.md
├── config-files/       # Baseline config references: settings.json / config.toml, etc.
├── system-prompts/     # Upstream system prompt reference copies
├── mcp/             # MCP Server installation and configuration guides
├── output-styles/   # AI output style / personality presets
├── tools/           # User-side maintenance / migration tools and docs
├── skills/          # Skill definitions
├── slash-commands/  # Slash Commands
├── sub-agents/      # Sub-Agent role layers and examples
├── packs/           # Composite packages and external toolkit references
└── ai-services/     # External API service references commonly used with AI workflows
```

## Usage

1. Clone the repository locally
2. Pick modules from `agent-instructions/` and assemble your `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`
3. Refer to the `settings.json` / `config.toml` samples in `config-files/` to fill in model, provider, auth, and permission settings
4. Place the files in the config directory of the corresponding CLI tool and adjust as needed

## Contributing

Issues and Pull Requests are welcome.

## License

MIT
