---
name: create-work-item
description: Create a Sanchuang engineering work item only with explicit authority, a verifiable contract, and a valid Project #1 projection.
---

# Create Work Item

Use this Skill when a maintainer explicitly asks to create or record an engineering work item.

## Authority

Issue creation is a repository mutation and requires explicit creation authority.

Discussion, review findings, audits, TODO discovery, or a recommendation that something should be tracked do not authorize autonomous Issue creation.

One instruction may authorize creation and later actions together, for example: "建卡然后开始做". Do not invent a second confirmation if authority is already explicit.

Creating an Issue does not automatically authorize implementation, merge, deployment, release, acceptance, closure, or reopen.

## Work-item kind

Choose exactly one before writing the Issue.

### Implementation slice

Use this for work that may be executed directly.

An implementation slice must be the smallest coherent unit that can be implemented, reviewed, verified, and reverted independently without dragging an unrelated outcome with it.

It should normally have:

- one owning repository;
- one explicit implementation base branch;
- one bounded outcome;
- observable acceptance criteria;
- proportionate evidence;
- one implementation branch / PR unless the task contract explicitly requires otherwise.

If two parts can land, verify, or roll back independently, prefer two slices.

### Milestone shell

Use this for a human-verifiable outcome that spans several implementation slices.

A milestone shell:

- is not a direct coding-agent assignment;
- is not implemented as one broad PR;
- keeps the larger outcome and human acceptance contract;
- must contain an `Implementation slices` section linking the small executable child Issues.

If decomposition has not happened yet, write that explicitly and do not start implementation from the parent.

Do not use a milestone shell as a disguised implementation task.

## Procedure

1. retrieve current Organization `AGENTS.md`;
2. determine the owning repository;
3. read the repository's applicable `AGENTS.md`;
4. inspect actual code/config/workflow/runtime when current facts matter;
5. search for an existing Issue and existing PR that already own the same outcome;
6. choose `Implementation slice` or `Milestone shell`;
7. write one coherent Issue contract;
8. create the Issue in the owning repository;
9. verify that Organization Project intake projects the Issue into Project `#1` when Project access is available;
10. if the same instruction authorizes implementation, start only from an implementation slice and verify the implementation base before substantive work.

Do not assume Project intake succeeded merely because an Actions workflow is green. Verify the Issue is actually present in Project `#1`, or report the projection gap.

## Issue contract

Use these sections:

- Work item kind
- Goal
- Context
- Scope
- Non-goals when useful
- Acceptance criteria
- Verification / evidence
- Dependencies / risks when material
- Implementation slices for a milestone shell

### Implementation-slice context

For an implementation slice, Context should identify:

- the parent milestone / owning outcome when one exists;
- the explicit implementation base, normally `dev` under the Organization environment model;
- any dependency that must already be true.

Do not rely on the repository default branch to imply the implementation base.

### Acceptance and evidence

Acceptance criteria must be observable and independently decidable for this work item.

Required evidence must be proportionate to the changed surface and must prove the claimed behavior. CI and AI Review may supplement behavioral evidence but do not replace it.

Do not write unexecuted tests, deployments, browser checks, device checks, or external-service checks as passed.

Do not invent a lifecycle state such as `Ready for acceptance`. When implementation evidence is complete but acceptance authority is not granted, leave the Issue open and state that acceptance/closure remains with the authorized maintainer.

## Coding-agent / PR guard

When a coding agent may create a PR automatically:

1. search for an existing PR for the Issue before opening another one;
2. reuse the existing PR when it is the valid implementation vehicle;
3. verify that its base branch matches the Issue's explicit implementation base;
4. correct or stop on a wrong base before substantive review/merge work continues;
5. do not create a second PR merely because the first one was created by an agent.

A coding-agent PR created against `main` does not override an Issue contract that says the implementation base is `dev`.

If a stale duplicate PR already exists, do not treat it as current implementation evidence. Close or supersede it only with authority for that PR mutation.

## Metadata

Do not duplicate Project Status, Priority, Effort, dates, assignees, or linked-PR metadata in the Issue body.

Project Status owns coarse lifecycle position. Environment branches own environment position. PR / review / CI own implementation evidence.
