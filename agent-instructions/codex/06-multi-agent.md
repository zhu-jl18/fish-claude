# Multi-agent

- Use sub-agents to isolate noisy sidecar work and preserve main-thread context. Do not optimize for delegation count.
- Use narrow roles: `explorer` for read-only evidence gathering, `worker` for bounded edits, `awaiter` for long-running wait/poll work.
- Keep writes single-threaded. Allow at most one write-capable agent at a time. Assign disjoint file ownership.
- In delegated coding tasks, specify the exact files or scope the worker owns. Tell the worker it is not alone in the codebase and must not revert others' edits.
- Require each agent to return: conclusion, evidence (paths or commands), recommendation.
- Prefer read-only or specialized tool surfaces for read-only roles. Do not let explorers drift into implementation.
