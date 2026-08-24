# Specialist agents

A specialist agent is a durable responsibility boundary with its own prompt, tools, permissions, model policy, and skills.

It is more than a persona. It owns a distinct part of the system.

## Use a specialist agent when

- a domain has different data access;
- a role needs a restricted tool set;
- a separate model or reasoning policy is justified;
- the responsibility recurs across many workflows;
- the agent has a stable input and output contract;
- independent governance or audit ownership matters;
- routing into the domain is clearer than exposing every specialist tool to the main agent.

Example:

A security-review agent may have read-only repository access, vulnerability scanners, security references, and no deployment tools. A release agent may have package registry access and approval-gated publish tools. Those are real authority boundaries.

## Do not create agents for tone

Weak boundaries:

- “friendly agent”;
- “careful agent”;
- “senior engineer agent”;
- one agent per small skill;
- a worker with the same prompt, tools, data, and output as the parent.

Tone and quality rules belong in instructions. Procedures belong in skills.

## Scope skills per agent

Do not attach every skill to every specialist. Give each agent the smallest catalogue needed for its role.

This matters because harnesses load skills differently. Some use on-demand discovery. Some configurations eagerly inject selected skills into a custom agent at startup. Measure the actual startup context in the target harness.

## Design the routing boundary

A specialist description should state:

- the user intent it owns;
- the evidence it can access;
- the actions it may take;
- the result it returns;
- the neighbouring domain it does not own.

Example:

> Review authentication and session-management changes. Use read-only code access and security scanners. Return ranked findings and missing controls. Do not approve deployment or modify production configuration.

## Governance

Document:

- owner;
- model and version policy;
- tools and permissions;
- data access;
- skill set;
- audit logs;
- escalation path;
- evaluation suite;
- retirement conditions.

## Measure before multiplying agents

Start with one capable agent and scoped tools. Add a specialist when routing, permissions, context, or repeated domain work shows a real failure.

Track task success, routing accuracy, context, cost, delegation failures, permission violations, and maintenance burden.

**Evidence:** `start-single-agent`, `subagent-isolation`, `copilot-eager-skills`
