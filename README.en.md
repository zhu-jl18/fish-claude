<div align="center">
<img src="repo-logo.svg" alt="Fish Claude logo" width="180" />

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

English | [中文](README.md)

</div>

## Introduction

My personal Coding CLI configs, rule modules, skills, sub-agents, patches, reference docs, and more.

- Claude Code
- Codex
- Gemini CLI
- Oh My Pi
- Warp

But not:
- 🚫 OpenCode — basically dogwater

## Directory Structure

```text
.
├── agent-instructions/ # Rule modules for AGENTS.md / CLAUDE.md / GEMINI.md
├── config-files/       # Baseline config references: settings.json / config.toml
├── system-prompts/     # Upstream system prompt reference copies
├── mcp/                # MCP Server installation and configuration guides
├── output-styles/      # AI output style / personality presets
├── tools/              # Maintenance / migration tools
├── skills/             # Skill definitions
├── slash-commands/     # Slash Commands
├── sub-agents/         # Sub-Agent role layers and examples
├── packs/              # Composite packages and external toolkit references
├── preset-cards/       # Reusable preset cards / persona presets
├── themes/             # Warp / Claude Code theme references
├── tips/               # Practical knowledge fragments
├── reports/            # Deep-dive research reports
└── ai-services/        # External API service references
```

## Usage

1. Clone the repository
2. Pick modules from `agent-instructions/` and assemble `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`
3. Reference `config-files/` samples to fill in model, provider, auth, etc.
4. Place MCP configs, skills, packs, etc. in the corresponding CLI directories and adjust as needed

## Contributing

Issues are welcome. Please discuss and get permission before opening a Pull Request.

## License

MIT
