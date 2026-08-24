# Routing boundaries

Raw catalogue count is a weak metric. Overlap is the stronger signal.

Fifty skills can work well when a normal request clearly matches one or two. Ten skills can fail when six descriptions claim the same work.

## Define each catalogue item

A tool, skill, or specialist agent description should answer four questions:

1. **Intent:** what user request activates it?
2. **Evidence:** what data or files does it inspect?
3. **Output:** what result does it return?
4. **Negative boundary:** what close neighbour does it not own?

Example:

> Use for assessing breaking API changes during a framework migration. Inspect changed call sites, compatibility evidence, and migration references. Return a risk-ranked migration plan. Do not use for routine formatting or dependency vulnerability scans.

## Common overlap causes

- broad verbs such as “review,” “analyze,” or “help” without a domain;
- descriptions listing every possible neighbouring task;
- several skills named after teams rather than user intent;
- tools split by backend implementation instead of meaningful operation;
- two agents with the same evidence and output;
- positive descriptions with no negative boundary;
- old items left in the catalogue after a replacement ships.

## Build a routing eval

Freeze realistic prompts in five groups:

- clear positive cases;
- close negative neighbours;
- mixed tasks;
- ambiguous wording;
- cases where no catalogue item should activate.

Measure:

- top-1 accuracy;
- false activation;
- missed activation;
- ambiguity rate;
- score margin between first and second choice;
- pairwise description overlap;
- wrong-context cost after a false route.

Do not test only with prompts copied from the descriptions. Use natural requests from real traces or carefully reviewed synthetic cases.

## Fix overlap in this order

1. Tighten the description.
2. Add a negative boundary.
3. Merge items that own the same job.
4. Split a broad domain only when the pieces have independent intent and output.
5. Filter the catalogue by requesting agent or task context.
6. Introduce a specialist agent only when the domain also needs isolation, tools, or permissions.

## The flagship lab

[Lab 04](../../labs/04-overlapping-skills/README.md) keeps six capabilities constant and changes only descriptions and boundaries. Its deterministic router improves from 37.5% to 95.8% accuracy on 24 frozen cases. This is a reproducible structural result, not a claim about every model.

**Evidence:** `overlap-not-count`, `skill-lift-eval`, `skill-catalog-filtering`
