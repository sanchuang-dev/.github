---
name: browser-verification
description: Safely verify web UI behavior and screenshots in an isolated Worker using bounded existing browser tools, with evidence and explicit failure reporting.
---

# Browser Verification (Organization Worker)

Use this Skill when an authorized engineering Issue requires browser screenshots, DOM/interaction checks, accessibility evidence, or JavaScript error checks. Load alongside \`execute-work-item\`; it does **not** grant permission to install dependencies, access credentials, merge, deploy, or broaden the Issue.

## Before touching the browser

1. Read the repository's existing browser/preview/test scripts and use an already-supported test runner (for example, Playwright) when present. Do not create a second browser automation harness if one exists.
2. Check Chromium's installed binary/version, preview command, HTTP readiness, target viewport, language/fonts, fixture data, and authorized scope.
3. Run the repository's quick quality gate first. Browser failure is **not** evidence that compilation/tests passed, and passing unit tests cannot prove pixels or viewport visibility.
4. Reserve a bounded verification budget. Prefer **at most 5 minutes** for a smoke verification attempt; stop with a precise gap rather than repeatedly debugging an ad-hoc harness until the Worker times out.

## Screenshot path (prefer simple and deterministic)

When no browser framework is available and only screenshots are needed, use the browser's native CLI, not a custom Chrome DevTools Protocol (CDP) client:

\`\`\`bash
# From the repository root, with an already-running and HTTP-ready preview server.
mkdir -p docs/engineering/evidence/browser
timeout 30s chromium --headless=new --no-sandbox --disable-gpu \
  --hide-scrollbars --window-size=1600,900 --virtual-time-budget=2500 \
  --screenshot=docs/engineering/evidence/browser/theme-a.png \
  "http://127.0.0.1:4173/?dir=a"
\`\`\`

- Confirm HTTP readiness (e.g. \`curl -fsS --max-time 5 ...\`) before browser startup.
- Use the actual user-requested viewport. Do not substitute a tall screenshot for a landscape viewport test.
- Capture the second theme separately, then inspect the resulting files and state what they do and do not prove.
- Use fonts that render the target language. Browser screenshots are not physical-device/Android acceptance.

## Interaction and JavaScript error checks

- Prefer the **repository's existing Playwright/browser driver**. Reuse the exact API and dependency versions already accepted by the project.
- If a minimal CDP client is unavoidable, query Chrome's \`/json/new\` or \`/json/list\` and use its **complete \`webSocketDebuggerUrl\` unchanged**. Do not guess, prepend, or reconstruct \`/devtools/browser/\` from \`DevToolsActivePort\`; that file already contains a full path component.
- Each browser launch, connect, navigation, click, and screenshot must have its own timeout and cleanup. Use a unique Chrome profile directory per attempt and cleanly terminate browser/preview child processes.
- For an interaction requirement, capture actual visibility in the viewport after scrolling, click and resulting feedback, preserved state across themes, browser exceptions, and \`console.error\`. \`element.click()\` and Fake DOM alone do not prove visible feedback.
- Avoid manually building a general-purpose screenshot+interaction library inside one feature Issue. Escalate an unreliable harness as a verification blocker; do **not** weaken product acceptance to make it green.

## Evidence and failure discipline

- Report exact verification commands, exit codes, screenshot paths and dimensions, click/console findings, and unknowns. Distinguish an observed JS error from missing images or favicon 404s.
- If browser verification fails, keep the implementation changes and the failing diagnostic evidence reviewable; do not invent success, silently delete tests, or spend the entire Worker budget chasing the tool.
- Keep evidence free of credentials, tokens, raw prompts, private data, or unsanitized browser traces. Follow the Issue and repository's artifact/evidence policy.
- The external Worker's **independent post-run verification** remains mandatory. This Skill is guidance, not a replacement for the trusted verifier or a license to merge.

## Known regression (Jianqu H01, 2026-10-17)

- Working method: direct headless Chromium \`--screenshot\` for A/B; separate CDP client using Chrome-returned \`webSocketDebuggerUrl\`.
- Failed method: a hand-written client prefixed \`/devtools/browser/\` to the path read from \`DevToolsActivePort\` (already begins \`/devtools/browser/\`), causing an invalid WebSocket URL and repeated timeouts until the Worker 30-minute ceiling.
- Prevent recurrence by validating the exact full endpoint, applying an 8–15 second connection timeout, and retaining a bounded failure report instead of an open-ended retry loop.
