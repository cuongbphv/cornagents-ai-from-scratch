# LLM From Scratch — a 15-Week Self-Study Roadmap

**From Transformer internals to an Agentic SDLC & Graph Engineering.**

This repository is a structured, self-paced curriculum for going from "I can call an LLM API" to genuinely understanding how large language models work — and then applying that understanding to build **CornAgents.AI**, a personal agentic-SDLC framework anchored to the Finance Banking domain.

The material is spread evenly across **15 weeks (~10–15 hrs/week, ~3.5–4 months part-time)** so no single week is overloaded. Every week has its own folder with a README, starter code skeletons, note templates, and a self-check quiz.

## Why this roadmap

Most LLM tutorials teach you to *use* models. This roadmap makes you *build* them first — backprop, attention, and a GPT-2-class model from scratch in pure PyTorch — because the applied phases (RAG, fine-tuning, agents) only truly click when you understand what is happening underneath. The final phase turns that understanding into working multi-agent systems, following the engineering progression: **Prompt → Context → Harness → Loop → Graph engineering**.

## The three phases

### Phase 1 — Deep Internals (Weeks 1–7)
Build and pretrain a GPT-2-class model from scratch.

| Week | Topic |
|------|-------|
| 1 | Math foundations + PyTorch prerequisites |
| 2 | Backprop from scratch (micrograd) + transformer mental model |
| 3 | Tokenization, embeddings, attention from scratch |
| 4 | Assemble and run the full GPT model |
| 5 | Pretraining: training loop + a real (cloud) GPT-2 run |
| 6 | Instruction fine-tuning (classification + instruction-following + LoRA) |
| 7 | Intro to alignment: SFT → Reward Model → DPO/PPO → GRPO |

### Phase 2 — Applied: RAG & Fine-Tuning (Weeks 8–11)
Move from from-scratch code to production tooling.

| Week | Topic |
|------|-------|
| 8 | Practical QLoRA fine-tuning (Unsloth, 7B–8B on 8GB VRAM) |
| 9 | Mac/MLX fine-tuning + local inference stack (Ollama, LM Studio) |
| 10 | End-to-end RAG pipeline over your own domain documents |
| 11 | Advanced RAG: hybrid search, reranking, RAGAS evaluation, tracing |

### Phase 3 — Agentic SDLC: CornAgents.AI (Weeks 12–15)
Build a multi-agent software-delivery assistant, grounded in your domain.

| Week | Topic |
|------|-------|
| 12 | Agentic foundations: the 5 engineering layers, Claude Agent SDK, MCP, your first measured loop |
| 13 | Map LLMs onto SDLC stages; multi-agent graph with the 5 Anthropic workflow patterns |
| 14 | **Graph Engineering**: a knowledge graph (built entirely from Claude API calls) as shared memory, grounding layer, and persistent world model |
| 15 | Capstone: ship one polished workflow end-to-end + evaluation & observability |

## Repository layout

```
Week-00/          Full roadmap (Vietnamese + English) + advanced-topics gap analysis
Week-01..15/      One folder per week: README, code skeletons, note templates, quiz
docs/             Source documents for Phase 3:
                    - Graph-Engineering-Athropic-Playbook.pdf   (knowledge-graph pipeline)
                    - Graph-Engineering-Athropic-Karpathy-Loop.pdf (loop → swarm → graph)
                    - 5-layers-multi-agent.jpg                  (the 5 engineering layers)
Report/           Interactive web portal: roadmap, per-week checklists, flip-card quizzes
                  (open Report/index.html in a browser; progress saved locally)
scripts/          quiz_bank.json (single source of truth, 93 questions)
                  generate_quiz.py (regenerates Week-XX quizzes + portal data)
```

## How to use it

1. **Read the plan** in [Week-00/plan_llm_from_scratch_en.md](Week-00/plan_llm_from_scratch_en.md) (or the Vietnamese version) for the detailed week-by-week objectives, sources, and deliverables.
2. **Work one week at a time**: each `Week-XX/README.md` lists objectives, tasks, deliverables, and a progress checklist. Code the skeletons yourself first, then compare against the canonical sources.
3. **Self-test**: answer `Week-XX/quiz.md` before opening `quiz_solution.md`. Quizzes are generated from `scripts/quiz_bank.json`:
   ```bash
   python scripts/generate_quiz.py            # regenerate everything
   python scripts/generate_quiz.py --week 3   # one week only
   ```
4. **Go deeper when the week calls for it**: [Week-00/advanced_topics_vi.md](Week-00/advanced_topics_vi.md) holds the advanced material (modern architecture, inference, training dynamics, alignment, evaluation, agentic/graph engineering). It is **not** meant to be read front-to-back — it opens with a navigation table mapping *each week → the exact sections to read*, and every week's README carries a matching "🚀 Bổ sung nâng cao" block pointing back. The anchoring is bidirectional, so you never have to guess when a topic belongs. Weeks 1–2 deliberately have none.
5. **Track progress** in the web portal: open `Report/index.html` — interactive checklists, phase progress, and flip-card quizzes (state is stored in your browser).
6. **Use Claude as a co-learner**: implement first, then have Claude review; paste loss curves and stack traces for debugging; rubber-duck architecture decisions in Phase 3.

## Hardware assumptions

| Machine | Role |
|---------|------|
| RTX 3070 Ti (8GB) | From-scratch coding, small training runs, 7B–8B QLoRA |
| MacBook Pro 24GB (MLX) | Local inference of quantized 7B–14B models, silent LoRA fine-tunes |
| Cloud (RunPod / Lambda / Colab) | The one-time GPT-2 pretrain (~$15–35) and any heavier fine-tune |

Rule of thumb: the moment a local run projects beyond ~24h (or OOMs at batch size 1), move it to a rented GPU.

## What is CornAgents.AI?

CornAgents.AI is **your own concept, not a product** — the name of the personal agentic-SDLC framework you build in Phase 3 on top of **Claude Agent SDK + MCP + LangGraph/CrewAI**, with a knowledge-graph layer (Week 14) for shared memory and grounded fact-checking. All applied artifacts (RAG corpus, fine-tuning dataset, capstone) anchor to the **Finance Banking domain**, kept generic — pick the business area you know best.

## Core sources

- **Sebastian Raschka** — *Build a Large Language Model (From Scratch)* + `reasoning-from-scratch`
- **Andrej Karpathy** — *Neural Networks: Zero to Hero*, nanoGPT, nanochat, autoresearch
- **Giles Thomas** — *LLM from scratch* blog series (parts 1–33)
- **FareedKhan-dev** — `train-llm-from-scratch` (full alignment suite in pure PyTorch)
- **Anthropic** — Building Effective AI Agents, Claude Agent SDK, MCP, Knowledge Graph Construction Cookbook
- The two Graph-Engineering study notes and the 5-layers diagram in [docs/](docs/)

---

> *"The model is becoming a commodity. The system around it is where the real engineering lives now."*
