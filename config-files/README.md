# config-files

各 CLI 的基础配置参考。

## Oh My Pi

| 文件 | 目标路径 |
|------|---------|
| `oh-my-pi/agent.config.yml` | `~/.omp/agent/config.yml` |
| `oh-my-pi/agent.models.yml` | `~/.omp/agent/models.yml` |

## Claude Code

| 文件 | 目标路径 |
|------|---------|
| `claude/example.settings.json` | `~/.claude/settings.json` |

## Codex

| 文件 | 目标路径 |
|------|---------|
| `codex/default.config.toml` | `~/.codex/config.toml` |
| `../sub-agents/codex/*.toml` | `~/.codex/agents/` |
| `../sub-agents/codex/role-layer.example.toml` | 写法示例 |

- `description` 是给 host agent 的调度提示，短、清楚、偏职责边界；sub-agent 实际 prompt 在 `developer_instructions`
- `[agents.<role>]` 同名 shadow builtin；role layer 只覆写实际写出的键，其余继承父线程
- spawn runtime 会重写 `approval_policy`、`shell_environment_policy`、`sandbox`、`cwd`，这些不用放进 role layer
