"""Generate README infographic SVGs. Run: python docs/diagrams/_gen_svgs.py"""
from __future__ import annotations

import html as htmlmod
from pathlib import Path

OUT = Path(__file__).resolve().parent

C = {
    "bg": "#eef3f9",
    "card": "#ffffff",
    "ink": "#0f172a",
    "muted": "#64748b",
    "line": "#94a3b8",
    "softline": "#dbe3ee",
    "data": "#0d9488",
    "model": "#2563eb",
    "train": "#d97706",
    "align": "#e11d48",
    "eval": "#16a34a",
    "rag": "#0891b2",
    "agent": "#9333ea",
    "graph": "#4f46e5",
}


def r(v: float, n: int = 1) -> float:
    return round(v, n)


def font(size: int = 13, weight: int = 600, fill: str | None = None) -> str:
    fill = fill or C["ink"]
    return (
        'font-family="IBM Plex Sans, Segoe UI, Helvetica, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}"'
    )


def head(w: int, h: int, title: str, desc: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <title>{htmlmod.escape(title)}</title>
  <desc>{htmlmod.escape(desc)}</desc>
  <defs>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#0f172a" opacity="0.05"/>
    </pattern>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
    <linearGradient id="rail" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{C['data']}"/>
      <stop offset="20%" stop-color="{C['model']}"/>
      <stop offset="40%" stop-color="{C['train']}"/>
      <stop offset="55%" stop-color="{C['align']}"/>
      <stop offset="70%" stop-color="{C['rag']}"/>
      <stop offset="85%" stop-color="{C['agent']}"/>
      <stop offset="100%" stop-color="{C['graph']}"/>
    </linearGradient>
    <marker id="arrowHead" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="{C['line']}"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="{C['bg']}"/>
  <rect width="{w}" height="{h}" rx="18" fill="url(#dots)"/>
"""


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body, encoding="utf-8")
    print(f"wrote {name} ({path.stat().st_size} bytes)")


def gen_pipeline() -> None:
    w, h = 1000, 260
    stages = [
        ("1", "Data", C["data"]),
        ("2", "Token", C["data"]),
        ("3", "Model", C["model"]),
        ("4", "Pretrain", C["train"]),
        ("5", "Align", C["align"]),
        ("6", "Eval", C["eval"]),
        ("7", "Serve", C["eval"]),
        ("8", "RAG", C["rag"]),
        ("9", "Agent", C["agent"]),
        ("10", "Graph", C["graph"]),
    ]
    n = len(stages)
    margin = 36
    gap = 10
    pw = r((w - 2 * margin - (n - 1) * gap) / n, 1)
    ph = 72
    py = 108
    parts = [head(w, h, "Pipeline journey", "End-to-end pipeline from Data to Graph")]
    parts.append(f'<text x="{margin}" y="38" {font(20, 700)}>Pipeline · hành trình end-to-end</text>')
    parts.append(
        f'<text x="{margin}" y="60" {font(12, 500, C["muted"])}>'
        "Data → Model → Align → Serve → RAG → Agent → Graph</text>"
    )
    # Rail behind cards (subtle), motion above legend
    rail_y = py + ph + 18
    parts.append(
        f'<rect x="{margin}" y="{rail_y - 3}" width="{w - 2 * margin}" height="6" '
        f'rx="3" fill="url(#rail)" opacity="0.35"/>'
    )
    path = f"M {r(margin + pw / 2)} {rail_y} H {r(w - margin - pw / 2)}"
    for rad, col, beg in ((5, C["data"], "0s"), (4, C["agent"], "1.6s"), (4, C["graph"], "3.2s")):
        parts.append(
            f'<circle r="{rad}" fill="{col}" opacity="0.95">'
            f'<animateMotion dur="5.5s" begin="{beg}" repeatCount="indefinite" path="{path}"/>'
            "</circle>"
        )
    for i, (num, lab, col) in enumerate(stages):
        x = r(margin + i * (pw + gap), 1)
        parts.append(f'<g transform="translate({x},{py})">')
        parts.append(
            f'<rect width="{pw}" height="{ph}" rx="14" fill="{C["card"]}" '
            f'stroke="{col}" stroke-width="2" filter="url(#soft)"/>'
        )
        parts.append(f'<rect width="{pw}" height="7" rx="3.5" fill="{col}"/>')
        parts.append(f'<circle cx="{r(pw / 2)}" cy="32" r="12" fill="{col}"/>')
        parts.append(
            f'<text x="{r(pw / 2)}" y="36" text-anchor="middle" {font(11, 700, "#fff")}>{num}</text>'
        )
        parts.append(
            f'<text x="{r(pw / 2)}" y="58" text-anchor="middle" {font(12, 700)}>{lab}</text>'
        )
        parts.append("</g>")
    legend = [
        ("Data/Token", C["data"]),
        ("Model", C["model"]),
        ("Train", C["train"]),
        ("Align", C["align"]),
        ("Eval/Serve", C["eval"]),
        ("RAG", C["rag"]),
        ("Agent", C["agent"]),
        ("Graph", C["graph"]),
    ]
    lx = margin
    for lab, col in legend:
        parts.append(f'<rect x="{lx}" y="{h - 28}" width="10" height="10" rx="3" fill="{col}"/>')
        parts.append(f'<text x="{lx + 15}" y="{h - 19}" {font(11, 500, C["muted"])}>{lab}</text>')
        lx += 112
    write("01-pipeline-journey.svg", "\n".join(parts) + "</svg>\n")


def gen_phases() -> None:
    w, h = 960, 300
    parts = [head(w, h, "Three phases", "15 weeks across three phases")]
    parts.append(f'<text x="32" y="40" {font(20, 700)}>Ba phase · 15 tuần</text>')
    parts.append(
        f'<text x="32" y="62" {font(12, 500, C["muted"])}>'
        "Deep Internals → RAG &amp; Fine-Tuning → Agentic SDLC</text>"
    )
    phases = [
        (32, C["model"], "Phase 1", "Deep Internals", "Tuần 1–7", ["Build &amp; pretrain", "GPT-2-class from scratch"]),
        (336, C["data"], "Phase 2", "RAG &amp; Fine-Tuning", "Tuần 8–11", ["QLoRA, local serve", "RAG + RAGAS"]),
        (640, C["agent"], "Phase 3", "Agentic SDLC", "Tuần 12–15", ["CornAgents.AI", "agents + knowledge graph"]),
    ]
    for i, (x, col, p, title, weeks, body) in enumerate(phases):
        parts.append("<g>")
        parts.append(
            f'<rect x="{x}" y="84" width="288" height="176" rx="18" fill="{C["card"]}" '
            f'stroke="{col}" stroke-width="2.5" filter="url(#soft)"/>'
        )
        parts.append(f'<rect x="{x}" y="84" width="288" height="44" rx="18" fill="{col}"/>')
        parts.append(f'<rect x="{x}" y="110" width="288" height="18" fill="{col}"/>')
        parts.append(f'<circle cx="{x + 28}" cy="106" r="14" fill="#fff" opacity="0.95"/>')
        parts.append(f'<text x="{x + 28}" y="111" text-anchor="middle" {font(13, 700, col)}>{i + 1}</text>')
        parts.append(f'<text x="{x + 52}" y="111" {font(15, 700, "#fff")}>{p}</text>')
        parts.append(f'<text x="{x + 24}" y="156" {font(15, 700)}>{title}</text>')
        parts.append(f'<text x="{x + 24}" y="180" {font(12, 600, C["muted"])}>{weeks}</text>')
        for j, line in enumerate(body):
            parts.append(f'<text x="{x + 24}" y="{208 + j * 20}" {font(13, 500)}>{line}</text>')
        parts.append(
            f'<rect x="{x - 2}" y="82" width="292" height="180" rx="20" fill="none" '
            f'stroke="{col}" stroke-width="2" opacity="0">'
        )
        parts.append(
            f'<animate attributeName="opacity" values="0;0.35;0" dur="3.8s" '
            f'begin="{r(i * 0.45, 2)}s" repeatCount="indefinite"/>'
        )
        parts.append("</rect></g>")
    for x, col in ((320, C["data"]), (624, C["agent"])):
        parts.append(
            f'<path d="M{x} 172 H{x + 16}" stroke="{C["line"]}" stroke-width="2.5" '
            'marker-end="url(#arrowHead)"/>'
        )
        parts.append(
            f'<circle r="4" fill="{col}">'
            f'<animateMotion dur="2.2s" repeatCount="indefinite" path="M{x} 172 H{x + 16}"/>'
            "</circle>"
        )
    write("02-three-phases.svg", "\n".join(parts) + "</svg>\n")


def gen_attention() -> None:
    w, h = 540, 390
    layers = [
        (C["data"], "Embed + positional encoding"),
        (C["model"], "Causal multi-head attention"),
        (C["model"], "Transformer block (N×)"),
        (C["train"], "LM head → next-token logits"),
    ]
    parts = [head(w, h, "Attention stack", "Minimal GPT forward pass")]
    parts.append(f'<text x="28" y="40" {font(20, 700)}>Mental model · attention stack</text>')
    parts.append(f'<text x="28" y="62" {font(12, 500, C["muted"])}>Phase 1 · forward pass tối giản</text>')
    ly = 88
    for i, (col, lab) in enumerate(layers):
        parts.append(
            f'<rect x="64" y="{ly}" width="412" height="54" rx="14" fill="{C["card"]}" '
            f'stroke="{col}" stroke-width="2" filter="url(#soft)"/>'
        )
        parts.append(f'<rect x="64" y="{ly}" width="12" height="54" rx="6" fill="{col}"/>')
        parts.append(f'<circle cx="106" cy="{ly + 27}" r="15" fill="{col}"/>')
        parts.append(
            f'<text x="106" y="{ly + 32}" text-anchor="middle" {font(13, 700, "#fff")}>{i + 1}</text>'
        )
        parts.append(f'<text x="136" y="{ly + 32}" {font(14, 600)}>{lab}</text>')
        if i < 3:
            parts.append(
                f'<line x1="270" y1="{ly + 54}" x2="270" y2="{ly + 72}" '
                f'stroke="{C["softline"]}" stroke-width="3"/>'
            )
        ly += 70
    end_y = 88 + 3 * 70 + 27
    parts.append(
        f'<circle r="5" fill="{C["model"]}">'
        f'<animateMotion dur="4s" repeatCount="indefinite" path="M270 115 V {end_y}"/>'
        "</circle>"
    )
    write("03-attention-stack.svg", "\n".join(parts) + "</svg>\n")


def gen_alignment() -> None:
    w, h = 880, 230
    steps = [
        ("SFT", C["train"]),
        ("Reward Model", C["align"]),
        ("DPO / PPO", C["align"]),
        ("GRPO", C["agent"]),
    ]
    parts = [head(w, h, "Alignment flow", "SFT to GRPO")]
    parts.append(f'<text x="32" y="40" {font(20, 700)}>Alignment · Tuần 7</text>')
    parts.append(
        f'<text x="32" y="62" {font(12, 500, C["muted"])}>'
        "Neo FareedKhan-style pipeline, scaled-down để học</text>"
    )
    sw, sy, sh = 175, 100, 64
    for i, (lab, col) in enumerate(steps):
        x = 40 + i * 210
        parts.append(f'<g transform="translate({x},{sy})">')
        parts.append(f'<rect width="{sw}" height="{sh}" rx="14" fill="{col}" filter="url(#soft)"/>')
        parts.append(f'<circle cx="28" cy="{r(sh / 2)}" r="13" fill="#fff" opacity="0.92"/>')
        parts.append(
            f'<text x="28" y="{r(sh / 2 + 5)}" text-anchor="middle" {font(12, 700, col)}>{i + 1}</text>'
        )
        parts.append(
            f'<text x="{r((sw + 28) / 2 + 10)}" y="{r(sh / 2 + 5)}" text-anchor="middle" '
            f'{font(14, 700, "#fff")}>{lab}</text>'
        )
        parts.append("</g>")
        if i < 3:
            parts.append(
                f'<path d="M{x + sw + 6} {r(sy + sh / 2)} H{x + 204}" stroke="{C["line"]}" '
                'stroke-width="2.5" marker-end="url(#arrowHead)"/>'
            )
    mid_y = r(sy + sh / 2)
    parts.append(
        f'<circle r="5" fill="#fff" stroke="{C["align"]}" stroke-width="2">'
        f'<animateMotion dur="4.5s" repeatCount="indefinite" '
        f'path="M {r(40 + sw / 2)} {mid_y} H {r(40 + 3 * 210 + sw / 2)}"/>'
        "</circle>"
    )
    parts.append(
        f'<text x="440" y="{h - 28}" text-anchor="middle" {font(11, 500, C["muted"])}>'
        "SFT → RM → preference / RL → GRPO</text>"
    )
    write("04-alignment-flow.svg", "\n".join(parts) + "</svg>\n")


def gen_pipeline_weeks() -> None:
    w, h = 960, 388
    rows = [
        (C["data"], "Data / Token / Model", "W1–W4"),
        (C["train"], "Pretrain", "W5"),
        (C["align"], "Align (SFT → RM → DPO/PPO → GRPO)", "W6–W7"),
        (C["eval"], "Eval / Serve", "W5, W8–W9"),
        (C["rag"], "RAG", "W10–W11"),
        (C["agent"], "Agent", "W12–W13"),
        (C["graph"], "Graph", "W14–W15"),
    ]
    parts = [head(w, h, "Pipeline mapped to weeks", "Stages mapped to curriculum weeks")]
    parts.append(f'<text x="32" y="40" {font(20, 700)}>Map pipeline ↔ tuần</text>')
    parts.append(
        f'<text x="32" y="62" {font(12, 500, C["muted"])}>'
        "Cùng một hành trình, hai khung nhìn song song</text>"
    )
    parts.append(f'<text x="52" y="94" {font(11, 700, C["muted"])}>STAGE</text>')
    parts.append(f'<text x="700" y="94" {font(11, 700, C["muted"])}>TUẦN NEO</text>')
    y = 110
    row_h = 34
    for i, (col, stage, weeks) in enumerate(rows):
        parts.append(
            f'<rect x="32" y="{y}" width="560" height="{row_h}" rx="10" fill="{C["card"]}" '
            f'stroke="{C["softline"]}"/>'
        )
        parts.append(f'<rect x="32" y="{y}" width="8" height="{row_h}" rx="4" fill="{col}"/>')
        parts.append(f'<text x="52" y="{y + 22}" {font(13, 600)}>{stage}</text>')
        parts.append(
            f'<line x1="600" y1="{y + 17}" x2="650" y2="{y + 17}" stroke="{col}" '
            'stroke-width="2" stroke-dasharray="5 4"/>'
        )
        parts.append(f'<circle cx="625" cy="{y + 17}" r="3.5" fill="{col}"/>')
        parts.append(f'<rect x="650" y="{y}" width="278" height="{row_h}" rx="10" fill="{col}"/>')
        parts.append(
            f'<text x="789" y="{y + 22}" text-anchor="middle" {font(13, 700, "#fff")}>{weeks}</text>'
        )
        parts.append(
            f'<rect x="32" y="{y}" width="896" height="{row_h}" rx="10" fill="{col}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.08;0" dur="5.5s" '
            f'begin="{r(i * 0.4, 1)}s" repeatCount="indefinite"/></rect>'
        )
        y += row_h + 4
    write("05-pipeline-weeks.svg", "\n".join(parts) + "</svg>\n")


def gen_cloud() -> None:
    w, h = 760, 340
    parts = [head(w, h, "Local vs cloud", "Decision tree for renting GPU")]
    parts.append(f'<text x="32" y="38" {font(20, 700)}>Quyết định local ↔ cloud</text>')
    parts.append(
        f'<text x="32" y="60" {font(12, 500, C["muted"])}>'
        "Validate local trước; thuê GPU khi chạm ngưỡng</text>"
    )
    # Start
    parts.append(
        f'<rect x="270" y="78" width="220" height="40" rx="20" fill="{C["model"]}" filter="url(#soft)"/>'
    )
    parts.append(f'<text x="380" y="103" text-anchor="middle" {font(13, 700, "#fff")}>Bắt đầu workload</text>')
    parts.append(f'<line x1="380" y1="118" x2="380" y2="140" stroke="{C["line"]}" stroke-width="2.5"/>')
    # Local validate
    parts.append(
        f'<rect x="250" y="140" width="260" height="42" rx="14" fill="{C["card"]}" '
        f'stroke="{C["data"]}" stroke-width="2" filter="url(#soft)"/>'
    )
    parts.append(f'<text x="380" y="166" text-anchor="middle" {font(13, 600)}>Validate / train local</text>')
    parts.append(f'<line x1="380" y1="182" x2="380" y2="204" stroke="{C["line"]}" stroke-width="2.5"/>')
    # Decision
    parts.append(
        f'<rect x="210" y="204" width="340" height="52" rx="14" fill="{C["train"]}" filter="url(#soft)"/>'
    )
    parts.append(f'<text x="380" y="226" text-anchor="middle" {font(13, 700, "#fff")}>OOM ở batch=1</text>')
    parts.append(
        f'<text x="380" y="244" text-anchor="middle" {font(11, 500, "#fff")}>'
        "hoặc dự phóng &gt; 24 giờ?</text>"
    )
    # Branch connectors
    parts.append(
        f'<path d="M210 230 H120 V268" fill="none" stroke="{C["eval"]}" stroke-width="2.5" '
        'marker-end="url(#arrowHead)"/>'
    )
    parts.append(
        f'<path d="M550 230 H640 V268" fill="none" stroke="{C["align"]}" stroke-width="2.5" '
        'marker-end="url(#arrowHead)"/>'
    )
    parts.append(f'<text x="150" y="222" text-anchor="middle" {font(11, 700, C["eval"])}>Không</text>')
    parts.append(f'<text x="610" y="222" text-anchor="middle" {font(11, 700, C["align"])}>Có</text>')
    # Outcomes — clear padding from bottom edge
    parts.append(
        f'<rect x="40" y="276" width="160" height="36" rx="12" fill="{C["eval"]}" filter="url(#soft)"/>'
    )
    parts.append(f'<text x="120" y="299" text-anchor="middle" {font(13, 700, "#fff")}>Ở lại local</text>')
    parts.append(
        f'<rect x="560" y="276" width="160" height="36" rx="12" fill="{C["align"]}" filter="url(#soft)"/>'
    )
    parts.append(f'<text x="640" y="299" text-anchor="middle" {font(13, 700, "#fff")}>Thuê cloud GPU</text>')
    # Motion
    parts.append(
        f'<circle r="4" fill="{C["model"]}">'
        '<animateMotion dur="3s" repeatCount="indefinite" path="M380 98 V161"/>'
        "</circle>"
    )
    parts.append(
        f'<circle r="3.5" fill="{C["eval"]}">'
        '<animateMotion dur="3.5s" begin="0.4s" repeatCount="indefinite" path="M210 230 H120 V294"/>'
        "</circle>"
    )
    parts.append(
        f'<circle r="3.5" fill="{C["align"]}">'
        '<animateMotion dur="3.5s" begin="1s" repeatCount="indefinite" path="M550 230 H640 V294"/>'
        "</circle>"
    )
    write("06-cloud-decision.svg", "\n".join(parts) + "</svg>\n")


def gen_layers() -> None:
    w, h = 580, 430
    layers = [
        (C["data"], "1 · Prompt engineering"),
        (C["model"], "2 · Context engineering"),
        (C["train"], "3 · Harness engineering"),
        (C["align"], "4 · Loop engineering"),
        (C["graph"], "5 · Graph engineering"),
    ]
    parts = [head(w, h, "Five engineering layers", "Prompt to Graph")]
    parts.append(f'<text x="28" y="40" {font(20, 700)}>5 tầng · CornAgents.AI</text>')
    parts.append(
        f'<text x="28" y="62" {font(12, 500, C["muted"])}>Phase 3 · từ prompt tới knowledge graph</text>'
    )
    ly = 92
    for i, (col, lab) in enumerate(layers):
        ww = 440 - i * 22
        xx = r((w - ww) / 2, 1)
        parts.append(
            f'<rect x="{xx}" y="{ly}" width="{ww}" height="48" rx="14" fill="{col}" filter="url(#soft)"/>'
        )
        parts.append(
            f'<text x="{r(w / 2)}" y="{ly + 30}" text-anchor="middle" {font(14, 700, "#fff")}>{lab}</text>'
        )
        parts.append(
            f'<rect x="{xx}" y="{ly}" width="{ww}" height="48" rx="14" fill="#fff" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.14;0" dur="3.6s" '
            f'begin="{r(i * 0.28, 2)}s" repeatCount="indefinite"/></rect>'
        )
        if i < 4:
            parts.append(
                f'<line x1="{r(w / 2)}" y1="{ly + 48}" x2="{r(w / 2)}" y2="{ly + 60}" '
                f'stroke="{C["softline"]}" stroke-width="3"/>'
            )
        ly += 62
    parts.append(
        f'<circle r="5" fill="#fff" stroke="{C["graph"]}" stroke-width="2">'
        f'<animateMotion dur="4.2s" repeatCount="indefinite" '
        f'path="M{r(w / 2)} 116 V {92 + 4 * 62 + 24}"/>'
        "</circle>"
    )
    write("07-five-layers.svg", "\n".join(parts) + "</svg>\n")


def gen_palette() -> None:
    text = f"""# Diagram palette

Stage coloring for README infographics (original assets).

| Token | Hex | Meaning |
|-------|-----|---------|
| data | `{C["data"]}` | Data / Token |
| model | `{C["model"]}` | Model / Phase 1 |
| train | `{C["train"]}` | Pretrain / SFT |
| align | `{C["align"]}` | Alignment / cloud branch |
| eval | `{C["eval"]}` | Eval / Serve / stay local |
| rag | `{C["rag"]}` | RAG |
| agent | `{C["agent"]}` | Agent |
| graph | `{C["graph"]}` | Graph / Phase 3 |

Motion: subtle SMIL (`animate` / `animateMotion`). GitHub README keeps SMIL when SVG is embedded via `img`; some scrapers/proxies show a static first frame.

Regenerate: `python docs/diagrams/_gen_svgs.py`
"""
    (OUT / "PALETTE.md").write_text(text, encoding="utf-8")
    print("wrote PALETTE.md")


def write_preview_html() -> None:
    prev = Path("/tmp/svgprev")
    prev.mkdir(parents=True, exist_ok=True)
    for svg in OUT.glob("0*.svg"):
        (prev / svg.name).write_bytes(svg.read_bytes())
    lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>preview</title></head>",
        "<body style='margin:20px;background:#cbd5e1'>",
    ]
    for svg in sorted(prev.glob("0*.svg")):
        lines.append(f"<h3 style='font-family:sans-serif'>{svg.name}</h3>")
        lines.append(
            f"<img src='{svg.name}' style='display:block;margin:0 0 28px;max-width:100%;"
            "background:#fff;border-radius:12px'/>"
        )
    lines.append("</body></html>")
    (prev / "preview.html").write_text("\n".join(lines), encoding="utf-8")
    print("wrote /tmp/svgprev/preview.html")


if __name__ == "__main__":
    gen_pipeline()
    gen_phases()
    gen_attention()
    gen_alignment()
    gen_pipeline_weeks()
    gen_cloud()
    gen_layers()
    gen_palette()
    write_preview_html()
