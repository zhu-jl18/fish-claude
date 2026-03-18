# clean_chat_history.py

`clean_chat_history.py` 用于清理多种 CLI 的历史数据，当前覆盖：

- Claude Code
- Codex
- OpenCode
- Gemini CLI

## 目标

1. 交互式选择要清理的 CLI。
2. 交互式输入“删除多少天以前”的阈值。
3. 先预览，再确认，再执行，避免误删。
4. Windows 场景可用，并正确处理 OpenCode 的数据库与缓存目录。

## 目录定位方法

方法只有两步：

1. 先用官方提供的路径机制或命令确认标准目录。
2. 再用本机实际扫描验证真实落盘位置和文件结构。

本次实现对应如下：

1. Claude Code
- 目录重点：`~/.claude/projects`、`~/.claude/transcripts`、`~/.claude/history.jsonl`

2. Codex
- 目录重点：`~/.codex/sessions`、`~/.codex/archived_sessions`、`~/.codex/history.jsonl`

3. OpenCode
- 先通过 `opencode debug paths` 获取官方路径分层
- 本机关键目录：
`~/.local/share/opencode`
`~/.config/opencode`
`~/.local/state/opencode`
- 关键数据：
`~/.local/share/opencode/opencode.db`
`~/.local/share/opencode/storage/*`

4. Gemini CLI
- 目录重点：`~/.gemini/tmp`、`~/.gemini/history`

## 执行流程

```text
select cli + days
      |
      v
build cleanup plan
      |
      v
preview
      |
      v
confirm DELETE
      |
      v
execute + summary
```

关键设计点：

1. `CliCleanupPlan` 统一抽象各 CLI 的删除计划。
2. 文件类历史按 `mtime` 过滤删除。
3. JSONL 历史按时间字段剪裁行，而不是删整文件。
4. 删除前必须预览，执行前必须输入 `DELETE`。
5. 删除后输出统计结果。

## OpenCode 特殊问题

### 卡顿根因

最初版本逐条调用：

`opencode session delete <session_id>`

这会导致每删一条都启动一次 CLI 进程，删除多条时明显卡顿。

修复方式：

1. 预览阶段直接查 SQLite 统计待删会话。
2. 执行阶段用 SQLite 单次批量删除 `session`。
3. 执行时输出进度，避免黑盒等待。

### “删了但还能看到”根因

根因是数据源不一致：

1. 脚本最初删除的是 DB 的 `session`。
2. 第三方工具读取的是 `storage/session` 缓存 JSON。

修复方式：

1. OpenCode 改成双通道清理：`opencode.db` + `storage/*`
2. 按会话 ID 级联清理：
`storage/session`
`storage/session_diff`
`storage/message/<session_id>`
`storage/part/<message_id>`
`storage/todo`

## 当前清理策略

1. Claude Code
- 删除旧会话文件：`projects/**/*.jsonl`、`transcripts/*.jsonl`
- 剪裁命令历史：`history.jsonl`

2. Codex
- 删除旧会话文件：`sessions/**/*.jsonl`、`archived_sessions/*.jsonl`
- 剪裁命令历史：`history.jsonl`

3. OpenCode
- 删除旧会话：SQLite `session` 表
- 清理关联缓存：`storage/session|session_diff|message|part|todo`

4. Gemini CLI
- 清理旧会话相关文件：`~/.gemini/tmp`
- 清理历史目录：`~/.gemini/history`，保留 `.project_root`

## 验证方式

1. 语法检查：`python -m py_compile scripts/clean_chat_history.py`
2. 流程检查：验证交互输入有效和无效路径
3. 安全检查：预览后取消，不触发删除
4. 结果检查：删除后反查 DB 条数和缓存文件数
5. 交叉检查：对照第三方工具列表

## 使用方式

```bash
python scripts/clean_chat_history.py
```

建议：

1. 先用较小时间范围试跑。
2. 删除前先关闭相关 CLI 和查看器。
3. 删除后重启查看器再检查结果。

## 参考

1. `opencode debug paths`
2. XDG Base Directory Specification
3. Gemini CLI checkpoint/history 文档
