---
name: gpt-isms-stamp-out
description: Strip GPT-5.4 verbal tics from text. Use when user asks to de-GPT a document, remove AI-isms, stamp out GPT tics, or clean up AI-written text. Also use proactively when creating documents (README, docs, proposals, specs) to avoid GPT-5.4 tic patterns in the output.
---

# GPT-Isms Stamp Out

Remove GPT-5.4 verbal tics from text. Apply these rules when editing or creating documents.

## When to Apply

- User explicitly asks: "去 GPT 味", "去掉 AI 口癖", "de-GPT this", "stamp out GPT-isms", "clean up the AI voice"
- User asks to create a document — apply rules proactively to avoid tics in output
- User provides AI-generated text for cleanup

## Detection Rules — Chinese (ZH)

### Level 1: Must Remove — Structural Tics

**「不是……而是……」句式**
GPT-5.4 abuses this to manufacture faux cognitive contrast. Rewrite as direct statement.
```
❌ "能把她拉出来的不是道理，而是一个能让情绪重新对上的节拍"
✅ "节拍和旋律——而非道理——才能把她拉出来"  (or just state B directly)
```
Rule: When the "negated A" is not a real viewpoint anyone holds, delete the negation and state B directly.

**「把」字句泛滥**
GPT-5.4 overuses 把-construction far beyond natural Chinese frequency.
```
❌ "GPT 把把字句使用得很多"
✅ "GPT 高频使用把字句"
```

**结尾主动推销**
Never end with unsolicited offers for follow-up.
```
❌ "如果你需要，我可以……" / "需要我……吗？" / "下一步，我可以……" / "只要你回复我"
✅ [Just stop. No trailing offer.]
```

### Level 2: Must Remove — Filler Phrases

| Tic | Fix |
|-----|-----|
| "简单的说" / "简单来说" | Delete or use "简言之" sparingly |
| "总结一下" / "一句话总结" | Delete; just state the conclusion |
| "结论先说清楚" | Delete |
| "我逐步说清楚" | Delete |
| "我来解释" | Delete |
| "换句话说" | Delete or use "即" |
| "从某种角度来说" | Delete |
| "值得注意的是" / "值得一提的是" | Delete; if truly notable, let content speak |
| "综上所述" / "总而言之" | Delete |
| "首先……其次……最后……" | Restructure to avoid numbered-transition chain |

### Level 3: Must Remove — Sycophancy

```
❌ "你问到问题的核心" / "你太清醒了" / "你说的太对了"
❌ "我会稳稳地接住你" / "我就在这里，不躲不藏，随时接住你"
❌ "你只是太久没被人接住了"
✅ [Delete entirely. No flattery, no pseudo-empathy.]
```

### Level 4: Must Remove — Internet Corporate Jargon

| Tic | Fix |
|-----|-----|
| 兜底 | "保底" or rephrase |
| 落盘 | "确认" / "定下来" |
| 闭环 | "完整流程" or rephrase |
| 说穿 | Delete |
| 口径 | "说法" / "表述" |
| 拆开 / 抽层 / 收口 / 压实 | Rephrase in plain language |
| 顺一下 / 补一个 / 拉起 | Rephrase |
| 砍一刀 / 补一刀 / 切 / 狠狠干 | Delete violent metaphor |

### Level 5: Must Remove — False Certainty

```
❌ "我已经确定" / "我找到问题所在" / "这版一定可以解决"
✅ "当前分析显示……" / "这个方案……" (proportional confidence)
```

### Level 6: Must Remove — Structural & Stylistic

**标题括号注释**
```
❌ "## 架构设计（非常易懂）" / "## 快速开始（可以跳过）"
✅ "## 架构设计" / "## 快速开始"
```

**开头宣告句式**
```
❌ "我会为你……" / "下面给出一份……"
✅ Just start the content.
```

**滥用双引号做强调** — Use bold or italics for emphasis, not quotation marks.

**思维链外露** — Remove self-talk like "这个地方你可以……" / "这里需要说明的是……"

**编造简称** — "二改" / "根掉" → spell out or use standard terms.

**搭配蹩脚 / 词性混用** — Flag and rephrase: "对环境要求很宽" → "对环境要求宽松"

**音律坏** — Single-character words disrupting rhythm: flag and suggest multi-character alternatives.

**中译中啰嗦** — If a sentence can be halved without losing meaning, halve it.

### Level 7: Overused Vocabulary

| Tic | Replacement |
|-----|-------------|
| 非常 / 十分 / 极其 | Delete; let the adjective stand alone |
| 至关重要 | "关键" or delete |
| 不可忽视 | Delete |
| 深入探讨 | "讨论" / "分析" |
| 赋能 | "支持" / "帮助" |
| 落地 | "实施" / "执行" |

## Detection Rules — English (EN)

Apply when document is in English or mixed-language.

### Structural

| Tic | Fix |
|-----|-----|
| "It's not X, it's Y" / "Not X, but Y" | State Y directly unless X is a real, named viewpoint |
| "That's a great question!" | Delete |
| "I completely understand…" | Delete |
| "Let me walk you through step by step" | Just do it; don't announce it |
| "Would you like me to…" / "Let me know if…" / "Shall I…" | Delete; end at conclusion |
| "In conclusion…" / "Ultimately…" | Delete |

### Vocabulary

| Tic | Replacement |
|-----|-------------|
| delve | explore / dig into / discuss |
| tapestry | mix / combination / fabric |
| nuanced | subtle / fine-grained (or delete) |
| multifaceted | complex / many-sided |
| landscape | field / area / scene |
| robust | strong / solid / reliable |
| pivotal | key / central |
| paramount | critical / vital |
| transformative | big-change / overhaul (or be specific) |
| holistic | comprehensive / full |
| leverage | use / tap into |
| foster | build / grow / encourage |
| paradigm | model / framework |
| Furthermore / Moreover | Delete or use "And" / "Also" |
| It's important to note that | Delete; just state the point |
| It's worth mentioning that | Delete |

### Em-dash Overuse

Limit to at most one em-dash per paragraph. Replace extras with period, semicolon, or parenthesis.

## Workflow

### Mode A: Clean Existing Document

1. Read the target file(s)
2. Scan line by line against all detection rules above
3. For each hit: report the tic, category, and suggested fix
4. Apply fixes (Edit tool) — one category at a time, starting from Level 1 structural tics
5. After all fixes: re-read the document, verify no new tics introduced, report before/after stats

### Mode B: Create New Document (Proactive)

1. When user asks to create a doc, apply all rules above during composition
2. Before writing each section, mentally check against the tic list
3. After writing: run a self-scan pass (Mode A step 2-4)
4. Report: "Written with GPT-isms stamped out. [N] tics avoided."

## Reporting

After cleanup, report:
```
GPT-isms stamped out: [N] tics removed
- Structural (不是…而是…): [N]
- Filler phrases: [N]
- Sycophancy: [N]
- Corporate jargon: [N]
- Vocabulary: [N]
- Other: [N]
```

## Edge Cases

- **Quoted text**: Do not modify content inside blockquotes or verbatim quotes — those belong to the quoted source
- **Code blocks**: Never modify content inside code fences
- **Deliberate style**: If user explicitly wants a specific tic pattern kept (e.g., marketing copy using "赋能"), respect it
- **Mixed language docs**: Apply both ZH and EN rules; prioritize the primary language of each section
