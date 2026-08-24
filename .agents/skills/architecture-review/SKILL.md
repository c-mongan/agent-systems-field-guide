---
name: architecture-review
description: Reviews an AI agent system and decides whether behaviour belongs in instructions, a skill, a reference, a script or tool, MCP, a hook, a workflow, a subagent, or a specialist agent. Use when designing, simplifying, or evaluating an agent architecture.
license: Apache-2.0
compatibility: Requires repository read access and Python 3.11+ to run the bundled validation commands.
---
# Architecture review

## Goal

Recommend the smallest architecture change that fixes a measured failure.

## Process

1. State the task, evidence inputs, output, side effects, and acceptance check.
2. Inspect one representative trace before proposing decomposition.
3. Classify each responsibility:
   - always-needed rule → instructions;
   - reusable judgment → skill;
   - optional specialist knowledge → reference;
   - exact operation → script or tool;
   - reusable external capability → MCP;
   - exact event reaction → hook;
   - required order or side effect → workflow;
   - independent isolated reasoning → subagent;
   - durable role, tools, or permissions → specialist agent.
4. Identify the measured failure: wrong routing, context waste, repeated mechanics, control risk, polluted reasoning, or missing isolation.
5. Read [the decision matrix](references/decision-matrix.md) when two primitives appear valid.
6. Read [the evaluation gate](references/evaluation-gate.md) before accepting added complexity.
7. Return:
   - current boundary;
   - observed failure and evidence;
   - smallest proposed change;
   - expected benefit;
   - new cost or risk;
   - frozen eval needed;
   - keep/revert rule.

## Rules

- Do not split only because a file is long.
- Treat 500 lines and 5,000 tokens as Agent Skills guidance, not a universal quality law.
- Prefer code for deterministic work.
- Do not create a subagent for a trivial function.
- Do not claim improvement without a paired evaluation.
- Mark unknowns instead of inventing traces or metrics.
