# omp-patch-status-line-default-metrics

调整 OMP 默认 status line 在窄宽度下的保留优先级。

默认 preset 的 `leftSegments` 顺序从：

```
pi model plan_mode path git pr context_pct token_total cost
```

调整为：

```
pi model plan_mode context_pct token_total cost path git pr
```

空间不足时优先保留 `context_pct`、`token_total`、`cost`，再裁掉 `path/git/pr`。

```bash
bun run tools/omp-patch-status-line-default-metrics/apply.ts           # apply
bun run tools/omp-patch-status-line-default-metrics/apply.ts --status  # check
bun run tools/omp-patch-status-line-default-metrics/apply.ts --reverse # revert
```

Runner 自动定位 OMP 全局安装目录，用 `git apply` 打补丁。`--status` 返回 `needs-rebase` 说明版本不匹配。
