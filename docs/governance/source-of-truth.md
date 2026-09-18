# Source of Truth

Policy revision: `2026-09-18.1`

This document defines where different kinds of truth live inside `sanchuang-dev`.

## Current technical reality

Use this order when deciding what currently exists or runs:

1. runtime and deployed environment, when the claim is about runtime behavior;
2. code, configuration, dependency manifests, and workflow definitions;
3. repository-local technical documentation;
4. Organization documentation;
5. comments, historical discussion, and memory.

A document saying that a workflow exists is not stronger evidence than the workflow file itself.

## Work-item truth

For a specific task:

1. the user's current explicit instruction defines current authority and requested action;
2. the current Issue / PR / task contract defines the agreed work-item scope and outcome;
3. PR diff, review, CI, build, and deployment results provide implementation and verification evidence.

Implementation evidence does not automatically authorize merge, deployment, release, Issue closure, or acceptance.

## Repository ownership

Repository-specific architecture, build commands, branch semantics, environment mappings, secrets usage, deployment procedure, and product boundaries belong to the repository that owns them.

Organization policy must not silently invent repository-specific facts.

## Conflict handling

When sources disagree:

- prefer observable current reality for factual claims;
- prefer the current explicit task contract for requested outcome;
- surface material conflicts instead of silently choosing the most convenient interpretation;
- repair stale documentation when authorized rather than duplicating contradictory truth elsewhere.
