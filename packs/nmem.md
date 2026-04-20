# nmem (Nowledge Mem)

外部工具参考页。

## 来源

- 官网: <https://mem.nowledge.co>
- 文档: <https://mem.nowledge.co/docs>
- CLI 文档: <https://mem.nowledge.co/docs/cli>
- GitHub 组织: <https://github.com/nowledge-co>
- CLI 主仓: `nowledge-co/nowledge-mem`

## 为什么选它

- **跨 AI 工具共用记忆** —— Claude Code / Codex / Cursor / Gemini CLI / Copilot 共享同一本地记忆库，换工具不失忆
- **本地优先** —— 数据默认不出本机，SQLite + 向量索引都在 `~/.nowledge-mem/`，远程访问靠自建 tunnel
- **主动 + 被动双路** —— Claude Code 每轮 hook 提示「先搜已有」「顺手存决策」，无需手动管理；同时 `nmem m add`/`t save` 可显式保存
- **Working Memory 每日简报** —— session start 读 `nmem wm` 就能拿回昨天的未完成 focus / 未解悬念，跨会话延续上下文
- **知识图谱** —— 自动抽取实体与关系、社区聚类，支持 `nmem g expand <id>` 可视化追溯关联

## 核心命令

| 命令 | 作用 |
|---|---|
| `nmem status` | 检查服务状态 |
| `nmem m search "query"` | 搜索记忆（BM25 + 向量混合，默认 fast 模式） |
| `nmem m add "content" -t "Title" -i 0.8` | 新增记忆，指定标题和重要度 |
| `nmem t save --from claude-code` | 导入当前 Claude Code 真实会话消息 |
| `nmem t search "query"` / `nmem t show <id>` | 搜 / 读历史会话 |
| `nmem wm` / `nmem wm edit` / `nmem wm patch` | 读 / 编辑 / 局部更新 Working Memory |
| `nmem f --days 1` | 今日 activity feed |
| `nmem g expand <id>` | 展开记忆的知识图谱关联 |
| `nmem c detect` | 触发社区（topic cluster）聚类 |
| `nmem tui` | 交互式 TUI |
| `nmem --json ...` | JSON 输出（脚本 / agent 用） |

别名：`m`=memories, `t`=threads, `wm`=working-memory, `g`=graph, `c`=communities, `f`=feed, `s`=sources

## 具体原理

- **Server**：本地 HTTP 服务（端口 14242），SQLite + FTS5 全文索引 + 向量索引 + 知识图谱
- **CLI**：薄客户端，所有操作走 REST API；优先级 `--api-url flag > NMEM_API_URL env > config.json > defaults`
- **异步富化链**：新记忆入库后，后台抽取实体、建立关系、分配社区、打标签（`enriches` chain）
- **MCP 集成**：Nowledge Mem 对外暴露 MCP server，Claude Code / Cursor 等 agent 通过工具直接调用搜 / 存
- **Hook 触发**：Claude Code `UserPromptSubmit` hook 每轮注入「search proactively / save autonomously」提示，由模型决定是否调

## 安装

- **后端**：Windows 侧装 Nowledge Mem desktop app,作为本地 server 跑在 `localhost:14242`
- **CLI**：Windows 与 Linux (WSL) 两侧各装一份 `nmem-cli`,都指向同一个 desktop app 后端,记忆库共用
  - `pip install nmem-cli` / `uv pip install nmem-cli` / `uvx --from nmem-cli nmem --help`
  - 要求 Python 3.11+
- **远程客户端**：`nmem config client set url https://...` + `nmem config client set api-key ...`

## 与 RTK / context-mode / caveman 的定位

四者分工不同，不冲突：

| 工具 | 解决的问题 |
|---|---|
| RTK | 已进上下文的 Bash 输出做压缩重写 |
| context-mode | 原始大输出关 sandbox，不让进上下文 |
| caveman | 控模型生成端，输出风格压缩 |
| **nmem** | 跨会话 / 跨工具的长期记忆持久化与检索 |

## 与本仓库的关系

- 纯外部工具参考页
- `agent-instructions/general/` 与 `CLAUDE.md` 已有 nmem 使用规范，不在此重复
