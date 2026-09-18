# Work Item Lifecycle

Status: active Organization guidance.

Sanchuang engineering work uses one GitHub Issue contract and one native Project lifecycle field.

## 1. One lifecycle field

`Sanchuang Development` uses native Project `Status`:

```text
Todo -> In Progress -> Done
```

Do not create a second lifecycle in labels, Issue prose, PR text, CI state, or environment branches.

## 2. Ownership boundaries

- **Issue** — goal, scope, acceptance criteria, decisions, evidence, outcome.
- **Project Status** — coarse management position only.
- **Project fields** — Priority, Effort, Start date, Target date and similar planning metadata.
- **PR / review / CI** — implementation and verification evidence.
- **Environment model** — code / deployment position, not lifecycle.

## 3. Status semantics

### Todo

The Issue is open but not under active execution. It may be newly captured, queued, paused, or waiting for an explicit start decision.

`Todo` does not authorize implementation.

### In Progress

The Issue is open and substantive execution has been explicitly authorized and is underway.

Review, CI, local verification, acceptance preparation, and temporary blockers do not need extra lifecycle columns.

### Done

The Issue is closed and no longer active.

`Done` means inactive. The Issue close reason owns the outcome:

- completed — accepted / finished;
- not planned — deliberately not completed;
- duplicate — superseded by another work item.

## 4. Blocked work

`Blocked` is a condition, not a fourth lifecycle state.

Record the blocker on the Issue. If work remains actively owned, keep `In Progress`. If it is deliberately paused and dequeued, return it to `Todo`.

## 5. Creation and intake

Creating a work item means creating the Issue contract in the repository that owns the work.

Issue creation requires explicit creation authority. Discussion, review findings, audit findings, or TODO discovery do not authorize autonomous Issue creation.

Organization intake should add open Issues to `Sanchuang Development`. Newly added work should begin at `Todo`.

Creating an Issue does not itself authorize implementation.

## 6. Starting work

When execution is explicitly authorized:

1. keep the Issue open;
2. move Project Status to `In Progress` when the capability is available;
3. create a work branch from the correct repository/environment base when needed;
4. execute under the Issue, repository, testing, review, and environment contracts.

Do not infer `In Progress` merely from a branch name, PR, commit, CI run, or timestamp.

## 7. Review and verification

A PR merge, AI review verdict, human review, CI run, build, device check, deployment, or smoke result is evidence.

Evidence does not grant acceptance authority. Keep the Issue open while required verification or acceptance remains unresolved.

## 8. Environment promotion

Project Status does not encode `dev`, `test`, or `prod`.

If acceptance requires environment evidence, keep the Issue open until the required evidence exists unless promotion is owned by a separate work item.

Closing an implementation Issue does not by itself authorize promotion or release.

## 9. Acceptance and closure

Acceptance is an authority decision against the current Issue contract.

For an authorized completed outcome:

1. verify the exact acceptance criteria;
2. identify accepted gaps or exceptions;
3. record material evidence when useful;
4. close the Issue as completed;
5. Project Status should project the closed item as `Done`.

A merged PR or green CI is not an automatic closure trigger.

## 10. Reopening

Reopening requires explicit authority and does not itself authorize resumed implementation.

Default reopened position is `Todo`. If the same instruction explicitly authorizes immediate execution, use `In Progress`.

Automation may repair the unambiguous stale projection `open + reopened + Status=Done -> Todo`.
