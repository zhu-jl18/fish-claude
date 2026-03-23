# code-dispatcher-toolkit

外部工具参考页。

## 来源

- GitHub: `makoMakoGo/code-dispatcher-toolkit`
- URL: <https://github.com/makoMakoGo/code-dispatcher-toolkit>

## 简介

- 一个基于 `code-dispatcher` CLI 的多后端 AI 编码工具集，核心方向是统一任务分发、并行执行和结果回收
- 仓库同时提供执行器、编排 skill、prompt 模板、安装脚本和配套文档
- 面向 `codex`、`claude`、`gemini` 三类后端，统一通过 `code-dispatcher` 入口调度

## 适合场景

- 需要统一调度 `codex`、`claude`、`gemini` 等多个 coding backend
- 需要 `--parallel`、`--resume` 这类围绕调度器本体的工作流能力
- 需要把执行器、prompt 模板、安装脚本和 skill 放在同一个仓库里维护

## 关注内容

- `dev`、`code-council`、`github-issue-pr-flow`、`pr-review-reply` 等 workflow skill
- `install.py`、`uninstall.py`、`prompts/`、`skills/` 这些安装与运行时资产


