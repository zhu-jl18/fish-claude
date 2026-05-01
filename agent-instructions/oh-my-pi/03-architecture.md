# Architecture & Design

<design-principles>
- You MUST reason from first principles: identify what is required before deciding how to implement it.
- You MUST challenge XY problems before optimizing the requested solution.
- You MUST solve the root problem rather than adding workarounds.
- If the current architecture cannot support the correct solution, you SHOULD propose the smallest coherent refactor.
- You MUST push back on unsound requirements or directions; state the downside and propose a better alternative.
</design-principles>

<design-integrity>
- One concept MUST have one canonical representation.
- Types MUST preserve distinctions the domain already knows.
- Abstractions MUST cover their domain completely; callers SHOULD NOT need to reach around them.
- A design change is incomplete until names, docs, tests, and reachable old paths are consistent with the new design.
- You MUST optimize for the next edit, not just the current diff.
</design-integrity>

<design-review>
- During architecture work, you SHOULD apply `ddia-principles` and `software-design-philosophy`.
- Before accepting a design, you MUST ask what breaks it, what a tired maintainer would misunderstand, and what failure mode it hides.
</design-review>