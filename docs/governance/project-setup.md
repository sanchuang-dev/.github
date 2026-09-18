# Sanchuang Development Project Setup

Status: target Project contract. The repository workflow is already staged and becomes active when the Project number and credential are configured.

## Project

Create one Organization Project:

```text
Sanchuang Development
```

Recommended visibility: private.

## Native Status

Keep exactly three lifecycle values:

```text
Todo
In Progress
Done
```

Do not add Blocked, Review, Verification, Ready to Ship, dev, test, or prod as lifecycle columns. Those concepts belong elsewhere.

## Planning fields

Recommended fields:

- Priority: Urgent / High / Normal / Low
- Effort: S / M / L / XL
- Start date
- Target date

These fields are planning metadata, not Issue acceptance criteria.

## Semantics

- new open work item -> Todo
- explicitly started work -> In Progress
- closed Issue -> Done
- blocked but actively owned -> remain In Progress
- deliberately paused/dequeued -> Todo
- reopened Issue left at Done -> Organization automation repairs to Todo

The Issue close reason carries whether Done means completed, not planned, or duplicate.

## Automatic intake

The workflow at:

```text
.github/workflows/project-auto-add.yml
```

runs every five minutes and adds open Issues from `sanchuang-dev` that are not yet in the Project.

It is currently safe to commit before the Project exists: when required configuration is missing, the workflow exits successfully without mutation.

To activate it, configure on `sanchuang-dev/.github`:

- repository variable `SANCHUANG_PROJECT_NUMBER` = the Organization Project number;
- repository secret `ORG_GITHUB_TOKEN` = a credential with permission to read/write the Organization Project and read Organization Issues.

The credential must not be exposed to PR-controlled code.

## Project automation boundary

Project automation owns management projection only.

It must not infer:

- implementation authority;
- acceptance authority;
- release authority;
- production readiness;
- Issue closure.

Those decisions remain governed by the Issue contract, Organization policy, repository policy, and explicit maintainer authority.
