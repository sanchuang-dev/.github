# Permissions Model

Policy revision: `2026-09-18.2`

This is the target access model for `sanchuang-dev`. It is deliberately stricter around release and infrastructure than around ordinary development.

## 1. Organization owners

Organization Owner is exceptional authority.

Target:

- company principal: Owner;
- designated technical owner: Owner;
- ordinary engineers: not Owners.

Owners exist for Organization administration, recovery, policy, billing/security settings, and exceptional repository administration. Do not use Owner as a convenience substitute for repository/team permissions.

## 2. Team model

Create these teams as the Organization grows:

| Team | Repository role / purpose |
| --- | --- |
| `engineering` | normal engineers; Write on assigned application repositories |
| `mobile-maintainers` | Maintain on Android/iOS; review and repository stewardship |
| `infra-maintainers` | Maintain on gateway/infrastructure repositories |
| `release-managers` | narrow group allowed to perform production promotion/deployment |
| `qa-reviewers` | Triage/Read where review/acceptance does not require code write |
| automation identities | GitHub Apps / Actions with explicit machine permissions only |

A person may belong to several teams; do not solve every responsibility by granting Admin.

## 3. Base permission

Target Organization base permission: `None` or `Read`.

Never use Organization-wide `Write` merely because the team is currently small. Grant write authority through teams/repositories so future membership does not silently widen access.

## 4. Repository matrix

### dr-card-android / dr-card-ios

- engineering: Write
- mobile-maintainers: Maintain
- release-managers: Maintain; production release authority supplied separately by rules/environment controls
- qa-reviewers: Triage or Read
- Owners: emergency/admin authority

### 3chuang-ai-gateway

- engineering: Read by default
- infra-maintainers: Maintain
- release-managers: Maintain/Admin only if repository settings require it
- ordinary mobile developers: no implicit write
- Owners: emergency/admin authority

The gateway is a sensitive infrastructure repository and should have a smaller write set than application code.

## 5. Branch and ruleset target

### dev

- changes normally arrive through PR;
- prevent deletion and force push;
- require relevant CI checks once the repository has meaningful CI;
- Maintainers may retain a narrowly scoped bypass for recovery.

### test

- promotion normally comes from `dev`;
- prevent deletion and force push;
- require PR and required checks;
- direct feature work on `test` is not normal.

### prod

- promotion comes from `test` or a documented repository-specific release gate;
- prevent deletion and force push;
- require PR;
- require all relevant checks;
- require release authority / environment approval where available;
- bypass is restricted to Owners for emergency recovery.

A repository-specific validation branch such as `check` may add a stricter gate but must not create an undocumented way around `prod`.

## 6. Environment authority

### dev

Normal developers may contribute under repository rules.

### test

Promotion authority is narrower than feature development. Direct ad-hoc implementation should not occur here.

### prod

Only Owners, Release Maintainers, or explicitly trusted automation may promote/deploy production.

Production credentials must not be exposed to ordinary feature branches.

## 7. Secrets

Prefer the narrowest workable scope:

1. environment-scoped secrets for production-only credentials;
2. repository secrets for credentials owned by one repository;
3. Organization secrets only when multiple repositories truly share the same credential, restricted to an explicit repository set.

Never place production credentials in source, Issues, PR text, AI review output, workflow logs, or agent instructions.

## 8. Automation permissions

Automation must receive the minimum required GitHub permissions.

Examples:

- CI: contents read;
- Issue intake: issue/project write only where required;
- review publisher: PR/Issue comment write but no code write;
- deployment: contents read plus environment/repository secrets, not Organization Owner authority.

Provider credentials for AI review must be isolated from PR-controlled code.
