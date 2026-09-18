# Permissions Model

Policy revision: `2026-09-18.2`

This document defines the target access model for `sanchuang-dev`. Apply least privilege without turning ordinary development into ceremony.

## Principles

- Organization Owner is an exceptional role, not a normal engineering permission.
- Day-to-day access should be granted through teams and repository roles.
- Production authority is narrower than development authority.
- Secrets and deployment credentials belong to the narrowest repository/environment scope that can support the workflow.
- Automation receives only the permissions required for its job.

## Organization roles

| Role | Intended users | Normal authority |
| --- | --- | --- |
| Owner | company principal + designated technical owner | Organization administration, emergency recovery, billing/security settings |
| Release Maintainer | small trusted release group | Maintain/Admin only where production workflows require it; production promotion |
| Maintainer | technical leads / repository maintainers | Maintain on owned repositories, triage/review, workflow stewardship |
| Developer | ordinary engineers | Write on assigned repositories, feature branches, PRs |
| Reviewer / QA | review or acceptance participants | Triage or Read unless code changes are part of their job |
| Automation | GitHub Apps / Actions / bots | explicit machine permissions only |

## Base permissions

Target Organization base permission: `None` or `Read`.

Do not use Organization-wide `Write` merely because the team is small. Give write access through repository teams.

## Repository roles

- `Read`: inspect code and evidence.
- `Triage`: manage Issues / PR metadata without code write authority.
- `Write`: normal implementation.
- `Maintain`: repository stewardship without unnecessary destructive Organization authority.
- `Admin`: exceptional; use for repositories that truly require settings/secrets/rules management.

## Environment authority

### dev

Normal developers may contribute through PRs and repository workflows.

### test

Promotion should come from `dev`. Direct ad-hoc work on `test` is discouraged.

### prod

Production promotion is restricted to Owners / Release Maintainers or an explicitly trusted automation path.

Production deployment credentials must not be exposed to ordinary feature branches.

## Sensitive repositories

Infrastructure, gateway, signing, release, identity, billing, or credential-management repositories should use narrower Admin and secret access than ordinary application repositories.

## Secrets

Prefer, in order:

1. environment-scoped secrets for production-only credentials;
2. repository secrets for credentials owned by one repository;
3. Organization secrets only when several repositories genuinely share the same credential and access can be restricted to an explicit repository set.

Never place production credentials in source, Issue text, PR text, review output, logs, or agent instructions.

## Branch / ruleset target

For environment branches:

- prevent force push and deletion;
- require PR-based promotion where practical;
- require relevant checks before promotion;
- use stricter review / deployment controls as code moves toward `prod`;
- do not let a feature branch deploy production.

Repository-local exceptions must document why the same safety property is preserved another way.
