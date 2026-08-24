"""Generate exact SVG diagrams. Text and geometry are deterministic."""

from __future__ import annotations

from pathlib import Path

PALETTE = {
    "ink": "#172033",
    "muted": "#5D6B82",
    "paper": "#F7F9FC",
    "line": "#CBD5E1",
    "blue": "#3B82F6",
    "teal": "#0F9D8A",
    "amber": "#D97706",
    "violet": "#7C3AED",
    "red": "#DC4C64",
    "white": "#FFFFFF",
}


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _svg(width: int, height: int, body: str, title: str, description: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{_escape(title)}</title>
<desc id="desc">{_escape(description)}</desc>
<style>
  .bg{{fill:{PALETTE["paper"]}}}.card{{fill:{PALETTE["white"]};stroke:{PALETTE["line"]};stroke-width:2}}
  .h{{font:700 26px system-ui,sans-serif;fill:{PALETTE["ink"]}}}.t{{font:600 17px system-ui,sans-serif;fill:{PALETTE["ink"]}}}
  .s{{font:400 14px system-ui,sans-serif;fill:{PALETTE["muted"]}}}.line{{stroke:{PALETTE["muted"]};stroke-width:2;fill:none}}
  .label{{font:700 12px ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}}
  @media(prefers-color-scheme:dark){{.bg{{fill:#0B1020}}.card{{fill:#141B2D;stroke:#344155}}.h,.t{{fill:#F2F5FA}}.s{{fill:#AAB6CA}}.line{{stroke:#8391A8}}}}
</style>
<rect class="bg" width="100%" height="100%" rx="24"/>
{body}
</svg>'''


def _card(x: int, y: int, w: int, h: int, title: str, subtitle: str, accent: str) -> str:
    return f'''<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/>
<rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{accent}"/>
<text class="t" x="{x + 24}" y="{y + 36}">{_escape(title)}</text>
<text class="s" x="{x + 24}" y="{y + 62}">{_escape(subtitle)}</text>'''


def _arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return f'''<path class="line" d="M{x1} {y1} L{x2} {y2}"/><path d="M{x2 - 8} {y2 - 5} L{x2} {y2} L{x2 - 8} {y2 + 5}" fill="none" stroke="{PALETTE["muted"]}" stroke-width="2"/>'''


def build_diagrams(output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    diagrams: dict[str, str] = {}

    body = '<text class="h" x="60" y="64">Agent systems: use the smallest effective primitive</text>'
    cards = [
        (60, 110, "Instructions", "Rules needed on most tasks", PALETTE["blue"]),
        (350, 110, "Skill", "Reusable judgment and procedure", PALETTE["teal"]),
        (640, 110, "Script / tool", "Exact or repetitive work", PALETTE["amber"]),
        (930, 110, "Subagent", "Isolated independent reasoning", PALETTE["violet"]),
    ]
    for x, y, title, sub, accent in cards:
        body += _card(x, y, 250, 100, title, sub, accent)
    body += _arrow(310, 160, 350, 160) + _arrow(600, 160, 640, 160) + _arrow(890, 160, 930, 160)
    body += '<text class="s" x="60" y="264">References add optional knowledge. MCP exposes external capability. Workflows control required order and side effects.</text>'
    diagrams["hero.svg"] = _svg(
        1240,
        310,
        body,
        "Agent systems field guide",
        "A spectrum from global instructions to isolated subagents.",
    )

    body = '<text class="h" x="50" y="56">What are you adding?</text>'
    body += _card(50, 95, 220, 88, "Always-needed rule", "Instructions", PALETTE["blue"])
    body += _card(310, 95, 220, 88, "Reusable procedure", "Skill", PALETTE["teal"])
    body += _card(570, 95, 220, 88, "Optional knowledge", "Reference", PALETTE["violet"])
    body += _card(830, 95, 220, 88, "Exact operation", "Script or tool", PALETTE["amber"])
    body += _card(180, 235, 220, 88, "External boundary", "MCP", PALETTE["red"])
    body += _card(440, 235, 220, 88, "Required control flow", "Workflow", PALETTE["blue"])
    body += _card(700, 235, 220, 88, "Separate context", "Subagent / agent", PALETTE["violet"])
    diagrams["primitive-map.svg"] = _svg(
        1100, 370, body, "Primitive map", "Seven architecture primitives grouped by purpose."
    )

    body = '<text class="h" x="50" y="54">Decision path</text>'
    steps = [
        (50, 90, "Can code do it exactly?", "Yes → script or tool", PALETTE["amber"]),
        (50, 205, "Must order or side effects be fixed?", "Yes → workflow", PALETTE["blue"]),
        (50, 320, "Is it a reusable procedure?", "Yes → skill", PALETTE["teal"]),
        (50, 435, "Is detail needed only sometimes?", "Yes → reference", PALETTE["violet"]),
        (50, 550, "Does it need isolated reasoning?", "Yes → subagent", PALETTE["red"]),
    ]
    for x, y, title, sub, accent in steps:
        body += _card(x, y, 560, 82, title, sub, accent)
        if y < 550:
            body += _arrow(330, y + 82, 330, y + 115)
    body += _card(
        680,
        250,
        300,
        120,
        "Default",
        "Keep one capable agent until an eval shows a real failure.",
        PALETTE["teal"],
    )
    diagrams["decision-tree.svg"] = _svg(
        1040,
        680,
        body,
        "Architecture decision tree",
        "Questions for selecting the smallest suitable primitive.",
    )

    body = '<text class="h" x="50" y="54">Progressive disclosure</text>'
    body += _card(50, 100, 260, 100, "1. Catalogue", "Name + description for discovery", PALETTE["blue"])
    body += _arrow(310, 150, 390, 150)
    body += _card(390, 100, 260, 100, "2. SKILL.md", "Core procedure after activation", PALETTE["teal"])
    body += _arrow(650, 150, 730, 150)
    body += _card(730, 100, 260, 100, "3. Resources", "References and scripts as needed", PALETTE["violet"])
    body += '<text class="s" x="50" y="260">The point is not smaller files. The point is less irrelevant context per task.</text>'
    diagrams["progressive-disclosure.svg"] = _svg(
        1040, 310, body, "Progressive disclosure", "Catalogue, activated skill, and on-demand resources."
    )

    body = '<text class="h" x="50" y="54">Architecture change gate</text>'
    labels = [
        (70, 115, "Observe", "Find the actual failure", PALETTE["blue"]),
        (340, 115, "Change one thing", "Cheapest suitable primitive", PALETTE["teal"]),
        (610, 115, "Run frozen eval", "Same cases and policy", PALETTE["amber"]),
        (880, 115, "Keep or revert", "Complexity must earn its cost", PALETTE["violet"]),
    ]
    for index, (x, y, title, sub, accent) in enumerate(labels):
        body += _card(x, y, 220, 100, title, sub, accent)
        if index < len(labels) - 1:
            body += _arrow(x + 220, y + 50, labels[index + 1][0], y + 50)
    body += '<path class="line" d="M990 215 C990 285 180 285 180 215"/><text class="s" x="474" y="278">expand cases after each failure</text>'
    diagrams["evaluation-loop.svg"] = _svg(
        1170, 330, body, "Architecture evaluation loop", "Observe, change, evaluate, and keep or revert."
    )

    body = '<text class="h" x="50" y="54">Decompose by failure, not file size</text>'
    body += _card(
        70,
        100,
        260,
        104,
        "Symptom",
        "Wrong route, excess context, repeated mechanics, or polluted reasoning",
        PALETTE["red"],
    )
    body += _arrow(330, 152, 430, 152)
    body += _card(
        430, 100, 260, 104, "Boundary", "Reference, script, workflow, or isolated worker", PALETTE["teal"]
    )
    body += _arrow(690, 152, 790, 152)
    body += _card(
        790, 100, 260, 104, "Proof", "Paired success, latency, token, and trace evidence", PALETTE["blue"]
    )
    diagrams["decomposition-flow.svg"] = _svg(
        1120, 270, body, "Decomposition flow", "A measured symptom leads to a boundary and proof."
    )

    body = '<text class="h" x="50" y="54">Context budget: eager versus on demand</text>'
    body += '<text class="t" x="70" y="105">Eager</text><rect x="70" y="125" width="820" height="58" rx="12" fill="#E5E7EB"/>'
    segments = [
        (360, PALETTE["blue"], "active"),
        (260, PALETTE["red"], "other skills"),
        (200, PALETTE["violet"], "unused refs"),
    ]
    cursor = 70
    for width, color, label in segments:
        body += f'<rect x="{cursor}" y="125" width="{width}" height="58" fill="{color}"/><text x="{cursor + 12}" y="160" font-family="system-ui" font-size="14" fill="white">{label}</text>'
        cursor += width
    body += '<text class="t" x="70" y="245">Progressive</text><rect x="70" y="265" width="470" height="58" rx="12" fill="#E5E7EB"/>'
    segments = [
        (110, PALETTE["blue"], "catalog"),
        (230, PALETTE["teal"], "active skill"),
        (130, PALETTE["violet"], "needed ref"),
    ]
    cursor = 70
    for width, color, label in segments:
        body += f'<rect x="{cursor}" y="265" width="{width}" height="58" fill="{color}"/><text x="{cursor + 10}" y="300" font-family="system-ui" font-size="14" fill="white">{label}</text>'
        cursor += width
    diagrams["context-budget.svg"] = _svg(
        980,
        380,
        body,
        "Context budget",
        "Eager loading includes unused skill and reference content; progressive loading does not.",
    )

    body = '<text class="h" x="50" y="54">Same six skills. Clearer boundaries.</text>'
    body += '<rect class="card" x="60" y="100" width="430" height="220" rx="20"/>'
    body += f'<rect x="60" y="100" width="8" height="220" rx="4" fill="{PALETTE["red"]}"/>'
    body += '<text class="label" x="88" y="135" fill="#DC4C64">BASELINE</text>'
    body += '<text class="t" x="88" y="172">Broad, overlapping descriptions</text>'
    body += '<text class="s" x="88" y="205">Accuracy</text><text class="h" x="88" y="246">37.5%</text>'
    body += '<text class="s" x="270" y="205">Ambiguity</text><text class="h" x="270" y="246">70.8%</text>'
    body += '<text class="s" x="88" y="286">Several skills claim review, release, security,</text>'
    body += '<text class="s" x="88" y="307">migration, documentation, and production risk.</text>'
    body += _arrow(510, 210, 610, 210)
    body += '<rect class="card" x="630" y="100" width="430" height="220" rx="20"/>'
    body += f'<rect x="630" y="100" width="8" height="220" rx="4" fill="{PALETTE["teal"]}"/>'
    body += '<text class="label" x="658" y="135" fill="#0F9D8A">CANDIDATE</text>'
    body += '<text class="t" x="658" y="172">Distinct intent, evidence, and output</text>'
    body += '<text class="s" x="658" y="205">Accuracy</text><text class="h" x="658" y="246">95.8%</text>'
    body += '<text class="s" x="840" y="205">Ambiguity</text><text class="h" x="840" y="246">12.5%</text>'
    body += '<text class="s" x="658" y="286">Skill names, jobs, cases, and router stay fixed.</text>'
    body += '<text class="s" x="658" y="307">Only descriptions and negative boundaries change.</text>'
    body += '<text class="s" x="60" y="365">Deterministic structural lab • 24 frozen prompts • not a live model benchmark</text>'
    diagrams["routing-proof.svg"] = _svg(
        1120,
        410,
        body,
        "Routing boundary proof",
        "The same six skills improve structural routing after descriptions are made distinct.",
    )

    for name, content in diagrams.items():
        (output_dir / name).write_text(content + "\n", encoding="utf-8")
    return diagrams


def check_diagrams(output_dir: Path) -> list[str]:
    expected_dir = output_dir.parent / ".diagram-check"
    expected_dir.mkdir(exist_ok=True)
    expected = build_diagrams(expected_dir)
    drift: list[str] = []
    for name, content in expected.items():
        actual = output_dir / name
        if not actual.exists() or actual.read_text(encoding="utf-8") != content + "\n":
            drift.append(name)
    for path in expected_dir.glob("*.svg"):
        path.unlink()
    expected_dir.rmdir()
    return drift
