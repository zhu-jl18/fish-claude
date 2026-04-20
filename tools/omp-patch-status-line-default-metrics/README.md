# omp-patch-status-line-default-metrics

给已安装的 OMP 二进制打本地补丁，调整默认 status line 在窄宽度下的保留优先级。

## What changes

将默认 preset 的 `leftSegments` 顺序从：

```text
pi model plan_mode path git pr context_pct token_total cost
```

调整为：

```text
pi model plan_mode context_pct token_total cost path git pr
```

这样在空间不足时，优先保留 `context_pct`、`token_total`、`cost`，再裁掉 `path/git/pr`。

## Usage

```bash
bun run tools/omp-patch-status-line-default-metrics/apply.ts          # apply
bun run tools/omp-patch-status-line-default-metrics/apply.ts --status # check status
bun run tools/omp-patch-status-line-default-metrics/apply.ts --reverse # revert
```

## Notes

- 目录内包含 `apply.ts` 与 `patch.diff`。
- runner 会自动定位全局安装的 OMP 包根目录，并用 `git apply` 执行补丁。
- `--status` 返回 `needs-rebase` 时，说明当前安装版本与补丁不再干净匹配，需要手动 rebase。
