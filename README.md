<div align="center">

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

[English](README.en.md) | 中文

</div>

## 简介

这个仓库用于分享我本人各种 Coding CLI 的项目文档规则模块、基础配置参考、packs、sub-agents、slash commands 和 skills 等，包括但不限于：

- Claude Code
- Codex
- Gemini CLI
- Others

opencode is shit.

另外也包含少量维护/迁移工具，主要用于清理或修复各类 CLI 的本地状态与历史数据。

## 目录结构

```text
.
├── agent-instructions/ # 用于拼装 AGENTS.md / CLAUDE.md / GEMINI.md 的规则模块
├── config-files/       # settings.json / config.toml 等基础配置参考文件
├── system-prompts/     # 上游 system prompt 参考副本
├── mcp/             # MCP Server 安装配置指南
├── output-styles/   # AI 输出风格/人格预设
├── tools/           # 用户侧维护/迁移工具与说明
├── skills/          # Skills 定义
├── slash-commands/  # Slash Commands
├── sub-agents/      # Sub-Agent role layer 与示例
├── packs/           # 组合包与外部工具集参考
└── ai-services/     # 常与 AI 工作流配合使用的外部 API 服务参考
```

## 使用方法

1. 克隆仓库到本地
2. 从 `agent-instructions/` 中挑选模块，拼装你的 `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`
3. 参考 `config-files/` 中的 `settings.json` / `config.toml` 样例，填写模型、provider、认证和运行权限等基础设置
4. 将文件放置到对应 CLI 工具的配置目录，并按个人需求继续调整

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT
