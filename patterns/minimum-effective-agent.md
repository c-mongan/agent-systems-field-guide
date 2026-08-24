---
id: minimum-effective-agent
status: recommended
evidence:
  - start-single-agent
---
# Minimum effective agent

Start with one capable agent, a small set of clear tools, and the minimum instructions needed to work safely.

## Problem

Teams often add specialist agents before they know whether one agent actually fails. The result is extra routing, duplicated context, and harder debugging without a proven quality gain.

## Pattern

1. Give one agent the tools required for the representative task set.
2. Keep global rules small.
3. Put exact work in code.
4. Record traces and failures.
5. Add a skill, workflow, or isolated worker only when one specific failure appears.

```text
one agent
   ↓
measured failure
   ↓
smallest useful boundary
   ↓
paired eval
```

## Use when

- a new system has no reliable baseline;
- teams are debating agent count from intuition;
- the tool catalogue is still changing;
- no stable handoff contract exists;
- most tasks fit within one context.

## Do not force it when

A single agent is not a rule forever. Split when evidence shows a real permission boundary, independent workstream, context-pollution problem, or workflow-control need.

## Proof

Compare the one-agent baseline with the proposed boundary on the same cases. Track task success, latency, tokens, tool calls, and new failure modes.

**Evidence:** `start-single-agent`, `subagent-isolation`
