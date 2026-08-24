# Skills

A skill is a reusable procedure for work that still needs model judgment.

A good skill helps the model decide what evidence to gather, which exact operations to run, when to read deeper material, when to stop, and what result to return.

## A healthy skill has one coherent job

A useful `SKILL.md` normally contains:

1. a specific name and description;
2. clear activation conditions;
3. the core procedure;
4. required evidence;
5. tool and script usage;
6. reference read conditions;
7. stop or escalation conditions;
8. an output contract.

Example job:

> Review a proposed authentication change, run exact configuration checks, load the relevant OAuth or session reference, and return evidence-backed risks and missing controls.

That is one coherent responsibility. “Review security, write documentation, deploy the fix, and notify customers” is several jobs.

## Write a description for routing

The description is part of the catalogue. It should answer:

- What user intent activates this skill?
- What evidence does it inspect?
- What result does it produce?
- What neighbouring work does it not own?

Good:

> Use for reviewing OAuth, OIDC, session-cookie, or token-lifecycle changes. Inspect configuration and auth flow evidence, then return ranked security findings. Do not use for general dependency scanning.

Weak:

> Use for code review and security tasks.

The weak description overlaps many neighbours and gives the router little information.

## When a skill should wrap a script

Wrap a script when the model must make a decision before or after execution.

```text
User task
   ↓
Skill decides whether the operation applies
   ↓
Script performs exact work
   ↓
Skill interprets result and chooses next step
```

Use this pattern when the model must:

- choose the correct input or arguments;
- judge whether the script is safe to run;
- interpret partial or uncertain results;
- combine several exact results;
- escalate when evidence is missing.

Do not add a skill when its only content is “run `format.py`” and the command is already directly exposed, safe, and self-explanatory. A tiny discovery skill can still be valid when the capability would otherwise be invisible, but measure whether it improves routing.

## When a skill needs references

Keep common rules in `SKILL.md`. Move detail out when it is conditional.

```text
SKILL.md
  - common procedure
  - decision rules
  - output contract
  - “read X when Y appears”

references/
  - framework-specific rules
  - API semantics
  - detailed examples
  - rare edge cases
```

The Agent Skills specification recommends keeping `SKILL.md` under 500 lines and below about 5,000 tokens. Treat that as an upper bound, not a target. Split earlier when sections have independent activation conditions.

## Split a skill when

- it owns more than one user intent;
- sections can activate independently;
- outputs are unrelated;
- different sections need different permissions;
- several descriptions could be written without overlap;
- eval traces show the agent skipping or confusing branches.

Do not split only to make files short. Six tiny overlapping skills are worse than one clear 250-line skill.

## Test the skill

A skill eval should include:

- prompts that should activate it;
- close neighbours that should not activate it;
- mixed tasks;
- missing-evidence cases;
- cases that require one reference but not another;
- cases where the correct action is to stop or escalate.

Compare against a baseline without the skill or against the previous version. Track activation, task success, cost, tool use, and new failure modes.

Lab 04 keeps the same six skills and changes only their routing boundaries: [overlapping skills](../../labs/04-overlapping-skills/README.md).

**Evidence:** `skill-size-guidance`, `progressive-disclosure`, `skill-lift-eval`, `overlap-not-count`
