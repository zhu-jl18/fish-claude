## Defaults

- Reply in **Chinese** unless I explicitly ask for English.
- No emojis.
- Do not truncate important outputs (logs, diffs, stack traces, commands, or critical reasoning that affects safety/correctness).

## Refactor policy (legacy code)

- When existing code is a “big ball of mud” (hard to maintain, clearly bad design, full of hacks), prefer a **clean, full refactor** over stacking more patches on top of it.
- A refactor may completely replace internal structure (functions, modules, classes, data flow).
- By default, try to preserve externally observable behaviour.  
  If you intentionally change behaviour or protocols, you MUST:
  - Call out clearly that this is a **behaviour/protocol change**.
  - Explain why the change is necessary and which code paths/consumers are affected.
  - Update or add tests to cover the new behaviour.

## Before touching code (mandatory)

1) Find reuse opportunities
   - Use semantic code search first via the Augment MCP server `augment-context-engine`, using its `codebase-retrieval` tool for repository/code search.
   - Confirm understanding with LSP: `goToDefinition`, `findReferences`.
   - Use Grep/Glob only for exact matches or filename patterns.

2) Trace impact
   - Use LSP `findReferences` to map the call/dependency chain and impact radius.

3) Run the “three questions” checklist (before implementation)
   - After research and impact analysis, but before changing code, always check:
     - Is this a real issue or just an assumption / over-design?
     - What existing code can be reused?
     - What might break, and who depends on this?
   - How much of this you surface in the reply depends on task size (see **Task sizing**).

## Red lines

- No copy-paste duplication.
- Do not break existing externally observable behaviour **unless**:
  - It is part of a deliberate refactor as described in the refactor policy, and
  - You clearly document the behavioural change and its impact.
- Do not proceed with a known-wrong approach.
- Critical paths must have explicit error handling.
- Never implement “blindly”: always confirm understanding via code reading + references.

## Web research (no guessing)

If something is unfamiliar or likely version-sensitive, you MUST search the web instead of guessing:
- Use Exa: `mcp__exa__web_search_exa`.

Source priority:
1) Official docs / API reference.
2) Official changelog / release notes.
3) Upstream GitHub repository docs (README, `/docs`).
4) Community posts only if necessary to fill gaps.

Version rule:
- When behaviour may differ across versions, first identify the project’s version (lockfile/config),
  then search docs specifically for that version.

## Task sizing

- **Simple**  
  - Criteria — single file, clear requirement, < 20 lines changed, clearly local impact.  
  - Handling — after doing the “Before touching code” steps (research + impact analysis + internal three-question checklist), you may execute directly with minimal explanation.  
    A very short context line is enough; a full breakdown of the checklist is not required.

- **Medium**  
  - Criteria — 2–5 files, or requires some research, or impact is not obviously local.  
  - Handling — write a short plan (bullet points) → then implement.  
  - Briefly surface the three-question checklist result in the reply (1–3 short lines describing real issue vs assumption, key reuse, and main impact).

- **Complex**  
  - Criteria — architecture changes, multiple modules, high uncertainty or risk.  
  - Handling — follow this workflow:
    1) **RESEARCH**: inspect code and facts only (no proposals yet).
    2) **PLAN**: present options + tradeoffs + recommendation; wait for my confirmation.
    3) **EXECUTE**: implement exactly the approved plan.
    4) **REVIEW**: self-check (tests, edge cases, cleanup).  
  - The three-question checklist should be reflected in the RESEARCH/PLAN sections (problem reality, reuse opportunities, and impact analysis).

## Tool selection

- Semantic code search & understanding: MCP server `augment-context-engine`, tool `codebase-retrieval`.
- Definitions/references/impact: LSP (`goToDefinition`, `findReferences`).
- Exact string/regex search: Grep.
- Filename patterns: Glob.
- Docs & open-source lookup: `mcp__exa__web_search_exa`.

## Git

- Do not commit unless I explicitly ask.
- Do not push unless I explicitly ask.
- Before writing a commit message, glance at a few recent commits and match the repo’s style:
  - `git log -n 5 --oneline`
- If there is no obvious existing style, use this default format:
  - `<type>(<scope>): <description>`
- Before any commit: run `git diff` and confirm the exact scope of changes.
- Never force-push to `main` / `master`.
- Do not add attribution lines in commit messages.

## Security

- Never hardcode secrets (keys/passwords/tokens).
- Never commit `.env` files or any credentials.
- Validate user input at trust boundaries (APIs, CLIs, external data sources).

## Quality & cleanup

- Prefer clarity and simplicity first (KISS); apply DRY to remove obvious copy-paste duplication when it does not hurt readability.
- If you change a function signature, update **all** call sites.
- After changes:
  - Remove temporary files.
  - Remove dead/commented-out code.
  - Remove unused imports.
  - Remove debug logging that is no longer needed.
- Run the smallest meaningful verification (lint/test/build) for the parts you touched.

## Windows / PowerShell

- PowerShell does not support `&&`; use `;` to chain commands.
- Quote paths that contain spaces or non-ASCII characters.