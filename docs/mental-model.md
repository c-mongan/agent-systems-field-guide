# Mental model

An agent system becomes easier to design when each primitive owns one type of problem.

```text
Knowledge   → reference
Procedure   → skill
Action      → script, tool, MCP, or hook
Control     → workflow
Isolation   → subagent or specialist agent
```

The primitives can compose. They should not collapse into one large prompt.

![Primitive map](../diagrams/primitive-map.svg)

## The five questions

Ask these questions in order.

### 1. Can normal code do it exactly?

Use code for parsing, filtering, joins, graph traversal, validation, counting, ordering, and other bounded work. Code is easier to test and cheaper to repeat. Let the model interpret the compact result instead of making it perform the mechanics.

Example: a release agent should not manually infer a package publish order from 300 dependency records. A script should calculate the directed graph and return the ordered packages, cycles, and blocked nodes.

### 2. Does the model still need a reusable procedure?

Use a skill when the work needs judgment but follows a repeatable method. The skill explains how to gather evidence, when to call tools, when to stop, and how to present the result.

Example: a security-review skill may decide which exact checks apply to an OAuth change, call deterministic scanners, inspect missing evidence, and produce a risk-ranked review.

### 3. Is some knowledge conditional?

Keep the common procedure in `SKILL.md`. Put framework rules, schemas, long examples, and rare cases in references. The skill should state the exact condition for reading each reference.

Example: an incident skill can keep the common correlation method in its core file and load a PostgreSQL lock guide only when database waits or blocked transactions appear.

### 4. Must the system control the path?

Use a workflow when order, retry, approval, checkpointing, or side effects matter. A skill lets the model choose the method. A workflow guarantees which step runs next.

Example: publishing a release, updating a registry, posting an announcement, and opening a rollback window should not depend on a model remembering the right order from prose.

### 5. Does the work need isolation?

Use a subagent for a large independent reasoning task that benefits from separate context or parallel execution. Use a specialist agent when that boundary becomes durable and owns different tools, permissions, or model policy.

Example: during a production incident, an application investigator and a database investigator may work independently. They should return compact evidence contracts to one coordinator rather than passing full raw logs between agents.

## The smallest suitable primitive

1. Put a rule in global instructions only when most tasks need it.
2. Put a reusable reasoning procedure in a skill.
3. Put conditional manuals, schemas, and examples in references.
4. Put exact transformations and data work in code.
5. Use MCP when a capability needs a reusable external protocol boundary.
6. Use a hook when an event must trigger exact behaviour.
7. Use a workflow when order or side effects must be controlled.
8. Use a subagent only when isolation or independent work pays for the extra coordination.
9. Use a specialist agent only for a real responsibility boundary.

## Complexity has a carrying cost

Every extra primitive adds one or more costs:

- another routing decision;
- more context or schemas;
- another permission surface;
- more latency;
- more failure modes;
- more versioning and maintenance;
- more evidence to inspect when something goes wrong.

A boundary is useful only when its measured benefit is larger than that cost.

## A concrete example

Consider a team that handles production checkout incidents.

```text
Global instructions
  - never claim an upstream provider cause without provider evidence
  - redact secrets from stored traces

Incident skill
  - define the investigation order and output contract

References
  - database lock patterns
  - payment-provider status semantics
  - queue redelivery rules

Scripts
  - correlate request IDs and timestamps
  - summarize error families
  - calculate retry rates

Workflow
  - open incident → collect evidence → require approval → communicate → close

Subagents
  - application, database, and provider investigations only when each has enough work
```

Each layer has a clear job. Removing a layer should have a clear consequence.

## The default stance

Start with one capable agent, a small instruction file, and deterministic tools. Add a skill when a repeatable method appears. Add references when only some cases need deep knowledge. Add isolation only after traces show context pollution, tool conflicts, or independent work that can run in parallel.

**Evidence:** `start-single-agent`, `scripts-for-determinism`, `progressive-disclosure`, `skill-v-workflow`, `subagent-isolation`
