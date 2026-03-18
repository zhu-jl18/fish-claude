# Codex provider history 迁移说明

## 1. 先说结论

Codex 的 chat history / resume / fork 并不是"只看会话文件是否还在"，而是会先按 `model_provider` 做筛选。

这意味着：

```text
旧会话: model_provider = right
新配置: model_provider = packycode
默认筛选: 只看 packycode
结果: right 这批旧历史不会在默认列表里出现
```

根本原因不是历史丢了，而是 **provider key 变了**。

关键点只有两个：

1. `model_provider` 是内部 bucket key。
2. `name` 只是显示名，不是历史归属键。

因此，最稳的做法不是频繁改 provider key，而是：

1. 选一个稳定 key，例如 `custom`。
2. 之后只改显示名 `name`、`base_url`、鉴权方式。
3. 历史需要归并时，再用迁移脚本统一旧 bucket。

## 2. 这个脚本解决什么问题

脚本文件：`scripts/migrate_codex_provider_history.py`

它解决的是这类场景：

1. 你曾经用过 `right`、`packycode`、`xychatai` 等多个 provider key。
2. 你现在想统一到一个稳定 key，例如 `custom`。
3. 你希望 Codex CLI / Codex App 默认能重新看到旧历史。

脚本会处理两部分：

1. `~/.codex/sessions` 和 `~/.codex/archived_sessions` 中 rollout JSONL 的 `session_meta.payload.model_provider`
2. 状态库 `state_*.sqlite` 中 `threads.model_provider`。默认会按 `config.toml` 的 `sqlite_home`、环境变量 `CODEX_SQLITE_HOME`、`CODEX_HOME` 的顺序查找；也可用 `--state-db` 显式覆盖

也就是说，它不会只改原始 rollout，也不会只改 SQLite 索引，而是两边一起对齐。

## 3. 它不会替你做什么

脚本**不会**自动重写 `config.toml`。

原因如下：

1. 历史归并是数据迁移问题。
2. `config.toml` 是你的运行配置。
3. 自动改配置很容易误伤已有 provider 结构。

所以脚本只做一件事：**迁移历史数据**。

但它会检查当前 `config.toml`，并明确提醒你：

1. 当前 `model_provider` 是什么
2. 目标 provider 是否已经在 `model_providers` 中定义（如果目标是内建 provider，这项可能天然不存在；如果不是，则通常应该显式定义）
3. 如果配置没对齐，为什么迁完历史仍可能默认看不到

## 4. 推荐配置模式

推荐把自定义 provider 固定为一个稳定 key，例如：

```toml
model_provider = "custom"

[model_providers.custom]
name = "cc-switch"
base_url = "http://127.0.0.1:15721/v1"
wire_api = "responses"
requires_openai_auth = true
```

这里的含义是：

1. `custom`：稳定 bucket key，用来保证历史连续
2. `cc-switch`：显示名，可以按你的代理/网关名字改

如果你以后把 `cc-switch` 改成别的代理，只要 key 仍然是 `custom`，历史就不会再被切桶。

## 5. 用法

### 5.1 先预览，不写入

**Bash:**
```bash
python scripts/migrate_codex_provider_history.py
```

**PowerShell:**
```powershell
python scripts/migrate_codex_provider_history.py
```

默认行为：

1. 目标 provider 是 `custom`
2. 默认保留 `openai`
3. 自动按 `sqlite_home` / `CODEX_SQLITE_HOME` / `CODEX_HOME` 查找状态库
4. 仅预览，不写入

### 5.2 真正执行迁移

**Bash:**
```bash
python scripts/migrate_codex_provider_history.py --apply
```

**PowerShell:**
```powershell
python scripts/migrate_codex_provider_history.py --apply
```

### 5.3 迁移前先做备份

**Bash:**
```bash
python scripts/migrate_codex_provider_history.py --apply --backup-dir "/mnt/d/temp/codex-provider-backup"
```

**PowerShell:**
```powershell
python scripts/migrate_codex_provider_history.py --apply --backup-dir "D:/temp/codex-provider-backup"
```

### 5.4 指定 Codex Home

**Bash:**
```bash
python scripts/migrate_codex_provider_history.py --codex-home "/mnt/d/portable/codex-home" --apply
```

**PowerShell:**
```powershell
python scripts/migrate_codex_provider_history.py --codex-home "D:/portable/codex-home" --apply
```

### 5.5 保留更多 provider，不并到 custom

**Bash:**
```bash
python scripts/migrate_codex_provider_history.py --keep-provider openai --keep-provider custom --keep-provider oss
```

**PowerShell:**
```powershell
python scripts/migrate_codex_provider_history.py --keep-provider openai --keep-provider custom --keep-provider oss
```

---

**路径格式说明：**

- **Bash (Git Bash/WSL)**：使用正斜杠 `/`，Windows 盘符挂载在 `/mnt/` 下
- **PowerShell**：可用正斜杠 `/` 或反斜杠 `\`（推荐正斜杠避免转义问题）
- 路径包含空格时必须用引号 `"` 包裹

## 6. 建议的执行顺序

```text
关闭 Codex CLI / App
        |
        v
确认 config.toml 目标 key 已定好
        |
        v
先 dry-run 看 provider 分布
        |
        v
--apply 执行 rollout + sqlite 迁移
        |
        v
重启 Codex CLI / App
        |
        v
检查 history / resume / fork 是否恢复
```

## 7. 关于 auth.json / 代理托管

这个脚本处理的是 **history bucket**，不是认证实现本身。

像 `cc-switch -> 127.0.0.1:15721 -> auth.json -> PROXY_MANAGED` 这种代理托管模式，本身没有问题。

这两个维度需分开理解：

1. `auth.json` / `PROXY_MANAGED`：请求怎么鉴权
2. `model_provider`：历史会话归到哪个 bucket

建议将两者分开处理，避免混淆导致排查困难。
