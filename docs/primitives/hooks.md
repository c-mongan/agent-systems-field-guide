# Hooks

A hook is deterministic behaviour tied to an event in the agent lifecycle.

Examples include pre-tool checks, post-tool logging, formatting gates, audit events, and exact policy enforcement.

## Use hooks when

- an action must happen every time a known event occurs;
- the rule should not depend on model judgment;
- the check is fast and objective;
- the event and response are easy to define;
- failure behaviour can be stated clearly.

Examples:

- block writes outside an allowed directory;
- redact secrets before a trace is stored;
- run a formatter after a file edit;
- record every external side-effect request;
- require an approval token before a publish tool executes.

## Do not use hooks for planning

A hook is a reaction, not a reasoning process.

Poor use:

> After every tool call, inspect the whole task, reconsider the architecture, decide whether to contact three teams, and create a recovery plan.

That belongs in a skill or workflow. A hook can record the event or enforce one exact condition.

## Hook or workflow?

Use a hook for one event-response rule.

Use a workflow when:

- several steps have state;
- order matters;
- a process can pause and resume;
- retries could repeat side effects;
- approvals occur between steps;
- compensation or rollback is required.

## Fail-open or fail-closed

Every hook should define what happens when it fails.

- **Fail closed:** block the action. Use for security, permissions, destructive writes, and release approval.
- **Fail open:** record the failure but allow progress. Use only when blocking would be worse and the risk is understood.

Do not leave this as an accidental runtime default.

## Measure hooks

Track:

- activation count;
- blocked actions;
- false blocks;
- missed events;
- added latency;
- hook failures;
- bypasses;
- user overrides;
- audit completeness.

A hook that silently fails is not a control.

**Evidence:** `skill-v-workflow`, `skill-security-review`
