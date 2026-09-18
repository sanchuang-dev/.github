---
name: close-work-item
description: Verify, accept, close, decline, duplicate, or reopen Sanchuang work items without inferring outcome authority from implementation evidence.
---

# Close Work Item

## Authority first

Closing or reopening an Issue changes the recorded outcome and requires explicit authority.

Do not infer closure authority merely because implementation finished, a PR merged, AI review found no blockers, CI passed, deployment succeeded, or acceptance criteria appear satisfied.

## Re-read the contract

Before deciding an outcome:

1. retrieve current Organization `AGENTS.md`;
2. read applicable repository instructions;
3. read the current Issue and material contract-changing comments;
4. read the work-item lifecycle;
5. inspect the evidence required by the current acceptance criteria.

## Evidence vs acceptance

Evidence answers whether criteria are supported. Acceptance is the authorized decision that the contract is satisfied.

For every material criterion, identify evidence or an explicit accepted gap.

## Outcomes

- `completed` — authorized and criteria satisfied, or an authorized maintainer explicitly accepts the gap.
- `not_planned` — explicitly decided not to complete under this Issue.
- `duplicate` — canonical replacement work item is identifiable.

Blocked, paused, stale, or difficult does not automatically mean `not_planned`.

## Reopen

Reopening requires explicit authority. Default Project position is `Todo`; use `In Progress` only when the same instruction also authorizes resumed execution.

Reopen alone does not authorize implementation.

## Settlement verification

After an authorized closure or reopen, verify the recorded Issue outcome and, when Project access is available, verify the Organization Project `#1` projection matches the native lifecycle contract: closed Issues are `Done`; reopened Issues are `Todo` unless the same authority also resumed execution. Do not treat a successful mutation response or a green synchronization workflow as proof of a correct ledger projection. Report any projection gap explicitly.
