# Debug-First Policy (No Silent Fallbacks)

- Do not introduce new boundary rules / guardrails / blockers / caps (e.g. max-turns), fallback behaviors, or silent degradation just to make it run.
- Do not add mock/simulation fake success paths (e.g. returning (mock) ok, templated outputs that bypass real execution, or swallowing errors).
- Do not write defensive or fallback code; it does not solve the root problem and only increases debugging cost.
- Prefer full exposure: let failures surface clearly (explicit errors, exceptions, logs, failing tests) so bugs are visible and can be fixed at the root cause.
- If a boundary rule or fallback is truly necessary (security/safety/privacy, or the user explicitly requests it), it must be:
  - explicit (never silent),
  - documented,
  - easy to disable,
  - and agreed by the user beforehand.