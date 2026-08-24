# Quick reference

Use this page when you need a decision in a few minutes.

## Pick the smallest boundary

| Situation | Start with | Move up only when |
|---|---|---|
| A rule matters on nearly every task | Instructions | it becomes task-specific |
| A repeatable task still needs judgment | Skill | the work needs its own context or authority |
| Detailed knowledge is needed in some cases | Reference | it is used on almost every run |
| A result can be calculated exactly | Script or tool | the agent must choose or interpret the operation |
| Several clients need one external capability | MCP | a local library is no longer enough |
| An event must always trigger the same action | Hook | the reaction becomes a stateful process |
| Steps, approvals, retries, or side effects must be controlled | Workflow | a bounded step needs flexible expert judgment |
| A large task benefits from separate context | Subagent | the role becomes durable and needs distinct permissions |
| A domain owns separate tools, permissions, or model policy | Specialist agent | the boundary is only a different tone or persona |

## Common review triggers

These are prompts to investigate. They are not universal limits.

| Signal | First test |
|---|---|
| `AGENTS.md` or equivalent has many task-specific sections | move one procedure into a skill and rerun the same eval |
| `SKILL.md` approaches 500 lines or 5,000 tokens | move conditional detail into focused references |
| several skills plausibly match common prompts | rewrite descriptions and add negative boundaries |
| the same reference is read on most runs | move its essential rules into `SKILL.md` |
| the model filters, joins, sorts, or counts repeatedly | replace that loop with code |
| a tool catalogue contains many near-duplicates | batch related operations or tighten schemas |
| a subagent returns one short deterministic value | replace it with a function or tool |
| the system sends emails, charges money, or publishes releases from prose alone | put side effects behind a workflow and approval gate |
| a remote capability has one caller and no identity boundary | keep it local instead of adding MCP |
| the new architecture looks cleaner but the frozen eval does not improve | revert it |

## Skill wrapping a script

Wrap a script in a skill when the model must do at least one of these:

- decide whether the script is relevant;
- choose safe arguments;
- select input data;
- interpret uncertain output;
- combine the result with other evidence;
- decide the next step.

Do not add a skill when the only instruction is “run this command” and the command is already easy to discover and safe to call directly.

## Skill using references

Move content from `SKILL.md` into a reference when all three are true:

1. the content is needed only for a subset of runs;
2. the skill can state a clear read condition;
3. loading it every time would add irrelevant context.

Good reference names express the decision already made:

```text
references/oauth-session-rules.md
references/postgresql-lock-analysis.md
references/react-19-breaking-changes.md
```

Avoid names such as `everything.md` or `misc.md`.

## Subagent test

Use a subagent only when at least one benefit is material:

- large context stays out of the parent;
- work can run independently in parallel;
- the worker needs a different tool or permission set;
- the worker needs a different model policy;
- the parent only needs a compact evidence-backed result.

Then measure the cost: startup context, duplicated retrieval, latency, failures, and coordination tokens.

## Architecture acceptance gate

```text
Freeze cases and policy
          ↓
Run baseline
          ↓
Change one boundary
          ↓
Run candidate
          ↓
Compare quality + cost + safety
          ↓
Keep or revert
```

A file split is not proof. A new diagram is not proof. A measured improvement on representative cases is proof for that workload.

**Evidence:** `skill-size-guidance`, `scripts-for-determinism`, `skill-v-workflow`, `subagent-isolation`, `skill-lift-eval`
