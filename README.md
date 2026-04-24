<div align="center">
<img src="repo-logo.svg" alt="Fish Claude logo" width="180" />

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

[English](README.en.md) | 中文

</div>

## 简介

分享我本人在用的 Coding CLI 配置、规则模块、skills、sub-agents、patch 和参考文档等。

- Claude Code
- Codex
- Gemini CLI
- Oh My Pi
- Warp

不包括：
- 🚫 OpenCode：就是构史

## 目录结构

```text
.
├── agent-instructions/ # 拼装 AGENTS.md / CLAUDE.md / GEMINI.md 的规则模块
├── config-files/       # settings.json / config.toml 等基础配置参考
├── system-prompts/     # 上游 system prompt 参考副本
├── mcp/                # MCP Server 安装配置指南
├── output-styles/      # AI 输出风格/人格预设
├── tools/              # 维护/迁移工具
├── skills/             # Skills 定义
├── slash-commands/     # Slash Commands
├── sub-agents/         # Sub-Agent role layer 与示例
├── packs/              # 组合包与外部工具参考
├── preset-cards/       # 可复用 preset card / 人格预设
├── themes/             # Warp / Claude Code 主题参考
├── tips/               # 实用知识碎片
├── reports/            # 深度调研报告
└── ai-services/        # 外部 API 服务参考
```

## 使用方法

1. 克隆仓库到本地
2. 从 `agent-instructions/` 中挑选模块，拼装 `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`
3. 参考 `config-files/` 中的样例填写模型、provider、认证等基础设置
4. MCP、skill、pack 等同样放到对应 CLI 的配置目录，按需调整

## 贡献

欢迎提交 Issue；如需提交 Pull Request，请先沟通并获得许可。

## 许可证

MIT
