---
id: mega-instructions
status: avoid
evidence:
  - progressive-disclosure
---
# Mega instructions

Task-specific procedures, manuals, and examples are always loaded for every task.

## Symptoms

- many sections start with “when doing X”;
- unrelated tasks follow specialist rules;
- instruction conflicts increase;
- changing one procedure affects other domains;
- most tokens are irrelevant to the current request.

## Example

One repository file contains release steps, security-review rules, incident playbooks, migration guidance, and documentation style. A simple unit-test fix loads all of it.

## Better boundary

- keep universal safety and repository facts in instructions;
- move reusable task methods into skills;
- move conditional manuals into references;
- move exact checks into code or hooks.

## Proof required

Freeze normal tasks from several domains. Compare success, conflict hits, and loaded context before and after moving one procedure.

See [Lab 01](../labs/01-mega-instructions/README.md).

**Evidence:** `progressive-disclosure`
