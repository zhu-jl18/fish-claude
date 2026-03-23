# config-files

这里存放各 CLI 的基础配置参考文件。

## Claude

- `claude/example.settings.json`：Claude `settings.json` 参考模板

## Codex

- `codex/default.config.toml`：Codex 主配置参考模板，涵盖模型、provider、service tier、runtime 等基础设置；复制到 `~/.codex/` 后重命名为 `config.toml` 再按需调整
- `../sub-agents/codex/*.toml`：Codex sub-agent role layer 的唯一模板来源；复制到 `~/.codex/agents/`
- `../sub-agents/codex/role-layer.example.toml`：sub-agent role layer 的实用示例
- 如果不希望子 agent 带入主线程 roleplay/persona，优先在 `agents/*.toml` 里用中性的 `developer_instructions` 覆盖，而不是试图靠 `AGENTS.md` 做 per-agent 隔离
- `config.toml` 里的 `[agents.<role>]` 负责 role metadata：`description`、`config_file`、`nickname_candidates`
- `description` 是给 host agent 看的调度提示，应该短、清楚、偏职责边界；sub-agent 自己实际收到的 prompt 放在 role layer 的 `developer_instructions`
- 同名 `[agents.<role>]` 会优先于 builtin role metadata；写了就会 shadow builtin 对应项
- role layer 只覆写文件里实际写出的配置键；没写的继续继承父线程当前有效配置
- spawn runtime 会重新写回 live `approval_policy`、`shell_environment_policy`、`sandbox` 和 `cwd`，这些通常不值得放进 role layer
- multi-agent 当前是 stable 且默认开启；`features.multi_agent = true` 写出来主要是为了显式化
- 当前官方 builtin role 是 `default`、`explorer`、`worker`
- `spark` 和 `awaiter` 在这里是本地自定义 role，不是当前默认 builtin role
