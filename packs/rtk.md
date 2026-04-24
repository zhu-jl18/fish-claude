# rtk

Token 优化 CLI 代理——把高噪声 shell 输出压缩成 LLM 友好格式。

## 来源

- GitHub：<https://github.com/rtk-ai/rtk>

## 是什么

`rtk <command>` 替代原始命令，自动过滤冗余输出。`git status`、`cargo test`、`pytest` 这类动辄几十上百行的结果，rtk 只留关键信息，省 60-90% token。

## 各 CLI 支持

- **Claude Code**：官方支持。`rtk init -g` 写入全局 `CLAUDE.md`，PreToolUse hook 自动代理 Bash 命令
- **Codex**：官方支持。`rtk init --codex` 写入 `RTK.md` 并 `@RTK.md` 接入 `AGENTS.md`
- **OMP**：上游尚未支持。已提 [PR #1365](https://github.com/rtk-ai/rtk/pull/1365)（extension-based rewrite），本地在用，等待合并
