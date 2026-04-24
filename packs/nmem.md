# nmem (Nowledge Mem)

跨 AI 工具的本地优先长期记忆系统。

## 来源

- 官网：<https://mem.nowledge.co>
- 文档：<https://mem.nowledge.co/docs>
- CLI 文档：<https://mem.nowledge.co/docs/cli>
- GitHub：<https://github.com/nowledge-co>

## 是什么

本地记忆服务（`localhost:14242`），SQLite 存储，数据不出本机。CLI 是薄客户端，所有操作走 REST API。

核心能力：

- **记忆存取** — 搜（BM25 + 向量混合）、存、更新、删，支持标签、重要度、时间范围过滤
- **会话导入** — `nmem t save --from claude-code` 导入真实对话，可回溯
- **Working Memory** — 每日简报（`nmem wm`），跨会话延续上下文，存储文件 `~/ai-now/memory.md`
- **知识图谱** — 自动抽取实体与关系，`nmem g expand <id>` 可视化追溯，支持 EVOLVES 版本链
- **知识社区** — 自动聚类主题（`nmem c detect`），发现非显式关联
- **Library** — 导入 PDF / Word / PPT / CSV，解析索引后可搜索

## 为什么选它

我同时用 Claude Code、Codex、Gemini CLI，需要一个跨工具共享的记忆层，换 CLI 不丢上下文。

数据存在本地（`~/.nowledge-mem/`），不依赖第三方服务器。远程 LLM 是可选的，开了也只用于增强检索，Nowledge 不碰记忆数据。

日常不用手动管——hook 每轮自动提醒模型搜和存，该记的自然就记了。Working Memory 每日简报让新会话能接上之前的焦点。
