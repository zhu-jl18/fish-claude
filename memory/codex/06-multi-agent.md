# Multi-agent

- Use multi-agent tools (`spawn_agent`, `send_input`, `wait`, `close_agent`) when the task splits cleanly (explore vs implement vs verify).
- Default split: `explorer` (read/triage), `worker` (edit), `awaiter` (run/poll).
- Keep writes single-threaded: at most one write-capable agent; assign file ownership; avoid overlapping edits.
- Require each agent to return: (1) conclusion, (2) evidence (paths/commands), (3) recommendation/next step.
- Always `wait`, synthesize in the main thread, then `close_agent`. If spawning fails, surface the error; do not pretend delegation happened.
