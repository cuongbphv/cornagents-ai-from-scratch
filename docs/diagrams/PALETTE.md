# Diagram palette

Stage coloring for README infographics (original assets).

| Token | Hex | Meaning |
|-------|-----|---------|
| data | `#0d9488` | Data / Token |
| model | `#2563eb` | Model / Phase 1 |
| train | `#d97706` | Pretrain / SFT |
| align | `#e11d48` | Alignment / cloud branch |
| eval | `#16a34a` | Eval / Serve / stay local |
| rag | `#0891b2` | RAG |
| agent | `#9333ea` | Agent |
| graph | `#4f46e5` | Graph / Phase 3 |

Motion: subtle SMIL (`animate` / `animateMotion`). GitHub README keeps SMIL when SVG is embedded via `img`; some scrapers/proxies show a static first frame.

Regenerate: `python docs/diagrams/_gen_svgs.py`
