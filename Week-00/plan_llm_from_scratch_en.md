# From Transformer Internals to an Agentic SDLC & Graph Engineering: A 15-Week LLM Mastery Roadmap

> **Disclaimer:** personal academic, research-only, non-commercial project. This document references open sources only (public GitHub repos, open-access papers, official tool documentation, verified open-license datasets). See [CLAUDE.md](../CLAUDE.md).

## TL;DR
- **Achievable in ~3.5–4 months part-time (10–15 hrs/week)**, with the material spread evenly across 15 weeks so no single week is overloaded: Weeks 1–7 build and pretrain a GPT-2-class model from scratch (open-source repos micrograd/makemore/nanoGPT/nanochat + `train-llm-from-scratch` + open papers; instruction fine-tuning and alignment are now two separate weeks); Weeks 8–11 do applied RAG and QLoRA/MLX fine-tuning; Weeks 12–15 build an agentic SDLC assistant — including a dedicated **Graph Engineering** week (knowledge graph as shared memory for multi-agent systems, per the documents in `docs/`). The hard constraint is your 8GB RTX 3070 Ti — it is excellent for learning-scale from-scratch coding and 7B–8B QLoRA fine-tuning, but full GPT-2 pretraining and any 13B+ work should go to cheap cloud GPUs.
- **Hardware verdict:** Use the 3070 Ti for from-scratch coding/small training and 7B QLoRA via Unsloth; use the 24GB MacBook Pro (MLX) for local inference of quantized 7B–14B models and small LoRA fine-tunes; rent a RunPod/Lambda GPU for the one-time GPT-2 pretrain (~$15–35) and any heavier fine-tune.
- **"CornAgents.AI" is your own concept, not a product you must adopt.** Treat CornAgents.AI as your personal agentic-SDLC framework and build it on Claude Agent SDK + MCP + LangGraph/CrewAI (plus a knowledge-graph layer in Week 14), anchored to your Finance Banking / BA domain.

## Key Findings

**The roadmap's spine is public open-source repositories and open-access papers.** Karpathy's from-scratch repo chain (`micrograd` → `makemore` → `nanoGPT` → `llm.c`) covers the full path from backprop to GPT-2 pretraining; open papers (Attention Is All You Need, GPT-2, LoRA, DPO...) are the primary theory sources; *The Annotated Transformer* (Harvard NLP) is the annotated paper implementation. The FareedKhan-dev repo extends beyond pretraining to a full from-scratch alignment suite (Base → SFT → Reward Model → PPO/DPO → GRPO) in pure PyTorch on real datasets (Alpaca, Dolly, Anthropic HH-RLHF, UltraFeedback, GSM8K).

**Karpathy's open-repo ecosystem evolved in a way that directly helps you.** In October 2025 he released **nanochat** (`github.com/karpathy/nanochat`), a ~8,000-line full-stack ChatGPT-clone pipeline (tokenizer → pretrain → midtrain → SFT → GRPO → web UI) — the intended capstone of his still-in-development LLM101n course. As of mid-2026 Karpathy joined Anthropic. Per the nanochat repo, "you can train your own GPT-2 capability LLM (which cost ~$43,000 to train in 2019) for only $48 (~2 hours of 8×H100 GPU node)"; the full `speedrun.sh` takes ~3 hours and "on a spot instance, the total cost can be closer to ~$15" (the 8×H100 node "is costing us about ~$24/hr"). So for you nanochat is primarily a *reading/forking* reference and an optional cloud capstone, not local work.

**On your 8GB RTX 3070 Ti, here is what is real:** QLoRA 4-bit fine-tuning of 7B (≈5GB) and 8B (≈6GB) models fits comfortably per Unsloth's official VRAM table; up to ~11B (7.5GB) is at the edge; 14B (8.5GB) just exceeds 8GB. Practical config: batch size 1–2, sequence length ≤1024, gradient checkpointing on. Pretraining a GPT-2 small (124M) from scratch is technically possible locally but slow — `[Inference]` an 8GB card fits ~batch 1–2 with heavy gradient accumulation, projecting well past 48h for a GPT-2-small token budget — so do the pretraining run in the cloud.

**Cloud is cheap for the one-time pretrain.** Per RunPod's official RTX 4090 page (rechecked May 24, 2026), Community Cloud is from $0.34/hr. Karpathy reproduced GPT-2 124M (12-layer, 10B FineWeb tokens, seq len 1024) on "one 8×A100 80GB SXM node [in] ~90 minutes…on Lambda this node goes for ~$14/hr, so the total cost…is about $20" (`karpathy/llm.c` Discussion #481).

## Details

### How to use Claude as your co-learner (woven through every week)
You have an active Claude subscription and want Claude as a study partner. Concrete, high-leverage uses:
- **Explain the math:** Paste an equation from the original papers (e.g., scaled dot-product attention from "Attention Is All You Need", cross-entropy, KL divergence from the DPO paper) and ask Claude to derive it step by step, then to quiz you. Use it as a Socratic tutor: "Ask me three questions to check I understand causal masking."
- **Review your from-scratch code:** After you implement an attention block or training loop *yourself*, paste it and ask Claude to compare against the canonical open-repo implementations (micrograd, nanoGPT), flag bugs, and explain divergence. Do not let it write the first draft — implement first, review second. (Note: Karpathy himself reported that coding agents struggled on nanochat because the repo is "too far off the data distribution"; expect Claude to be strongest on standard PyTorch patterns and weaker on novel from-scratch tricks.)
- **Debug training runs:** Paste loss curves, OOM stack traces, or `nvidia-smi` output and ask Claude to diagnose (batch size, gradient accumulation, mixed precision, memory fragmentation — e.g. `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`).
- **Generate practice exercises and spaced repetition:** Ask Claude to produce self-test exercises for each week's topics, or flashcards on terms (RoPE, GQA, MoE, MLA).
- **Rubber-duck architecture decisions** in Phase 3: describe your CornAgents.AI agent graph and have Claude critique orchestration, tool boundaries, and failure modes.
- **Use Claude Code as a pair-programmer** for the applied phases (RAG/agents), but in Phase 1 prefer hand-coding to build genuine intuition.
- **Vietnamese ↔ English:** have Claude explain a dense English passage in Vietnamese, then switch back to English technical terms.

### PHASE 1 — Deep Internals (Weeks 1–7)

**Week 1 — Math + PyTorch prerequisites (only what's needed).**
- *Objectives:* Refresh linear algebra (matrix multiply, dot products), calculus (gradients/chain rule), probability (softmax, cross-entropy); get fluent in PyTorch tensors and autograd.
- *Sources:* PyTorch official tutorials — "Learn the Basics" and "Deep Learning with PyTorch: A 60 Minute Blitz" (pytorch.org/tutorials); PyTorch docs on `torch.Tensor` and autograd.
- *Task:* Re-implement a tiny MLP and training loop in PyTorch from scratch; confirm GPU works on the 3070 Ti (`torch.cuda.is_available()`).
- *Hardware:* 3070 Ti (or Mac MPS) — trivial workloads.
- *Deliverable:* A working notebook that trains an MLP on a toy dataset; a one-page "math cheat sheet" you wrote with Claude's help.
- *Time:* ~10–12 hrs.

**Week 2 — Backprop from scratch + the transformer mental model.**
- *Objectives:* Truly understand backpropagation; build a high-level mental model of transformers and attention before coding them.
- *Sources:* Open repos `karpathy/micrograd` and `karpathy/makemore` (read the code + README, reimplement yourself); *The Annotated Transformer* (Harvard NLP, nlp.seas.harvard.edu) for the mental model; the original "Attention Is All You Need" (arXiv 1706.03762).
- *Task:* Read the micrograd code, then build it yourself from scratch; start makemore (bigram → MLP).
- *Hardware:* 3070 Ti / Mac — CPU/GPU both fine.
- *Deliverable:* Your own micrograd repo; written explanation (reviewed by Claude) of why attention is permutation-equivariant and needs positional info.
- *Time:* ~12–15 hrs.

**Week 3 — Tokenization, embeddings, attention from scratch.**
- *Objectives:* Implement BPE/data loading, token + positional embeddings, and self-attention → causal → multi-head, by hand.
- *Sources:* BPE paper "Neural Machine Translation of Rare Words with Subword Units" (arXiv 1508.07909) + open repos `openai/tiktoken`, `karpathy/minbpe`; The Annotated Transformer (Harvard NLP, nlp.seas.harvard.edu); "Attention Is All You Need"; the attention code in `karpathy/nanoGPT` (`model.py`).
- *Task:* Code the full attention stack yourself (self → causal → multi-head); verify shapes against `nanoGPT/model.py`.
- *Hardware:* 3070 Ti.
- *Deliverable:* A `multihead_attention.py` you wrote from scratch with passing shape tests; Claude code-review notes.
- *Time:* ~12–15 hrs (this is the conceptual crux — go slow).

**Week 4 — Assemble and run the GPT model.**
- *Objectives:* Build the full GPT-2 architecture (layer norm, GELU FFN, residual/shortcut connections, transformer blocks) and generate (untrained) text.
- *Sources:* Karpathy nanoGPT (`github.com/karpathy/nanoGPT`) as the primary reference (especially `model.py` and `from_pretrained`); the GPT-2 paper "Language Models are Unsupervised Multitask Learners" (OpenAI's open publication); "Layer Normalization" (arXiv 1607.06450) and "GELU" (arXiv 1606.08415) for the theory.
- *Task:* Instantiate the 124M config, load OpenAI GPT-2 pretrained weights (see how `nanoGPT` does it in `from_pretrained`) to confirm your architecture is correct, and generate text.
- *Hardware:* 3070 Ti (124M inference fits easily in 8GB).
- *Deliverable:* Your GPT model generating coherent text from loaded GPT-2 weights.
- *Time:* ~10–12 hrs.

**Week 5 — Pretraining: the training loop + a real (cloud) GPT-2 run.**
- *Objectives:* Understand the pretraining loop, cross-entropy/perplexity, LR scheduling, checkpointing; then actually pretrain a small model.
- *Sources:* `nanoGPT` (`train.py` — gradient clipping, LR decay, weight decay, mixed precision, gradient accumulation are all in there) and the nanoGPT/llm.c "Reproduce GPT-2 124M" discussion; HF Ultra-Scale Playbook (huggingface.co/spaces/nanotron/ultrascale-playbook) for gradient-accumulation/parallelism concepts.
- *Task:* First, train on a small public-domain text (e.g. a short story from Project Gutenberg) locally to validate your loop on the 3070 Ti. Then do a **real GPT-2-small pretraining run in the cloud** on FineWeb/FineWeb-Edu.
- *Hardware:* **Local 3070 Ti** for loop validation and a tiny model; **cloud** for the real run — rent a single RTX 4090 (RunPod from $0.34/hr Community) for a multi-hour run, or an 8×A100 node (Lambda, ~$14/hr for the node — per llm.c Discussion #481, the ~90-min GPT-2 124M reproduction cost ~$20). On 8GB locally you'd use micro-batch 1–2, seq len 1024, gradient accumulation ~16–64 to hit ~0.5M-token effective batches (Karpathy's GPT-2 setup targets ~524,288 tokens/update).
- *Deliverable:* A pretrained small base-model checkpoint + a short write-up comparing your loss curve to the original GPT-2.
- *Time:* ~12–15 hrs (plus unattended training time).

**Week 6 — Instruction fine-tuning (classification + instruction-following + LoRA).**
- *Objectives:* Fine-tune for classification and instruction-following; apply LoRA and compare it against full fine-tuning.
- *Sources:* The LoRA paper (arXiv 2106.09685); the InstructGPT paper "Training language models to follow instructions" (arXiv 2203.02155); HF fine-tuning + PEFT docs (huggingface.co/docs/peft); the SFT part of `FareedKhan-dev/train-llm-from-scratch`.
- *Task:* Fine-tune a classifier (swap the LM head for a classification head); instruction-fine-tune your model (or a small pretrained one) with an Alpaca-style template; compare full FT vs. LoRA.
- *Hardware:* 3070 Ti is enough (small models, LoRA).
- *Deliverable:* An instruction-following mini-model you can chat with; notes on full FT vs. LoRA.
- *Time:* ~10–12 hrs.

**Week 7 — Intro to alignment: SFT → Reward Model → DPO/PPO → GRPO (FareedKhan + open papers).**
- *Objectives:* Understand the alignment pipeline (SFT → reward model → PPO/DPO → GRPO) conceptually and run at least one stage from scratch. (Split out of the old Week 6 to reduce pressure.)
- *Sources:* FareedKhan-dev/train-llm-from-scratch `src/post_training/` (SFT/RM/PPO/DPO/GRPO in pure PyTorch on Alpaca, Dolly, Anthropic HH-RLHF, UltraFeedback, GSM8K); the DPO paper (arXiv 2305.18290), InstructGPT/RLHF (arXiv 2203.02155), and GRPO in the DeepSeekMath paper (arXiv 2402.03300).
- *Task:* Read through the SFT/RM/DPO structure; run one alignment stage (start with SFT or DPO) scaled-down from the FareedKhan repo.
- *Hardware:* 3070 Ti for the scaled-down stage; cloud if you push to larger bases or full PPO/GRPO (the FareedKhan dev box used 2×H100 with DDP + bf16 — replicate scaled-down or rent).
- *Deliverable:* Logs/checkpoint of one alignment stage; notes distinguishing SFT vs. DPO vs. GRPO.
- *Time:* ~10–12 hrs.

> **If time is tight in Phase 1:** the deepest-value weeks are 2–5 (backprop, attention, GPT assembly, pretraining). You can compress Week 7 alignment to *conceptual* understanding + one DPO run, and defer reasoning-model/GRPO depth to after the roadmap.

### PHASE 2 — Applied: RAG + Fine-Tuning (Weeks 8–11)

**Week 8 — Practical QLoRA fine-tuning on the 3070 Ti with Unsloth.**
- *Objectives:* Move from from-scratch to production tooling; fine-tune a real 7B–8B model with 4-bit QLoRA.
- *Sources:* Unsloth docs (unsloth.ai/docs — Fine-tuning Guide, LoRA Hyperparameters Guide, Requirements table); HF PEFT + TRL docs (SFTTrainer); NVIDIA "How to Fine-Tune LLMs on RTX GPUs With Unsloth."
- *Task:* QLoRA fine-tune Llama 3.1 8B or Qwen on a small instruction dataset (start 500–1,000 examples). Config for 8GB: `load_in_4bit=True`, batch size 1–2, seq len ≤1024, gradient checkpointing, r=16, α=16, target all attention + MLP projections. Export merged model + GGUF.
- *Hardware:* **3070 Ti** (7B QLoRA ≈5GB, 8B ≈6GB — fits). Expect a 1,000–5,000-example run to take several hours to overnight on 8GB. Use **Google Colab free T4 (15GB)** as an easy alternative.
- *Deliverable:* A fine-tuned 7B/8B adapter + eval comparing base vs. fine-tuned on held-out examples.
- *Time:* ~10–12 hrs.

**Week 9 — Mac/MLX fine-tuning + local inference stack.**
- *Objectives:* Use the 24GB MacBook for what it's best at; build your local inference toolkit.
- *Sources:* `mlx-lm` docs and `mlx_lm.lora`; MLX LoRA Studio (GUI) and mlx-tune (SFT/DPO/GRPO on MLX) as options; Ollama, LM Studio (runs both GGUF and MLX), llama.cpp.
- *Task:* Fine-tune a 7B–8B model with LoRA/QLoRA in MLX on the Mac (`mlx_lm.lora --model ... --train --data ... --iters 500`), fuse adapters, run via Ollama/LM Studio. On 24GB unified memory you can also fine-tune up to ~13–14B (QLoRA ~14–18GB working memory).
- *Hardware:* **MacBook Pro 24GB** (unified memory shines here; ~2–4× slower than NVIDIA but fits bigger models). Stand up **Ollama** on both machines for serving.
- *Deliverable:* A working local inference stack (Ollama + LM Studio) + an MLX-fine-tuned model; a short note on when to use Mac vs. 3070 Ti vs. cloud.
- *Time:* ~8–10 hrs.

**Week 10 — Build an end-to-end RAG pipeline.**
- *Objectives:* Chunking, embeddings, vector store, retrieval, generation — over your own (Finance Banking) documents.
- *Sources:* LlamaIndex and LangChain docs (each has an official end-to-end RAG tutorial); NirDiamant/RAG_Techniques and sosanzma/rag-techniques-handbook on GitHub; the original RAG paper (arXiv 2005.11401) for the theory.
- *Task:* Build a baseline RAG over a corpus of your own Finance Banking domain documents: load PDFs → `RecursiveCharacterTextSplitter` (chunk ~800, overlap ~100) → embed → store in **Chroma** (dev) → retrieve top-k → generate with a local Ollama model or Claude. Use **pgvector/Qdrant** if you want a production-grade store.
- *Hardware:* Mac or 3070 Ti for local embeddings/inference; embeddings are light.
- *Deliverable:* A working RAG app answering questions over your Finance Banking docs.
- *Time:* ~12 hrs.

**Week 11 — Advanced RAG + evaluation.**
- *Objectives:* Add hybrid search, reranking, and rigorous evaluation; learn observability.
- *Sources:* RAGAS docs (context precision/recall, faithfulness, answer relevancy); Langfuse (open source) for tracing/LLM-as-judge; the open BGE cross-encoder reranker; GraphRAG (Microsoft, open repo) as optional advanced reading.
- *Task:* Upgrade Week 10's pipeline with hybrid (BM25 + vector) retrieval and a reranker; measure before/after with RAGAS; wire Langfuse/LangSmith tracing.
- *Hardware:* Local; reranker cross-encoder runs fine on the Mac/3070 Ti.
- *Deliverable:* A RAGAS evaluation report showing measurable relevancy improvement from reranking; a traced pipeline.
- *Time:* ~10–12 hrs.

### PHASE 3 — SDLC / CornAgents.AI Application (Weeks 12–15)

**Week 12 — Agentic foundations: the 5 engineering layers, Claude Agent SDK, MCP, and a framework.**
- *Objectives:* Internalize the 5-layer model — Prompt → Context → Harness → Loop → Graph engineering (`docs/5-layers-multi-agent.jpg`); understand agent loops, tools, subagents, and MCP; build your first measured loop (Karpathy autoresearch style); choose your orchestration layer.
- *Sources:* Claude Agent SDK docs (code.claude.com/docs/en/agent-sdk) and Anthropic's "Building agents with the Claude Agent SDK"; Model Context Protocol docs (200+ servers: GitHub, Postgres, Slack, Jira); `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` (Section II autoresearch, Section VI.A–B build path Day 1–2); LangGraph and CrewAI docs (you're already exploring both); AutoGen as alternative.
- *Task:* Build a minimal agent with the Claude Agent SDK that reads a repo, runs a tool, and returns structured output; connect one MCP server (e.g., GitHub or filesystem). Build a **reflective loop**: generate → evaluator with explicit criteria → revise → stopping rule (max rounds + budget) — and understand the four conditions that make Karpathy's loop work (verifiable output, reversible actions, short horizon, bounded environment). Decide your CornAgents.AI stack: Claude Agent SDK for the harness, MCP for tool/data access, LangGraph (stateful graphs) or CrewAI (role-based crews) for multi-agent orchestration.
- *Hardware:* Any; this is API/orchestration work. Use your Claude subscription (note: from June 15, 2026, headless Agent SDK usage on subscription plans draws from a separate weekly pool — heavy automation may need API credits).
- *Deliverable:* A working single agent + MCP connection; a working reflective loop; a one-page CornAgents.AI architecture diagram.
- *Time:* ~12 hrs.

**Week 13 — Map LLMs onto SDLC stages; build the CornAgents.AI agent graph.**
- *Objectives:* Design specialized agents for requirements → design → code → review → test → docs, with human-in-the-loop gates.
- *Sources:* `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` Section IV (Anthropic's five workflow patterns: Prompt Chaining, Routing, Parallelization, Orchestrator–Workers, Evaluator–Optimizer + Dynamic Workflows) and Section VIII (the six-question decision framework); industry references on agentic SDLC (CodeRabbit's agentic-SDLC guide, Sonar's AC/DC framework, GlobalLogic's VelocityAI case study) for patterns and quality gates; the Claude Agent SDK code-review example (reads PRs, flags bugs/security, posts comments).
- *Task:* Implement 2–3 agents in your chosen framework: e.g., a **Requirements Analyst agent** (your BA strength — turns a Finance Banking feature request into structured user stories/acceptance criteria, grounded by your Week 10–11 RAG over internal domain documents), a **Code Review agent**, and a **Test-Generation agent**. Add human approval checkpoints and tool least-privilege scoping.
- *Hardware:* Any; orchestration + API.
- *Deliverable:* A multi-agent workflow that takes a requirement and produces stories + a design note + generated tests, with a human gate; every agent handoff is a schema-backed artifact contract.
- *Time:* ~12–15 hrs.

**Week 14 — Graph Engineering: a knowledge graph as shared memory for multi-agent systems.**
- *Objectives:* Understand why multi-agent systems need a graph infrastructure layer (each agent's memory dies with its context window; the graph is where facts survive across sessions); build the four-stage knowledge-graph pipeline entirely from Claude API calls; distinguish RAG (single-hop retrieval) from knowledge graphs (multi-hop reasoning) — complementary, not competing.
- *Sources:* `docs/Graph-Engineering-Athropic-Playbook.pdf` (extraction → resolution → assembly → querying pipeline, full prompts, gold-set evaluation, scaling guidance); `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` (Loop → Chain → Swarm → DAG → Knowledge Graph; commit DAG vs. knowledge graph); Anthropic's Knowledge Graph Construction Cookbook; NetworkX docs.
- *Task:* Build the KG pipeline over 5–10 of your Finance Banking documents: Extraction (Haiku + structured outputs; the Pydantic schema is the only "training data") → Resolution (Sonnet clusters surface forms using descriptions as context) → Assembly (NetworkX MultiDiGraph; every edge carries provenance) → Querying (serialize the k-hop subgraph; grounded answers that cite edges). Run graph diagnostics; compare grounded vs. ungrounded answers; build a mini gold set and run the evaluation feedback loop (change prompt → rerun scorer → watch F1). Wire the graph into the Week 13 workflow as shared memory + the evaluator's grounding layer.
- *Hardware:* Any; API work (Haiku for volume, Sonnet for reasoning) — cheap with prompt caching.
- *Deliverable:* A `kg_pipeline.py` that runs over your corpus + notes on diagnostics/eval/grounded-vs-ungrounded.
- *Time:* ~10–12 hrs.

**Week 15 — Capstone + evaluation/observability.**
- *Objectives:* Ship one polished, domain-relevant CornAgents.AI workflow end-to-end and evaluate it.
- *Sources:* Langfuse/LangSmith for agent tracing and eval; promptfoo or LLM-as-judge for output quality; your Phase 1–2 understanding to reason about model choice (Claude for the agent brain; a fine-tuned local 7B for a narrow domain-classification sub-task).
- *Task:* Pick the single highest-value SDLC stage for your context — recommended: **spec-to-stories + automated review for a Finance Banking feature** (pick the business area you know best, kept generic). Combine RAG (domain grounding) + the Week 14 knowledge graph (shared memory + multi-hop fact-checking) + agents (workflow) + optionally your fine-tuned model. Declare a complexity budget up front (max calls/tokens/cost/retries). Instrument with tracing; write an eval rubric; measure success rate, human-override rate, and groundedness.
- *Hardware:* Local for fine-tuned sub-models; API for the agent brain.
- *Deliverable:* A demoable CornAgents.AI capstone + an evaluation report + a written retrospective tying back to Phase 1 internals (what you now understand about *why* it works).
- *Time:* ~12–15 hrs.

> **Where time is tight / what to defer:** Phase 1 alignment depth (full PPO/GRPO from scratch, Week 7) is the most deferrable. The advanced-RAG week (11) and capstone (15) can each spill a few days. If you fall behind, protect Weeks 2–5 (the irreplaceable from-scratch core) and Weeks 12–15 (your actual goal), and trim Week 9 (Mac/MLX) to inference-only.

## Recommendations

1. **Start now with Weeks 1–2 prerequisites even though they feel basic** — the payoff is that attention (Week 3) and pretraining (Week 5) will click instead of frustrate. *Threshold to skip ahead:* if you can already implement backprop and a training loop unaided, compress Weeks 1–2 into 3–4 days.
2. **Do the GPT-2 pretraining run in the cloud, not locally.** Budget ~$15–35 one-time on RunPod (single RTX 4090 from $0.34/hr) or Lambda (8×A100, node ~$14/hr; ~$20 for the 90-min llm.c run per Karpathy's Discussion #481). Use the 3070 Ti only to validate your loop on a tiny dataset first. *Trigger to go cloud:* the moment your local run projects beyond ~24h.
3. **For fine-tuning, default to Unsloth QLoRA on the 3070 Ti for 7B–8B; use the Mac/MLX when you need 13B–14B or want silent local runs; rent an A100 only if you need full fine-tuning or fast iteration.** *Threshold:* if a fine-tune needs >24h locally or OOMs at batch size 1, move to a rented 4090/A100.
4. **Anchor every applied artifact to your Finance Banking/BA domain.** Your RAG corpus, your fine-tune dataset, and your capstone should all be Finance Banking domain material (kept generic — no specific product line). This is your differentiation and makes the portfolio credible.
5. **Build CornAgents.AI on Claude Agent SDK + MCP + (LangGraph or CrewAI).** Start with LangGraph if you want explicit, auditable stateful control (better for regulated finance workflows); CrewAI if you prefer fast role-based prototyping. Add human-in-the-loop gates and tool least-privilege from day one.
6. **Use Claude as co-learner deliberately:** implement-first-then-review in Phase 1; pair-program in Phases 2–3. *Benchmark:* if you can't explain a component to Claude in your own words, you haven't learned it yet — that's your signal to slow down.

## Caveats
- **Hardware time estimates for the 3070 Ti are extrapolations**, not measured benchmarks: `[Inference]` they're inferred from the single-GPU figures in the nanoGPT/llm.c documentation (which assume ≥24GB cards). Your 8GB card with batch 1–2 + heavy gradient accumulation will be slower for the same token budget. Re-verify with a short local smoke test before committing to a long run.
- **Cloud prices are live and volatile.** RunPod/Vast.ai are marketplace-driven; verify rates at deployment. Figures cited (RTX 4090 from $0.34/hr Community, ~$0.69/hr Secure; A100 ~$1.49/hr; Lambda 8×A100 node ~$14/hr) were 2026 checks and will drift.
- **Vietnam/region note:** cloud GPU access (RunPod, Lambda, Vast.ai, Colab) works from Vietnam; the main friction is payment method (international card) and latency to US/EU regions — minor for batch training. Choose Asia-Pacific regions where offered for interactive work.
- **Subscription metering changed:** from June 15, 2026, headless Claude Agent SDK usage on Pro/Max plans draws from a separate weekly token pool; budget API credits for heavy agentic automation in Phase 3.
- **"CornAgents.AI" is your own learning concept**, not tied to any commercial product — treat it simply as the name of the personal agentic-SDLC framework you build in Phase 3. (GlobalLogic's "VelocityAI SDLC" is a separate enterprise case study, useful only as a pattern reference.)

## Consolidated Resource List / Tech Stack

**Phase 1 (internals):** Karpathy's open repos — `micrograd`, `makemore`, `minbpe`, `nanoGPT`, `llm.c`, `nanochat`; FareedKhan-dev `train-llm-from-scratch`; *The Annotated Transformer* (Harvard NLP); PyTorch official tutorials; open papers — "Attention Is All You Need", GPT-2, BPE, LoRA, InstructGPT, DPO, DeepSeekMath (GRPO); HF Ultra-Scale Playbook.

**Phase 2 (applied):** Unsloth + HF PEFT/TRL; MLX-LM / mlx-tune / MLX LoRA Studio; Ollama, LM Studio, llama.cpp, vLLM; LangChain, LlamaIndex; Chroma (dev), Qdrant/Weaviate/pgvector (prod); BGE reranker (open source); RAGAS; NirDiamant/RAG_Techniques.

**Phase 3 (SDLC/CornAgents.AI):** Claude Agent SDK + Claude Code; Model Context Protocol; LangGraph, CrewAI, AutoGen; NetworkX + Anthropic's Knowledge Graph Construction Cookbook (Week 14); Langfuse/LangSmith, promptfoo; the two documents in `docs/` (Graph-Engineering Playbook + Karpathy Loop) and the 5-layer diagram `docs/5-layers-multi-agent.jpg`.

**Hardware roles:** 3070 Ti (8GB) → from-scratch coding, small/loop-validation training, 7B–8B QLoRA. MacBook 24GB → local inference of quantized 7B–14B, MLX LoRA up to ~14B, silent fine-tunes. Cloud (RunPod/Lambda/Vast.ai/Colab) → one-time GPT-2 pretrain (~$15–35), full fine-tunes, optional nanochat capstone (~$15–48 on 8×H100).