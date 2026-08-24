# Reproducible example — Authentication security review

An account portal changes session-cookie and OAuth configuration.

The example runs exact policy checks before any open-ended security reasoning.

## Architecture

```text
Policy + configuration
        ↓
Deterministic checks
        - Secure / HttpOnly / SameSite
        - PKCE
        - exact redirect URI allowlist
        - browser token storage
        ↓
Structured findings + explicit not-checked list
        ↓
Security-review skill
        - inspect code and flow evidence
        - load OAuth or session references
        - judge exploitability and business context
        - rank remediation
```

## What code owns

[`run.py`](run.py) compares configuration against an explicit policy. Every finding has:

- stable code;
- severity;
- exact evidence;
- concrete fix.

It also lists areas not checked, such as identity-provider tenant policy and network controls.

## What an agent should own

A real security agent may:

- determine whether the configured flow matches the deployed code;
- inspect token lifecycle and logout behaviour;
- assess compensating controls;
- identify missing runtime evidence;
- prioritize findings by exposure and user impact;
- refuse to claim full coverage when important systems were not inspected.

## Run

```bash
python examples/security-review/run.py \
  examples/security-review/fixtures/input.json
```

Expected output is frozen in [`expected/output.json`](expected/output.json).

## Security lesson

Use code for policy checks with objective answers. Use agent judgment for evidence gaps, exploit paths, trade-offs, and prioritization. Do not ask the model to “remember” an allowlist or count configuration failures from prose.
