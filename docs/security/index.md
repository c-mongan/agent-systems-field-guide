# Security

Agent architecture changes the attack surface. Skills, references, scripts, tools, MCP servers, hooks, workflows, and subagents all deserve explicit trust boundaries.

## Treat skills as dependencies

A skill can contain instructions that influence tool use and scripts that execute code. Review it like an open-source dependency.

Before adoption:

- verify author and repository provenance;
- read `SKILL.md`, references, scripts, and manifests;
- inspect network, file, and process access;
- check for instructions that bypass policy or hide actions;
- pin a reviewed version;
- record the source and update process;
- run static and behavioural tests.

Do not trust a skill because its name looks familiar. Typosquatting and copied repositories are possible.

## Least privilege by primitive

| Primitive | Minimum control |
|---|---|
| Instructions | review changes; protect repository ownership |
| Skill | scoped activation; reviewed instructions; allowed tools |
| Reference | provenance; read-only access; prompt-injection handling |
| Script/tool | sandbox; schema validation; timeout; exact permissions |
| MCP | authentication; authorization; transport security; audit logs |
| Hook | tamper resistance; fail-open/fail-closed decision |
| Workflow | persisted state; idempotency; approval and compensation |
| Subagent | bounded context; scoped tools; explicit handoff |
| Specialist agent | durable permission, data, and model governance |

## Separate data from instructions

Tool and reference content may contain untrusted text that tries to change agent behaviour. Mark external content as data. Do not let a retrieved document redefine permissions or override system policy.

Use structured extraction when possible. Preserve source IDs so suspicious instructions can be traced back to the input.

## Control side effects

For writes, publishing, payments, messages, and destructive changes:

- require explicit permission;
- use idempotency keys;
- validate target and arguments;
- record the external operation ID;
- verify the result independently;
- use a workflow for multi-step effects;
- define rollback or compensation.

A model statement such as “the action probably completed” is not sufficient state.

## Secure live evals

Live traces may contain source code, customer data, credentials, or internal prompts.

- use synthetic or approved data where possible;
- redact before publication;
- restrict raw artifact access;
- do not store the full environment;
- hash prompts in summary records;
- keep provider credentials out of fixtures;
- use read-only or plan-style defaults;
- review network access.

## Supply-chain validation

The release workflow pins GitHub Actions by commit SHA, pins Python quality tools, pins Node.js, and pins `agnix`. Missing release tools are failures.

Static validation is necessary but not sufficient. Behavioural evals must still prove that the architecture helps on representative tasks.

**Evidence:** `skill-security-review`, `pinned-validation`, `mcp-boundary`
