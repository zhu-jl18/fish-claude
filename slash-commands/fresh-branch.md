---
description: 基于最新远程main分支创建并切换到新功能分支（默认名：from-main-to-dev）
argument-hint: [分支名称 或 功能描述]
allowed-tools: Bash, Read
---

分支名称由 `$ARGUMENTS` 决定：
- 未提供 → 默认 `from-main-to-dev`
- 已是合法分支名（如 `feature/new-api`）→ 直接使用
- 自然语言描述（如 "添加用户登录功能"）→ 推导为 `feat/user-login` 风格的分支名，创建前先告知用户

## 流程

1. `git status --porcelain` 检查工作树 — 如果有未提交更改，**停止并提示用户处理**，不要自作主张
2. `git fetch origin main`
3. `git checkout -b <分支名> origin/main` — 若分支已存在则停止并告知
4. 输出当前分支名和最新 commit 摘要作为确认
