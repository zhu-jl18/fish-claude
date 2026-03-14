# config-files

这里存放各 CLI 的基础配置参考文件。

## Claude

- `claude/example.settings.json`：Claude `settings.json` 参考模板

## Codex

- `codex/default.config.toml`：Codex 主配置参考模板，涵盖模型、provider、service tier、runtime 等基础设置；复制到 `~/.codex/` 后重命名为 `config.toml` 再按需调整
- `../sub-agents/codex/*.toml`：与 Codex 主配置配套的 sub-agent role layer
- `../sub-agents/codex/role-layer.example.toml`：sub-agent role layer 的实用示例
- `config.toml` 里的 `[agents.<role>]` 负责 role metadata：`description`、`config_file`、`nickname_candidates`
- 同名 `[agents.<role>]` 会优先于 builtin role metadata；写了就会 shadow builtin 对应项
- role layer 只覆写文件里实际写出的配置键；没写的继续继承父线程当前有效配置
- spawn runtime 会重新写回 live `approval_policy`、`shell_environment_policy`、`sandbox` 和 `cwd`，这些通常不值得放进 role layer
- 当前 Codex 0.112.0 默认 builtin role 是 `default`、`explorer`、`worker`
- `awaiter` 在这里是本地自定义 role，不是当前默认 builtin role
