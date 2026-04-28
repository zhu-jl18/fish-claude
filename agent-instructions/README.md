# agent-instructions

不同的 CLI 内置的工具不同，适合的模型不同，适配的 MCP 也不同，因此需要差异化对待。因此本部分被拆分成 **独立、可自由组合**的模块——按需选取后拼接为全局的 `AGENTS.md` 等。

## 全局提示词存储位置

| CLI         | 全局文件路径                   |
| ----------- | ------------------------------ |
| OMP         | `~/.omp/agent/AGENTS.md`       |
| Claude Code | `~/.claude/CLAUDE.md`          |
| Codex       | `~/.codex/AGENTS.md`           |
| Gemini CLI  | `~/.gemini/GEMINI.md`          |
| Warp        | Warp Drive（云端，App 内 Personal → Rules，或 `/add-rule`） |


## General

| #   | 模块                                         | 职责                                    | 依赖     |
| --- | -------------------------------------------- | --------------------------------------- | -------- |
| 01  | [no-extra-notes](general/01-no-extra-notes.md)   | 禁止在文档主结构外多嘴补注释或说明 | — |
| 02  | [environment](general/02-environment.md)         | Windows + WSL2 环境模板（Python / Go / Rust / Git） | 本机环境可选模块 |
| 03  | [git-commit-push](general/03-git-commit-push.md) | Git 提交 / push / commit message 通用规则 | — |
| 04  | [reply-style](general/04-reply-style.md)         | 回答风格（简洁直接、反模板化）            | — |


## Claude Code

| #   | 模块                                          | 职责                                   | 依赖                                                              |
| --- | --------------------------------------------- | -------------------------------------- | ----------------------------------------------------------------- |
| 01  | [defaults](claude/01-defaults.md)             | 交互默认行为（语言、格式、先读后写）   | —                                                                 |
| 02  | [code-quality](claude/02-code-quality.md)     | 代码质量标准、红线、安全、清理         | —                                                                 |
| 03  | [research](claude/03-research.md)             | 查资料方法论（禁止猜测）               | [Context7](../mcp/context7.md), [Grok Search](../skills/grok-search.md) |
| 04  | [priority-stack](claude/04-priority-stack.md) | 优先级堆栈（最高级行为约束）           | —                                                                 |
| 05  | [dev-workflow](claude/05-dev-workflow.md)     | code-dispatcher 开发工作流（按需启用） | [code-dispatcher-toolkit](../packs/code-dispatcher-toolkit.md) |
| 06  | [playwright](claude/06-playwright.md)         | Playwright UI 验证规则（按需启用）     | [Playwright](../mcp/playwright.md)                                |
| 07  | [agent-teams](claude/07-agent-teams.md)       | Agent Teams 使用规范（按需启用）       | —                                                                 |



## Codex

| #   | 模块                                               | 职责                                     | 依赖                                                            |
| --- | -------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------- |
| 01  | [basic-rules](codex/01-basic-rules.md)             | 通用行为准则（语言、输出风格、沟通方式） | —                                                               |
| 02  | [inherited-tool](codex/02-inherited-tool.md)       | 工具优先级与并行编排                     | —                                                               |
| 03  | [role-play-sm](codex/03-role-play-sm.md)           | 角色扮演人设                             | —                                                               |
| 04  | [debug-first](codex/04-debug-first.md)             | 调试策略（禁止静默兜底）                 | —                                                               |
| 05  | [multi-agent](codex/05-multi-agent.md)             | 多智能体协作规范                         | 默认开启；显式配置见 [default.config.toml](../config-files/codex/default.config.toml) |
| 06  | [no-compat](codex/06-no-compat.md)                 | 禁止向后兼容（优先干净架构）             | —                                                               |




## Oh My Pi

| #   | 模块                                          | 职责                                         | 依赖     |
| --- | --------------------------------------------- | -------------------------------------------- | -------- |
| 01  | [defaults](oh-my-pi/01-defaults.md)           | 交互默认行为（语言、风格、直接执行）         | —        |
| 02  | [code-style](oh-my-pi/02-code-style.md)       | 代码风格（函数式、KISS、DRY）                | [ai-coding-discipline](../skills/ai-coding-discipline.md)        |
| 03  | [architecture](oh-my-pi/03-architecture.md)   | 架构与设计原则（第一性原理、反 XY）          | [software-design-philosophy](../skills/software-design-philosophy.md)        |

## Gemini

| #   | 模块                                         | 职责                                      | 依赖 |
| --- | -------------------------------------------- | ----------------------------------------- | ---- |
| 01  | [reasoning-depth](gemini/01-reasoning-depth.md) | Gemini 深度推理 prompt hack（`EFFORT LEVEL`） | — |

## _archived

| 文件                                                         | 归档原因                                       |
| ------------------------------------------------------------ | ---------------------------------------------- |
| [text-editing-tool](_archived/text-editing-tool.md) | Codex 已很少出现 apply_patch 调用错误，不再需要 |
| [serena](_archived/serena.md) | Serena MCP 当前很少使用了 |
