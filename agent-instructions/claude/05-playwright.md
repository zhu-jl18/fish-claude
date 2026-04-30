# Playwright Guidelines

<important if="you are verifying, testing, or modifying UI/UX with Playwright">
- Check whether a project preview/development server is already running (process and endpoint reachability). Reuse the existing server if available; start a new one only when none is running.
- Execute Playwright verification (including screenshots), analyze the results, fix issues, and rerun until requirements are met.
- Store all verification screenshots in a project-root-level `screenshots` folder, and ensure this folder is included in `.gitignore`.
</important>
