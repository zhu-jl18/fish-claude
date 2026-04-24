# codex-provider-history-migrator

## 问题

Codex 的 history / resume / fork 不是只看会话文件在不在，而是先按 `model_provider` 筛选。你换过 provider key（`right` → `packycode` → `xychatai`），旧历史的 key 不对，列表里就看不到。

根因：`model_provider` 是内部 bucket key，`name` 只是显示名。

## 解决

把旧 provider key 的历史统一迁到一个稳定 key（如 `custom`），之后只改 `name`、`base_url`、鉴权，不再动 key。

脚本处理两部分：

- `~/.codex/sessions` 和 `~/.codex/archived_sessions` 中 rollout JSONL 的 `session_meta.payload.model_provider`
- 状态库 `state_*.sqlite` 中 `threads.model_provider`

两边一起对齐，不会只改一边。

## 推荐配置

```toml
model_provider = "openai"

[model_providers.openai]
name = "cc-switch"
base_url = "http://127.0.0.1:15721/v1"
wire_api = "responses"
requires_openai_auth = true
```

`openai` 是稳定 bucket key（ChatGPT OAuth 默认值），`cc-switch` 是显示名。换代理只改显示名，key 不变，历史不会切桶。

## 用法

```bash
# 预览（默认，不写入）
python tools/codex-provider-history-migrator/migrate.py

# 执行迁移
python tools/codex-provider-history-migrator/migrate.py --apply

# 带备份
python tools/codex-provider-history-migrator/migrate.py --apply --backup-dir "/mnt/d/temp/codex-provider-backup"

# 指定 Codex Home
python tools/codex-provider-history-migrator/migrate.py --codex-home "/mnt/d/portable/codex-home" --apply

# 保留更多 provider
python tools/codex-provider-history-migrator/migrate.py --keep-provider openai --keep-provider custom --keep-provider oss
```

默认目标 provider 是 `openai`，默认保留 `openai`。路径含空格时加引号。

## 执行顺序

关闭 Codex → 确认 config.toml 目标 key → dry-run 看分布 → `--apply` → 重启 Codex → 检查 history/resume/fork
