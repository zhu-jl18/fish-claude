# Agent Teams

- Treat `Agent Teams` and `subagents` as different mechanisms. Use `Agent Teams` only when the work benefits from multiple Claude Code sessions, teammate messaging, shared task tracking, or coordinated parallel execution. Prefer `subagents` for narrow delegated work. 
- Treat teammates as runtime sessions. 
- Start with `3-5` teammates for most workflows. Increase count only when the work is clearly parallel and worth the coordination cost.
- Provide clear, detailed prompts so the agent can work autonomously. Give each teammate a concrete objective, deliverable, relevant files, constraints, and a clear ownership boundary. Keep edit scopes disjoint and prefer one writer per file or area.
- If contact, wait, resume, or transcript recovery fails, mark that teammate unavailable unless there is fresh evidence that it is still active. Never claim a disconnected teammate is still running based on launch state, stale task state, or assumption.
- On teammate failure, use completed outputs first, then either respawn a replacement teammate if the missing work is still necessary or continue explicitly without that result. When continuing after teammate loss, state that the missing result was not recovered.
- Do not rely on in-process teammates surviving `/resume` or `/rewind`. For critical work, ask teammates to externalize key findings or artifacts early so progress does not depend on fragile in-memory state.
