# AI Review Gateway

Status: Organization contract established; execution backend may be wired independently.

The Sanchuang AI Review Gateway is a provider-independent review pipeline. It exists so review semantics do not belong to one model vendor or GitHub App.

## Pipeline

```text
PR event
  -> trusted context resolver
  -> base/head identity binding
  -> repository review profile + Organization policy
  -> provider adapter
  -> normalized output validator
  -> publisher
  -> stale-result detector
```

## Trust rules

1. PR head content is untrusted input.
2. Organization policy comes from the trusted `sanchuang-dev/.github` source.
3. Repository review controls come from the trusted base SHA unless an Organization control explicitly says otherwise.
4. Provider credentials and GitHub publication credentials never enter PR-controlled execution.
5. Review is read-only and advisory.
6. The gateway validates output against [OUTPUT-CONTRACT.md](OUTPUT-CONTRACT.md) before publication.

## Provider adapter

A provider adapter may call OpenAI, Codex, CodeRabbit, Claude, OpenCode, or another engine.

Adapters may differ in transport and prompt packaging, but they must not change Organization severity, verdict, trust, identity, or publication semantics.

## Repository review profile

A repository may define additional review scope and acceptance context on a trusted base branch, for example:

```text
.github/ai-review/profile.md
```

A profile may refine platform-specific risks, critical paths, commands, or required evidence. It may not weaken gateway credential isolation or read-only boundaries.

## Publication

The publisher should update or replace the current Organization review result for the exact PR head rather than accumulating several apparently-current verdicts.

Historical stale reviews may remain visible but must be marked stale by identity.

## Execution boundary

The governance repository owns this contract. A concrete gateway service or reusable workflow may live elsewhere as long as it consumes the current Organization policy and produces the normalized output contract.

Do not claim that automated AI Review is active until an actual trigger, provider credential, runtime, publisher, and stale-detection path have been verified end to end.
