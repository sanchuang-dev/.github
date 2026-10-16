# Sanchuang External Worker

Owner: `sanchuang-dev/.github`. Execution contract: [Execute Work Item](../../skills/execute-work-item/SKILL.md).
Reference implementation: Mira's reusable External Worker, adapted to Sanchuang's governance and permission model. **Current visibility:** the Organization repository is Public, confirmed with unauthenticated GitHub API/AGENTS.md access on 2026-10-16. Legacy V1 remains untouched.

## V2 native free Worker (separate, keyless model route)

The opt-in `.github/workflows/sanchuang-free-worker-v2.yml` is a **new**, independent, public-policy-based Organization reusable workflow for both public and private callers now that `sanchuang-dev/.github` is public. The Organization engine has now been merged and completed the real Sanchuang Jianqu Issue #4 DeepSeek Free → independently verified Draft PR #23 trial. Each additional repository still requires its own reviewed, SHA-pinned opt-in caller; use the [Organization standard onboarding guide](./free-worker-onboarding.md). The legacy `sanchuang-external-worker.yml` and existing managed public-repository copies are deliberately unchanged. V2 requires no OpenCode/Zen API key.

- Uses pinned official OpenCode CLI `2.0.24` via `https://opencode.ai/v2/install`.
- Default `opencode/mimo-v2.6-flash-free`; explicit alternate `opencode/deepseek-v4.1-flash-free`; allowlist checked against official model catalog before invocation. Provider availability is **not guaranteed**, and a catalog entry is not proof of a successful inference. No paid fallback or custom endpoint/header impersonation.
- Loads canonical `AGENTS.md` and `skills/execute-work-item/SKILL.md` from the **same resolved Organization main commit** using the caller-scoped `github.token` only in a trusted policy-loading step, now that the Organization repository is public. OpenCode does not receive this token. No cross-repository policy PAT or API key is required. Mirrors that Skill to the V2 native global directory and verifies bytes.
- Denies all other native Skill IDs and fails closed when project OpenCode config/Skill sources or a same-name Skill could shadow the pinned Organization contract.
- Keeps original per-Issue authorization, verified maintainer comment amendments, isolated worker branch, trusted repository-owned verification, Draft PR only, and bounded diagnostic evidence. The model is not granted Issue-close, merge or release authority.
- **Patch and credential isolation:** the model runner has only read-level GitHub permissions and packages the implementation patch **before** independent verification. A fresh second read-only Runner downloads and applies that exact patch, runs the repository-owned verification, checks the immutable patch hash and staged snapshot, then records its approval. Only if that second Job succeeds may a third, fresh `delivery` Runner obtain write permissions, independently download the same patch, verify its SHA-256 against the verification Job's result, apply it with hooks disabled and create the Draft PR. No model, build scripts or repository-controlled processes run in the write-token Job. Local malicious-Hook and Git clean-filter regression fixtures reproduced both original vulnerabilities and verified the isolated fix.

An AI dispatcher should load `skills/dispatch-worker/SKILL.md` to recognize maintainer requests, validate the authorization, and use an **already activated target-repository caller**. A phrase such as “让免费牛马做 dr-card-android#123” is a language-level instruction to that dispatcher AI, **not** an automatic GitHub trigger.

### Required integration for a calling repository (public or private after visibility change)

Both public and private callers can reference the reviewed and immutable Organization reusable-workflow commit once this PR is merged. The target repository must install a thin workflow on its **default branch** for `workflow_dispatch`; the implementation base remains its documented `dev` or other trusted branch. A public caller must not expose Organization secrets or copy internal policy. Sample caller:

```yaml
name: Sanchuang Free Worker
on:
  workflow_dispatch:
    inputs:
      issue_number:
        required: true
        type: number
      model:
        required: true
        type: choice
        default: mimo-v2.6-flash-free
        options:
          - mimo-v2.6-flash-free
          - deepseek-v4.1-flash-free

jobs:
  worker:
    permissions:
      contents: write
      issues: read
      pull-requests: write
    uses: sanchuang-dev/.github/.github/workflows/sanchuang-free-worker-v2.yml@<reviewed-40-character-SHA>
    with:
      issue_number: ${{ fromJSON(inputs.issue_number) }}
      model: ${{ inputs.model }}
      base_branch: dev # Replace with repository-specific, verified delivery base.
      verification_command: |
        ./gradlew :app:assembleDebug # Example ONLY; use the caller's trusted checks.
```

Do not deploy this example unchanged: verify the repository's default branch, delivery base, appropriate task-check commands and the reviewed reusable commit. For **public** `dr-card-web`, replace the managed local copy only after the Organization repo is public, this PR is accepted, and an independent, explicit opt-in PR is reviewed; preserve the existing caller until then.

### Verification and rollout boundary

**Organization V2 proven on Sanchuang, 2026-10-16:** DeepSeek Free completed a real Jianqu [Issue #4](https://github.com/sanchuang-dev/ai-mirror/issues/4) → [Actions #38875822060](https://github.com/sanchuang-dev/ai-mirror/actions/runs/38875822060) → [Draft PR #23](https://github.com/sanchuang-dev/ai-mirror/pull/23). The native Skill loaded, isolated Worker changed actual docs, the independent verification runner passed, and the write-isolated delivery runner created the Draft PR. The PR later passed Codex review and was merged under separate authorization. Engine revision used in that confirmed E2E: `0118f124b7bb95d75273f377b69dbab9ca050750`. The current standard template instead pins security-reviewed [Organization PR #8](https://github.com/sanchuang-dev/.github/pull/8) merge SHA `985ff50c297b844af65a920bd38f9c0b1ae31098`, which adds trusted default-ref/default-tip checks; **no separate live malicious-ref fixture or E2E for that new revision has been run yet**.

In Mira, MiMo V2.6 Free passed earlier upstream native Skill and file-tool smoke runs, but **MiMo has not yet passed equivalent Sanchuang Issue-to-Draft-PR E2E**. Do not claim that free-model catalog existence guarantees inference availability. Other Sanchuang repositories remain un-enrolled until their own callers are reviewed and tested. Use the [standard onboarding document](./free-worker-onboarding.md), not the limited Jianqu F01 caller.


## Legacy V1 route and lifecycle (historical)

- The reusable workflow is [`sanchuang-external-worker.yml`](../../.github/workflows/sanchuang-external-worker.yml), invoked explicitly from a repository-local `workflow_dispatch` caller **in a private calling repository**. GitHub does not permit public callers to use reusable workflows stored in private repositories.
- The only authorized model route is **`opencode/deepseek-v4.1-flash-free`** (OpenCode Zen). Fail closed if that free route disappears or fails; never silently use the paid `deepseek-v4.1-flash` model. Free access is time-limited and may change.
- Require a real *open* GitHub Issue; only human maintainer comments with verified write/maintain/admin authority can amend its implementation contract.
- Work from the caller's trusted `base_branch` into `feat/worker-<issue>-<run-id>-<attempt>`.
- The model can edit/run local commands in its isolated runner but cannot perform trusted Git mutations or deployment. The workflow owns isolated commit, branch push, trusted verification and **Draft** PR creation.
- No issue closure/reopening, merging, `dev → test → prod` promotion or production deployment. Review and final acceptance remain separate decisions.
- Log bounded, structured evidence for each run; do not equate a green Action with product acceptance.

## Legacy V1: private Organization access (historical contract)

The original Worker was built when `sanchuang-dev/.github` was private. The following token and copying rules document the **unchanged legacy V1** flow only. They are not requirements or recommendations for the new public-policy V2 flow.

The workflow's *trusted policy-loading step* requires a separate `organization_policy_token`, with read-only access to the `sanchuang-dev/.github` repository contents and metadata. It resolves `main` to an immutable commit at the beginning of policy loading, then fetches both `AGENTS.md` and `skills/execute-work-item/SKILL.md` from that same revision. The token is **not** passed to OpenCode.

Each calling application repo provides two secrets:

- `OPENCODE_API_KEY`: OpenCode Zen API key (only needed for model calls).
- `SANCHUANG_ORG_POLICY_READ_TOKEN`: narrowly scoped read-only fine-grained PAT or GitHub App credential with access to the private `.github` repository. Avoid Organization Owner or broad write permissions.

Because the called workflow is private, GitHub Actions settings for the `sanchuang-dev/.github` repository must also allow its reusable workflows to be used by other **private** repositories in the organization. This is an Organization/repository settings action, not a source-code change. Public repositories such as `dr-card-web` **cannot** invoke it, regardless of this setting.

These prerequisites are intentionally explicit: missing credentials or private workflow sharing means the caller is **not ready**, not silently successful.

## Legacy V1: public repository exception

While the Organization repository was private, public callers such as `dr-card-web` needed a **managed, repository-local workflow copy**. Now that `sanchuang-dev/.github` is public, both public and private callers may opt in to **new V2** by immutable SHA after its own review/merge. The V1 managed copy remains in place until its own reviewed opt-in migration PR; it is not auto-replaced by Organization visibility changes.

`dr-card-web` is the initial public pilot: the manual dispatch workflow lives on its historical default branch `main` (GitHub UI registration requirement), while its code checkout and Draft PR base remain `dev`. Keep actual H5 product work on `dev`, not `main`. Do not generalize this pilot to `base-prototype`, which has independent client-demo branch rules.

## Legacy V1: private repository caller contract

Private callers must pin the reusable workflow to a verified commit SHA on `main`, use their documented base branch (normally `dev`), and define repository-owned verification commands. The `issue_number` input is supplied manually by an authorized dispatcher; untrusted Issue comments, pull_request events and external PR code must not automatically trigger a write-capable Worker.

Example:

```yaml
jobs:
  worker:
    permissions:
      contents: write
      issues: read
      pull-requests: write
    uses: sanchuang-dev/.github/.github/workflows/sanchuang-external-worker.yml@<40-character-main-commit>
    with:
      issue_number: ${{ fromJSON(inputs.issue_number) }}
      base_branch: dev
      verification_command: |
        npm ci --no-audit --no-fund
        npm run lint
        npm run typecheck
        npm test
        npm run build:dev
    secrets:
      opencode_api_key: ${{ secrets.OPENCODE_API_KEY }}
      organization_policy_token: ${{ secrets.SANCHUANG_ORG_POLICY_READ_TOKEN }}
```

Do not add a global dispatch that can affect every repository. Each private repository opts in with its own verified caller and tests. Public repositories receive a separately reviewed, provenance-tracked local copy. Repository-specific exceptions such as `base-prototype` client-demo branches are **not** covered by the default `dev` assumption.

## Evidence and secrets

The worker uses Mira's bounded metadata-only trajectory, stage/verification summaries and 14-day Actions artifact pattern. Never persist raw prompts, token values, or unsanitized session transcripts as evidence. Policy read credentials belong to trusted workflow steps; provider API credentials are supplied only to the model execution process. Future model/provider changes require an explicit maintainer decision and workflow review.
