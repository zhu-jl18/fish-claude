# Fish Claude

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

## 简介

这个仓库用于分享我本人各种 Coding CLI 的自定义规则模块、成品 profile、sub-agents、slash commands 和 skills 等，包括但不限于：

- Claude Code
- Codex
- OpenCode
- Gemini CLI
- Others

另外也包含少量维护/迁移脚本，主要用于清理或修复各类 CLI 的本地状态与历史数据。

## 目录结构

```text
.
├── memory/          # 规则模块（可拼装）
├── profile/         # 可直接复制使用的成品配置
├── mcp/             # MCP Server 安装配置指南
├── output-styles/   # AI 输出风格/人格预设
├── scripts/         # 维护/迁移脚本与说明
├── skills/          # Skills 定义
├── slash-commands/  # Slash Commands
└── sub-agents/      # Sub-Agents 配置（预留）
```

## 使用方法

1. 克隆仓库到本地
2. 根据需要选用 `memory/` 中的模块，或直接复制 `profile/` 下的成品配置
3. 将文件放置到对应 CLI 工具的配置目录
4. 根据个人需求调整配置

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT
