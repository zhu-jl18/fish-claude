# config-files

这里存放各 CLI 的基础配置参考文件。

## Oh My Pi

- `oh-my-pi/agent.config.yml`：OMP 全局 `config.yml` 参考副本；复制到 `~/.omp/agent/config.yml` 后按需调整
- `oh-my-pi/agent.models.yml`：OMP 全局 `models.yml` 参考副本；复制到 `~/.omp/agent/models.yml`，并自行填入真实 API Key
- `oh-my-pi/rules/rtk.md`：OMP 用户级 `rules/rtk.md` 参考副本；复制到 `~/.omp/agent/rules/rtk.md` 使用

> [!NOTE]
> 这不是 RTK 官方内建支持，而是基于 OMP 原生 rules 的本地适配


## Claude

- `claude/example.settings.json`：Claude `settings.json` 参考模板

## Codex

- `codex/default.config.toml`：Codex 主配置参考模板，涵盖模型、provider、service tier、runtime 等基础设置；复制到 `~/.codex/` 后重命名为 `config.toml` 再按需调整
- `../sub-agents/codex/*.toml`：Codex sub-agent role layer 的唯一模板来源；复制到 `~/.codex/agents/`
- `../sub-agents/codex/role-layer.example.toml`：sub-agent role layer 的实用示例

> [!TIP]
> `description` 是给 host agent 看的调度提示，应该短、清楚、偏职责边界；sub-agent 自己实际收到的 prompt 放在 role layer 的 `developer_instructions`

> [!NOTE]
> - `config.toml` 里的 `[agents.<role>]` 负责 role metadata：`description`、`config_file`、`nickname_candidates`
> - 同名 `[agents.<role>]` 会优先于 builtin role metadata；写了就会 shadow builtin 对应项
> - role layer 只覆写文件里实际写出的配置键；没写的继续继承父线程当前有效配置
> - spawn runtime 会重新写回 live `approval_policy`、`shell_environment_policy`、`sandbox` 和 `cwd`，这些通常不值得放进 role layer
> - 当前官方 builtin role 是 `default`、`explorer`、`worker`；`spark` 和 `awaiter` 是本地自定义 role
> - 当前参考模板显式开启 `features.multi_agent = true` 和 `features.multi_agent_v2 = true`，因为现阶段 Codex 仍用 `multi_agent` 作为 v2 工具面的前置门控
> - 如果要细调 v2 行为，可改成 `[features.multi_agent_v2]` table 并设置 `enabled`、`usage_hint_enabled`、`usage_hint_text`、`hide_spawn_agent_metadata`
