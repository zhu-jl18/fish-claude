# Serena MCP

用于语义检索、符号级代码定位与项目记忆管理，适合中大型代码库。

参考 [serena官方文档](https://oraios.github.io/serena)

## 安装前提

依赖：`uvx`（由 `uv` 提供）。

## 安装（Claude Code）

二选一即可，不要同时配。

### 方案 A：单项目配置（推荐）

在目标项目根目录执行：

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project "$(pwd)"
```

PowerShell 等价写法：

```powershell
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project "$PWD"
```

### 方案 B：全局配置（跨项目）

按当前工作目录自动绑定项目：

```bash
claude mcp add --scope user serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context=claude-code --project-from-cwd
```

## 安装后验证

1. 重新启动 Claude Code。
2. 在会话里确认能看到 Serena 工具。
3. 让模型执行一次符号检索（如查找某函数定义）验证可用性。

## 使用方式

1. 优先让 Serena 做“找代码、看关系、定位符号”。
2. 在 `claude-code` 上下文且已通过 `--project` 或 `--project-from-cwd` 绑定项目时，不需要手动先调 `activate_project`。
3. 需要时可让模型检查 onboarding/memory 状态，但这不是每次开局的强制步骤。
4. 不在规则文件里硬编码 Serena 工具清单，避免版本漂移导致配置失效。
5. --context claude-code 会自动注入上下文相关工具，确保 MCP 配置正确即可。

