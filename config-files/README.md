# config-files

这里存放各 CLI 的基础配置参考文件，而不是 `agent-instructions/` 里的可拼装规则模块。

## Codex

- `codex/default.config.toml`：Codex 主配置参考模板，涵盖模型、provider、service tier、runtime 等基础设置；复制到 `~/.codex/` 后重命名为 `config.toml` 再按需调整
- `codex/README.md`：Codex 配置与 role resolution 机制说明
- `../sub-agents/codex/*.toml`：与 Codex 主配置配套的 sub-agent role layer
- `../sub-agents/codex/role-layer.example.toml`：sub-agent role layer 的实用示例

## Claude

- `claude/README.md`：Claude 配置说明
- `claude/example.settings.json`：Claude `settings.json` 参考模板
