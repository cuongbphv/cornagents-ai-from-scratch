# Lộ trình 15 tuần làm chủ LLM: Từ nội tại Transformer đến Agentic SDLC & Graph Engineering

## Tóm tắt nhanh (TL;DR)

- **Khả thi trong ~3.5–4 tháng học bán thời gian (10–15 giờ/tuần)**, kiến thức được chia đều 15 tuần để không tuần nào quá tải: Tuần 1–7 tự xây và pretrain một model cỡ GPT-2 from scratch (sách Raschka + Karpathy + Giles Thomas; instruction fine-tuning và alignment giờ là hai tuần riêng); Tuần 8–11 làm phần ứng dụng RAG và fine-tuning bằng QLoRA/MLX; Tuần 12–15 xây một agentic SDLC assistant — gồm một tuần riêng về **Graph Engineering** (knowledge graph làm shared memory cho multi-agent, theo tài liệu trong `docs/`). Ràng buộc khó nhất là chiếc RTX 3070 Ti 8GB — rất tốt cho việc code/train ở quy mô học tập và fine-tuning QLoRA model 7B–8B, nhưng pretraining GPT-2 đầy đủ và mọi tác vụ 13B+ nên đẩy lên cloud GPU giá rẻ.

- **Phân vai phần cứng:** Dùng 3070 Ti cho việc code from scratch / train nhỏ và QLoRA 7B qua Unsloth; dùng MacBook Pro 24GB (MLX) cho local inference các model quantized 7B–14B và fine-tune LoRA nhỏ; thuê RunPod/Lambda cho lần pretrain GPT-2 một lần duy nhất (~$15–35) và các fine-tune nặng hơn.

- **"CornAgents.AI" là khái niệm của riêng bạn, không phải một sản phẩm có sẵn phải mua.** Hãy coi CornAgents.AI là agentic-SDLC framework cá nhân của bạn, xây trên nền Claude Agent SDK + MCP + LangGraph/CrewAI (và một lớp knowledge graph ở Tuần 14), neo vào domain Finance Banking / BA của bạn.

---

## Các phát hiện chính

**Ba nguồn chính bạn đã xác định đều còn cập nhật, được duy trì tốt, và tạo thành một bộ xương sống mạch lạc.** Cuốn *Build a Large Language Model (From Scratch)* của Raschka (Manning, 2024; repo `github.com/rasbt/LLMs-from-scratch`) là giáo trình lõi. Phần sequel *Build a Reasoning Model (From Scratch)* hiện đang ở Early Access và dự kiến phát hành đầy đủ trên Manning vào 28/07/2026 — Raschka thông báo trên LinkedIn rằng "tất cả các chương" đã hoàn tất và sách "Now in Early Access", còn **code repo `github.com/rasbt/reasoning-from-scratch` đã public** và dùng được cho GRPO/RLVR và công việc về inference-scaling.

Loạt blog của Giles Thomas đã đến phần 33 (tháng 4/2026), và quan trọng là anh ấy ghi lại quá trình train một model cỡ GPT-2-small trên chính chiếc RTX 3090 của mình trong "hơn 48 tiếng một chút trên phần cứng của tôi" (đạt loss 3.944 so với 3.500 của GPT-2 gốc) — một tham chiếu gần như hoàn hảo cho các câu hỏi về phần cứng của bạn.

Repo FareedKhan-dev hiện mở rộng vượt ra ngoài pretraining để có một bộ alignment from scratch đầy đủ (Base → SFT → Reward Model → PPO/DPO → GRPO) viết bằng pure PyTorch trên các dataset thật (Alpaca, Dolly, Anthropic HH-RLHF, UltraFeedback, GSM8K).

**Hệ sinh thái của Karpathy phát triển theo hướng giúp ích trực tiếp cho bạn.** Loạt "Neural Networks: Zero to Hero" vẫn là khóa video from scratch miễn phí tốt nhất (micrograd → makemore → nanoGPT). Tháng 10/2025 anh phát hành **nanochat** (`github.com/karpathy/nanochat`), một pipeline full-stack ~8.000 dòng tái tạo một bản clone của ChatGPT (tokenizer → pretrain → midtrain → SFT → GRPO → web UI) — vốn là capstone dự kiến của khóa LLM101n vẫn đang phát triển của anh. Tính đến giữa 2026, Karpathy đã gia nhập Anthropic. Theo nanochat repo, "bạn có thể train một LLM ở năng lực GPT-2 (vốn tốn ~$43.000 để train vào năm 2019) chỉ với $48 (~2 giờ trên một node 8×H100)"; toàn bộ `speedrun.sh` mất ~3 giờ và "trên spot instance, tổng chi phí có thể gần ~$15" (node 8×H100 "tốn của chúng tôi khoảng ~$24/giờ"). Vậy với bạn, nanochat chủ yếu là một tài liệu *để đọc/fork* và là một capstone cloud tùy chọn, không phải việc làm local.

**Trên chiếc RTX 3070 Ti 8GB của bạn, đây là những gì thực sự khả thi:** Fine-tuning QLoRA 4-bit cho model 7B (≈5GB) và 8B (≈6GB) vừa thoải mái theo bảng VRAM chính thức của Unsloth; tới ~11B (7.5GB) là ở mức giới hạn; 14B (8.5GB) thì vừa vặn vượt qua 8GB. Config thực tế: batch size 1–2, sequence length ≤1024, bật gradient checkpointing. Pretraining một GPT-2 small (124M) from scratch về mặt kỹ thuật là làm được ở local nhưng chậm — Giles cần ~48 giờ cho một model tương đương trên chiếc 3090 24GB mà cũng chỉ vừa batch=6; một card 8GB chỉ vừa ~batch 1–2 với gradient accumulation rất nặng, đẩy thời gian vượt xa 48 giờ — nên hãy làm lần pretraining này trên cloud.

**Cloud rất rẻ cho lần pretrain một lần duy nhất.** Theo trang RTX 4090 chính thức của RunPod (kiểm tra lại 24/05/2026), Community Cloud từ $0.34/giờ; bài review RunPod tháng 6/2026 của ToolChase liệt kê Secure Cloud "RTX 4090 từ $0.69/giờ, A100 từ $1.49/giờ, và H100 từ $2.89/giờ." Karpathy tái tạo GPT-2 124M (12-layer, 10B FineWeb tokens, seq len 1024) trên "một node 8×A100 80GB SXM [trong] ~90 phút… trên Lambda node này có giá ~$14/giờ, nên tổng chi phí… khoảng $20" (`karpathy/llm.c` Discussion #481). Giles train model 163M của mình trên 8×A100 40GB (Lambda) "trong chưa tới bốn tiếng… với khoảng US$35, chưa tính validation."

---

## Chi tiết

### Cách dùng Claude làm co-learner (lồng xuyên suốt mọi tuần)

Bạn có subscription Claude đang hoạt động và muốn dùng Claude làm bạn học. Những cách dùng cụ thể, đòn bẩy cao:

- **Giải thích phần toán:** Dán một công thức hay một đoạn từ sách Raschka (ví dụ scaled dot-product attention, cross-entropy, KL divergence trong DPO) và yêu cầu Claude derive từng bước, rồi quiz lại bạn. Dùng như một gia sư kiểu Socratic: "Hỏi tôi ba câu để kiểm tra xem tôi đã hiểu causal masking chưa."

- **Review code from scratch của bạn:** Sau khi *tự bạn* implement một attention block hay một training loop, hãy dán vào và yêu cầu Claude so sánh với bản canonical của Raschka/Karpathy, chỉ ra bug, và giải thích chỗ khác biệt. Đừng để nó viết bản nháp đầu tiên — implement trước, review sau. (Lưu ý: chính Karpathy báo rằng các coding agent gặp khó với nanochat vì repo "quá xa khỏi data distribution"; hãy lường trước Claude mạnh nhất với các pattern PyTorch chuẩn và yếu hơn với các thủ thuật from scratch lạ.)

- **Debug các lần train:** Dán loss curve, OOM stack trace, hoặc output `nvidia-smi` và yêu cầu Claude chẩn đoán (batch size, gradient accumulation, mixed precision, memory fragmentation — ví dụ `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`).

- **Tạo bài tập luyện và spaced repetition:** Yêu cầu Claude tạo bài tập mô phỏng theo "Test Yourself" guide của Raschka, hoặc flashcard về các thuật ngữ (RoPE, GQA, MoE, MLA).

- **Rubber-duck các quyết định kiến trúc** trong Phase 3: mô tả agent graph CornAgents.AI của bạn và để Claude phản biện về orchestration, ranh giới tool, và các failure mode.

- **Dùng Claude Code làm pair-programmer** cho các phase ứng dụng (RAG/agents), nhưng trong Phase 1 hãy ưu tiên tự tay code để xây trực giác thật.

- **Việt ↔ Anh:** trợ lý AI trên liveBook của Raschka trả lời được mọi ngôn ngữ; bạn cũng có thể nhờ Claude giải thích một đoạn tiếng Anh khó bằng tiếng Việt, rồi chuyển ngược lại các thuật ngữ kỹ thuật tiếng Anh.

---

### PHASE 1 — Hiểu sâu nội tại (Tuần 1–7)

**Tuần 1 — Toán nền + PyTorch prerequisites (chỉ những gì cần).**
- *Mục tiêu:* Ôn linear algebra (matrix multiply, dot products), calculus (gradient/chain rule), probability (softmax, cross-entropy); thành thạo PyTorch tensors và autograd.
- *Nguồn:* Loạt visual "Neural Networks" và "Linear Algebra" của 3Blue1Brown (3blue1brown.com); tài liệu miễn phí **"PyTorch in One Hour: From Tensors to Training Neural Networks on Multiple GPUs"** của Raschka (sebastianraschka.com/teaching/pytorch-1h/); Appendix A sách Raschka.
- *Task:* Tự re-implement một MLP nhỏ và một training loop trong PyTorch from scratch; xác nhận GPU chạy trên 3070 Ti (`torch.cuda.is_available()`).
- *Phần cứng:* 3070 Ti (hoặc Mac MPS) — workload không đáng kể.
- *Deliverable:* Một notebook train được MLP trên một toy dataset; một "math cheat sheet" một trang bạn tự viết với sự hỗ trợ của Claude.
- *Thời gian:* ~10–12 giờ.

**Tuần 2 — Backprop from scratch + mental model của transformer.**
- *Mục tiêu:* Hiểu thật sự backpropagation; xây mental model cấp cao về transformer và attention trước khi code chúng.
- *Nguồn:* Karpathy "Neural Networks: Zero to Hero" Lecture 1 (micrograd) và Lecture 2–4 (makemore); 3Blue1Brown "Attention in transformers, step-by-step" (Ch.6) và chương MLP; "The Illustrated Transformer" của Jay Alammar (jalammar.github.io/illustrated-transformer/); paper gốc "Attention Is All You Need".
- *Task:* Theo Karpathy và tự build micrograd; bắt đầu makemore (bigram → MLP).
- *Phần cứng:* 3070 Ti / Mac — CPU/GPU đều ổn.
- *Deliverable:* Repo micrograd của riêng bạn; một bản giải thích (được Claude review) về việc tại sao attention là permutation-equivariant và cần positional info.
- *Thời gian:* ~12–15 giờ.

**Tuần 3 — Tokenization, embeddings, attention from scratch (Raschka ch.2–3).**
- *Mục tiêu:* Tự tay implement BPE/data loading, token + positional embeddings, và self-attention → causal → multi-head.
- *Nguồn:* Sách Raschka ch.2 (Working with text data) và ch.3 (Coding attention mechanisms); đọc song song: Giles Thomas phần 1–14 (đặc biệt phần 8 trainable self-attention, phần 9 causal attention, phần 12 multi-head, phần 13 "attention heads are dumb"); The Annotated Transformer (Harvard NLP, nlp.seas.harvard.edu).
- *Task:* Tự code toàn bộ attention stack của ch.3; kiểm tra shape đối chiếu với repo sách.
- *Phần cứng:* 3070 Ti.
- *Deliverable:* Một file `multihead_attention.py` bạn viết from scratch với shape test pass; ghi chú code-review từ Claude.
- *Thời gian:* ~12–15 giờ (đây là điểm then chốt về khái niệm — hãy đi chậm).

**Tuần 4 — Lắp ráp và chạy GPT model (Raschka ch.4).**
- *Mục tiêu:* Build full kiến trúc GPT-2 (layer norm, GELU FFN, residual/shortcut connections, transformer blocks) và generate text (chưa train).
- *Nguồn:* Raschka ch.4 (Implementing a GPT model from scratch); Giles Thomas phần 15–19 (layer norm, feed-forward, residuals, kết thúc ch.4); nanoGPT của Karpathy (`github.com/karpathy/nanoGPT`) làm tham chiếu chéo.
- *Task:* Khởi tạo config 124M, load pretrained weights GPT-2 của OpenAI (như sách hướng dẫn) để xác nhận kiến trúc đúng, và generate text.
- *Phần cứng:* 3070 Ti (inference 124M vừa thừa trong 8GB).
- *Deliverable:* GPT model của bạn generate được text mạch lạc từ weights GPT-2 đã load.
- *Thời gian:* ~10–12 giờ.

**Tuần 5 — Pretraining: training loop + một lần chạy GPT-2 thật (trên cloud) (Raschka ch.5).**
- *Mục tiêu:* Hiểu pretraining loop, cross-entropy/perplexity, LR scheduling, checkpointing; rồi thực sự pretrain một model nhỏ.
- *Nguồn:* Raschka ch.5 (Pretraining on unlabeled data) + Appendix D (bells & whistles); Giles Thomas phần 20–29 (training, cross-entropy, mini-series "Interventions" về gradient clipping, dropout, LR, weight decay, weight tying, mixed precision — phần 32a–32m); discussion "Reproduce GPT-2 124M" của Karpathy ở nanoGPT/llm.c; HF Ultra-Scale Playbook (huggingface.co/spaces/nanotron/ultrascale-playbook) cho các khái niệm gradient-accumulation/parallelism.
- *Task:* Trước tiên, train trên dataset nhỏ "The Verdict" ở local để validate loop trên 3070 Ti. Sau đó làm **một lần pretraining GPT-2-small thật trên cloud** với FineWeb/FineWeb-Edu.
- *Phần cứng:* **Local 3070 Ti** để validate loop và train một model tí hon; **cloud** cho lần chạy thật — thuê một RTX 4090 đơn (RunPod từ $0.34/giờ Community) cho lần chạy vài giờ, hoặc một node 8×A100 (Lambda, ~$14/giờ cho cả node) để tái tạo trong <4 giờ với ~$35 (chi phí Giles ghi lại). Ở local 8GB bạn sẽ dùng micro-batch 1–2, seq len 1024, gradient accumulation ~16–64 để đạt effective batch ~0.5M tokens (setup GPT-2 của Karpathy nhắm tới ~524.288 tokens/update).
- *Deliverable:* Một base-model checkpoint nhỏ đã pretrain + một bản viết ngắn so sánh loss curve của bạn với GPT-2 gốc, theo kiểu phân tích của Giles.
- *Thời gian:* ~12–15 giờ (cộng thời gian train chạy không giám sát).

**Tuần 6 — Instruction fine-tuning (Raschka ch.6–7 + LoRA).**
- *Mục tiêu:* Fine-tune cho classification (ch.6) và instruction-following (ch.7); áp dụng LoRA và so với full fine-tuning.
- *Nguồn:* Raschka ch.6–7 + Appendix E (LoRA).
- *Task:* Fine-tune classifier theo ch.6; instruction-fine-tune model của bạn (hoặc một model pretrained nhỏ) theo ch.7 với Alpaca-style template; so sánh full FT vs LoRA.
- *Phần cứng:* 3070 Ti là đủ (model nhỏ, LoRA).
- *Deliverable:* Một mini-model biết làm theo instruction để bạn chat thử; ghi chú full FT vs LoRA.
- *Thời gian:* ~10–12 giờ.

**Tuần 7 — Nhập môn alignment: SFT → Reward Model → DPO/PPO → GRPO (FareedKhan + reasoning repo).**
- *Mục tiêu:* Hiểu pipeline alignment (SFT → reward model → PPO/DPO → GRPO) ở mức khái niệm và chạy ít nhất một stage from scratch. (Tách khỏi tuần 6 cũ để lộ trình bớt dồn.)
- *Nguồn:* FareedKhan-dev/train-llm-from-scratch `src/post_training/` (SFT/RM/PPO/DPO/GRPO trong pure PyTorch trên Alpaca, Dolly, Anthropic HH-RLHF, UltraFeedback, GSM8K); repo `reasoning-from-scratch` của Raschka cho GRPO/RLVR và evaluation.
- *Task:* Đọc hiểu cấu trúc SFT/RM/DPO; chạy một stage alignment (bắt đầu bằng SFT hoặc DPO) scaled-down từ repo FareedKhan.
- *Phần cứng:* 3070 Ti cho stage scaled-down; cloud nếu bạn đẩy lên base lớn hơn hoặc full PPO/GRPO (dev box của FareedKhan dùng 2×H100 với DDP + bf16 — hãy tái tạo ở quy mô nhỏ hơn hoặc đi thuê).
- *Deliverable:* Log/checkpoint một stage alignment đã chạy; ghi chú phân biệt SFT vs. DPO vs. GRPO.
- *Thời gian:* ~10–12 giờ.

> **Nếu Phase 1 bị bó thời gian:** các tuần giá trị nhất là 2–5 (backprop, attention, lắp ráp GPT, pretraining). Bạn có thể nén Tuần 7 alignment xuống mức hiểu *khái niệm* + một lần chạy DPO, và để dành phần reasoning-model/GRPO sâu cho sau lộ trình (sách dù sao cũng phát hành đầy đủ vào tháng 7/2026).

---

### PHASE 2 — Ứng dụng: RAG + Fine-Tuning (Tuần 8–11)

**Tuần 8 — Fine-tuning QLoRA thực chiến trên 3070 Ti với Unsloth.**
- *Mục tiêu:* Chuyển từ from-scratch sang tooling production; fine-tune một model 7B–8B thật bằng QLoRA 4-bit.
- *Nguồn:* Unsloth docs (unsloth.ai/docs — Fine-tuning Guide, LoRA Hyperparameters Guide, bảng Requirements); HF PEFT + TRL docs (SFTTrainer); NVIDIA "How to Fine-Tune LLMs on RTX GPUs With Unsloth."
- *Task:* QLoRA fine-tune Llama 3.1 8B hoặc Qwen trên một instruction dataset nhỏ (bắt đầu 500–1.000 ví dụ). Config cho 8GB: `load_in_4bit=True`, batch size 1–2, seq len ≤1024, gradient checkpointing, r=16, α=16, target tất cả attention + MLP projections. Export merged model + GGUF.
- *Phần cứng:* **3070 Ti** (QLoRA 7B ≈5GB, 8B ≈6GB — vừa). Một lần chạy 1.000–5.000 ví dụ sẽ mất từ vài giờ đến qua đêm trên 8GB. Dùng **Google Colab free T4 (15GB)** làm phương án thay thế dễ dàng.
- *Deliverable:* Một adapter 7B/8B đã fine-tune + eval so sánh base vs. fine-tuned trên held-out examples.
- *Thời gian:* ~10–12 giờ.

**Tuần 9 — Fine-tuning trên Mac/MLX + local inference stack.**
- *Mục tiêu:* Dùng MacBook 24GB cho đúng sở trường của nó; xây toolkit inference local.
- *Nguồn:* `mlx-lm` docs và `mlx_lm.lora`; MLX LoRA Studio (GUI) và mlx-tune (SFT/DPO/GRPO trên MLX) làm tùy chọn; Ollama, LM Studio (chạy được cả GGUF lẫn MLX), llama.cpp.
- *Task:* Fine-tune một model 7B–8B bằng LoRA/QLoRA trong MLX trên Mac (`mlx_lm.lora --model ... --train --data ... --iters 500`), fuse adapters, chạy qua Ollama/LM Studio. Với 24GB unified memory bạn cũng có thể fine-tune tới ~13–14B (QLoRA ~14–18GB working memory).
- *Phần cứng:* **MacBook Pro 24GB** (unified memory tỏa sáng ở đây; chậm hơn NVIDIA ~2–4× nhưng chứa được model lớn hơn). Dựng **Ollama** trên cả hai máy để serving.
- *Deliverable:* Một local inference stack hoạt động (Ollama + LM Studio) + một model fine-tune bằng MLX; một ghi chú ngắn về khi nào dùng Mac vs. 3070 Ti vs. cloud.
- *Thời gian:* ~8–10 giờ.

**Tuần 10 — Xây một RAG pipeline end-to-end.**
- *Mục tiêu:* Chunking, embeddings, vector store, retrieval, generation — trên chính tài liệu (Finance Banking) của bạn.
- *Nguồn:* Khóa "Retrieval Augmented Generation" của DeepLearning.AI (audit miễn phí) và/hoặc "RAG from Scratch" của freeCodeCamp; docs của LlamaIndex và LangChain; NirDiamant/RAG_Techniques và sosanzma/rag-techniques-handbook trên GitHub.
- *Task:* Build một RAG baseline trên một corpus tài liệu nghiệp vụ Finance Banking của bạn: load PDF → `RecursiveCharacterTextSplitter` (chunk ~800, overlap ~100) → embed → lưu vào **Chroma** (dev) → retrieve top-k → generate bằng một model Ollama local hoặc Claude. Dùng **pgvector/Qdrant** nếu muốn store cấp production.
- *Phần cứng:* Mac hoặc 3070 Ti cho embeddings/inference local; embeddings nhẹ.
- *Deliverable:* Một RAG app trả lời được câu hỏi trên tài liệu Finance Banking của bạn.
- *Thời gian:* ~12 giờ.

**Tuần 11 — Advanced RAG + evaluation.**
- *Mục tiêu:* Thêm hybrid search, reranking, và evaluation chặt chẽ; học observability.
- *Nguồn:* RAGAS docs (context precision/recall, faithfulness, answer relevancy); LangSmith và Langfuse cho tracing/LLM-as-judge; Cohere Rerank hoặc BGE cross-encoder reranker mã nguồn mở; GraphRAG (Microsoft) làm tài liệu nâng cao tùy chọn.
- *Task:* Nâng cấp pipeline Tuần 10 với hybrid retrieval (BM25 + vector) và một reranker; đo before/after bằng RAGAS; gắn tracing Langfuse/LangSmith.
- *Phần cứng:* Local; reranker cross-encoder chạy ổn trên Mac/3070 Ti.
- *Deliverable:* Một báo cáo evaluation RAGAS cho thấy cải thiện relevancy đo được nhờ reranking; một pipeline có tracing.
- *Thời gian:* ~10–12 giờ.

---

### PHASE 3 — Ứng dụng SDLC / CornAgents.AI (Tuần 12–15)

**Tuần 12 — Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP, và một framework.**
- *Mục tiêu:* Nắm mô hình 5 tầng Prompt → Context → Harness → Loop → Graph engineering (`docs/5-layers-multi-agent.jpg`); hiểu agent loop, tools, subagents, và MCP; build loop có đo lường đầu tiên kiểu Karpathy autoresearch; chọn lớp orchestration của bạn.
- *Nguồn:* Claude Agent SDK docs (code.claude.com/docs/en/agent-sdk) và bài "Building agents with the Claude Agent SDK" của Anthropic; docs Model Context Protocol (200+ server: GitHub, Postgres, Slack, Jira); `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` (mục II autoresearch, mục VI.A–B build path Day 1–2); docs LangGraph và CrewAI (bạn đang khám phá cả hai); AutoGen làm phương án thay thế.
- *Task:* Build một agent tối thiểu bằng Claude Agent SDK đọc một repo, chạy một tool, và trả về structured output; kết nối một MCP server (ví dụ GitHub hoặc filesystem). Build một **reflective loop**: generate → evaluator với tiêu chí tường minh → revise → stopping rule (max rounds + budget) — hiểu 4 điều kiện làm loop chạy được (output verifiable, action reversible, horizon ngắn, environment bounded). Quyết định stack CornAgents.AI: Claude Agent SDK làm harness, MCP cho truy cập tool/data, LangGraph (stateful graphs) hoặc CrewAI (role-based crews) cho orchestration nhiều agent.
- *Phần cứng:* Bất kỳ; đây là việc API/orchestration. Dùng subscription Claude của bạn (lưu ý: từ 15/06/2026, việc dùng headless Agent SDK trên các gói subscription rút từ một pool riêng theo tuần — automation nặng có thể cần API credits).
- *Deliverable:* Một single agent hoạt động + một kết nối MCP; một reflective loop chạy được; một sơ đồ kiến trúc CornAgents.AI một trang.
- *Thời gian:* ~12 giờ.

**Tuần 13 — Map LLM vào các stage của SDLC; xây agent graph CornAgents.AI.**
- *Mục tiêu:* Thiết kế các agent chuyên biệt cho requirements → design → code → review → test → docs, có human-in-the-loop gate.
- *Nguồn:* `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` mục IV (5 workflow patterns của Anthropic: Prompt Chaining, Routing, Parallelization, Orchestrator–Workers, Evaluator–Optimizer + Dynamic Workflows) và mục VIII (decision framework 6 câu hỏi); các tài liệu ngành về agentic SDLC (hướng dẫn agentic-SDLC của CodeRabbit, framework AC/DC của Sonar, case study VelocityAI của GlobalLogic) để lấy pattern và quality gate; ví dụ code-review của Claude Agent SDK (đọc PR, flag bug/security, post comment).
- *Task:* Implement 2–3 agent trong framework bạn chọn: ví dụ một **Requirements Analyst agent** (sở trường BA của bạn — biến một feature request Finance Banking thành user story/acceptance criteria có cấu trúc, được grounding bởi RAG Tuần 10–11 trên tài liệu nghiệp vụ nội bộ), một **Code Review agent**, và một **Test-Generation agent**. Thêm các checkpoint phê duyệt của con người và scoping tool theo nguyên tắc least-privilege.
- *Phần cứng:* Bất kỳ; orchestration + API.
- *Deliverable:* Một workflow nhiều agent nhận một requirement và tạo ra story + một design note + test được generate, có một human gate; mỗi handoff giữa agent là một artifact contract có schema.
- *Thời gian:* ~12–15 giờ.

**Tuần 14 — Graph Engineering: knowledge graph làm shared memory cho multi-agent.**
- *Mục tiêu:* Hiểu vì sao multi-agent cần lớp hạ tầng graph (mỗi agent chết theo context window; graph là nơi facts sống xuyên session); tự xây knowledge graph pipeline 4 bước hoàn toàn bằng Claude API; phân biệt RAG (single-hop retrieval) vs knowledge graph (multi-hop reasoning) — bổ trợ, không thay thế nhau.
- *Nguồn:* `docs/Graph-Engineering-Athropic-Playbook.pdf` (pipeline extraction → resolution → assembly → querying, prompt đầy đủ, evaluation vs gold set, scaling guidance); `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` (Loop → Chain → Swarm → DAG → Knowledge Graph; commit DAG vs knowledge graph); Anthropic Knowledge Graph Construction Cookbook; NetworkX docs.
- *Task:* Build KG pipeline trên 5–10 tài liệu Finance Banking của bạn: Extraction (Haiku + structured outputs, Pydantic schema là "training data" duy nhất) → Resolution (Sonnet cluster surface forms, descriptions làm ngữ cảnh) → Assembly (NetworkX MultiDiGraph, mọi edge mang provenance) → Querying (serialize k-hop subgraph, grounded answer có cite edges). Chạy graph diagnostics; so sánh grounded vs ungrounded; lập mini gold set và chạy evaluation feedback loop (đổi prompt → chạy scorer → xem F1). Cắm graph vào workflow Tuần 13 làm shared memory + grounding layer cho evaluator.
- *Phần cứng:* Bất kỳ; việc API (Haiku cho volume, Sonnet cho reasoning) — chi phí thấp nhờ prompt caching.
- *Deliverable:* `kg_pipeline.py` chạy được trên corpus của bạn + ghi chú diagnostics/eval/grounded-vs-ungrounded.
- *Thời gian:* ~10–12 giờ.

**Tuần 15 — Capstone + evaluation/observability.**
- *Mục tiêu:* Hoàn thiện và ship một workflow CornAgents.AI sát domain, end-to-end và đánh giá nó.
- *Nguồn:* Langfuse/LangSmith cho agent tracing và eval; promptfoo hoặc LLM-as-judge cho chất lượng output; vận dụng hiểu biết Phase 1–2 để lập luận về việc chọn model (Claude làm bộ não agent; một model 7B fine-tuned local cho một sub-task phân loại nghiệp vụ hẹp).
- *Task:* Chọn đúng một stage SDLC giá trị nhất với bối cảnh của bạn — khuyến nghị: **spec-to-stories + automated review cho một feature Finance Banking** (chọn nghiệp vụ bạn thạo nhất, giữ ở mức tổng quát). Kết hợp RAG (grounding domain) + knowledge graph Tuần 14 (shared memory + fact-check multi-hop) + agents (workflow) + tùy chọn model fine-tuned của bạn. Khai báo complexity budget trước khi chạy (max calls/tokens/cost/retries). Gắn tracing; viết một eval rubric; đo success rate, human-override rate, và groundedness.
- *Phần cứng:* Local cho sub-model fine-tuned; API cho bộ não agent.
- *Deliverable:* Một capstone CornAgents.AI demo được + một báo cáo evaluation + một bản retrospective viết lại, gắn ngược về phần internals của Phase 1 (giờ bạn đã hiểu *vì sao* nó hoạt động).
- *Thời gian:* ~12–15 giờ.

> **Chỗ nào thời gian là bó / cái gì có thể để dành:** Độ sâu alignment ở Phase 1 (full PPO/GRPO from scratch, Tuần 7) và sách reasoning của Raschka (phát hành đầy đủ tháng 7/2026) là dễ để dành nhất. Tuần advanced-RAG (11) và capstone (15) mỗi cái có thể tràn thêm vài ngày. Nếu bị tụt lại, hãy bảo vệ Tuần 2–5 (phần lõi from-scratch không thể thay thế) và Tuần 12–15 (mục tiêu thực sự của bạn), và cắt gọn Tuần 9 (Mac/MLX) xuống chỉ còn inference.

---

## Khuyến nghị

1. **Bắt đầu ngay với prerequisite Tuần 1–2 dù chúng có vẻ cơ bản** — phần thưởng là attention (Tuần 3) và pretraining (Tuần 5) sẽ "thông" thay vì gây ức chế. *Ngưỡng để nhảy cóc:* nếu bạn đã tự implement được backprop và một training loop không cần trợ giúp, hãy nén Tuần 1–2 còn 3–4 ngày.

2. **Làm lần pretraining GPT-2 trên cloud, không phải local.** Dự trù ~$15–35 một lần trên RunPod (RTX 4090 đơn từ $0.34/giờ) hoặc Lambda (8×A100, node ~$14/giờ → ~$35 cho lần chạy <4 giờ, theo Giles Thomas; ~$20 cho lần chạy llm.c 90 phút của Karpathy). Chỉ dùng 3070 Ti để validate loop trên một dataset tí hon trước. *Điều kiện kích hoạt đi cloud:* ngay khi lần chạy local của bạn dự phóng vượt ~24 giờ.

3. **Với fine-tuning, mặc định dùng Unsloth QLoRA trên 3070 Ti cho 7B–8B; dùng Mac/MLX khi cần 13B–14B hoặc muốn chạy yên tĩnh ở local; chỉ thuê A100 khi cần full fine-tuning hoặc iterate nhanh.** *Ngưỡng:* nếu một lần fine-tune cần >24 giờ ở local hoặc OOM ở batch size 1, hãy chuyển sang 4090/A100 thuê.

4. **Neo mọi artifact ứng dụng vào domain Finance Banking/BA của bạn.** Corpus RAG, dataset fine-tune, và capstone của bạn đều nên là tài liệu nghiệp vụ Finance Banking (ở mức tổng quát, không gắn sản phẩm cụ thể). Đây là điểm khác biệt của bạn và làm portfolio đáng tin.

5. **Xây CornAgents.AI trên Claude Agent SDK + MCP + (LangGraph hoặc CrewAI).** Bắt đầu với LangGraph nếu bạn muốn stateful control tường minh, audit được (tốt hơn cho workflow tài chính có ràng buộc quy định); CrewAI nếu bạn thích prototype nhanh theo role. Thêm human-in-the-loop gate và tool least-privilege ngay từ ngày đầu.

6. **Dùng Claude làm co-learner một cách có chủ đích:** implement-trước-rồi-review trong Phase 1; pair-program trong Phase 2–3. *Thước đo:* nếu bạn không giải thích được một component cho Claude bằng ngôn ngữ của chính mình, nghĩa là bạn chưa học được — đó là tín hiệu để đi chậm lại.

---

## Cảnh báo (Caveats)

- **Ước lượng thời gian phần cứng cho 3070 Ti là phép ngoại suy**, không phải benchmark đo thực tế: chúng được suy ra từ dải "4–24 giờ single GPU" chung của Karpathy (vốn giả định card ≥24GB) và kết quả RTX 3090 (24GB, batch 6, ~48 giờ) của Giles Thomas. Card 8GB của bạn với batch 1–2 + gradient accumulation nặng sẽ chậm hơn cho cùng token budget. Hãy verify lại bằng một smoke test local ngắn trước khi cam kết một lần chạy dài.

- **Giá cloud là biến động theo thời gian thực.** RunPod/Vast.ai vận hành theo marketplace; hãy verify giá lúc deploy. Các con số trích dẫn (RTX 4090 từ $0.34/giờ Community, ~$0.69/giờ Secure; A100 ~$1.49/giờ; node 8×A100 của Lambda ~$14/giờ) là số kiểm tra năm 2026 và sẽ trôi.

- **Lưu ý vùng Việt Nam:** truy cập cloud GPU (RunPod, Lambda, Vast.ai, Colab) hoạt động được từ Việt Nam; cản trở chính là phương thức thanh toán (thẻ quốc tế) và latency tới region US/EU — không đáng kể cho batch training. Chọn region Asia-Pacific khi có để làm việc tương tác.

- **Sách reasoning của Raschka** đang Early Access nhưng chưa phát hành đầy đủ tới 28/07/2026; hiện tại hãy dựa vào repo public `reasoning-from-scratch`.

- **Cơ chế tính subscription đã đổi:** từ 15/06/2026, việc dùng headless Claude Agent SDK trên gói Pro/Max rút từ một pool token riêng theo tuần; hãy dự trù API credits cho automation agentic nặng ở Phase 3.

- **Tên "CornAgents.AI" là khái niệm học tập của riêng bạn**, không gắn với sản phẩm thương mại nào — cứ coi nó là tên của framework agentic-SDLC cá nhân bạn xây trong Phase 3. ("VelocityAI SDLC" của GlobalLogic là một case study doanh nghiệp riêng biệt, chỉ hữu ích như tham chiếu pattern.)

---

## Danh sách nguồn hợp nhất / Tech Stack

**Phase 1 (internals):** Raschka *Build a LLM (From Scratch)* + repo `rasbt/LLMs-from-scratch`; Raschka `reasoning-from-scratch`; Giles Thomas `gilesthomas.com/llm-from-scratch`; FareedKhan-dev `train-llm-from-scratch`; Karpathy "Neural Networks: Zero to Hero" (`karpathy/nn-zero-to-hero`), nanoGPT, nanochat; loạt DL của 3Blue1Brown; Jay Alammar "Illustrated Transformer"; Annotated Transformer (Harvard NLP); Raschka "PyTorch in One Hour"; "Attention Is All You Need"; HF Ultra-Scale Playbook.

**Phase 2 (applied):** Unsloth + HF PEFT/TRL; MLX-LM / mlx-tune / MLX LoRA Studio; Ollama, LM Studio, llama.cpp, vLLM; LangChain, LlamaIndex; Chroma (dev), Qdrant/Weaviate/pgvector (prod); Cohere Rerank / BGE reranker; RAGAS; DeepLearning.AI RAG course; NirDiamant/RAG_Techniques.

**Phase 3 (SDLC/CornAgents.AI):** Claude Agent SDK + Claude Code; Model Context Protocol; LangGraph, CrewAI, AutoGen; NetworkX + Anthropic Knowledge Graph Construction Cookbook (Tuần 14); Langfuse/LangSmith, promptfoo; hai tài liệu trong `docs/` (Graph-Engineering Playbook + Karpathy Loop) và sơ đồ 5 tầng `docs/5-layers-multi-agent.jpg`.

**Vai trò phần cứng:** 3070 Ti (8GB) → code from scratch, train nhỏ/validate loop, QLoRA 7B–8B. MacBook 24GB → local inference các model quantized 7B–14B, MLX LoRA tới ~14B, fine-tune yên tĩnh. Cloud (RunPod/Lambda/Vast.ai/Colab) → pretrain GPT-2 một lần (~$15–35), full fine-tune, capstone nanochat tùy chọn (~$15–48 trên 8×H100).
