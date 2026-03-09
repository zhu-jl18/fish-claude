# codex config

- `default.config.toml`：Codex 主配置参考模板，承载模型、provider、service tier、runtime 等基础设置；复制到 `~/.codex/` 后重命名为 `config.toml` 再按需修改
- `../../sub-agents/codex/*.toml`：与主配置配套的 sub-agent role layer
- `../../sub-agents/codex/role-layer.example.toml`：最小实用的 sub-agent role layer 示例

## Role Resolution

- `config.toml` 里的 `[agents.<role>]` 负责 role metadata：`description`、`config_file`、`nickname_candidates`
- 同名 `[agents.<role>]` 会优先于 builtin role metadata；写了就会 shadow builtin 对应项
- `agents/*.toml` 是 role layer，只覆写文件里实际写出的配置键；没写的继续继承父线程当前有效配置
- spawn runtime 会重新写回 live `approval_policy`、`shell_environment_policy`、`sandbox` 和 `cwd`，这些通常不值得放进 role layer

## Builtin Roles

- 当前 Codex 0.112.0 默认 builtin role 是 `default`、`explorer`、`worker`
- `awaiter` 不是当前默认 builtin role；这里是本地补出来的自定义 role
- 如果自定义了同名 role，官方 builtin 的 metadata 和 builtin role layer 都不会再自动生效
