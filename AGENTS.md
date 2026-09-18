# Sanchuang Development Organization AI Instructions

Policy revision: `2026-09-18.2`
Constitution: `v1.0`

This file is the canonical AI collaboration entry for repositories owned by the `sanchuang-dev` GitHub Organization.

It contains durable Organization rules plus routing to task-specific policy and Skills. Repository-specific architecture, commands, product boundaries, and exceptions belong in each repository.

## Constitution v1.0

### 1. Small and independently verifiable

Prefer the smallest coherent unit of work that can be implemented, reviewed, verified, and reverted without dragging unrelated work with it.

A task is not complete because code changed. It is complete only when the agreed outcome can be decided from concrete evidence.

### 2. One concern, one source of truth

Do not maintain the same decision independently in several places.

- code / configuration / workflow / runtime describe current technical reality;
- GitHub Issue owns the work-item contract and outcome;
- native GitHub Project `Status` owns coarse lifecycle position;
- Project fields own structured planning metadata;
- PR / review / CI own implementation and verification evidence;
- `feat/* -> dev -> test -> prod` owns environment position unless a repository documents an exception;
- Organization docs own shared policy and reusable SOPs;
- repository docs own repository-specific rules and exceptions.

When projections disagree, repair the stale projection instead of creating another copy.

### 3. Verify reality before inference

When current technical state matters, inspect the actual repository, workflow, configuration, branch, or runtime when practical.

Do not let remembered behavior, stale documentation, branch naming, or generic model knowledge override observable reality.

### 4. Authority is explicit

A role may act only within the authority granted by the current task and applicable contract.

Creating an Issue does not itself authorize implementation. Reviewing does not authorize editing, merging, acceptance, release, deployment, Project mutation, Issue closure, or reopen unless the current instruction or contract grants that authority.

Do not manufacture an extra confirmation round when the maintainer already granted multiple actions explicitly in one instruction.

### 5. Conflicts are surfaced

If current instructions, repository contracts, Organization policy, or observable reality materially disagree, identify the conflict. Do not silently invent a convenient interpretation.

### 6. Completion requires evidence

Never report an unexecuted test, build, deployment, review, device check, or smoke check as passed.

If required evidence is unavailable, record the validation gap explicitly and match verification cost to the changed surface.

### 7. Rules live with their owner

Organization-wide rules and reusable SOPs belong in `sanchuang-dev/.github`.

Repository-specific implementation constraints, build commands, product boundaries, branch exceptions, and deployment details belong in the owning repository.

### 8. Policy is current

Use the current retrieved version of this file when it is available. Do not substitute memory for current Organization policy.

## Coding guidance

1. Understand before changing: inspect relevant implementation, nearby types, tests, configuration, and active documentation.
2. Make the minimum coherent change required by the accepted outcome.
3. Preserve public contracts, schemas, persistence semantics, security boundaries, and deployment behavior unless the task explicitly changes them.
4. Prefer an existing working pattern over speculative abstraction.
5. Do not hide failure with swallowed errors, production mocks, disabled checks, hard-coded local values, or other false-green workarounds.
6. Comments should explain intent, invariants, constraints, or non-obvious tradeoffs rather than restating code.
7. Treat compatibility paths as liabilities that need an identified consumer and removal condition.
8. Put mechanical enforcement in tooling / CI when practical.

## Testing guidance

Shared principles live in [docs/engineering/testing-standard.md](docs/engineering/testing-standard.md).

Use the lowest sufficient evidence, but strengthen verification for authentication, permissions, secrets, persistence, migration, destructive operations, external side effects, signing, deployment, and public contracts.

## Start here

When working on a `sanchuang-dev` repository:

1. Retrieve the current version of this file.
2. Read the target repository's applicable `AGENTS.md` from the branch that actually owns the work, if one exists.
3. Read the current Issue / PR / explicit task contract.
4. Load only the Organization policy, SOP, or Skill relevant to the task.
5. Verify current technical claims against repository / workflow / configuration / branch / runtime evidence.

If current Organization guidance cannot be retrieved when required, say so explicitly instead of reconstructing it from memory.

## Instruction priority

1. current explicit maintainer/user instruction;
2. current Issue / PR / task contract;
3. applicable repository-specific `AGENTS.md`, policy, or documented exception;
4. applicable Organization policy / SOP / Skill from this repository;
5. generic engineering practice or model defaults.

A higher-priority instruction may change the requested outcome, but it cannot make an unverified technical claim true.

## Organization routing

| Task | Read |
| --- | --- |
| Create or record an engineering work item | [skills/create-work-item/SKILL.md](skills/create-work-item/SKILL.md) |
| Verify for acceptance, close, decline, duplicate, or reopen work | [skills/close-work-item/SKILL.md](skills/close-work-item/SKILL.md) |
| Work-item lifecycle / Project Status | [docs/governance/work-item-lifecycle.md](docs/governance/work-item-lifecycle.md) |
| Determine source-of-truth boundaries | [docs/governance/source-of-truth.md](docs/governance/source-of-truth.md) |
| Repository / team permissions and production authority | [docs/governance/permissions-model.md](docs/governance/permissions-model.md) |
| Branch / environment promotion | [docs/engineering/environment-model.md](docs/engineering/environment-model.md) |
| Testing and evidence | [docs/engineering/testing-standard.md](docs/engineering/testing-standard.md) |
| Organization AI PR Review | [ai-review/POLICY.md](ai-review/POLICY.md) and [ai-review/OUTPUT-CONTRACT.md](ai-review/OUTPUT-CONTRACT.md) |
| AI Review execution architecture | [ai-review/GATEWAY.md](ai-review/GATEWAY.md) |

## Stop conditions

Stop and report the gap instead of guessing when:

- required Organization guidance cannot be retrieved;
- the target repository or owning surface is ambiguous;
- a repository contract conflicts materially with Organization policy and precedence does not resolve the intended action;
- Issue creation, acceptance, closure, merge, deployment, release, or destructive mutation lacks authority;
- required evidence is unavailable but necessary to claim completion or safety.
