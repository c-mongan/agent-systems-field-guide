# Live provider protocol

Use this protocol before publishing a model-specific claim.

## 1. Freeze the run specification

Record:

- provider and harness version;
- exact model identifier;
- date and region when relevant;
- model settings;
- system, repository, and skill files;
- tool and permission policy;
- timeout and retry policy;
- source-data snapshot;
- case set and grader version.

## 2. Isolate hidden configuration

Headless harnesses may load user instructions, skills, plugins, MCP servers, memory, or local settings.

Use the strongest supported isolation controls. The included adapters use bounded defaults such as:

- non-persistent sessions;
- read-only or plan-style permissions;
- explicit model selection;
- structured output;
- ignored user rules where supported;
- hard process timeout;
- no shell execution.

Document any ambient configuration that cannot be disabled.

## 3. Run paired cases

For each `case_id`:

1. run the baseline;
2. run the candidate under the same policy;
3. repeat enough times to observe nondeterminism;
4. store all successes, failures, and timeouts;
5. do not retry only the losing variant.

Randomize order when practical to reduce time-related bias.

## 4. Grade

Use exact deterministic checks first. Use a written rubric for semantic quality. Blind the grader to architecture labels where practical.

Keep raw outputs so humans can audit disagreements.

## 5. Report

Publish:

- number of cases and attempts;
- success distribution;
- confidence interval or variance;
- latency and token distribution;
- tool calls and worker count;
- errors and timeouts;
- cost when available;
- all changed variables;
- known limitations.

Do not report only the best run.

## 6. Protect data

Provider output and tool traces may contain source code, secrets, customer information, or personal data. Redact before publication and preserve access controls for raw artifacts.

## Adapter commands

Render a command without executing it:

```bash
agent-guide adapter render claude-code "Route this case" --model EXACT_MODEL_ID
agent-guide adapter render codex "Route this case" --model EXACT_MODEL_ID
```

Execute only with explicit acknowledgement:

```bash
agent-guide adapter run codex "Route this case" \
  --model EXACT_MODEL_ID \
  --schema labs/04-overlapping-skills/adapter-contracts/output-schema.json \
  --output-dir runs/case-001 \
  --execute
```

**Evidence:** `headless-adapter-controls`, `blind-comparison`, `microsoft-agent-evaluation`
