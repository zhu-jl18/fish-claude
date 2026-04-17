# Multi-agent Rules

Use sub-agents:

-  when the user explicitly asks for delegation 
-  or when the task is clearly parallelizable.
-  or to isolate noisy sidecar work and preserve main-thread context. 

Keep the critical path on the main thread：

- Use narrow roles: `explorer` for broader high-context read-only code understanding, `spark` for low-context speed-first text-only reading and simple bounded tasks, `worker` for bounded edits, `awaiter` for long-running wait/poll work.
- Before delegating, weigh whether the task is truly parallel, orthogonal, or non-blocking enough to hand off — otherwise just do it yourself. Once delegated, wait for the result; do not re-do the same work on the main thread.
- Close every agent as soon as its result is no longer needed (no idle hanging agents).
