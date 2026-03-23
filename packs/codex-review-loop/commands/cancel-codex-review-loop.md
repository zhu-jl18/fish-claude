---
description: "Cancel an active codex review loop"
allowed-tools:
  - Bash(test -f .claude/review-loop.local.md *)
  - Bash(rm -f .claude/review-loop.local.md)
  - Read
---

Check if a review loop is active:

```bash
test -f .claude/review-loop.local.md && echo "ACTIVE" || echo "NONE"
```

If active, read `.claude/review-loop.local.md` to get the current phase and review ID.

Then remove the state file:

```bash
rm -f .claude/review-loop.local.md
```

Report: "Review loop cancelled (was at phase: X, review ID: Y)"

If no review loop was active, report: "No active review loop found."
