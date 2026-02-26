# AGENTS.md

不同的 CLI 内置的工具不同，适合的模型不同，适配的 MCP 也不同，因此需要差异化对待。

## Claude Code

以下模块**独立、可自由组合**——按需选取后拼接为项目的 `CLAUDE.md`。

### 模块清单

| # | 模块 | 职责 | 依赖 |
|---|------|------|------|
| 01 | [defaults](claude/01-defaults.md) | 交互默认行为（语言、格式、先读后写） | — |
| 02 | [code-quality](claude/02-code-quality.md) | 代码质量标准、红线、安全、清理 | — |
| 03 | [research](claude/03-research.md) | 查资料方法论（禁止猜测） | [Context7](mcp/context7.md) |
| 04 | [git](claude/04-git.md) | Git 工作流、提交规范、账号身份 | `gh` CLI |
| 05 | [environment](claude/05-environment.md) | OS / Shell / Python 环境配置 | — |
| 06 | [priority-stack](claude/06-priority-stack.md) | 优先级堆栈（最高级行为约束） | — |
| 07 | [dev-workflow](claude/07-dev-workflow.md) | code-dispatcher 开发工作流（按需启用） | code-dispatcher skill |
| 08 | [serena](claude/08-serena.md) | Serena MCP 语义检索规则（按需启用） | [Serena](mcp/serena.md) |
| 09 | [playwright](claude/09-playwright.md) | Playwright UI 验证规则（按需启用） | Playwright |

### 组合示例

```bash
# 通用开发（推荐基线）
cat claude/01-defaults.md claude/02-code-quality.md claude/03-research.md \
    claude/04-git.md claude/05-environment.md claude/06-priority-stack.md \
    > CLAUDE.md

# 追加 Serena 支持
cat claude/08-serena.md >> CLAUDE.md

# 追加 Playwright 验证
cat claude/09-playwright.md >> CLAUDE.md
```

MCP 安装配置见 [mcp/](mcp/)。

## Codex

## Gemini
