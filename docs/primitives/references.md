# References

References hold specialist knowledge that only some skill runs need.

They are usually Markdown files near `SKILL.md`, but the architecture idea is broader: load detailed knowledge only after the task has been narrowed enough to justify it.

## Good reference material

Use references for:

- framework or platform variants;
- API field semantics;
- policy details;
- schemas and data dictionaries;
- long worked examples;
- rare failure modes;
- compatibility tables;
- detailed checklists used only in one branch.

Keep the core decision in the skill. Put the specialist detail in the reference.

## State the read condition

A reference is useful only when the skill tells the model when to read it.

Good:

> When the change modifies refresh-token rotation, read `references/oauth-token-lifecycle.md` before grading replay risk.

Weak:

> See the references folder for more information.

The first instruction is a routing decision. The second invites eager reading.

## Do references slow the system down?

A reference adds cost when it is read:

- one retrieval or file-read step;
- more input tokens;
- more material competing for attention;
- possibly more latency and billing.

That small cost is usually lower than loading every specialist manual on every run. References are a performance improvement when the selection rule is accurate.

The useful metric is not the number of files. It is the amount of irrelevant content loaded per task.

## Move content back into `SKILL.md` when

- almost every run reads the same reference;
- the skill cannot make a correct first decision without it;
- the reference contains a critical invariant;
- the read step is often forgotten and causes failures.

Move only the essential rule back. The full manual can remain separate.

## Split a reference when

- it covers several independently triggered topics;
- a normal run needs only a small section;
- it grows beyond easy navigation;
- the filename no longer describes one decision;
- the skill must say “read sections 2, 8, and 14.”

Prefer:

```text
references/
├── oauth-token-lifecycle.md
├── session-cookie-controls.md
└── saml-signature-validation.md
```

Avoid:

```text
references/all-auth-knowledge.md
```

Keep reference chains shallow. A skill should normally point directly to the resource it needs, rather than loading one index that points to another index.

## Measure reference quality

Track:

- reference load rate;
- relevant-token ratio;
- tasks where a required reference was missed;
- tasks where an unnecessary reference was loaded;
- latency and tokens added by the read;
- task success with and without the reference.

Lab 03 compares a monolithic skill with a core procedure plus focused references: [mega skill](../../labs/03-mega-skill/README.md).

**Evidence:** `progressive-disclosure`, `skill-size-guidance`
