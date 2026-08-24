# Instructions

Instructions are rules that should affect most tasks in a repository, session, or product.

Typical files include `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, repository Copilot instructions, and product-level system prompts.

## Use instructions for

- stable repository facts;
- universal safety and privacy rules;
- required verification before claiming success;
- naming, formatting, and testing conventions that apply across the project;
- permanent permission boundaries;
- a small amount of role and product context.

Good instruction:

> Do not state that a command passed unless its exit code and output were checked.

Poor global instruction:

> For every dependency upgrade, inspect release notes, classify API changes, scan migration guides, create rollout batches, and calculate a rollback score.

The second item is a task-specific procedure. It belongs in a skill.

## Keep the always-loaded layer small

The problem is not a specific line count. The problem is irrelevant instructions competing with the current task.

A 180-line file may be valid if nearly every line matters on every run. A 60-line file may already be too large if half of it applies only to releases or security reviews.

Review each section with this question:

> Would removing this section reduce quality on most normal tasks?

- **Yes:** keep it in instructions.
- **No, only on one task family:** move it into a skill.
- **No, only on rare cases within that task:** move it into a reference.
- **No, it is an exact check:** turn it into code or a hook.

## What not to put here

Avoid:

- long API manuals;
- framework-specific migration steps;
- large catalogues of error signatures;
- examples for rare cases;
- instructions that restate what the model already knows;
- deterministic calculations written as prose;
- every specialist persona in one file.

## Practical review triggers

These are heuristics, not limits:

- the file has several headings that start with “When doing X”;
- one task activates many instructions that other tasks never use;
- teams frequently add exceptions to earlier rules;
- the same rule exists in global instructions and a skill;
- changing one procedure breaks unrelated work;
- maintainers cannot say which rules are universal.

A rough size of 150–200 lines is a useful review point for many repositories, but the activation pattern matters more than the number.

## Verification

Measure instructions with representative tasks, not with prose review alone.

Track:

- task success before and after removing or moving a section;
- instruction-conflict rate;
- always-loaded tokens;
- false application of specialist rules;
- maintenance changes caused by one rule update.

Lab 01 demonstrates this structure with frozen synthetic cases: [mega instructions](../../labs/01-mega-instructions/README.md).

## Example boundary

For a large codebase:

```text
AGENTS.md
  - use the repository's formatter
  - do not edit generated files
  - run the nearest relevant test suite
  - report commands actually executed

migration skill
  - classify each change as mechanical or semantic
  - run codemods where safe
  - load framework references only when detected
```

The instructions define the ground rules. The skill owns the specialist method.

**Evidence:** `progressive-disclosure`, `start-single-agent`
