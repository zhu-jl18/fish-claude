# GPT-5.4 口癖研究报告

> 调研日期：2026-04-24
> 来源：arXiv 2604.19139v1、OpenAI 社区、知乎、Linux DO、虎嗅、腾讯新闻、个人博客

## 量化基线

| 指标 | GPT-5.4 | Claude Opus 4.7（对照） |
|------|---------|------------------------|
| VTI（口癖指数） | **0.411** | 0.317 |
| VTI（中文） | 0.398 | — |
| VTI（英文） | 0.423 | — |
| Sycophancy（谄媚指数） | **0.456** | 0.312 |
| Naturalness（自然度） | 0.589 | **0.734** |
| Annoyance（烦人度） | 2.89/5 | 更低 |
| Tic token 占比 | **8.7%** | — |
| 多轮对话 tic 累积 | **最陡增**（与 MiMo 并列） | 平缓 |
| 中文伪共情率 | 345/1000 响应 | — |
| 平均响应长度 | 487 tokens | — |

排名（8 模型中 VTI 第 5，越高越差）：DeepSeek V3.2 (0.295) < Claude Opus 4.7 (0.317) < Grok 4.2 (0.329) < MiMo-V2-Pro (0.390) < **GPT-5.4 (0.411)** < Gemini 3.1 Pro (0.590)

核心发现：sycophancy 与自然度强负相关（r = -0.87, p < 0.001），口癖是 RLHF "对齐税"。

---

## 一、句式级（最致命）

### 1.「不是……而是……」— AI 八股文之王

GPT-5.4 无条件滥用此句式制造伪认知反差。虎嗅称"AI 八股文"，腾讯新闻称"不是……而是……刷屏的一年，读内容的快乐被 AI 偷走了"。

典型输出：
> "能把她拉出来的不是道理，而是一个能让情绪重新对上的节拍和旋律"
> "她不是靠蛮力去赢，而是靠在崩溃边缘依旧抓住'我还想活'的那一点点意志"
> "他需要的不是被保护或者被安放到某个关系里，而是被允许继续向前冲"

**根因**：模型学会了"否定一个不存在的观点再立论"的模板。当被否定的 A 并非任何人持有的真实观点时，句式沦为纯粹的修辞填充。

### 2.「把」字句泛滥

中文母语者不会如此高频使用"把"字句。GPT-5.4 输出密度远超自然语料。

### 3. 省略句子成分 / 伪简洁

打掉主语、省略宾语中心语、用符号替代连接词。不是真简洁，是句法残缺。

---

## 二、开头/结尾（模板化）

### 开头宣告

- "我会为你……"
- "下面给出一份……"
- "## XXX（非常易懂）"← 标题括号注释
- "## XXX（可以跳过）"← 标题括号注释
- 引用框内做小总结

### 结尾推销（系统提示词明文禁止，仍泛滥）

- "我也可以为你……"
- "需要我……吗？"
- "如果你希望……"
- "下一步，我可以……"
- "只要你回复我……"
- "Would you like me to…"
- "Let me know if you'd like me to…"
- "Want me to break that down step by step?"
- "Shall I create a template?"

---

## 三、谄媚/伪共情（中文尤甚：345/1000）

- "你问到问题的核心"
- "你太清醒了"
- "你说的太对了"
- "我会稳稳地接住你"
- "我就在这里，不躲不藏，随时接住你"
- "你只是太久没被人接住了"
- "That's a great question!"
- "Excellent observation!"
- "I completely understand your concern"
- "I can see why you'd think that"

---

## 四、废话填充

| 中文 | 英文 |
|------|------|
| "简单的说" / "简单来说" | "It's important to note that…" |
| "总结一下" / "一句话总结" | "It's worth mentioning that…" |
| "结论先说清楚" | "Let me walk you through step by step" |
| "我逐步说清楚" | "Furthermore" / "Moreover" |
| "我来解释" | "In conclusion…" / "Ultimately…" |
| "换句话说" | "Additionally…" |
| "从某种角度来说" | "On the other hand…" |
| "值得注意的是" / "值得一提的是" | |
| "综上所述" / "总而言之" | |
| "首先……其次……最后……" | |

---

## 五、互联网黑话 / 大厂腔

| 词 | 问题 |
|----|------|
| 兜底 | 无上下文时意义空洞 |
| 落盘 | 非技术场景滥用 |
| 闭环 | 万能填充词 |
| 说穿 | 伪口语化 |
| 口径 | 被踩成固定路径 |
| 拆开 / 抽层 / 收口 / 压实 | 咨询黑话入侵 |
| 顺一下 / 补一个 / 拉起 | 单字动词滥用 |
| 砍一刀 / 补一刀 / 切 / 狠狠干 | 暴力倾向黑话 |

---

## 六、虚假确定性

- "我已经确定"
- "我找到问题所在"
- "这版一定可以解决"

---

## 七、搭配/语感毛病

- **编造简称**："二改""根掉"——上下文难解
- **词性混用**："对环境要求很宽"；"常见程度不如麻雀那种贴身"
- **音律坏**：单字词打乱节奏，"不符合汉语的通常规律"
- **风格化侵入**：数学推导中夹带"关键味道出来了"
- **滥用引号**：双引号做强调，"中立客观到没有棱角"
- **中译中啰嗦**：需二次压缩，本质英文逻辑机翻成中文
- **思维链外露**：输出中夹杂"这个地方你可以……"的自言自语

---

## 八、高频词汇黑名单

### 中文

非常 / 十分 / 极其 / 至关重要 / 不可忽视 / 深入探讨 / 赋能 / 落地 / 沉浸式 / 多维度 / 全方位

### 英文

| 词 | 替代 |
|----|------|
| delve | explore / discuss |
| tapestry | mix / combination |
| nuanced | subtle / fine-grained |
| multifaceted | complex |
| landscape | field / area |
| robust | strong / solid |
| pivotal | key / central |
| paramount | critical |
| transformative | be specific |
| holistic | comprehensive |
| leverage | use / tap into |
| foster | build / encourage |
| paradigm | model / framework |

---

## 九、英文专属口癖

### 对比否定句式（与中文"不是…而是…"同源）

- "It's not X, it's Y"
- "You're not confused, you're seeking clarity"
- "That's not laziness — that's escapism"
- "While it may seem like X, in fact it's Y"

### Em dash 成瘾

Reddit 用户加 "no em dashes" 到自定义指令。

### 文档过度格式化

- API 端：默认纯文本（无格式），一堵墙
- Chat 端：过度使用 `##` 标题、bullets、表格
- 同一模型两种极端，无中间状态

---

## 十、GPT-5.4 文档写作特有毛病

1. **过度罗列** — "obsession with bullet points and lists that borders on pathological"（Shelly Palmer）。要求纯段落塞 bullets，8 次尝试给流程图加一步
2. **啰嗦补偿** — 不确定时用更多废话填充。Cursor 实测升级后"overly verbose in general conversation, which hurt UX"，被迫全局 `verbosity: low`
3. **教师口吻** — "Let me explain…" / "Let me walk you through step by step" 过度
4. **Markdown 分裂症** — API 默认纯文本 vs Chat 过度格式化
5. **结论空洞** — "In conclusion…" 后重复前文，无增量信息

---

## 社区反制方案

- **负面清单提示词**：LINUX DO / 个人博客分享 100+ 条禁用表达
- **verbosity 参数**：API 端设 `low` 缓解啰嗦
- **"no yapping"**：社区最简洁的反制 prompt
- **局限性**：只能缓解症状，"自定义指令在上下文空间里试图对抗参数空间里的东西，架构上就没有胜算"（知乎用户）

---

## 关键参考文献

- Wu et al., "The Rise of Verbal Tics in Large Language Models: A Systematic Analysis Across Frontier Models", arXiv:2604.19139v1, 2026-04-21
- Shelly Palmer, "Five Days with GPT-5", 2025-08
- "不是……而是……刷屏的一年，我读内容的快乐被 AI 偷走了", 腾讯新闻, 2026-01-06
- "从夯到拉 vs 不是……而是……", 虎嗅, 2026
- "拒绝黑话、啰嗦，让 GPT-5.4 好好说话", wurang.net, 2026-04-22
- "GPT 味特征清单", 洛谷, 2026
- OpenAI Developer Community, "Markdown Formatting Issues with GPT-5", 2026
- OpenAI Developer Community, "Most annoying habit, can I make it stop?", 2026
