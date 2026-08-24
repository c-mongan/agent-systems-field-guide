# Reproducible example — Production incident

A checkout service shows intermittent payment failures. Events come from the gateway, database, checkout API, and payment-provider boundary.

The example demonstrates a clean split between exact evidence preparation and model judgment.

## Architecture

```text
Raw events
   ↓
Deterministic correlation script
   - sort by time
   - group by request ID
   - count component errors
   - find repeated boundary patterns
   - preserve evidence IDs
   ↓
Compact evidence package
   ↓
Incident skill or investigator
   - assess causal story
   - state confidence
   - identify unknowns
   - recommend containment
```

## What code owns

[`run.py`](run.py) performs work with one objective result:

- time ordering;
- request correlation;
- error counts;
- repeated timeout detection;
- evidence-ID selection;
- structured output.

It does not claim access to the payment provider's internal systems.

## What an agent should own

A real incident investigator may:

- decide which additional evidence to collect;
- compare the pattern with recent changes;
- load a database, queue, or provider reference when the evidence points there;
- rank hypotheses;
- recommend safe containment;
- clearly separate observed facts from inference.

## Run

```bash
python examples/incident-response/run.py \
  examples/incident-response/fixtures/input.json
```

Expected output is frozen in [`expected/output.json`](expected/output.json). Verification compares bytes, so unexplained output drift fails.

## Expected interpretation

The fixture supports a high-confidence statement that failures appear first at the payment-provider boundary while database reads remain successful. It does **not** support a claim about the provider's internal root cause.

That distinction is the point: deterministic code organizes evidence; the agent reasons inside the evidence boundary.
