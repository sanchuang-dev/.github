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
- Organization reusable engine (after Organization `.github` visibility is changed to public): `sanchuang-dev/.github/.github/workflows/sanchuang-free-worker-v2.yml`.
- Default official native model: `mimo-v2.6-flash-free`.
- Alternative official native model: `deepseek-v4.1-flash-free` (explicit selection only; no automatic fallback).
- Runtime: official OpenCode CLI V2, with one pinned Organization `execute-work-item` Skill.
- Delivery: an isolated `feat/worker-*` branch, verified and returned as **Draft PR** to the caller-defined engineering base.

For public or private application repositories, once `sanchuang-dev/.github` is made **public**, the caller must pin an immutable SHA of the Organization workflow. The trusted policy loader reads public Organization policies with the caller's `github.token`; it needs **no separate Organization policy PAT and no model-provider API key**. Until visibility has actually changed, the new V2 workflow is not activated: never bypass that prerequisite by providing broad tokens.

Public repositories can invoke the public reusable workflow after visibility change, via a reviewed opt-in caller on their default branch. Until that point, preserve legacy managed local Workflows; do not switch callers preemptively. Do not copy the Organization constitution into a public project.

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

If the available GitHub connector cannot dispatch new runs, but the user has an authorized computer connection with working `gh`, that is an alternative dispatcher path; otherwise report the integration gap without claiming success. Prefer GitHub's official workflow-dispatch API / `gh` over an improvised webhook endpoint.

## Verification and handoff

After dispatch, resolve the **actual new run ID** and URL from GitHub, verify its repository, event, ref, workflow and input context. Track its steps. A run being queued is not successful implementation.

When completed, report which stages actually passed, the model, evidence artifact/run URL, and the resulting Draft PR (if created). Verify PR base, draft status and verification results. On error, report exact failure and whether no PR was created. Do not automatically retry, switch provider/model, accept/close an Issue, merge, deploy, promote environment, or publish a release.

The authority to implement one Issue never implies authority to create an unrelated Issue or amend its contract.
