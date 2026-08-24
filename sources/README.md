# Evidence ledger

The guide separates sourced facts from local advice.

| Label | Meaning |
|---|---|
| **Official** | A first-party product document, guide, workshop, or reference implementation states the point. |
| **Specification** | An open format or protocol defines the behaviour. |
| **Research** | A published evaluation supports the point. |
| **Heuristic** | A practical review trigger. It is not a universal limit. |
| **Measure** | The answer depends on the workload and must be tested. |

## Source catalogue

| ID | Publisher | Source | Type | Reviewed |
|---|---|---|---|---|
| `agent-skills-spec` | Agent Skills | [Agent Skills specification](https://agentskills.io/specification) | specification | 2026-08-24 |
| `agent-skills-best-practices` | Agent Skills | [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) | official-guide | 2026-08-24 |
| `agnix-049` | agent-sh | [agnix v0.49.0](https://github.com/agent-sh/agnix/releases/tag/v0.49.0) | tool-release | 2026-08-24 |
| `anthropic-decomposition-workshop` | Anthropic | [Agent decomposition workshop](https://github.com/anthropics/cwc-workshops/tree/main/agent-decomposition) | official-workshop | 2026-08-24 |
| `anthropic-skill-creator` | Anthropic | [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | official-skill | 2026-08-24 |
| `anthropic-cli` | Anthropic | [Claude Code CLI reference](https://code.claude.com/docs/en/cli-usage) | official-docs | 2026-08-24 |
| `anthropic-subagents` | Anthropic | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | official-docs | 2026-08-24 |
| `anthropic-headless` | Anthropic | [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) | official-docs | 2026-08-24 |
| `cursor-skills` | Cursor | [Cursor Agent Skills](https://cursor.com/docs/skills) | official-docs | 2026-08-24 |
| `github-agent-skills` | GitHub | [About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | official-docs | 2026-08-24 |
| `github-customization-cheatsheet` | GitHub | [Copilot customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet) | official-docs | 2026-08-24 |
| `github-sdk-custom-agents` | GitHub | [Copilot SDK custom agents](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents) | official-docs | 2026-08-24 |
| `github-custom-agents` | GitHub | [Custom agents and sub-agent orchestration](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli) | official-docs | 2026-08-24 |
| `gemini-skills` | Google | [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/) | official-docs | 2026-08-24 |
| `gemini-headless` | Google | [Gemini CLI headless mode](https://geminicli.com/docs/cli/headless/) | official-docs | 2026-08-24 |
| `google-okf` | Google Cloud | [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format) | specification | 2026-08-24 |
| `mcp-spec` | MCP | [Model Context Protocol specification](https://modelcontextprotocol.io/specification) | specification | 2026-08-24 |
| `microsoft-agent-evaluation` | Microsoft | [Agent Framework evaluation](https://learn.microsoft.com/en-us/agent-framework/agents/evaluation) | official-docs | 2026-08-24 |
| `microsoft-skills-workflows` | Microsoft | [Skills or workflows in Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/agents/skills) | official-docs | 2026-08-24 |
| `nvidia-skillevaluator-method` | NVIDIA | [Evaluating agent skill performance](https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/) | official-method | 2026-08-24 |
| `nvidia-skillevaluator` | NVIDIA | [NVIDIA SkillEvaluator](https://docs.nvidia.com/skills/skillevaluator) | official-docs | 2026-08-24 |
| `openai-practical-agents` | OpenAI | [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | official-guide | 2026-08-24 |
| `codex-noninteractive` | OpenAI | [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) | official-docs | 2026-08-24 |
| `openai-programmatic-tools` | OpenAI | [Programmatic tool calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling) | official-docs | 2026-08-24 |
| `openai-skill-evals` | OpenAI | [Testing Agent Skills systematically with evals](https://developers.openai.com/blog/eval-skills) | official-guide | 2026-08-24 |
| `owasp-agentic` | OWASP | [OWASP Agentic AI threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | security-guidance | 2026-08-24 |

## Claim map

| Claim ID | Class | Statement | Sources |
|---|---|---|---|
| `adapter-bounds` | official | Headless harness adapters should make model, permissions, output format, persistence, and schema controls explicit. | `codex-noninteractive`, `anthropic-cli`, `gemini-headless` |
| `blind-comparison` | official | Blind A/B comparison reduces evaluator bias when comparing skill variants. | `anthropic-skill-creator` |
| `copilot-eager-skills` | official | Copilot SDK custom-agent skills are injected in full when the agent starts and are not inherited by child agents. | `github-sdk-custom-agents` |
| `headless-adapter-controls` | official | A reproducible headless run should make the model, permissions, persistence, output format, timeout, and working data explicit. | `anthropic-headless`, `anthropic-cli`, `codex-noninteractive`, `gemini-headless` |
| `mcp-boundary` | specification | MCP is a protocol boundary for external capabilities and context, not a replacement for every local function. | `mcp-spec` |
| `microsoft-agent-evaluation` | official | Evaluate agent and workflow behavior with repeatable inputs, expected tools, stored results, and repeated runs where nondeterminism matters. | `microsoft-agent-evaluation` |
| `okf-optional` | specification | OKF can represent knowledge as Markdown plus metadata, but a guide may keep human-readable Markdown as its canonical source. | `google-okf` |
| `overlap-not-count` | official | Tool or skill overlap is a stronger warning signal than raw catalogue count. | `openai-practical-agents`, `agent-skills-best-practices` |
| `pinned-validation` | heuristic | Pin architecture validators and fail when they are missing; optional silent gates do not provide reproducible proof. | `agnix-049` |
| `progressive-disclosure` | specification | Agent Skills use catalogue metadata, activated SKILL.md instructions, then on-demand resources. | `agent-skills-spec` |
| `scripts-for-determinism` | official | Use executable code for bounded filtering, joining, ranking, deduplication, aggregation, validation, and other exact work. | `openai-programmatic-tools`, `agent-skills-spec` |
| `skill-catalog-filtering` | official | Large shared skill libraries can be filtered, deduplicated, and cached before exposure to a requesting agent. | `microsoft-skills-workflows` |
| `skill-lift-eval` | official | Evaluate skills with structural gates, overlap checks, and with-skill versus without-skill live runs. | `nvidia-skillevaluator`, `nvidia-skillevaluator-method`, `openai-skill-evals` |
| `skill-security-review` | official | Treat skills, references, and bundled scripts as executable supply-chain inputs that require review, least privilege, sandboxing, and audit logs. | `microsoft-skills-workflows`, `owasp-agentic` |
| `skill-size-guidance` | specification | Keep SKILL.md under 500 lines and below about 5,000 tokens where practical; move conditional detail to references. | `agent-skills-spec`, `agent-skills-best-practices` |
| `skill-v-workflow` | official | Use a skill when the model should decide how; use a workflow when order, checkpoints, side effects, or approvals must be controlled. | `microsoft-skills-workflows` |
| `start-single-agent` | official | Start with one capable agent and add more agents only when complexity or tool overlap causes measured failures. | `openai-practical-agents`, `anthropic-decomposition-workshop` |
| `subagent-isolation` | official | Subagents are useful for isolated context, specialist tools, or independent parallel work. | `anthropic-subagents`, `github-custom-agents` |

## How to audit a claim

1. Find the evidence ID on the guide page.
2. Read its statement and source IDs above.
3. Open the first-party source.
4. Confirm that the source still supports the exact wording.
5. Update the review date or narrow the claim when product behaviour changes.

The ledger records support checked on a date. It does not freeze vendor behaviour forever.

- [`sources.json`](sources.json) is the machine-readable source list.
- [`claims.json`](claims.json) is the machine-readable claim map.
