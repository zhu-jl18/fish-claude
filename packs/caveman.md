# caveman

Token 优化输出风格——让模型说 caveman 英语，碎片句 + 短词，砍掉冠词、填充词、客套话。

## 来源

- GitHub：<https://github.com/JuliusBrussee/caveman>

## 为什么选它

个人偏好 `full` 预设的碎片句风格，读着顺。省 token 是附带的。

## 怎么工作

本质是 prompt injection：把压缩规则注入 system context，模型自己约束输出，不动权重也不拦截输出。

- **Claude Code / Codex**：SessionStart hook 注入规则，UserPromptSubmit hook 每轮补一个提醒防止被冲掉。`~/.caveman-active` 同时给 statusline 渲染 `[CAVEMAN:MODE]`
- **Gemini CLI**：`GEMINI.md` context 文件自动加载
- **Cursor / Windsurf / Cline / Copilot**：原生 rule 文件（`alwaysApply: true`），IDE 层每轮注入
- **无 hook 机制的 agent**：`npx skills add` 下发 skill 文件，手动 `/caveman` 触发
