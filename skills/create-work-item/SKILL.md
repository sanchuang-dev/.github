---
name: create-work-item
description: Create a Sanchuang engineering work item only with explicit authority and a verifiable contract.
---

# Create Work Item

Use this Skill when a maintainer explicitly asks to create or record an engineering work item.

## Authority

Issue creation is a repository mutation and requires explicit creation authority.

Discussion, review findings, audits, TODO discovery, or a recommendation that something should be tracked do not authorize autonomous Issue creation.

One instruction may authorize creation and later actions together, for example: "建卡然后开始做". Do not invent a second confirmation if authority is already explicit.

## Procedure

1. retrieve current Organization `AGENTS.md`;
2. determine the owning repository;
3. read the repository's applicable `AGENTS.md`;
4. inspect actual code/config/workflow/runtime when current facts matter;
5. search for an existing Issue that already owns the same outcome;
6. write one coherent Issue contract;
7. create the Issue in the owning repository;
8. allow Organization Project intake to project it into `Todo`.

## Issue contract

Use:

- Goal
- Context
- Scope
- Non-goals when useful
- Acceptance criteria
- Verification / evidence
- Dependencies / risks when material

Acceptance criteria must be observable. Required evidence must be proportionate to the changed surface.

Do not write unexecuted tests or deployments as passed.

## Metadata

Do not duplicate Project Status, Priority, Effort, dates, assignees, or linked-PR metadata in the Issue body.

Creating the Issue does not automatically authorize implementation, merge, deployment, release, acceptance, closure, or reopen.
