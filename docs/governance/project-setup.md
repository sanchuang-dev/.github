# Organization Project Setup

Status: active Organization Project contract.

## Canonical Project

Organization Project `#1` is the canonical management board for `sanchuang-dev`.

The stable identity is the Project number, not its display name.

## Status

Use GitHub's native/default `Status` field as the only lifecycle field.

```text
Todo -> In Progress -> Done
```

Do not add a second lifecycle in labels, Issue prose, environment branches, or duplicate custom fields.

Keep the default Status setup unless a concrete workflow need appears.

## Optional fields

Additional fields such as Priority, Effort, Start date, or Target date are optional. Do not add them merely for ceremony.

## Semantics

- new open work item -> Todo
- explicitly started work -> In Progress
- closed Issue -> Done
- blocked but actively owned -> remain In Progress
- deliberately paused/dequeued -> Todo
- reopened Issue left at Done -> automation may repair it to Todo

The Issue close reason carries whether Done means completed, not planned, or duplicate.

## Automatic intake

`.github/workflows/project-auto-add.yml` is bound directly to Organization Project `#1`.

It periodically adds open Issues from `sanchuang-dev` that are not yet present in the Project.

The Project number is committed in the workflow; no Project-number repository variable is required.

To activate Project mutation, configure the repository secret `ORG_GITHUB_TOKEN` on `sanchuang-dev/.github` with access to the Organization Project and Organization Issues.

If that credential is absent, the workflow exits safely without Project mutation.

## Boundary

Project automation owns management projection only. It must not infer implementation authority, acceptance authority, release authority, production readiness, or Issue closure.
