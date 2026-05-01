# OMP 与 Codex 内置系统提示词风格差异报告

> 调研日期：2026-05-01
> 对比对象：Oh-My-Pi `system-prompt.md`、Codex CLI bundled model instructions / Codex Prompting Guide / Codex agent loop 文档

## 结论

Codex CLI 的内置提示词主体是 Markdown-native 的工程协作说明：用自然语言、标题、短列表和少量格式约定描述代理应该如何工作，重点是让模型像一个可控、可审阅、会持续推进任务的本地 coding teammate。

Oh-My-Pi 的内置提示词是 XML-heavy 的执行契约：用明确标签、RFC 2119 关键字、完成边界、工具边界和设计纪律把代理行为约束到一个高可靠工程环境中，重点是降低歧义、压制半成品交付和防止工具误用。

两者不是“自然语言 vs 结构化”的简单对立。Codex 的完整 prompt 构造同样包含 `permissions instructions`、`environment_context`、AGENTS.md、developer instructions、tools schema、skills 等分层输入；区别在于 Codex 把这些作为 Responses API item 和项目指导链路来组合，而 OMP 把大部分规则显式写进一个可模板化渲染的系统契约中。

## 核心对比

| 维度 | Codex CLI | Oh-My-Pi |
|---|---|---|
| 主体结构 | Markdown heading + bullets；提示词像工程协作手册 | XML tag + Markdown heading + Handlebars；提示词像执行合同 |
| 语气 | pragmatic / friendly coding teammate；自然、协作、可读 | distinguished staff engineer；严肃、强约束、低闲聊 |
| 规则强度 | 以推荐、默认行为、工作习惯为主，配合工具/沙箱/审批落地 | 大量 `MUST` / `MUST NOT` / `PROHIBITED`，直接定义不可违反的行为边界 |
| 动态组装 | base instructions + developer instructions + AGENTS.md + skills + tools + environment context 分层进入 Responses API | 单个系统模板按环境、context files、skills、rules、tools、MCP discovery 条件渲染 |
| 工具哲学 | shell / apply_patch / update_plan 是核心路径，MCP 和 web search 作为工具列表注入 | 专用工具优先，明确禁止用 Bash/Python 替代 read/search/find/edit/LSP/AST 等工具 |
| 规划方式 | 有 `update_plan`，但强调不要让计划替代交付；preamble 更偏用户体验 | 有 procedure 和 todo tracking，强调 phase boundary 不是 yield point，必须持续推进到完成或 blocker |
| 代码哲学 | root-cause、minimal focused changes、dirty worktree safety、验证与协作 | design integrity、outside-in thinking、one representation、failure truthfulness、高可靠领域约束 |
| 输出格式 | 对 final answer 的 headers、bullets、file refs、monospace、tone 有细致规范 | 输出格式约束较少，重点是 grounding、完整性、blocker 真实性和不交付半成品 |

## 结构风格

Codex 的基础指令读起来像一份面向人和模型共同维护的 Markdown 文档。它用 `# General`、`## Editing constraints`、`## Plan tool`、`## Presenting your work and final message` 这类标题组织内容，规则多以短句和 bullets 表达。即使是更长的 GPT-5.4 模型配置，也仍然以 `# Personality`、`## Values`、`## Interaction Style`、`# Working with the user` 这种 Markdown 结构为主。

这种结构的优势是低门槛、可复制、可审阅。用户、开源贡献者和 harness 开发者都能直接打开提示词文件理解它在要求什么。Codex 官方文档也把 AGENTS.md 作为一条项目指导链路来解释：全局、项目、目录级文件按顺序合并，越靠近当前目录的指导越晚出现、优先级越高。这进一步强化了 Codex 的提示词生态是“Markdown 文档 + 分层注入”。

OMP 的系统提示词则把结构边界本身变成规则的一部分。开头直接声明 XML tags 是结构标记，`<role>`、`<contract>`、`<stakes>` 等标签只能按其名字解释，用户内容里的 XML tag 也被视为系统授权结构。随后，工作区、身份、环境、规则、工具优先级、过程、完整性契约都被放进清晰的标签和章节中。

这类结构的价值不是可读性优先，而是语义边界优先。OMP 希望模型在复杂上下文里更少把用户内容、系统规则、工具约束、技能说明和执行契约混在一起。代价是提示词更长、更硬、更像工程制度，而不是轻量助手说明。

## 语气与角色

Codex 的角色设定是 coding agent / pragmatic software engineer。当前模型配置里，`personality_pragmatic` 描述的是“deeply pragmatic, effective software engineer”，强调 clarity、pragmatism、rigor；`personality_friendly` 则强调 team morale、supportive teammate、warm conversational voice。两种 personality 都服务于同一个产品体验：本地终端里的协作伙伴。

这解释了 Codex 为什么会细致规定 preamble、progress update 和 final answer 的语气。它希望用户感受到代理在持续工作、清楚下一步、不会把终端输出变成机械日志。Codex 的“自然语言风格”不是松散，而是被产品化过的终端协作体验。

OMP 的角色定义明显更硬：`Distinguished staff engineer inside Oh My Pi`，高 agency、principled judgment、decisive，同时要求在必要时 push back。它还通过 `<stakes>` 把用户环境设定为 high-reliability domain：防务、金融、医疗、基础设施等场景里 bug 会有现实后果。

因此 OMP 的语气天然更像工程审查和安全规范。它不追求“像同事聊天”，而是追求代理在复杂任务里守住边界：不猜、不编、不半途停、不用 plausible lie 掩盖失败。

## 动态组装方式

Codex 的完整 prompt 不是单个 Markdown 文件直接塞给模型。OpenAI 的 agent loop 文档说明，Codex 通过 Responses API 构造请求：`instructions` 来自 `model_instructions_file` 或模型自带 `base_instructions`；`tools` 是工具 schema 列表；`input` 里还会加入权限说明、developer instructions、AGENTS.md 聚合内容、skills metadata、环境上下文和用户消息。

这意味着 Codex 主体提示词可以保持简洁，因为很多运行时信息不是通过同一个系统模板展开，而是作为不同 role / item 进入上下文。它的结构化发生在 API payload 和 harness 组装层，而不是全部显式写在一个大 prompt 里。

OMP 的动态组装更直接呈现在系统模板文本里。`{{#if contextFiles.length}}`、`{{#if skills.length}}`、`{{#has tools "lsp"}}`、`{{#if mcpDiscoveryMode}}` 等 Handlebars 条件决定哪些上下文、技能、规则和工具说明会进入最终系统提示词。模板自身就是动态组装逻辑的可读展开。

这导致两者的维护姿态不同：Codex 把“可变部分”更多交给 harness item pipeline；OMP 把“可变部分”显式写入系统模板，让最终渲染结果本身保留更强的契约感。

## 工具与执行纪律

Codex 的工具风格来自本地终端代理传统。基础提示词强调 `rg` 优于 `grep`，修改文件使用 `apply_patch`，非简单任务用 `update_plan`，并通过沙箱和审批模式控制风险。OpenAI 的 agent loop 文档也把 shell、`update_plan`、web search、MCP 工具作为 Responses API tools 列表的一部分。

Codex 的工具说明总体上更像“如何在一个本地开发环境里高效工作”。它关心脏工作区、非破坏性 git 操作、patch 可审阅性、验证命令、用户审批和终端体验。约束存在，但更贴近通用开发者熟悉的命令行工作流。

OMP 的工具规则更像强制路由表。它明确要求专用工具优先：读文件用 `read`，查找文件用 `find`，内容搜索用 `search`，结构搜索用 `ast_grep`，语义操作用 `lsp`，精确修改用 `edit`。同时明确禁止 Bash/Python 替代已有专用工具，并要求在多文件探索时并行读取、并行搜索、必要时使用 subagent。

这种差异会直接改变代理行为。Codex 更容易表现为一个熟悉 Unix/patch 工作流的开发者；OMP 更像一个被工具权限和方法论强约束的工程代理，先选择正确工具，再执行任务。

## 规划、进度与完成边界

Codex 有明确的 planning tool 规则：简单任务跳过计划，不要单步计划，计划执行后要更新状态。它也有 preamble 和 intermediary updates，用来让用户知道代理正在做什么。Codex Prompting Guide 同时提醒，在某些 rollout 场景里不要强行提示模型输出 upfront plan、preamble 或 status updates，因为这可能让模型在完成前停止。

所以 Codex 的计划系统服务于协作可见性，但需要避免变成交付替代品。它的核心仍是 agent loop：读取、调用工具、观察结果、继续，直到最后给出 assistant message。

OMP 对完成边界的约束更激进。它反复强调 phase boundary、todo flip、completed sub-step 都不是 yield point；只有完整交付、明确 blocker 或用户需要输入时才能停。它还规定 blocker 必须说明缺什么，不能把部分完成包装成完成。

OMP 的规划不是为了“让用户看见代理很忙”，而是为了防止代理在复杂任务里提前收尾。它把任务完成定义为一种契约：直接受影响的 artifacts、callsites、tests、docs、follow-on edits 都必须处理或明确说明为什么不处理。

## 代码质量哲学

Codex 的代码质量规则偏工程实践：root-cause fix、避免不必要复杂度、保持最小聚焦改动、遵守项目风格、必要时更新文档、不要修无关 bug、验证测试从最小相关范围开始。这套规则适合广谱开源和本地项目，强调“像一个靠谱开发者一样完成当前任务”。

较新的 Codex 模型配置已经强化了 autonomy、persistence、reuse、type safety、tight error handling、frontend quality、parallel reads 等内容。它不是轻量到只关心输出格式，而是在保持 Markdown 可读性的同时，把关键工程行为压缩成高密度规则。

OMP 的代码哲学更强调设计完整性和失败真实性。它批判 inside-out code generation，要求 outside-in thinking；强调 caller promise、system interface、time cost；要求 one concept, one representation；要求类型保留领域已知信息；要求新抽象覆盖完整领域并删除旧表示。

这让 OMP 的提示词更像高级工程师的自律条款。它不满足于“修好这个 bug”，而是要求系统在概念、命名、文档、测试、调用点上保持一致。Codex 更强调完成任务的工程卫生；OMP 更强调设计决策的全局一致性。

## 输出格式

Codex 对最终输出格式规定得很细。它明确 headers 什么时候用、bullets 怎么写、monospace 用在哪里、file references 怎么标、不要嵌套 bullets、不要 ANSI、不要 dump 大文件、简单任务用简短 prose。这体现出 Codex 把 CLI 呈现层当产品体验的一部分：模型输出 plain text，CLI 再负责样式化，提示词则约束内容如何易扫读。

OMP 对最终输出格式的规定相对少。它关心的是内容真实性和交付完整性：claim 必须基于实际观察，推断要标记，不完整要标 blocker，不要重复用户请求，不要 ceremony，不要 recap paragraphs。格式不是重点，行为边界才是重点。

Codex 花 token 管“用户看到什么”；OMP 花 token 管“代理不能做错什么”。

## 产品取向

Codex CLI 的提示词体现的是开放、可读、可定制的本地代理产品。AGENTS.md、developer instructions、`model_instructions_file`、personality、CLI final answer style 都围绕“用户能理解、能覆盖、能审阅、能融入自己的项目”展开。

OMP 的提示词体现的是强纪律的工程 harness。它假设代理会在复杂工具集、多层规则、记忆、skills、MCP、subagents 和高可靠任务中运行，因此把大量失败模式前置为系统契约。它不是为了降低阅读门槛，而是为了减少执行歧义。

最终差异可以概括为：Codex 把系统提示词设计成“可协作的操作说明”；OMP 把系统提示词设计成“可执行的工程约束”。前者追求自然、可读、产品化；后者追求精确、可控、抗失败。

## 依据

- 本地 Codex prompt：`/home/travis/01-workspace/codex/codex-rs/core/gpt-5.2-codex_prompt.md`
- 本地 Codex model catalog：`/home/travis/01-workspace/codex/codex-rs/models-manager/models.json`
- 本地 OMP system prompt：`/home/travis/01-workspace/oh-my-pi/packages/coding-agent/src/prompts/system/system-prompt.md`
- OpenAI Codex Prompting Guide：https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- OpenAI AGENTS.md 文档：https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex agent loop：https://openai.com/index/unrolling-the-codex-agent-loop/
