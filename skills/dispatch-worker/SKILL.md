---
name: dispatch-worker
description: Dispatch one explicitly authorized Sanchuang GitHub Issue to the isolated free OpenCode V2 Worker and report real Actions and Draft PR evidence; never infer execution from natural-language trigger text alone.
---

# Dispatch Sanchuang Worker

This Skill is for a **dispatcher AI**, not the implementation agent. Never give the implementation Worker permission to invoke this Skill or to self-dispatch.

## Intent and trigger phrases

Recognize clear maintainer commands such as:

- “让三创免费牛马做 dr-card-android#123”
- “派牛马处理 sanchuang-dev/dr-card-android#123，用小米”
- “让免费牛马做这张卡，交 Draft PR”

Natural-language trigger phrases are **instructions to the dispatcher AI**, not GitHub Actions events. The AI must have a connected, authorized Actions dispatch capability or an authorized computer with GitHub CLI. It must not claim a run started solely because a message was sent.

## Preconditions

1. Confirm the intended repository and Issue number; when several Issues or repositories are plausible, ask for the missing essential reference.
2. Verify the current user's explicit instruction authorizes implementation, not merely review/planning. Read the exact GitHub Issue; reject closed Issues, PR numbers and missing contracts.
3. Read current `sanchuang-dev/.github/AGENTS.md`, the target repository's `AGENTS.md`, and `docs/engineering/external-worker.md` for branch and private/public route rules.
4. Only use verified repository-controlled caller workflows. Do **not** invoke the reusable Organization workflow directly with untrusted Issue content or mint credentials.
5. If a separate authorization step, write permission, repository Actions setting, required secret, or a caller workflow on the default branch is missing, stop with the concrete blocker. Never modify `main`/`prod` to force dispatch.

## Default free route

- Organization: `sanchuang-dev`.
- Organization reusable engine (the `.github` repository is now Public; the target caller must be separately reviewed and enabled): `sanchuang-dev/.github/.github/workflows/sanchuang-free-worker-v2.yml`.
- Default official native model: `mimo-v2.6-flash-free`.
- Alternative official native model: `deepseek-v4.1-flash-free` (explicit selection only; no automatic fallback).
- Runtime: official OpenCode CLI V2, with one pinned Organization `execute-work-item` Skill.
- Delivery: an isolated `feat/worker-*` branch, verified and returned as **Draft PR** to the caller-defined engineering base.

For public or private application repositories, now that `sanchuang-dev/.github` is **public**, each caller must pin an immutable SHA of the Organization workflow. The trusted policy loader reads public Organization policies with the caller's `github.token`; it needs **no separate Organization policy PAT and no model-provider API key**. The Organization V2 workflow is deployed and has passed a real Sanchuang DeepSeek free Issue-to-Draft-PR run. Each target repository still requires a separately reviewed and enabled default-branch caller before dispatch.

Public and private repositories may start from the [Organization free Worker starter template](../../workflow-templates/sanchuang-free-worker.yml) and follow the [standard onboarding checklist](../../docs/engineering/free-worker-onboarding.md). It fails closed until the repository's base branch and verification are reviewed and enrolled. Until that caller is merged and smoke-tested, preserve existing workflows; do not switch callers preemptively. Jianqu's Issue #4-only F01 caller is not a general-purpose enrollment template. Do not copy the Organization constitution into an application repository.

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

If the available GitHub connector cannot dispatch runs, direct the maintainer to the GitHub Actions **Run workflow** UI or report the gap. Do not switch to a remote computer or local `gh` unless the user explicitly authorizes that channel for the current task. Never claim dispatch succeeded without a verified Actions run URL.

## Verification and handoff

After dispatch, resolve the **actual new run ID** and URL from GitHub, verify its repository, event, ref, workflow and input context. Track its steps. A run being queued is not successful implementation.

When completed, report which stages actually passed, the model, evidence artifact/run URL, and the resulting Draft PR (if created). Verify PR base, draft status and verification results. On error, report exact failure and whether no PR was created. Do not automatically retry, switch provider/model, accept/close an Issue, merge, deploy, promote environment, or publish a release.

The authority to implement one Issue never implies authority to create an unrelated Issue or amend its contract.
