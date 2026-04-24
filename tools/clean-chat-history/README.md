# clean-chat-history

清理 Claude Code / Codex / Gemini CLI 的本地对话历史。交互式选择 CLI 和天数阈值，预览后确认删除。

```bash
python tools/clean-chat-history/clean.py
```

## 清理范围

| CLI | 目录/文件 |
|-----|----------|
| Claude Code | `~/.claude/projects/`、`~/.claude/transcripts/`、`~/.claude/history.jsonl` |
| Codex | `~/.codex/sessions/`、`~/.codex/archived_sessions/`、`~/.codex/history.jsonl` |
| Gemini CLI | `~/.gemini/tmp/`、`~/.gemini/history/`（保留 `.project_root`） |

- 文件类历史按 `mtime` 过滤删除
- JSONL 历史按时间字段剪裁行，不删整文件
- 删除前必须预览，执行前必须输入 `DELETE`

## 注意事项

- 先用小范围试跑
- 删除前关闭相关 CLI
- 删除后重启查看器检查结果
