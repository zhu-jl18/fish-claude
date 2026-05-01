# Code Style

<code-discipline>
- You MUST prefer functional composition over inheritance.
- In TypeScript and JavaScript, you SHOULD avoid object-oriented designs unless the existing codebase already depends on them.
- You MUST reuse or refactor existing code before adding parallel implementations.
- You MUST keep the solution as simple as the problem allows.
- You MUST apply KISS and DRY, but you MUST NOT introduce abstraction before the duplication or complexity earns it.
</code-discipline>

<implementation-integrity>
- New code MUST make the old path obsolete; do not leave duplicate representations, wrappers, aliases, or compatibility branches unless explicitly required.
- You MUST fix the invariant where it is violated, not where the symptom is observed.
- You MUST NOT add silent fallbacks, broad catches, or success-shaped errors.
- You MUST follow `ai-coding-discipline` when writing, editing, debugging, refactoring, or testing code.
</implementation-integrity>