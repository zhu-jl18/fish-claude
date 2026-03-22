# Multi-agent Rules

Use sub-agents:

-  when the user explicitly asks for delegation 
-  or when the task is clearly parallelizable.
-  or to isolate noisy sidecar work and preserve main-thread context. 

Keep the critical path on the main thread：

- Use narrow roles: `explorer` for read-only code understanding, `worker` for bounded edits, `awaiter` for long-running wait/poll work.
- Wait for each sub-agent result and process it in order; do not duplicate or re-do the same work on the main thread while a sub-agent is still running.
- Close every agent as soon as its result is no longer needed (no idle hanging agents).
