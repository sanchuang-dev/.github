# Sanchuang External Worker

Owner: `sanchuang-dev/.github`. Execution contract: [Execute Work Item](../../skills/execute-work-item/SKILL.md).
Reference implementation: Mira's reusable External Worker, adapted to Sanchuang's **private** governance repository and its environment/permission model.

## Route and lifecycle

- The reusable workflow is [`sanchuang-external-worker.yml`](../../.github/workflows/sanchuang-external-worker.yml), invoked explicitly from a repository-local `workflow_dispatch` caller **in a private calling repository**. GitHub does not permit public callers to use reusable workflows stored in private repositories.
- The only authorized model route is **`opencode/deepseek-v4.1-flash-free`** (OpenCode Zen). Fail closed if that free route disappears or fails; never silently use the paid `deepseek-v4.1-flash` model. Free access is time-limited and may change.
- Require a real *open* GitHub Issue; only human maintainer comments with verified write/maintain/admin authority can amend its implementation contract.
- Work from the caller's trusted `base_branch` into `feat/worker-<issue>-<run-id>-<attempt>`.
- The model can edit/run local commands in its isolated runner but cannot perform trusted Git mutations or deployment. The workflow owns isolated commit, branch push, trusted verification and **Draft** PR creation.
- No issue closure/reopening, merging, `dev → test → prod` promotion or production deployment. Review and final acceptance remain separate decisions.
- Log bounded, structured evidence for each run; do not equate a green Action with product acceptance.

## Private Organization access

The `sanchuang-dev/.github` repository is private. Its contents **must not** be made public just to make the Worker run.

The workflow's *trusted policy-loading step* requires a separate `organization_policy_token`, with read-only access to the `sanchuang-dev/.github` repository contents and metadata. It resolves `main` to an immutable commit at the beginning of policy loading, then fetches both `AGENTS.md` and `skills/execute-work-item/SKILL.md` from that same revision. The token is **not** passed to OpenCode.

Each calling application repo provides two secrets:

- `OPENCODE_API_KEY`: OpenCode Zen API key (only needed for model calls).
- `SANCHUANG_ORG_POLICY_READ_TOKEN`: narrowly scoped read-only fine-grained PAT or GitHub App credential with access to the private `.github` repository. Avoid Organization Owner or broad write permissions.

Because the called workflow is private, GitHub Actions settings for the `sanchuang-dev/.github` repository must also allow its reusable workflows to be used by other **private** repositories in the organization. This is an Organization/repository settings action, not a source-code change. Public repositories such as `dr-card-web` **cannot** invoke it, regardless of this setting.

These prerequisites are intentionally explicit: missing credentials or private workflow sharing means the caller is **not ready**, not silently successful.

## Public repository exception

GitHub Actions only supports public-to-public reusable workflow calls. Public Sanchuang repositories therefore require a **managed, repository-local workflow copy**, derived from this Organization-owned executor and revised only for the repository's trusted verification command, dispatch ref, and secret bindings. This is a runtime/distribution exception, **not** a second copy of the Organization constitution: the worker must still fetch the canonical private Organization `AGENTS.md` and Skill at one resolved commit for every execution.

`dr-card-web` is the initial public pilot: the manual dispatch workflow lives on its historical default branch `main` (GitHub UI registration requirement), while its code checkout and Draft PR base remain `dev`. Keep actual H5 product work on `dev`, not `main`. Do not generalize this pilot to `base-prototype`, which has independent client-demo branch rules.

## Private repository caller contract

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
