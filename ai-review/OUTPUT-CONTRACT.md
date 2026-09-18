# Sanchuang AI Review Output Contract

Contract version: `sanchuang-ai-review-output/v1`

Published reviews use this marker exactly once:

```text
<!-- sanchuang-ai-review:v1 -->
```

## Required logical sections

1. Verdict
2. Findings
3. Validation gaps
4. Review metadata

## Verdict

Exactly one of:

```text
NO_BLOCKING_FINDINGS
CHANGES_NEEDED
HUMAN_CHECK_NEEDED
CONTRACT_CONFLICT
```

## Findings

Only high-confidence P0-P2 findings are normally published.

Each actionable finding includes:

```text
Severity
Observation
Inference
Judgment
Impact
Location
Suggested Fix
Verification
```

Do not duplicate one root cause across several findings. Do not echo credentials or secrets.

When no P0-P2 issue is established, say so explicitly instead of manufacturing low-confidence concerns.

## Validation gaps

Record material evidence that was unavailable or not performed and that affects confidence or acceptance.

A missing check is not automatically a defect.

## CONTRACT_CONFLICT

Identify the conflicting sources, the smallest conflicting requirements, why they alter judgment, and the Maintainer decision needed to resume review.

## Review metadata

The deterministic gateway/publisher attaches:

- repository and PR number;
- head SHA and base SHA;
- provider / engine;
- model when applicable;
- Organization policy identity;
- repository review-profile identity when applicable;
- gateway/runtime version;
- review timestamp.

Provider-native scores, approval states, prose summaries, or severity names are not authoritative unless normalized into this contract.

A result whose recorded identity no longer matches the current PR/control state is stale.
