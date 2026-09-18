# Source of Truth

Policy revision: `2026-09-18.2`

Sanchuang uses different sources of truth for different kinds of information. No single surface is authoritative for everything.

## 1. Current technical reality

For what currently exists or runs, prefer:

1. runtime / deployed environment when the claim is about runtime behavior;
2. code, configuration, dependency manifests, workflow definitions, and current branch state;
3. repository-local technical documentation;
4. Organization documentation;
5. historical discussion and memory.

Documentation does not override observable runtime or repository reality.

## 2. GitHub Issue — work-item contract and outcome

An Issue owns the agreed goal, scope, non-goals, acceptance criteria, contract-changing decisions, evidence links, and final open/closed outcome for one work item.

Do not duplicate Project Status, assignees, dates, or linked PR metadata in prose merely to make the Issue look complete.

Issue truth and Issue mutation authority are separate: observable completion does not by itself authorize closure or acceptance.

## 3. GitHub Project — management projection

Organization Project `#1` uses GitHub's native Project `Status` only for coarse lifecycle position:

```text
Todo | In Progress | Done
```

Project custom fields own structured planning metadata such as Priority, Effort, Start date, and Target date.

Project Status is not Issue acceptance and is not an environment name.

## 4. PR / review / CI — implementation evidence

PR diffs, review results, checks, builds, tests, artifacts, and smoke results are evidence.

They do not automatically accept an Issue, authorize production promotion, or create outcome authority.

## 5. Environment position

The Organization default environment model is:

```text
feat/* -> dev -> test -> prod
```

Repository-local exceptions may add compatibility or validation branches, but must document their meaning. Project Status must not be used as an alias for environment position.

## 6. Organization docs — policy and reusable SOPs

`sanchuang-dev/.github` owns Organization-wide policy, shared Skills, lifecycle rules, environment conventions, testing principles, permissions guidance, and AI Review contracts.

## 7. Repository docs — repository-specific truth

Repository-specific architecture, commands, build systems, signing rules, product boundaries, environment exceptions, and deployment details belong in that repository.

## Conflict rule

When sources disagree, first identify which concept is stale and repair that projection.

```text
Issue              = work-item contract + outcome
Project Status     = Todo / In Progress / Done management position
Project fields     = Priority / Effort / dates
PR / Review / CI   = implementation + verification evidence
feat/dev/test/prod = environment position
.github/docs       = Organization policy and SOP
repo/config/runtime= current technical reality
```

Authority conflicts are resolved by the instruction-priority model in `AGENTS.md`, not by whichever source looks most complete.
