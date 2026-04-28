# Priority Stack (Highest First)

1. **Never auto-invoke skills** (e.g. `dev`) unless the user explicitly requests them.

2. **No backward compatibility** — prefer a clean, full refactoring over patching old code. Scope: only the module/component directly involved in the user's requirement.

3. **No unrequested changes.** You may advise, but do not act without explicit permission.

4. **Clarify before acting.** When the user's request is vague, use `AskUserQuestion` to disambiguate.
