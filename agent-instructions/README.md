# agent-instructions

不同的 CLI 内置的工具不同，适合的模型不同，适配的 MCP 也不同，因此需要差异化对待。因此本部分被拆分成 **独立、可自由组合**的模块——按需选取后拼接为全局的 `AGENTS.md` 等。

## 全局提示词存储位置

| CLI         | 全局文件路径                   |
| ----------- | ------------------------------ |
| Claude Code | `~/.claude/CLAUDE.md`          |
| Codex       | `~/.codex/AGENTS.md`           |
| Gemini CLI  | `~/.gemini/GEMINI.md`          |
| AmpCode     | `~/.config/amp/AGENTS.md`      |

## Claude Code

| #   | 模块                                          | 职责                                   | 依赖                                                              |
| --- | --------------------------------------------- | -------------------------------------- | ----------------------------------------------------------------- |
| 01  | [defaults](claude/01-defaults.md)             | 交互默认行为（语言、格式、先读后写）   | —                                                                 |
| 02  | [code-quality](claude/02-code-quality.md)     | 代码质量标准、红线、安全、清理         | —                                                                 |
| 03  | [research](claude/03-research.md)             | 查资料方法论（禁止猜测）               | [Context7](../mcp/context7.md)                                    |
| 04  | [git](claude/04-git.md)                       | Git 工作流、提交规范、账号身份         | `gh` CLI                                                          |
| 05  | [environment](claude/05-environment.md)       | OS / Shell / Python 环境配置           | —                                                                 |
| 06  | [priority-stack](claude/06-priority-stack.md) | 优先级堆栈（最高级行为约束）           | —                                                                 |
| 07  | [dev-workflow](claude/07-dev-workflow.md)     | code-dispatcher 开发工作流（按需启用） | [code-dispatcher-toolkit](../packs/code-dispatcher-toolkit.md) |
| 08  | [serena](claude/08-serena.md)                 | Serena MCP 语义检索规则（按需启用）    | [Serena](../mcp/serena.md)                                        |
| 09  | [playwright](claude/09-playwright.md)         | Playwright UI 验证规则（按需启用）     | [Playwright](../mcp/playwright.md)                                |
| 10  | [agent-teams](claude/10-agent-teams.md)       | Agent Teams 使用规范（按需启用）       | —                                                                 |



## Codex

| #   | 模块                                               | 职责                                     | 依赖                                                            |
| --- | -------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------- |
| 01  | [basic-rules](codex/01-basic-rules.md)             | 通用行为准则（语言、输出风格、沟通方式） | —                                                               |
| 02  | [text-editing-tool](codex/02-text-editing-tool.md) | 内置编辑工具指导                         | —                                                               |
| 03  | [inherited-tool](codex/03-inherited-tool.md)       | 工具优先级与并行编排                     | —                                                               |
| 04  | [role-play-sm](codex/04-role-play-sm.md)           | 角色扮演人设                             | —                                                               |
| 05  | [debug-first](codex/05-debug-first.md)             | 调试策略（禁止静默兜底）                 | —                                                               |
| 06  | [multi-agent](codex/06-multi-agent.md)             | 多智能体协作规范                         | 默认开启；显式配置见 [default.config.toml](../config-files/codex/default.config.toml) |
| 07  | [no-compat](codex/07-no-compat.md)                 | 禁止向后兼容（优先干净架构）             | —                                                               |

## Gemini
