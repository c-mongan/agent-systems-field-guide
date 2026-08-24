# MCP

Model Context Protocol (MCP) is a protocol boundary for external tools and context sources.

Use it when the capability benefits from a reusable client-server contract. Do not use it only because “agent tools should be MCP.”

## MCP earns its cost when

- several agents, products, or teams need the same capability;
- the capability is remote or has its own lifecycle;
- authentication and identity must be separated from the agent process;
- schemas and versioning need a stable contract;
- centralized auditing or policy enforcement matters;
- the capability must be discovered dynamically;
- deployment independence is valuable.

Example: a company-wide customer-data service used by several assistants may deserve an MCP boundary. A local helper that reads one repository file probably does not.

## Costs introduced by MCP

MCP adds real operational work:

- server deployment or process management;
- authentication and authorization;
- network or transport failure;
- version compatibility;
- schema changes;
- rate limits;
- observability;
- secret handling;
- availability and support ownership.

A protocol is not free simply because the interface looks clean.

## MCP versus a local script

Use a local script or library when:

- one repository owns the caller and implementation;
- there is no separate identity boundary;
- data is local;
- deployment independence has no value;
- a function call is easier to test and operate.

Use MCP when the capability is shared, remote, separately secured, or independently operated.

## Keep the tool surface narrow

An MCP server should expose meaningful capability boundaries, not every internal function.

Prefer:

```text
search-incidents
fetch-approved-evidence
create-change-request
```

Avoid dozens of near-identical low-level operations that force the model to reconstruct a client library through tool calls.

## Security and governance

For every server, document:

- who may call it;
- what data it can read or change;
- whether calls have side effects;
- approval requirements;
- audit records;
- timeout and retry rules;
- data retention;
- how tool descriptions are reviewed for prompt injection or ambiguity.

Treat server output as untrusted external data unless the source and contract justify more trust.

## Measure the boundary

Track:

- success and error rate;
- end-to-end latency;
- server availability;
- tool-selection accuracy;
- schema and version failures;
- authentication failures;
- duplicate or unsafe side effects;
- operational burden compared with a local alternative.

**Evidence:** `mcp-boundary`, `skill-security-review`
