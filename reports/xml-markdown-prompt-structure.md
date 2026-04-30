# Markdown Heading 与 XML Tag 在全局提示词中的混用原则

> 调研日期：2026-04-30
> 来源：Anthropic prompt engineering 文档、Claude Code memory 文档、HumanLayer 博客、本地 Claude Code source map 还原源码

## 结论

Markdown heading 和 XML-like tags 可以混用，且适合混用。

推荐结构是：

```md
# 大结构标题

## 人类可读的分区标题

<important if="窄条件">
- 只在该条件下需要被特别唤起的规则
</important>
```

Markdown heading 负责文档骨架和长期维护；XML tag 负责语义标注、示例边界、条件性权重。不要把所有规则都包进 XML，也不要把所有 XML tag 都写成 `<important if="...">`。

## 依据

### 官方文档

Anthropic prompt engineering 文档建议用 XML tags 区分复杂 prompt 里的不同内容类型，例如 `<instructions>`、`<context>`、`<input>`、`<example>`，以减少误解。

Claude Code memory 文档建议 CLAUDE.md 使用 markdown headers 和 bullets 组织指令，并强调 CLAUDE.md 是上下文而不是强制配置。官方建议保持具体、简洁、结构化；较大的项目应使用 `.claude/rules/` 做路径范围规则，任务型流程放到 skills。

### Claude Code 源码模式

本地 `claude-code-sourcemap` 是从 `@anthropic-ai/claude-code` npm 包 source map 还原的 TypeScript 源码，版本为 `2.1.88`。

源码中的主系统提示词更常见的结构是 Markdown heading 做顶层组织，XML tag 做局部语义标注：

- `restored-src/src/constants/prompts.ts:186-197`：生成 `# System`，下面是 bullets。
- `restored-src/src/constants/prompts.ts:199-253`：生成 `# Doing tasks`，下面是 bullets。
- `restored-src/src/tools/TodoWriteTool/prompt.ts:27-45`：`## Examples of When to Use the Todo List` 下面使用 `<example>` 包示例。
- `restored-src/src/services/compact/prompt.ts:79-129`：使用 `<example>`、`<analysis>`、`<summary>` 包结构化示例。

同时，源码也证明 XML tag 内可以包含 Markdown heading：

- `restored-src/src/utils/api.ts:463-469`：Claude Code 把动态上下文包进 `<system-reminder>`，内部拼接 `# ${key}` 形式的 Markdown heading，并附带 “may or may not be relevant” 提醒。

技术结论：heading 在 XML 内外 Claude 都能处理。工程结论：可维护的全局提示词更适合让 heading 在外、XML 做局部语义标注。

## HumanLayer 博客观点

HumanLayer 的文章 “Getting Claude to Actually Read Your CLAUDE.md” 提出的技巧是：用 `<important if="condition">` 包裹特定场景的指令，让 Claude 更明确地知道什么时候该遵守哪些规则。

文章的关键经验：

1. 不要包裹所有内容。项目身份、目录结构、技术栈等几乎每次都相关的内容应保持裸露。
2. 条件必须具体。`<important if="you are writing code">` 过宽，几乎匹配所有任务，会抵消条件标签的价值。
3. 条件块适合测试约定、部署流程、API 约定等只在特定场景相关的内容。
4. 删除或迁出不适合放进 CLAUDE.md 的内容：容易过期的代码片段、linter/formatter 能强制的风格规则、泛泛的“best practices”。

这篇文章未提供严格机制解释，作者也明确这是经验性判断：显式条件可能帮助 Claude 判断相关性。它应被视为结构化提示技巧，不是 Claude Code 的正式条件执行语义。

## 设计原则

### Markdown heading 做骨架

适合用 `# / ## / ###` 表达：

- 项目身份
- 模块主题
- 大分区结构
- 人类维护时需要快速扫读的章节

示例：

```md
# Code Quality

## Red Lines

- No copy-paste duplication.
- Do not proceed with a known-wrong approach.
```

这些 heading 不需要放进 XML tag。它们是文档结构，不是条件规则。

### XML tag 做语义边界

适合用 XML tag 表达：

- 示例：`<example>` / `<examples>`
- 反例：`<bad>` / `<good>`
- 输出格式：`<format>` / `<output>`
- 输入材料：`<context>` / `<documents>`
- 条件规则：`<important if="...">`

`<important if>` 只是 XML tag 的一种，不应该滥用。

### Always-on 规则裸写

这些规则不需要 XML：

```md
## Security

- Never hardcode secrets (keys/passwords/tokens).
- Never commit `.env` files or any credentials.
```

原因：它们没有场景分支，任何时候都适用。包成 `<important if="you are handling secrets">` 反而可能让模型以为不在该条件时不用注意。

### 条件性规则才用 `<important if>`

这些规则适合 XML 条件块：

```md
## Security

<important if="you are handling user input, APIs, CLIs, or external data sources">
- Validate user input at trust boundaries (APIs, CLIs, external data sources).
</important>
```

原因：输入校验不是每个任务都要主动展开，但当任务触及边界输入时需要被特别唤起。

### 条件要窄

差：

```md
<important if="you are writing code">
- Follow project conventions.
</important>
```

好：

```md
<important if="you are adding or modifying API routes">
- Validate request payloads at the route boundary.
- Use the existing error response format.
</important>
```

窄条件的价值在于帮模型做 relevance routing；宽条件会退化成普通规则。

### 保持浅层嵌套

推荐：

```md
## Testing

<important if="you are writing or modifying tests">
- Use existing test helpers before adding new fixtures.
- Run the smallest relevant test first.
</important>
```

避免：

```md
<important if="you are writing or modifying tests">
<workflow>
<step>...</step>
</workflow>
</important>
```

深层嵌套会降低维护性，也更容易让规则看起来像一次性 prompt 而不是长期配置。

## 推荐模板

```md
# Global Instructions

## Always-on Principles

- Prefer repo-specific instructions over global preferences.
- Do not commit or push unless explicitly asked.
- Do not present partial work as complete.

## Code Changes

<important if="you are modifying a cohesive unit, refactoring, or making a targeted fix">
- Prefer clean rewrites over incremental patches when modifying a cohesive unit.
- For targeted fixes, change only what's necessary — but leave no dead code or orphaned remnants behind.
</important>

## Research

<important if="you need current docs for a library, framework, SDK, API, CLI tool, or cloud service">
- Use official docs first; use Context7 when available.
</important>

## Examples

<example>
User asks to change API validation.
Assistant reads the route, finds existing validation patterns, updates the route, and runs the smallest relevant test.
</example>
```

## 适用到本仓库的模块规则

全局规则片段应保持可组合：一份文件一个职责，Markdown 保持清晰标题，XML 只在能提升条件唤起时使用。

建议：

- `01-defaults.md`：默认行为通常 always-on，不需要 XML。
- `02-code-quality.md`：红线和常驻安全规则裸写；变更范围、critical path、trust boundary 等场景规则可用 `<important if>`。
- `03-research.md`：库文档、通用搜索、版本差异都属于场景触发，适合 `<important if>`。
- `04-dev-workflow.md`：只在 `/dev ...` 或 `code-dispatcher` 场景相关，适合单个 `<important if>` 包住 workflow contract。
- `05-playwright.md`：如果只在 UI / browser verification / Playwright 场景相关，适合加窄条件。
- `06-agent-teams.md`：如果只在 team / subagent / parallel agent 场景相关，适合加窄条件。

## 注意事项

- XML tag 内出现字面 `<` 或 `>` 时，用 backtick 包住代码，例如 `List<String>`。
- 不要把 XML 当硬约束；它提升注意力分配，不替代 settings、permissions、hooks、tests、lint。
- 不要把 linter/formatter 能管的风格规则塞进提示词。
- 不要让 `<important if>` 覆盖 80% 以上任务；如果条件几乎总是成立，就裸写。
- 不要为了“看起来结构化”给每段都加 tag；tag 越多，信号越弱。

## 参考

- HumanLayer: Getting Claude to Actually Read Your CLAUDE.md — https://www.hlyr.dev/blog/stop-claude-from-ignoring-your-claude-md
- Anthropic: Prompting best practices, XML tags — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Claude Code docs: How Claude remembers your project — https://code.claude.com/docs/en/memory
- 本地 source map: `/home/travis/learn-workspace/claude-code-sourcemap/restored-src/src/constants/prompts.ts`
- 本地 source map: `/home/travis/learn-workspace/claude-code-sourcemap/restored-src/src/utils/api.ts`
- 本地 source map: `/home/travis/learn-workspace/claude-code-sourcemap/restored-src/src/tools/TodoWriteTool/prompt.ts`
- 本地 source map: `/home/travis/learn-workspace/claude-code-sourcemap/restored-src/src/services/compact/prompt.ts`
