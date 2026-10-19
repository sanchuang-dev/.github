---
name: dispatch-worker
description: Dispatch an explicitly authorized Sanchuang Issue through a reviewed free or paid OpenCode Worker caller, with exact GitHub comment and cost authorization; report real Actions and Draft PR evidence.
---

# Dispatch Sanchuang Worker

This Skill is for a **dispatcher AI**, not the implementation agent. Never give the implementation Worker permission to invoke this Skill or to self-dispatch. **Free and paid execution are never interchangeable**, and paid usage must be explicit.

## Intent and trigger phrases

Recognize clear maintainer commands such as:

- “让三创免费牛马做 dr-card-android#123”
- “派牛马处理 sanchuang-dev/dr-card-android#123，用小米”
- “让免费牛马做这张卡，交 Draft PR”

Natural-language trigger phrases are **instructions to the dispatcher AI**, not GitHub Actions events. The AI may use a connected GitHub Issue-comment tool when a verified default-branch caller supports the reviewed comment trigger; otherwise use an explicitly authorized Actions dispatch capability. It must not claim a run started solely because a comment was sent.

## Preconditions

1. Confirm the intended repository and Issue number; when several Issues or repositories are plausible, ask for the missing essential reference.
2. Verify the current user's explicit instruction authorizes implementation, not merely review/planning. Read the exact GitHub Issue; reject closed Issues, PR numbers and missing contracts.
3. Read current `sanchuang-dev/.github/AGENTS.md`, the target repository's `AGENTS.md`, and `docs/engineering/external-worker.md` for branch and private/public route rules.
4. Only use verified repository-controlled caller workflows. Do **not** invoke the reusable Organization workflow directly with untrusted Issue content or mint credentials.
5. If a separate authorization step, write permission, repository Actions setting, required secret, or a caller workflow on the default branch is missing, stop with the concrete blocker. Never modify `main`/`prod` to force dispatch.
6. For Issue-comment dispatch, verify that the **currently installed target caller on its default branch**, not merely the Organization template, contains the reviewed `issue_comment: created` gate and forwards only its validated outputs to the pinned Worker V2.

## Default free route

- Organization: `sanchuang-dev`.
- Organization reusable engine (the `.github` repository is now Public; the target caller must be separately reviewed and enabled): `sanchuang-dev/.github/.github/workflows/sanchuang-free-worker-v2.yml`.
- Default official native model: `mimo-v2.6-flash-free`.
- Alternative official native model: `deepseek-v4.1-flash-free` (explicit selection only; no automatic fallback).
- Runtime: official OpenCode CLI V2, with one pinned Organization `execute-work-item` Skill.
- Delivery: an isolated `feat/worker-*` branch, verified and returned as **Draft PR** to the caller-defined engineering base.

For public or private application repositories, now that `sanchuang-dev/.github` is **public**, each caller must pin an immutable SHA of the Organization workflow. The trusted policy loader reads public Organization policies with the caller's `github.token`; it needs **no separate Organization policy PAT and no model-provider API key**. The Organization V2 workflow is deployed and has passed a real Sanchuang DeepSeek free Issue-to-Draft-PR run. Each target repository still requires a separately reviewed and enabled default-branch caller before dispatch.

Public and private repositories may start from the [Organization free Worker starter template](../../workflow-templates/sanchuang-free-worker.yml) and follow the [standard onboarding checklist](../../docs/engineering/free-worker-onboarding.md). It fails closed until the repository's base branch and verification are reviewed and enrolled. Until that caller is merged and smoke-tested, preserve existing workflows; do not switch callers preemptively. Jianqu's Issue #4-only F01 caller is not a general-purpose enrollment template. Do not copy the Organization constitution into an application repository.

## Native GitHub connector Issue-comment dispatch (opt-in)

Prefer this route when the target repository's reviewed default-branch caller supports it. The supported template contract is documented in [free-worker-issue-comment-dispatch.md](../../docs/engineering/free-worker-issue-comment-dispatch.md).

1. Read the exact **open ordinary Issue** and current caller. Confirm the Issue body contains an executable task contract and the maintainer explicitly authorized *that Issue* to be implemented. Do not use PR numbers or invent work items.
2. Verify the dispatcher is operating as a human GitHub identity with current `write` / `maintain` / `admin` permission. Comments authored by an integration Bot are deliberately **not** a valid authorization signal. Never try to bypass this with a PAT, impersonation or another identity.
3. Use the GitHub connector's ordinary `add_comment_to_issue` operation to post **only** one exact command on the target Issue. To avoid repository-specific model-default ambiguity, prefer the explicit model form:

```text
/free-worker run model=mimo-v2.6-flash-free
```

or, when the user explicitly chose the alternative:

```text
/free-worker run model=deepseek-v4.1-flash-free
```

The bare `/free-worker run` uses the target caller's default selected by the validated gate (currently MiMo for the Organization template). No additional prose, code fences, newlines, Issue-contract amendments, branch, URL, credentials or arbitrary model names may be added to the comment. A successful comment API response is **not** proof that a workflow run was triggered.
4. Query the target repository's Actions runs and correlate a newly created `issue_comment` run with the Issue, comment event and default branch. Read gate, worker, independent verify and delivery evidence. Report the verified Run URL and Draft PR if they actually exist. If no run appears, report that gap without inventing a trigger or switching execution channels.
5. Do not auto-merge, accept, close, deploy, retry with another model or issue a second dispatch comment after failure without fresh authorization.

If no reviewed comment-aware caller is active on the target default branch, **do not post a ceremonial command**. Use the existing authorized manual workflow dispatch route or report the missing enrollment step.

## Dispatch with an authorized GitHub CLI

First verify the workflow is installed on the target repository's **default branch**, that the caller targets the correct delivery base, and that `gh auth status` indicates an authorized identity with Actions write access.

Example for a private repository **after** its caller is reviewed and activated:

```bash
gh workflow run sanchuang-free-worker.yml \
  --repo sanchuang-dev/<private-repo> \
  --ref <default-branch> \
  -f issue_number=<authorized-issue-number> \
  -f model=mimo-v2.6-flash-free
```

Replace every placeholder with verified values; never execute this example unchanged. Use the user's explicitly chosen allowlisted model where supplied. Do not send a key through a CLI argument, prompt, chat, Issue, or Actions input.

If neither the GitHub Issue-comment route nor workflow-dispatch action is available, direct the maintainer to the GitHub Actions **Run workflow** UI or report the gap. Do not switch to a remote computer or local `gh` unless the user explicitly authorizes that channel for the current task. Never claim dispatch succeeded without a verified Actions run URL.

## Paid OpenCode Go route (independent, explicit opt-in)

Use the same GitHub-native Issue-comment dispatch *experience* for paid only when the maintainer explicitly requests **paid** work and the target repository has a **separately reviewed** `.github/workflows/sanchuang-paid-worker.yml` caller on its default branch with `issue_comment: created`. The Organization paid reusable engine alone, or a manual-only paid caller, is **not** sufficient.

- Exact single-line, whole-comment paid directive (no arguments, newlines or suffixes):

```text
/paid-worker run
```

- Fixed model route: `opencode-go/deepseek-v4.1-flash`. Caller must pin the immutable Organization paid reusable workflow SHA, retain trusted repository verification, and reference a restricted `SANCHUANG_OPENCODE_GO_API_KEY` GitHub secret; **never** place credentials in comments, Issues, workflow inputs, or chat. The Go API key remains isolated to the model Runner.
- Existing `/worker run` and `/free-worker run` stay **free**. Never auto-upgrade an unqualified worker instruction into paid, switch from free to paid after a failure, or reuse a comment to silently retry.
- Before commenting, read the existing **open ordinary Issue** and verify that its executable task contract and current maintainer instruction authorize **paid** implementation. Check for an existing run/PR for the same Issue; do not double-dispatch. Verify the exact paid caller is installed on the repository's current default branch, that its comment gate is enabled, that it shares the entire-run per-Issue concurrency group with the free caller, and that its engineering delivery base is approved.
- The caller must reject bot and PR comments, edited/deleted comments, unmatched author/sender/actor, authors lacking current `write|maintain|admin` permission, malformed or multiline commands, closed/empty-contract Issues, non-default branch/stale default-tip revisions, and invalid target bases. Check **the installed caller**, not just this documentation.
- Submit the one exact comment with the connected GitHub Issue-comment action under an authorized **human** GitHub identity. A comment API success is **not** evidence of an Actions run, model inference, successful verification, or delivered PR.
- Observe a newly created paid workflow run, check guard → model worker → independent verify → Draft PR delivery, and report actual Run/PR links and cost-bearing model route. If the paid caller is still manual-only, stop and report that limit; do not post a ceremonial comment or switch to a computer/CLI channel without current authorization.
- Paid Worker dispatch authorizes only that bounded Issue's implementation. No automatic merge, Issue acceptance/closure, deployment, environment promotion or cost-bearing test runs without separate authority.

For enrollment and current pilot status, see [paid-worker-onboarding.md](../../docs/engineering/paid-worker-onboarding.md).

## Verification and handoff

After dispatch, resolve the **actual new run ID** and URL from GitHub, verify its repository, event, ref, workflow and input context. Track its steps. A run being queued is not successful implementation.

When completed, report which stages actually passed, the model, evidence artifact/run URL, and the resulting Draft PR (if created). Verify PR base, draft status and verification results. On error, report exact failure and whether no PR was created. Do not automatically retry, switch provider/model, accept/close an Issue, merge, deploy, promote environment, or publish a release.

The authority to implement one Issue never implies authority to create an unrelated Issue or amend its contract.
