---
id: mega-skill
status: avoid
evidence:
  - skill-size-guidance
---
# Mega skill

One skill owns several independent jobs or embeds every specialist manual in its core file.

## Symptoms

- sections activate independently;
- the description lists many unrelated intents;
- normal runs use only a small fraction of the file;
- one output contract cannot describe all branches;
- the skill approaches the specification size limit;
- maintainers add more headings instead of clearer boundaries.

## Better boundary

Keep one coherent procedure in `SKILL.md`. Move conditional knowledge to focused references. Split into multiple skills only when the jobs have distinct intent, evidence, and output.

## Warning

Do not replace one mega skill with ten vague skills. Routing overlap can become worse.

## Proof required

Compare loaded context, missed reference reads, task success, and routing accuracy. See [Lab 03](../labs/03-mega-skill/README.md).

**Evidence:** `skill-size-guidance`, `progressive-disclosure`
