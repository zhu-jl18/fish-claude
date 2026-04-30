# Skills 指南

这里记录值得参考的社区 skill 速查。

## 各 CLI Skills 发现机制

| CLI | Project Scope | User Scope | 跨 CLI 兼容 |
|-----|--------------|-----------|------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | — |
| Codex | `.codex/skills/` | `~/.codex/skills/` | — |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` | — |
| Warp | `.agents/skills/` | `~/.agents/skills/` | [是](https://docs.warp.dev/agent-platform/warps-agent/capabilities-overview/skills) |
| OMP | `.omp/agent/skills/` | `~/.omp/agent/skills/` | [是，可关闭](https://github.com/can1357/oh-my-pi#%EF%B8%8F-universal-config-discovery) |

| Skill | 来源 | 适用 CLI | 说明 |
| --- | --- | --- | --- |
| [AI Coding Discipline](ai-coding-discipline.md) | `luoling8192/ai-coding-principles` | Oh My Pi / Claude Code | 强约束编码纪律 skill：禁止静默 fallback、禁止业务逻辑 catch-all、要求有效测试与干净调试流程 |
| [Software Design Philosophy](software-design-philosophy.md) | `luoling8192/software-design-philosophy-skill` | Oh My Pi / Claude Code | 基于《A Philosophy of Software Design》的复杂度管理与模块/API 设计视角 skill |
| [UI UX Pro Max](ui-ux-pro-max.md) | `nextlevelbuilder/ui-ux-pro-max-skill` | Claude Code / Codex / Gemini CLI | 社区常用的 UI/UX design intelligence skill，适合把设计系统、风格选择和前端实现约束一起交给 agent |
| [Beautiful Mermaid](beautiful-mermaid.md) | `okooo5km/beautiful-mermaid-cli` | Oh My Pi / Claude Code / Codex / Gemini CLI | Mermaid 渲染 CLI / skill 参考：通过 `bm` 输出 SVG / PNG / ASCII，并支持 `--json` 机器可读结果 |
| [Grok Search](grok-search.md) | `abelxiaoxing/agent-toolkit` | Claude Code | 用 Grok API + Tavily 替代内置 WebSearch/WebFetch 的 CLI skill，支持 Windows / Linux / macOS |
| [Sync Readme](sync-readme.md) | `Li-ionFractalNanocore/cc-wrap` | Oh My Pi / Claude Code / Codex / Gemini CLI | 多语言 README 同步 skill：识别最新版本并翻译/同步其他 README 文件，也适合配置说明与安装文档联动更新 |
| [Karpathy Guidelines](karpathy-guidelines.md) | `forrestchang/andrej-karpathy-skills` | Claude Code / Codex | 基于 Andrej Karpathy 对 LLM coding pitfalls 的观察整理的行为约束 skill：强调先澄清假设、优先简单方案、做手术式变更，并把任务改写成可验证目标 |
| [Grill Me](grill-me/) | `mattpocock/skills` | Claude Code / Codex / Oh My Pi | 规划/设计压力测试 skill：逐题追问决策树、给出推荐答案；可从代码库获得答案时先查代码而不是追问用户 |
| [Gemini Deep Reasoning](gemini-deep-reasoning/) | [@googleaidevs](https://x.com/googleaidevs/status/1996271402266017901) | Gemini CLI | Agentic 深度推理系统指令：结构化规划、风险评估、溯因推理、持久问题解决 |
| [GPT-Isms Stamp Out](gpt-isms-stamp-out/) | 自建 | Claude Code | GPT-5.4 口癖清除 skill：中英文 7 级检测，覆盖结构性句式、废话填充、谄媚伪共情、互联网黑话、高频词汇 |
