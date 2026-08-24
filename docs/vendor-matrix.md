# Vendor matrix — reviewed August 24, 2026

Portable concepts come first. Syntax, discovery, inheritance, and loading behaviour vary by harness.

| Capability | Claude Code | OpenAI Codex | GitHub Copilot | Gemini CLI | Cursor |
|---|---|---|---|---|---|
| Repository instructions | `CLAUDE.md` | `AGENTS.md` | Copilot instructions and `AGENTS.md` | `GEMINI.md` | rules and `AGENTS.md` |
| Agent Skills | supported | supported | supported | supported | supported |
| Portable project skill path | product paths plus portable aliases | `.agents/skills/` | `.agents/skills/`, `.github/skills/`, `.claude/skills/` | `.agents/skills/` alias | `.agents/skills/` and product paths |
| Separate worker context | subagents | agents/subagents | custom agents and subagents | subagents | agents |
| Headless adapter in this repo | yes | yes | no | yes | no |
| Structured output used by adapter | JSON and optional schema | JSONL events and optional schema | not implemented | JSON | not implemented |

## Portable behaviour

The open Agent Skills model uses progressive disclosure:

```text
catalogue metadata
       ↓
activated SKILL.md
       ↓
on-demand references and scripts
```

Do not assume every product or SDK configuration follows this exact loading path.

## Important exceptions

### GitHub Copilot SDK

Custom agents can explicitly list skills that are eagerly injected in full at agent startup. Child agents do not inherit parent skills. Scope the list and measure startup context.

### Claude Code headless runs

Non-interactive runs can load normal project and user configuration unless isolation flags are used. Bare mode skips automatic discovery, so a controlled eval must state what configuration was intentionally added back.

### Codex non-interactive runs

`codex exec` supports explicit sandboxing, ephemeral runs, JSON events, and controls for ignoring user configuration and rules. Record all flags in the trace.

### Gemini CLI

Headless mode supports JSON and streaming JSON. Exit codes, model, tools, and ambient configuration belong in the run specification.

## Portability rule

Keep the core skill content portable. Put product-only frontmatter, tool names, command flags, and loading paths in thin adapter files.

A shared directory improves reuse. It does not replace a real compatibility test in each target harness.

## Unsupported does not mean impossible

The repo omits live Copilot and Cursor adapters because their command and output contracts were not implemented and tested here. It is better to document a gap than to ship a decorative adapter.

**Evidence:** `progressive-disclosure`, `copilot-eager-skills`, `headless-adapter-controls`
