<div align="center">
<img src="repo-logo.svg" alt="Fish Claude logo" width="180" />

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

A copyable, composable, install-what-you-need resource kit for AI coding CLIs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

<br>

<img src="https://img.shields.io/badge/Claude_Code-D4A27F?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code">
<img src="https://custom-icon-badges.demolab.com/badge/Codex-412991?style=flat-square&logo=openai&logoColor=white" alt="Codex">
<img src="https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini CLI">
<img src="https://img.shields.io/badge/Oh_My_Pi-333333?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4gPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4MDAgODAwIj4gPHBhdGggZmlsbD0iJTIzMDBENEFBIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9IiBNMTY1LjI5IDE2NS4yOSBINTE3LjM2IFY0MDAgSDQwMCBWNTE3LjM2IEgyODIuNjUgVjYzNC43MiBIMTY1LjI5IFogTTI4Mi42NSAyODIuNjUgVjQwMCBINDAwIFYyODIuNjUgWiAiLz4gPHBhdGggZmlsbD0iJTIzMDBENEFBIiBkPSJNNTE3LjM2IDQwMCBINjM0LjcyIFY2MzQuNzIgSDUxNy4zNiBaIi8+IDwvc3ZnPg==&logoColor=white" alt="Oh My Pi">
<img src="https://img.shields.io/badge/Warp-01A1FF?style=flat-square&logo=warp&logoColor=white" alt="Warp">

<br>

[中文](README.md) | English

</div>

## What This Is

My personal Coding CLI config resource kit: rule modules, skills, sub-agents, patches, MCP/config references, themes, and research notes. It is not a tutorial collection or a generic framework; it is a personal workbench you can copy from, assemble, and take apart.

Covers:

- Claude Code
- Codex
- Gemini CLI
- Oh My Pi
- Warp

## What You Can Steal

| Content | Entry | Use |
| --- | --- | --- |
| Rule modules | [`agent-instructions/`](agent-instructions/) | Composable fragments for assembling `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` |
| Skills | [`skills/`](skills/) | Skill definitions and references installable in Claude Code / Codex / OMP / Gemini CLI |
| Config samples | [`config-files/`](config-files/) | Baseline config references for `settings.json`, `config.toml`, OMP agent config, and more |
| MCP guides | [`mcp/`](mcp/) | Installation, configuration, and usage notes for common MCP servers |
| Packs | [`packs/`](packs/) | Composite bundles, external toolchains, and reusable install references |
| Tools / patches | [`tools/`](tools/) | Local maintenance tools, migration scripts, and OMP patch runners |
| Output styles and themes | [`output-styles/`](output-styles/) / [`preset-cards/`](preset-cards/) / [`themes/`](themes/) | Output personas, preset cards, and Warp / Claude Code themes |
| Sub-agents and commands | [`sub-agents/`](sub-agents/) / [`slash-commands/`](slash-commands/) | Sub-agent role layers and slash command templates |
| Tips / reports / services | [`tips/`](tips/) / [`reports/`](reports/) / [`ai-services/`](ai-services/) | Practical notes, research reports, and external API service references |

## Start Here

- [Rule module index](agent-instructions/README.md): see how instruction fragments are assembled for each CLI.
- [Skills guide](skills/README.md): browse installable community and custom skills.
- [Config file references](config-files/README.md): copy baseline CLI config samples.
- [MCP setup](mcp/README.md): connect MCP servers as needed.
- [Packs](packs/README.md): find composite bundles and external toolchain entries.
- [Tools](tools/README.md): use maintenance tools, migration scripts, and patch runners.
- [System prompts](system-prompts/README.md): inspect upstream system prompt reference copies.

## Contributing

Issues are welcome. Please discuss and get permission before opening a Pull Request.

## License

MIT
