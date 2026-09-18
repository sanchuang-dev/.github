# Testing Standard

Policy revision: `2026-09-18.1`

This is the Organization-wide minimum testing philosophy for `sanchuang-dev`. Concrete commands, runners, environments, and required CI jobs belong in each repository.

## Principles

### Test the claim

Verification should prove the behavior, contract, boundary, or failure mode that matters to the task.

Do not use a passing lower-level test as evidence for a higher-level behavior it cannot prove.

### Use the lowest sufficient evidence

Prefer the cheapest reliable verification that can actually decide the claim.

Examples:

- pure logic change: focused unit test may be sufficient;
- API contract change: contract or integration evidence is usually needed;
- UI interaction change: component, integration, or device/browser evidence may be needed;
- deployment change: workflow success alone may be insufficient if runtime behavior matters.

### Do not mock away the subject under test

Mocks and fakes are useful for unrelated external boundaries. They must not replace the behavior being claimed as verified.

### Bugs should leave regression evidence when practical

If a defect is deterministic and cheap to reproduce, add evidence that would fail for the old behavior and protect the fix from returning.

### Never make failure green by weakening verification

Do not skip, delete, disable, loosen, swallow, or over-mock merely to obtain a passing result.

If a check is obsolete, change or retire it for an explicit reason.

### Verification strength follows risk

Use stronger evidence for changes involving:

- authentication or authorization;
- secrets and credentials;
- persistence or migration;
- destructive operations;
- external side effects;
- deployment and infrastructure;
- public API or schema contracts;
- concurrency or background execution.

### Evidence belongs to the thing tested

A result must correspond to the relevant commit, build, environment, device, artifact, or deployment.

Evidence from another version or another layer must not be represented as proof for the current one.

### Coverage is diagnostic

Coverage can reveal gaps, but a global percentage is not an Organization goal by itself.

Prefer meaningful protection of critical contracts, failure paths, and user journeys.
