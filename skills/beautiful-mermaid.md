# Beautiful Mermaid

## 来源

- GitHub: `okooo5km/beautiful-mermaid-cli`
- URL: <https://github.com/okooo5km/beautiful-mermaid-cli>

## 简介

- Mermaid 渲染 CLI / skill 参考：通过 `bm` 输出 SVG、PNG 或终端 ASCII / Unicode box-drawing
- 支持 `render`、`ascii`、`themes`、`doctor`，适合让 agent 生成图后做可验证渲染
- `--json` 提供机器可读输出：成功写 stdout，错误写 stderr；错误码覆盖用法、解析、I/O 和 WASM / runtime 问题

## 安装

```bash
npm i -g beautiful-mermaid-cli
# 或
brew install okooo5km/tap/bm
```

## 适用场景

- 把 Mermaid flowchart、sequence diagram、class diagram、state diagram、ER diagram、gantt 等渲染成图片
- 在终端里生成 Mermaid 的 ASCII / Unicode 预览
- 在脚本或 agent workflow 中用 `bm doctor --json`、`bm themes --json`、`bm render --json` 做可检测的渲染前检查
