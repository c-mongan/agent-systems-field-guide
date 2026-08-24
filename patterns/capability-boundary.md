---
id: capability-boundary
status: recommended
evidence:
  - mcp-boundary
---
# Capability boundary

Expose a meaningful capability rather than every low-level implementation function.

## Problem

Large tool catalogues often mirror internal APIs. The model must reconstruct the client library through many calls, and several tools appear equally relevant.

## Pattern

Group operations around user intent and a compact result.

Prefer:

```text
correlate-incident-evidence
plan-package-release
validate-auth-configuration
```

Over:

```text
get-row
get-next-row
sort-row
join-row
count-row
```

## Local or MCP

Keep the capability local when one application owns both sides and no separate identity or lifecycle is needed. Use MCP when several clients need a shared remote, authenticated, versioned capability.

## Contract

Document:

- activation intent;
- allowed inputs;
- permission and side effects;
- output schema;
- timeout and truncation;
- error categories;
- provenance.

## Proof

Measure routing accuracy, calls per task, latency, result size, and operational burden.

**Evidence:** `mcp-boundary`, `scripts-for-determinism`
