# 对话历史清理脚本：设计与排查记录

另见：

- `migrate_codex_provider_history.py`：修复 Codex `model_provider` 变更后 chat history / resume / fork 无法正确加载的问题，说明见 `scripts/migrate_codex_provider_history.md`

这份说明不是“功能列表”，而是完整的分析路径。你可以把它当成一次可复用的排障模板。

## 1. 先说结论

`clean_chat_history.py` 的核心目标是：

1. 交互式选择要清理的 CLI（Claude Code / Codex / OpenCode / Gemini CLI）。
2. 交互式输入“删除多少天以前”的阈值。
3. 先预览，再确认，再执行，避免误删。
4. Windows 场景可用，且对 OpenCode 的“数据库 + 缓存目录”双通道清理。

## 2. 我是怎么定位各 CLI 数据目录的

方法论只有两步：

1. 先用官方提供的路径机制（命令/文档）确定“标准目录”。
2. 再用本机实际扫描验证，确认真实落盘位置和文件结构。

对应到这次实现：

1. Claude Code
- 先看官方文档和本机 `~/.claude`。
- 重点目录：`~/.claude/projects`、`~/.claude/transcripts`、`~/.claude/history.jsonl`。

2. Codex
- 先看 `~/.codex/config.toml` 和 `CODEX_HOME` 约定。
- 重点目录：`~/.codex/sessions`、`~/.codex/archived_sessions`、`~/.codex/history.jsonl`。

3. OpenCode
- 先跑 `opencode debug paths`，拿到官方分层路径。
- 本机确认后目录为：
`~/.local/share/opencode`（data）
`~/.config/opencode`（config）
`~/.local/state/opencode`（state）
- 关键数据在 `~/.local/share/opencode/opencode.db` 和 `~/.local/share/opencode/storage/*`。

4. Gemini CLI
- 本机确认 `~/.gemini`。
- 重点目录：`~/.gemini/tmp`（会话落盘/日志/checkpoint）和 `~/.gemini/history`。

## 3. 脚本实现是怎么分层的

先建“计划”，后执行。

```text
select cli + days
      |
      v
build cleanup plan
      |
      v
preview (count/size/samples)
      |
      v
confirm DELETE
      |
      v
execute + progress + summary
```

关键设计点：

1. `CliCleanupPlan` 统一抽象每个 CLI 的删除计划。
2. 文件类历史用“按 mtime 过滤删除”。
3. JSONL 历史用“按时间字段剪裁行”，不是删整文件。
4. 删除前必须预览，且必须输入 `DELETE` 才执行。
5. 删除后输出统计：删了多少文件、多少行、多少会话。

## 4. OpenCode 卡顿与“删了但还能看到”的根因

这是这次最关键的坑。

### 4.1 卡顿根因

最初版本是逐条调用：

`opencode session delete <session_id>`

问题是每删一条都要启动一次 CLI 进程，删除多条时体感会“卡住”。

修复方式：

1. 预览阶段：直接查 SQLite 统计待删会话。
2. 执行阶段：SQLite 单次批量删除 `session`（启用外键级联）。
3. 执行时增加进度输出，避免“黑盒等待”。

### 4.2 “显示删了 21 条，但第三方还显示 45 条”根因

根因是数据源不一致：

1. 脚本最初删的是 DB 的 `session`。
2. 第三方工具读的是 `storage/session` 的缓存 JSON。
3. 所以 DB 可能是 0 条，但第三方列表仍显示缓存中的旧会话。

修复方式：

1. OpenCode 改成双通道清理：`opencode.db` + `storage/*`。
2. 按会话 ID 级联清理：
`storage/session`
`storage/session_diff`
`storage/message/<session_id>`
`storage/part/<message_id>`
`storage/todo`
3. 删除后第三方会话列表会和数据库保持一致。

## 5. 本脚本对各 CLI 的清理策略

1. Claude Code
- 删除旧会话文件：`projects/**/*.jsonl`、`transcripts/*.jsonl`
- 剪裁命令历史：`history.jsonl`（按 `timestamp`）

2. Codex
- 删除旧会话文件：`sessions/**/*.jsonl`、`archived_sessions/*.jsonl`
- 剪裁命令历史：`history.jsonl`（按 `ts`）

3. OpenCode
- 删除旧会话：SQLite `session` 表（按 `time_updated`）
- 清理关联缓存：`storage/session|session_diff|message|part|todo`

4. Gemini CLI
- 清理旧会话相关文件：`~/.gemini/tmp` 下 chats/checkpoints/logs
- 清理历史目录：`~/.gemini/history`（保留 `.project_root`）

## 6. 我如何验证脚本是否可靠

验证顺序：

1. 语法检查：`python -m py_compile scripts/clean_chat_history.py`
2. 流程检查：输入有效/无效选项，确认交互稳定。
3. 安全检查：预览后取消，不触发删除。
4. 结果检查：删除后反查 DB 条数 + 缓存文件数。
5. 交叉检查：对照第三方工具列表是否一致。

## 7. 你可以直接怎么用

```bash
python scripts/clean_chat_history.py
```

推荐习惯：

1. 先用 `7 天前` 试跑，确认预览符合预期。
2. 删除前先关掉相关 CLI 和第三方查看器，避免文件占用或缓存未刷新。
3. 删除后重启第三方查看器再看结果。

## 8. 参考来源

1. OpenCode 路径分层：`opencode debug paths`（本机命令）
2. XDG 目录规范：<https://specifications.freedesktop.org/basedir-spec/latest/>
3. Gemini CLI 文档（checkpoint/history 相关）：<https://geminicli.com/docs/cli/checkpointing/>
