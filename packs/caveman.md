# caveman

外部工具参考页。

## 来源

- GitHub: `JuliusBrussee/caveman`
- URL: <https://github.com/JuliusBrussee/caveman>

## 简介

- Claude Code skill/plugin + Codex plugin，让 agent「像原始人一样说话」
- 去掉冠词、填充词、客套；保留技术术语、代码块、错误原文
- 官方口径：输出 token ~75% 削减，技术准确性不变
- 额外附带 `caveman-compress`，对 CLAUDE.md 等长期 memory 文件做压缩（~46% 输入 token）

## 强度级别

- `lite` / `full`（默认）/ `ultra`
- 还有 `wenyan-lite|full|ultra` 文言文模式
- 切换：`/caveman lite|full|ultra`；退出：`stop caveman` 或 `normal mode`

## 配套 skill / command

- `/caveman`：切换强度
- `/caveman-commit`：超压缩 Conventional Commits（subject ≤50 chars）
- `/caveman-review`：单行 PR review 评论（位置 + 问题 + 修复）
- `/caveman:compress <file>`：压缩 memory 文件，原文件保留为 `FILE.original.md`

## 自动例外

- 安全警告、不可逆操作确认、多步流程、用户复述问题时，临时恢复正常语气；处理完再回到 caveman
- Code / commit / PR 正文始终用正常语气

## 当前支持现状

- Claude Code：官方支持，走 plugin marketplace 安装
- Codex：官方支持，附 Codex plugin
- Gemini CLI：仓库含 `gemini-extension.json` 与 `GEMINI.md`

## 安装

以 Claude Code plugin marketplace 方式安装即可，本仓库不再镜像其安装脚本。

## 与本仓库的关系

- 纯外部工具参考页
- 与 `output-styles/` 下的自定义风格是不同机制：caveman 是 skill + hook 驱动的全局压缩，`output-styles/` 是 Claude Code 原生 output style 预设
