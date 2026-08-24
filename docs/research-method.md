# Research method

The guide separates portable architecture ideas from vendor syntax and local heuristics.

## Source order

Prefer sources in this order:

1. open specifications;
2. first-party product documentation;
3. first-party workshops and reference implementations;
4. first-party evaluation frameworks;
5. security standards and recognised guidance;
6. community tools used as implementation aids;
7. local heuristics, clearly labelled.

Community articles can reveal useful problems, but they do not define vendor behaviour.

## Claim ledger

[`sources/sources.json`](../sources/sources.json) records:

- stable source ID;
- publisher;
- title;
- source type;
- URL;
- review date.

[`sources/claims.json`](../sources/claims.json) maps each short evidence ID to one or more sources and a statement.

Guide pages reference evidence IDs rather than repeating raw links everywhere. This keeps the prose readable and makes dated product claims easier to audit.

## Labels

| Label | Meaning |
|---|---|
| Official | a first-party guide or product document states the point |
| Specification | an open format or protocol defines the behaviour |
| Research | a published evaluation supports the point |
| Heuristic | a practical review trigger, not a universal rule |
| Measure | the answer depends on the workload and must be tested |

## Vendor neutrality

A portable claim must survive a change of harness wording.

Portable:

> Load specialist knowledge only when the task needs it.

Vendor-specific:

> This product stores project skills in this exact directory and loads them through this command.

The first belongs in the core guide. The second belongs in the vendor matrix or adapter documentation.

## Reuse and attribution

The guide adopts the observe → diagnose → change → verify teaching method used in Anthropic's Apache-2.0 decomposition workshop. It does not copy the StockPilot exercise or present Anthropic-specific runtime details as universal rules.

Third-party names and source licences are recorded in [`NOTICE`](../NOTICE) and the evidence ledger.

## Review cadence

Recheck:

- product loading paths and CLI flags before each release;
- evaluation tools before changing pinned versions;
- open specifications after version changes;
- security guidance at least each major release;
- source links when automated link checks fail.

A review date means “checked on this date,” not “guaranteed forever.”
