# agent-instructions

不同的 CLI 内置的工具不同，适合的模型不同，适配的 MCP 也不同，因此需要差异化对待。

## 全局提示词（全局记忆）存储位置

| CLI         | 全局文件路径                       |
| ----------- | ---------------------------------- |
| Claude Code | `~/.claude/CLAUDE.md`              |
| Codex       | `~/.codex/AGENTS.md`               |
| Gemini CLI  | `~/.gemini/GEMINI.md`              |
| OpenCode    | `~/.config/opencode/AGENTS.md`     |
| AmpCode     | `~/.config/amp/AGENTS.md`          |

## Claude Code

以下模块**独立、可自由组合**——按需选取后拼接为项目的 `CLAUDE.md`。

### 模块清单

| #   | 模块                                          | 职责                                   | 依赖                           |
| --- | --------------------------------------------- | -------------------------------------- | ------------------------------ |
| 01  | [defaults](claude/01-defaults.md)             | 交互默认行为（语言、格式、先读后写）   | —                              |
| 02  | [code-quality](claude/02-code-quality.md)     | 代码质量标准、红线、安全、清理         | —                              |
| 03  | [research](claude/03-research.md)             | 查资料方法论（禁止猜测）               | [Context7](../mcp/context7.md) |
| 04  | [git](claude/04-git.md)                       | Git 工作流、提交规范、账号身份         | `gh` CLI                       |
| 05  | [environment](claude/05-environment.md)       | OS / Shell / Python 环境配置           | —                              |
| 06  | [priority-stack](claude/06-priority-stack.md) | 优先级堆栈（最高级行为约束）           | —                              |
| 07  | [dev-workflow](claude/07-dev-workflow.md)     | code-dispatcher 开发工作流（按需启用） | code-dispatcher skill          |
| 08  | [serena](claude/08-serena.md)                 | Serena MCP 语义检索规则（按需启用）    | [Serena](../mcp/serena.md)     |
| 09  | [playwright](claude/09-playwright.md)         | Playwright UI 验证规则（按需启用）     | Playwright                     |



## Codex

以下模块**独立、可自由组合**——按需选取后拼接为项目的 `AGENTS.md`。

配合 `config.toml` 使用：`developer_instructions` 默认留空，哪条规则遵循不佳就从 `AGENTS.md` 剪切到 `developer_instructions` 中加强。基础配置可参考 [`../config-files/codex/default.config.toml`](../config-files/codex/default.config.toml)，配套的 sub-agent role layer 在 [`../sub-agents/codex/*.toml`](../sub-agents/codex/) 。`agent-instructions/codex/` 只存放可拼装规则模块；模型、provider、认证、运行权限等基础配置参考统一放在 `config-files/`。

Codex 自定义 provider 建议使用稳定 key，例如 `custom`；如果频繁改 `model_provider` 的 key，历史会按 provider 分桶，默认 chat history / resume / fork 会看不到旧会话。需要归并旧 bucket 时，可用 `scripts/migrate_codex_provider_history.py`。

### 模块清单

| #   | 模块                                               | 职责                                     | 依赖              |
| --- | -------------------------------------------------- | ---------------------------------------- | ----------------- |
| 01  | [basic-rules](codex/01-basic-rules.md)             | 通用行为准则（语言、输出风格、沟通方式） | —                 |
| 02  | [text-editing-tool](codex/02-text-editing-tool.md) | apply_patch 工具使用规范                 | Codex CLI         |
| 03  | [inherited-tool](codex/03-inherited-tool.md)       | 工具优先级与并行编排                     | —                 |
| 04  | [role-play-sm](codex/04-role-play-sm.md)           | 角色扮演人设                             | —                 |
| 05  | [debug-first](codex/05-debug-first.md)             | 调试策略（禁止静默兜底）                 | —                 |
| 06  | [multi-agent](codex/06-multi-agent.md)             | 多智能体协作规范                         | Codex multi-agent |
| 07  | [no-compat](codex/07-no-compat.md)                 | 禁止向后兼容（优先干净架构）             | —                 |

## Gemini
