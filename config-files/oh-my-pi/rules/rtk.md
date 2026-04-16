---
alwaysApply: true
---

# RTK - Rust Token Killer

Prefer RTK for shell commands when it has a dedicated filter. Use `rtk <command>` instead of the raw command for common developer CLIs that produce verbose output.

Examples:

```bash
rtk git status
rtk git log -10
rtk cargo test
rtk pytest -q
rtk npm run build
rtk ls src/
rtk grep "pattern" src/
rtk docker ps
```

Rules:

- Do not prepend `rtk` to commands that already start with `rtk`.
- Do not prepend `rtk` to shell builtins or shell control flow such as `cd`, `export`, `source`, `alias`, `for`, `if`, or `while`.
- When a command is obviously a common output-heavy developer CLI and RTK likely supports it, prefer `rtk <command>`.
- When unsure whether RTK supports a command, keep the raw command instead of guessing.
- If raw output is intentionally needed, use `rtk proxy <cmd>` or `RTK_DISABLED=1 <cmd>`.

Meta commands:

```bash
rtk gain              # token savings dashboard
rtk gain --history    # per-command savings history
rtk discover          # find missed RTK opportunities
rtk proxy <cmd>       # run raw command without filtering
```

Verification:

```bash
rtk --version
rtk gain
which rtk
```
