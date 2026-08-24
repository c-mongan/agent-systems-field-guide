---
id: progressive-disclosure
status: recommended
evidence:
  - progressive-disclosure
---
# Progressive disclosure

Expose enough information to route the task, then load deeper procedure and knowledge only when needed.

## Structure

```text
Catalogue
name + description
      ↓ match
SKILL.md
core procedure
      ↓ condition
Reference or script
specialist detail or exact work
```

## Why it works

The system keeps discovery context small without hiding specialist capability. The task pays for deep context only after a relevant boundary is selected.

## Apply it well

- write distinct skill descriptions;
- keep the common procedure in `SKILL.md`;
- name references by the condition that activates them;
- state exact read triggers;
- return compact script results;
- avoid deep reference chains;
- measure missed and unnecessary loads.

## Example

A migration skill always defines classification, evidence, rollout, and rollback. It reads a React 19 reference only for React changes and a database-driver reference only when the changed API affects transaction or connection semantics.

## Failure modes

Progressive disclosure fails when the agent reads every reference anyway, when descriptions overlap, or when a critical invariant is hidden in an optional file.

## Proof

Measure initial catalogue size, activated skill tokens, reference load rate, relevant-context ratio, and task success. [Lab 06](../labs/06-eager-context/README.md) demonstrates the structural cost of eager loading.

**Evidence:** `progressive-disclosure`, `skill-size-guidance`
