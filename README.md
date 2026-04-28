<div align="center">
<img src="repo-logo.svg" alt="Fish Claude logo" width="180" />

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

可复制、可拼装、可按需安装的 AI coding CLI 配置素材库。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

<br>

<img src="https://img.shields.io/badge/Claude_Code-D4A27F?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code">
<img src="https://custom-icon-badges.demolab.com/badge/Codex-412991?style=flat-square&logo=openai&logoColor=white" alt="Codex">
<img src="https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini CLI">
<img src="https://img.shields.io/badge/Oh_My_Pi-333333?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4gPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4MDAgODAwIj4gPHBhdGggZmlsbD0iJTIzMDBENEFBIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9IiBNMTY1LjI5IDE2NS4yOSBINTE3LjM2IFY0MDAgSDQwMCBWNTE3LjM2IEgyODIuNjUgVjYzNC43MiBIMTY1LjI5IFogTTI4Mi42NSAyODIuNjUgVjQwMCBINDAwIFYyODIuNjUgWiAiLz4gPHBhdGggZmlsbD0iJTIzMDBENEFBIiBkPSJNNTE3LjM2IDQwMCBINjM0LjcyIFY2MzQuNzIgSDUxNy4zNiBaIi8+IDwvc3ZnPg==&logoColor=white" alt="Oh My Pi">
<img src="https://img.shields.io/badge/Warp-01A1FF?style=flat-square&logo=warp&logoColor=white" alt="Warp">

<br>

中文 | [English](README.en.md)

</div>

## 这是什么

这是我本人在用的 Coding CLI 配置素材库：规则模块、skills、sub-agents、patches、MCP/config 参考、主题和调研笔记。它不是教程合集，也不是通用框架；更像一个可以抄、可以拼、可以拆的个人工作台。

覆盖：

- Claude Code
- Codex
- Gemini CLI
- Oh My Pi
- Warp

## 可以直接拿什么

| 内容 | 入口 | 用途 |
| --- | --- | --- |
| 规则模块 | [`agent-instructions/`](agent-instructions/) | 拼装 `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` 的 composable fragments |
| Skills | [`skills/`](skills/) | 可安装到 Claude Code / Codex / OMP / Gemini CLI 的 skill 定义与参考 |
| 配置样例 | [`config-files/`](config-files/) | `settings.json`、`config.toml`、OMP agent config 等基础配置参考 |
| MCP 指南 | [`mcp/`](mcp/) | 常用 MCP server 的安装、配置和使用说明 |
| Packs | [`packs/`](packs/) | 组合包、外部工具链和可复用安装参考 |
| Tools / patches | [`tools/`](tools/) | 本地维护工具、迁移脚本、OMP patch runner |
| 输出风格与主题 | [`output-styles/`](output-styles/) / [`preset-cards/`](preset-cards/) / [`themes/`](themes/) | 输出人格、preset card、Warp / Claude Code 主题 |
| Sub-agents 与命令 | [`sub-agents/`](sub-agents/) / [`slash-commands/`](slash-commands/) | 子 agent role layer 和 slash command 模板 |
| Tips / reports / services | [`tips/`](tips/) / [`reports/`](reports/) / [`ai-services/`](ai-services/) | 实用知识碎片、调研报告和外部 API 服务参考 |

## 从哪里开始

- [规则模块索引](agent-instructions/README.md)：了解各 CLI 的 instruction fragments 怎么组合。
- [Skills 指南](skills/README.md)：查看可安装的 community / custom skills。
- [配置文件参考](config-files/README.md)：复制基础 CLI 配置样例。
- [MCP 配置](mcp/README.md)：按需接入 MCP server。
- [Packs](packs/README.md)：查看组合包和外部工具链入口。
- [Tools](tools/README.md)：使用维护工具、迁移脚本和 patch runner。
- [System prompts](system-prompts/README.md)：查看上游 system prompt 参考副本。

## 贡献

欢迎提交 Issue；如需提交 Pull Request，请先沟通并获得许可。

## 许可证

MIT
