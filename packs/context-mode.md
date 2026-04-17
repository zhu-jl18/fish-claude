# context-mode

外部工具参考页。

## 来源

- GitHub: `mksglu/context-mode`
- URL: <https://github.com/mksglu/context-mode>

## 简介

- Claude Code 插件 + MCP server，解决「MCP/CLI 原始输出淹没 context window」问题
- 核心做法：把大块原始输出（Playwright snapshot、日志、git log、API 响应等）留在 sandbox，仅把摘要/检索结果送回 context
- 官方口径：315 KB → 5.4 KB 量级（~98% 压缩），同时提供 session continuity（SQLite + FTS5/BM25）
- 倡导 "Think in Code"：让 LLM 生成脚本处理数据，不要把原始数据拉进 context 里心算

## 关键能力

- `ctx_batch_execute` / `ctx_execute` / `ctx_execute_file`：sandbox 内执行 shell/JS/TS/Python 等，自动索引输出
- `ctx_search`：对已索引内容做 BM25 检索
- `ctx_fetch_and_index`：替代 `WebFetch`，HTML→markdown 后索引
- `ctx_stats` / `ctx_doctor` / `ctx_insight`：用量统计与诊断

## 当前支持现状

- Claude Code：官方支持，走 plugin marketplace 安装
- 其他 CLI：README 声称覆盖 12 platforms，以上游为准

## 安装

以 Claude Code plugin marketplace 方式安装即可，本仓库不再镜像其安装脚本。

## 与本仓库的关系

- 纯外部工具参考页，不在 `mcp/` 下重复写接入指南
- 如果项目里需要硬性约束「大输出必须走 sandbox」，可在 `agent-instructions/claude/` 新增规则片段引用本页
