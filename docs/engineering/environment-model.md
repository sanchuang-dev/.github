# Environment Model

Policy revision: `2026-09-18.2`

This document defines the Organization default branch-to-environment convention.

## Standard flow

```text
feat/* -> dev -> test -> prod
```

### feat/*

Isolated feature or fix work.

- CI only.
- Must not deploy to a shared production runtime.
- Normally merges into `dev`.

### dev

Development integration.

- receives completed feature work;
- runs CI;
- may deploy to a dedicated development environment;
- is the normal base for new engineering work unless a repository documents otherwise.

### test

Test and acceptance.

- receives promotion from `dev`;
- runs CI;
- may deploy a dedicated test environment;
- is used for regression, smoke, and acceptance checks before production.

### prod

Production source.

- receives promotion from `test`;
- runs required production checks;
- is the only standard environment branch allowed to deploy production;
- production health / smoke verification should run after deployment where practical.

## main

`main` is not an environment name.

A repository may retain `main` for history, compatibility, a landing README, or external tooling. It must not silently bypass `prod` and deploy production.

The GitHub default branch is a UI/workflow choice, not the definition of production.

## Promotion

Promote an already-reviewed change through environments instead of rebuilding unrelated changes at each stage:

```text
feat/* -> dev -> test -> prod
```

High-risk repositories may require additional approval or a validation branch between `test` and `prod`.

## Repository exceptions

A repository may retain additional branches such as archival, compatibility, release-check, or vendor baselines.

The repository must document:

- the extra branch's purpose;
- whether it is mutable;
- where it sits relative to `dev/test/prod`;
- what safety property it adds or replaces.

Do not infer semantics from a branch name alone.
