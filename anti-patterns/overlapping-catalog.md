---
id: overlapping-catalog
status: avoid
evidence:
  - overlap-not-count
---
# Overlapping catalogue

Several skills, tools, or agents can plausibly match the same request.

## Symptoms

- descriptions use the same broad verbs and nouns;
- top routing scores have a small margin;
- false activations load large irrelevant context;
- users must name the desired component explicitly;
- adding more examples does not fix selection.

## Better boundary

For each item, state:

- exact activating intent;
- evidence inspected;
- output returned;
- close neighbour not owned.

Merge true duplicates. Filter shared catalogues before adding another routing layer.

## Proof required

Use clear positive, close negative, mixed, ambiguous, and no-match cases. Measure top-1 accuracy, ambiguity, false activation, and wrong-context cost.

See [Lab 04](../labs/04-overlapping-skills/README.md).

**Evidence:** `overlap-not-count`, `skill-catalog-filtering`
