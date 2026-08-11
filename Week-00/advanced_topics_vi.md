# Appendix — Kiến thức nâng cao cần bổ sung (Gap Analysis)

> **Vì sao có file này.** Lộ trình gốc (Tuần 1–15) dựng một model **cỡ GPT-2 (kiến trúc 2019)** rồi chuyển sang ứng dụng. Khi rà soát các nguồn mở của lộ trình — `karpathy/nanoGPT`, `karpathy/nanochat`, `FareedKhan-dev/train-llm-from-scratch` và các paper mở liên quan — có một loạt chủ đề **các model hiện đại (Llama 3, Qwen3, DeepSeek, gpt-oss) dùng nhưng GPT-2 không có**, cộng với các kỹ thuật train/inference/eval mà các nguồn đó đã ghi lại. File này gom chúng lại thành một "appendix" để học sau khi đã nắm GPT-2, và được neo vào đúng tuần liên quan.
>
> Cách dùng: **đừng đọc file này một lượt từ đầu tới cuối.** Mỗi tuần, mở đúng những mục được neo cho tuần đó (xem bảng điều hướng ngay dưới). README của từng tuần cũng có block "🚀 Bổ sung nâng cao" trỏ ngược lại đây — neo hai chiều, để bạn không bao giờ phải tự đoán "phần này học lúc nào". Đây là tài liệu tham khảo, không phải checklist bắt buộc — ưu tiên A và B nếu thời gian hẹp.

**Mục lục**

- [A. Kiến trúc hiện đại: từ GPT-2 (2019) đến Llama/Qwen (2024–2025)](#a-kiến-trúc-hiện-đại)
- [B. Tối ưu inference (sinh text nhanh & rẻ)](#b-tối-ưu-inference)
- [C. Attention ở quy mô lớn](#c-attention-ở-quy-mô-lớn)
- [D. Training dynamics — các can thiệp vào training loop](#d-training-dynamics)
- [E. Tokenizer: train BPE from scratch](#e-tokenizer-train-bpe-from-scratch)
- [F. Scale & Parallelism](#f-scale--parallelism)
- [G. Alignment & Reasoning đầy đủ](#g-alignment--reasoning-đầy-đủ)
- [H. Evaluation đúng cách](#h-evaluation-đúng-cách)
- [I. Agentic & Graph Engineering nâng cao (Phase 3)](#i-agentic--graph-engineering-nâng-cao)

---

## 🧭 Bảng điều hướng: tuần nào đọc mục nào

Đây là **bảng neo chính thức** — mỗi dòng là một tuần, cột giữa là các mục cần mở của tuần đó. Hai tuần đầu cố ý **không có** mục nào: đó là phần nền, thêm chủ đề nâng cao vào lúc đó chỉ gây tải nhận thức vô ích.

| Tuần | Mục cần đọc | Vì sao đọc lúc này |
|---|---|---|
| **1** — Toán + PyTorch | *(không)* | Xây nền; mọi thứ nâng cao đều cần attention trước đã. |
| **2** — Backprop + mental model | *(không)* | Tập trung tự viết autograd; đừng chia trí. |
| **3** — Attention từ đầu | **A1–A6**, **C1–C2**, **E** | Vừa code MHA xong là lúc duy nhất so sánh RoPE/GQA/MLA thấy "thấm". |
| **4** — Lắp ráp GPT | **A7**, **B1**, **B2** | Vừa sinh text xong → hiểu KV cache & sampling ngay trên code của mình. |
| **5** — Pretraining | **D**, **D1–D2**, **F**, **H** (bpb/CORE) | Bạn đang chạy train thật: đây là lúc các "intervention" có nghĩa. |
| **6** — Instruction fine-tuning | **G** (chỉ sơ đồ pipeline) | Để định vị: instruction FT của bạn ≈ bước SFT trong pipeline lớn. |
| **7** — Alignment | **G** (đầy đủ) | Đây *là* tuần alignment. |
| **8** — QLoRA | **B4**, **H** | Bạn bật cờ 4-bit → hiểu NF4/GPTQ/AWQ bên dưới; và cách eval base vs fine-tuned. |
| **9** — Mac/MLX + local inference | **B1**, **B3**, **B4** (GGUF) | Serving thật: KV cache là nút thắt VRAM, GGUF là định dạng bạn load. |
| **10** — RAG pipeline | **B2** | Temperature/top-p quyết định câu trả lời RAG có bịa hay không. |
| **11** — Advanced RAG + RAGAS | **H** (đầy đủ) | Bạn đang đo chất lượng → cần biết cạm bẫy LLM-as-judge trước khi tin số. |
| **12** — Nền tảng agentic | **I1**, **I2** | 5 tầng engineering + ratchet loop là chính nội dung tuần này. |
| **13** — Agent graph SDLC | **I2**, **I3** | Chọn pattern nào, khi nào tách vai, chi phí bao nhiêu. |
| **14** — Graph Engineering | **I3**, **I4** | Scale/storage/monitoring của KG pipeline bạn vừa build. |
| **15** — Capstone | **H**, **I4**, **I5** | Eval + complexity budget + production checklist trước khi "ship". |

> **Quy ước:** mục **A–H** là chiều sâu cho Phase 1–2 (model internals). Mục **I** là chiều sâu cho Phase 3 (agentic/graph), lấy từ hai PDF trong [`../docs/`](../docs/).

---

## A. Kiến trúc hiện đại

> **Học ở tuần:** 3–4 (sau khi đã code attention + GPT-2). Nguồn lõi: paper mở — RoPE (arXiv 2104.09864), GQA (arXiv 2305.13245), MLA trong DeepSeek-V2 (arXiv 2405.04434), Sliding Window trong Mistral 7B (arXiv 2310.06825), MoE/Switch Transformer (arXiv 2101.03961); code kiến trúc hiện đại trong nanochat `nanochat/gpt.py` và HF `transformers` (implementation Llama/Qwen).

GPT-2 dùng: **absolute learned positional embeddings**, **LayerNorm**, **GELU FFN**, **Multi-Head Attention (MHA)**, có bias ở các Linear. Các model hiện đại đổi gần như tất cả những thứ này. Bảng so sánh nhanh:

| Thành phần | GPT-2 (2019) | Llama 3 / Qwen3 (2024–25) |
|---|---|---|
| Positional | Learned absolute (cộng vào embedding) | **RoPE** (xoay Q,K theo vị trí) |
| Normalization | LayerNorm (có mean-centering + bias) | **RMSNorm** (bỏ mean & bias) |
| FFN | Linear → GELU → Linear (4×) | **SwiGLU** (gated, ~⅔·4× ẩn) |
| Attention | MHA | **GQA** (Llama/Qwen), **MLA** (DeepSeek) |
| Bias ở Linear | Có (qkv_bias) | Hầu hết **bỏ bias** |
| Vị trí norm | Pre-LN | Pre-norm (RMSNorm) |
| Sparsity | Dense | tuỳ chọn **MoE** (Qwen3-MoE, gpt-oss, DeepSeek) |

### A1. RoPE — Rotary Positional Embeddings

Thay vì *cộng* một vector vị trí vào embedding (GPT-2), RoPE **xoay** vector query/key theo một góc tỉ lệ với vị trí token. Với cặp chiều \((2i, 2i+1)\) và vị trí \(m\), tần số \(\theta_i = 10000^{-2i/d}\):

$$ \big(x_{2i},\,x_{2i+1}\big) \;\rightarrow\; \big(x_{2i}\cos m\theta_i - x_{2i+1}\sin m\theta_i,\;\; x_{2i}\sin m\theta_i + x_{2i+1}\cos m\theta_i\big) $$

Hệ quả quan trọng: tích vô hướng \(q_m \cdot k_n\) **chỉ phụ thuộc khoảng cách tương đối** \((m-n)\), không phụ thuộc vị trí tuyệt đối → tổng quát hoá tốt hơn ra ngoài độ dài đã train, và là nền của các thủ thuật mở rộng context (NTK/YaRN scaling). Áp dụng *trong* attention, lên Q và K, không lên V.

### A2. RMSNorm (thay LayerNorm)

LayerNorm trừ mean rồi chia std và có \(\gamma,\beta\). RMSNorm bỏ bước trừ mean và bỏ bias, chỉ chuẩn hoá theo *root-mean-square* — rẻ hơn, ổn định tương đương:

$$ \text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_i x_i^2 + \epsilon}}\cdot \gamma $$

### A3. SwiGLU FFN (thay GELU-FFN)

FFN có "cổng" (gated linear unit) dùng activation SiLU/Swish \(\;\text{SiLU}(x)=x\,\sigma(x)\):

$$ \text{SwiGLU}(x) = \big(\text{SiLU}(xW_{gate})\;\odot\;xW_{up}\big)\,W_{down} $$

Vì có 3 ma trận (gate, up, down), chiều ẩn thường lấy \(\approx \tfrac{2}{3}\times 4d\) để giữ số tham số tương đương FFN 4× cũ.

### A4. GQA / MQA — chia sẻ K,V để tiết kiệm KV cache

- **MHA**: mỗi head có Q,K,V riêng (GPT-2).
- **MQA** (Multi-Query): *tất cả* head dùng chung **một** K và **một** V → KV cache nhỏ nhất, nhưng chất lượng có thể giảm.
- **GQA** (Grouped-Query): chia head thành \(g\) nhóm, mỗi nhóm chung K,V → trung dung giữa MHA và MQA. Llama 3, Qwen3 dùng GQA. Lợi ích chính: **giảm kích thước KV cache** (xem B1) → inference dài rẻ hơn.

### A5. MLA — Multi-Head Latent Attention (DeepSeek)

Nén K,V xuống một **vector tiềm ẩn (latent) chiều thấp** rồi mới chiếu ngược ra khi cần. Mục tiêu giống GQA (giảm KV cache) nhưng giữ chất lượng gần MHA. Đây là điểm sáng kiến trúc của DeepSeek-V2/V3 (paper DeepSeek-V2, arXiv 2405.04434).

### A6. Sliding Window Attention

Mỗi token chỉ attend tới \(w\) token gần nhất (cửa sổ trượt) thay vì toàn bộ quá khứ → chi phí tuyến tính theo độ dài. Mistral/Qwen dùng xen kẽ lớp full-attention và sliding-window để cân bằng tầm xa và chi phí.

### A7. MoE — Mixture of Experts

Thay một FFN dày bằng **nhiều FFN "expert"**; một **router** chọn top-\(k\) expert cho mỗi token (ví dụ 8 trên 256). Tổng tham số rất lớn nhưng **tham số *active* mỗi token nhỏ** → "dung lượng" lớn với chi phí tính toán thấp. Cần lo **load balancing** (tránh dồn token vào ít expert). Qwen3-MoE, DeepSeek, gpt-oss đều theo hướng này (nền lý thuyết: Switch Transformer, arXiv 2101.03961; Mixtral, arXiv 2401.04088).

---

## B. Tối ưu inference

> **Học ở tuần:** 4 (sau khi sinh text: B1–B2), 8 (quantization: B4), 9 (local inference stack: B3–B4/GGUF), 10 (sampling ảnh hưởng câu trả lời RAG: B2). Nguồn: nanochat `engine.py` (KV cache), `scripts/chat_*`; docs llama.cpp/GGUF cho quantization.

### B1. KV Cache — bắt buộc phải hiểu

Khi sinh text tự hồi quy, mỗi bước chỉ thêm **1 token mới**, nhưng nếu tính lại attention cho toàn bộ chuỗi mỗi bước thì lãng phí \(O(n^2)\). **KV cache** lưu lại K,V của các token đã sinh; bước sau chỉ tính K,V cho token mới và attend vào cache → mỗi bước thành \(O(n)\). Đây là lý do GQA/MQA/MLA quan trọng: **bộ nhớ KV cache** \(\approx 2 \cdot n_{layers}\cdot n_{kv\_heads}\cdot d_{head}\cdot \text{seq} \cdot \text{dtype}\) — và là nút thắt VRAM khi context dài (rất liên quan tới giới hạn 8GB của 3070 Ti).

### B2. Sampling — điều khiển đầu ra

Từ logits → phân phối, các chiến lược:

- **Greedy / argmax**: luôn chọn token xác suất cao nhất → lặp, nhàm.
- **Temperature** \(T\): chia logits cho \(T\) trước softmax. \(T<1\) sắc nét hơn (an toàn), \(T>1\) đa dạng hơn (sáng tạo/rủi ro).
- **Top-k**: chỉ lấy mẫu trong \(k\) token cao nhất.
- **Top-p (nucleus)**: lấy tập token nhỏ nhất có tổng xác suất \(\ge p\).
- Thực tế thường kết hợp temperature + top-p. (Tuần 5 đã dùng temperature & top-k; phần này mở rộng thêm top-p.)

### B3. Speculative decoding (khái niệm)

Dùng một model "nháp" nhỏ để đề xuất nhiều token, model lớn **verify song song** → tăng tốc mà không đổi phân phối đầu ra. Hữu ích khi serving; chỉ cần nắm ý tưởng ở mức này.

### B4. Quantization internals (sâu hơn Tuần 8)

Tuần 8 dùng QLoRA/NF4 ở mức "bật cờ". Hiểu thêm các họ:

- **NF4** (QLoRA): kiểu 4-bit "normal float", phân bố tối ưu cho trọng số ~Gaussian; chỉ quantize *base*, train adapter LoRA ở bf16.
- **GPTQ**: post-training quant theo từng lớp, tối thiểu hoá lỗi tái dựng bằng thông tin Hessian.
- **AWQ**: bảo vệ ~1% kênh trọng số "salient" theo activation → ít mất chất lượng.
- **GGUF**: *định dạng file* của llama.cpp (k-quants Q4_K_M, Q5_K_M, Q8_0…), không phải thuật toán — đây là thứ Ollama/LM Studio load.

Quy tắc ngón tay: 4-bit ≈ ½ chất lượng/ bộ nhớ điểm ngọt cho local; 8-bit gần như không mất; perplexity tăng dần khi bit giảm.

---

## C. Attention ở quy mô lớn

> **Học ở tuần:** 3 (ngay sau khi tự code multi-head attention). Nguồn: paper FlashAttention (arXiv 2205.14135); PyTorch docs `F.scaled_dot_product_attention`.

### C1. Vì sao self-attention là \(O(n^2)\)

Ma trận score có shape \((\text{seq}\times\text{seq})\) → bộ nhớ và tính toán tăng **bình phương** theo độ dài context. Đây là rào cản chính cho context dài, và là động lực cho sliding-window (A6), MLA (A5), và FlashAttention.

### C2. FlashAttention (khái niệm)

Không *vật chất hoá* ma trận \(n\times n\) trong HBM. Nó **tiling** (chia khối) Q,K,V, tính softmax theo kiểu *online/streaming* trong SRAM, cộng dồn kết quả → cùng đầu ra toán học nhưng **giảm I/O bộ nhớ** mạnh, nhanh hơn và tiết kiệm VRAM. PyTorch gói sẵn qua `F.scaled_dot_product_attention` (chọn backend flash khi đủ điều kiện). Nắm: *cùng kết quả, khác cách dùng bộ nhớ*.

---

## D. Training dynamics

> **Học ở tuần:** 5 (pretraining). Nguồn: `nanoGPT/train.py` (mọi can thiệp dưới đây đều có trong code); nanochat `optim.py` (Muon), `common.py` (COMPUTE_DTYPE).

Các can thiệp phổ biến vào training loop và vai trò của chúng (đối chiếu trực tiếp trong `nanoGPT/train.py`):

- **Gradient clipping**: cắt norm gradient (vd. max_norm=1.0) → giảm loss-spike.
- **Dropout trong pretraining**: `[Suy luận từ cấu hình các repo mở]` với pretraining 1-epoch trên data lớn, các repo hiện đại đặt dropout = 0 (dropout hợp cho fine-tune data nhỏ, dễ overfit).
- **Attention bias**: nhiều kiến trúc hiện đại bỏ bias ở Q/K/V (xem config `bias=False` trong nanoGPT).
- **Learning rate**: warmup tuyến tính → cosine decay; LR là siêu tham số nhạy nhất.
- **Weight decay**: regularize, thường ~0.1; không áp lên bias/norm.
- **Weight tying**: chia sẻ trọng số embedding ↔ output head; tiết kiệm tham số.
- **float32 vs AMP**: mixed precision (bf16) nhanh + đỡ VRAM, gần như không hại loss cuối.
- **Noise/variance**: nhiều "cải thiện" nằm trong **nhiễu** giữa các lần chạy — phải chạy nhiều seed mới biết tín hiệu thật. *Bài học phương pháp luận quan trọng nhất.*
- **Gradient accumulation**: cộng dồn gradient qua nhiều micro-batch để đạt **effective batch** lớn trên VRAM nhỏ — chìa khoá cho 8GB.

### D1. Optimizers: AdamW vs Muon

AdamW là mặc định (momentum + adaptive LR + decoupled weight decay). **Muon** (nanochat dùng cho ma trận 2D) **orthogonalize** bản cập nhật bằng vài bước Newton-Schulz → hội tụ nhanh hơn ở pretraining; embedding/head vẫn dùng AdamW. Đây là một trong các yếu tố giúp nanochat "speedrun" GPT-2 nhanh.

### D2. Mixed precision & dtype

bf16 (Ampere+), fp16 (cần `GradScaler` chống underflow), fp8 (Hopper, nanochat leaderboard #2 dùng fp8). nanochat quản lý precision **tường minh** qua một biến `COMPUTE_DTYPE` thay vì autocast — trọng số fp32 cho optimizer, cast xuống compute-dtype khi forward.

---

## E. Tokenizer: train BPE from scratch

> **Học ở tuần:** 3 (mở rộng phần tokenization). Nguồn: nanochat `tok_train.py` + `tok_eval.py`; repo mở `karpathy/minbpe` (BPE from scratch).

Lộ trình gốc *dùng* tiktoken (đã train sẵn). Bước sâu hơn là **tự train** một BPE tokenizer kiểu GPT-4:

1. Bắt đầu từ byte-level (256 token cơ sở) → không bao giờ OOV.
2. Lặp: đếm cặp byte/token kề nhau xuất hiện nhiều nhất → **merge** thành token mới → lặp tới `vocab_size`.
3. Dùng **regex split pattern** (kiểu GPT-4) để tách số/chữ/khoảng trắng hợp lý trước khi merge.
4. **Đánh giá**: *compression rate* = bytes/token (cao = nén tốt). nanochat `tok_eval.py` đo chỉ số này.

Hiểu tokenizer giải thích nhiều "bug" nổi tiếng: đếm chữ "r" trong "strawberry", toán trên số nhiều chữ số, khoảng trắng/căn lề.

---

## F. Scale & Parallelism

> **Học ở tuần:** 5 (cloud run). Nguồn: HF *Ultra-Scale Playbook*; PyTorch DDP docs; nanochat `torchrun`.

- **DDP (Data Parallel)**: nhân bản model trên N GPU, mỗi GPU một phần batch, **all-reduce** gradient. Đây là mức song song đầu tiên cần biết (nanoGPT/llm.c đều train multi-GPU bằng DDP/torchrun).
- **Tensor Parallel (TP)**: chia *trong* một lớp (ma trận) qua nhiều GPU — cho model không vừa 1 GPU.
- **Pipeline Parallel (PP)**: chia *theo lớp* thành các stage.
- **ZeRO / FSDP**: shard optimizer state / gradient / param qua GPU để giảm bộ nhớ (DeepSpeed ZeRO-1/2/3, PyTorch FSDP).
- **MFU** (Model FLOPs Utilization): % FLOP lý thuyết thực sự dùng được — thước đo hiệu quả train (nanochat theo dõi `train/mfu`).

Với bạn (1 GPU 8GB local): chủ yếu dùng **gradient accumulation** (D) ở local; **DDP** chỉ khi thuê multi-GPU cloud cho lần pretrain.

---

## G. Alignment & Reasoning đầy đủ

> **Học ở tuần:** 6 (chỉ đọc sơ đồ pipeline để định vị instruction FT ≈ SFT) và **7** (đọc đầy đủ — đây là tuần alignment). Nguồn: **FareedKhan-dev `src/post_training/`** (SFT → Reward Model → PPO → DPO → GRPO, pure PyTorch trên Alpaca/Dolly/HH-RLHF/UltraFeedback/GSM8K); paper DPO (arXiv 2305.18290) và DeepSeekMath/GRPO (arXiv 2402.03300); nanochat `chat_sft.py`, `chat_rl.py`.

Pipeline đầy đủ "base → aligned reasoning model":

```
Pretrain  →  Midtrain  →  SFT  →  Reward Model  →  PPO / DPO  →  GRPO / RLVR
(dự đoán   (dạy format   (bắt    (học chấm điểm   (RL tối ưu   (RL cho reasoning,
 token)     hội thoại,    chước   ưu tiên giữa     reward)      reward kiểm chứng
            tool, special  phản    cặp output)                   được — toán/code)
            tokens)        hồi tốt)
```

- **Midtrain** (nanochat): bước *giữa* pretrain và SFT — dạy model định dạng hội thoại, special tokens, dùng tool, một ít kiến thức. Khái niệm này **không có** trong pipeline GPT-2 kinh điển.
- **Reward Model (RM)**: train một model chấm điểm; FareedKhan implement from scratch.
- **PPO**: RL kinh điển của RLHF, cần RM + critic + KL với policy gốc.
- **DPO**: bỏ RM/PPO, tối ưu trực tiếp từ cặp (chosen, rejected) — đơn giản & ổn định hơn (đã có công thức ở Tuần 7).
- **GRPO/RLVR**: *Group Relative Policy Optimization* — bỏ critic, chuẩn hoá reward theo **nhóm sample**; **RLVR** = reward *kiểm chứng được* (đáp án toán đúng/sai, test code pass) → nền của reasoning models (o1/R1-style).
- **Tool-use RL** (nanochat): model học gọi Python để đếm/tính (vd. "đếm r trong strawberry"), reward khi ra kết quả đúng.

---

## H. Evaluation đúng cách

> **Học ở tuần:** 5 (bpb/CORE khi so với GPT-2), 8 (eval base vs fine-tuned), 11 (RAGAS + cạm bẫy LLM-as-judge), 15 (eval capstone). Nguồn: nanochat `core_eval.py` (CORE/DCLM), `loss_eval.py` (bits-per-byte); tasks `mmlu/arc/gsm8k/humaneval`; khảo sát LLM-as-judge (arXiv 2306.05685, "Judging LLM-as-a-Judge").

- **Cross-entropy loss / Perplexity** \(\text{PPL}=e^{L}\): đo trên ngôn ngữ; nhưng **phụ thuộc vocab/tokenizer** nên khó so chéo model.
- **Bits-per-byte (bpb)**: chuẩn hoá loss về *byte* → **so sánh được** giữa các tokenizer/model khác nhau. nanochat dùng bpb thay loss thô. *Nên biết khi so model của bạn với GPT-2.*
- **CORE score (DCLM)**: tổ hợp nhiều benchmark; nanochat đo "time-to-GPT-2" theo CORE (GPT-2 = 0.2565).
- **Benchmark chuẩn**: MMLU (kiến thức rộng, trắc nghiệm), ARC (khoa học), GSM8K (toán tiểu học), HumanEval (code). nanochat có sẵn các task này.
- **LLM-as-judge**: dùng một LLM mạnh chấm output — tiện nhưng **nhiều bẫy** đã được ghi nhận trong nghiên cứu (thiên vị độ dài, vị trí, tự khen — arXiv 2306.05685). *Loss thấp hơn không tự động nghĩa là hữu ích hơn* → đừng tin một chỉ số duy nhất.

---

## I. Agentic & Graph Engineering nâng cao

> **Học ở tuần:** 12 (I1–I2), 13 (I2–I3), 14 (I3–I4), 15 (I4–I5). Nguồn: [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf), [`../docs/Graph-Engineering-Athropic-Playbook.pdf`](../docs/Graph-Engineering-Athropic-Playbook.pdf), [`../docs/5-layers-multi-agent.jpg`](../docs/5-layers-multi-agent.jpg); Anthropic *Building Effective AI Agents* + Knowledge Graph Construction Cookbook.

Phase 1–2 hỏi "model hoạt động thế nào". Phase 3 hỏi **"đặt bộ nhớ và đánh giá ở đâu"** — và đó mới là bottleneck thật. Câu chốt của cả mục này: *model là commodity, hệ thống quanh nó mới là chỗ engineering.*

### I1. Năm tầng engineering — mỗi tầng bọc tầng trước

| Tầng | Là gì | Unit of work |
|---|---|---|
| 1. Prompt | the message (role, instructions, examples, format) | một input |
| 2. Context | the memory (curate cái gì ở trong window) | cái ở trong window |
| 3. Harness | the machine (gather → act → verify, có retry) | một pass |
| 4. Loop | the system (run → check budget/max-iter/no-progress → decide) | một run |
| 5. Graph | the organization (nhiều agent + shared memory) | cả tổ chức |

Chẩn đoán khi hệ thống hỏng: hỏi *tầng nào đang thiếu?* Output sai định dạng → tầng 1. Model không biết thứ nó cần biết → tầng 2. Không ai kiểm tra kết quả → tầng 3. Chạy mãi không dừng → tầng 4. Các agent lặp lại việc của nhau → tầng 5.

### I2. Từ Loop đến Swarm: mỗi kiến trúc externalize một bottleneck khác

| Kiến trúc | Externalize cái gì |
|---|---|
| **Loop** | iteration + evaluation |
| **Chain** | thứ tự task |
| **Swarm** | parallel search + chuyên môn hoá vai |
| **DAG** | lineage thí nghiệm (đã thử gì, nhánh từ đâu) |
| **Knowledge graph** | shared facts, provenance, memory xuyên session |

**Ratchet loop** (Karpathy *autoresearch*): `inspect → propose → apply → evaluate → keep hoặc revert`. Chỉ giữ thay đổi khi metric tốt lên; crash thì revert. 630 dòng code chạy ~700 thí nghiệm trong 2 ngày, giữ lại ~20 tối ưu.

Bốn điều kiện làm loop đó chạy được — **thiếu một là loop vô nghĩa**:

1. **Output verifiable** — có metric đo được (không thì agent tối ưu thứ sai).
2. **Action reversible** — revert được (không thì một lỗi phá cả state).
3. **Horizon ngắn** — run ~5 phút → feedback dày.
4. **Environment bounded** — repo/không gian hành động hữu hạn.

**`program.md` = "programming the program"**: Software 1.0 viết lệnh tường minh, 2.0 nắn hành vi bằng data, **3.0 dùng ngôn ngữ tự nhiên làm interface lập trình được**. `program.md` khai báo: file nào được sửa / file nào bảo vệ, metric + hướng, budget, quy tắc commit-revert, chính sách escalate cho người.

**Commit DAG ≠ Knowledge graph** — đừng gộp: DAG trả lời *"cái gì đã thay đổi, thí nghiệm nào là cha"* (work lineage); KG trả lời *"entity nào tồn tại, liên quan thế nào, nguồn nào chống lưng"* (domain knowledge).

### I3. Năm workflow patterns + chi phí thật của multi-agent

- **Prompt Chaining** — các bước cố định nối tiếp, có gate giữa các bước.
- **Routing** — phân loại input → prompt/model chuyên biệt.
- **Parallelization** — call độc lập chạy song song (sectioning hoặc voting).
- **Orchestrator–Workers** — model trung tâm phân rã động, giao việc, tổng hợp.
- **Evaluator–Optimizer** — một bên sinh, một bên chấm theo tiêu chí, lặp.

Lời khuyên gốc của Anthropic: **"simple, composable patterns rather than complex frameworks"** — chọn pattern theo bài toán, đừng bê nguyên framework nặng.

Con số cần nhớ trước khi tách vai: multi-agent thắng single agent ~**90%** ở task cần nhiều hướng độc lập, nhưng tốn **10–15× token**. Nên: chỉ tách vai khi chuyên môn hoá **thêm tín hiệu**, và luôn định nghĩa **reducer** trước khi fan-out.

**Dynamic Workflows** (2026): thay vì bạn viết script fan-out tĩnh, model **sinh chương trình orchestration** rồi spawn tới ~1.000 sub-agent với context tươi. Ranh giới abstraction dịch lên, nhưng **trách nhiệm không mất**: bạn vẫn phải định nghĩa objective, file trong scope, output contract, permissions, verification policy, concurrency + token budget, rollback rule.

**Khi nào *đừng* fan-out:** task cần một mạch tư duy liền (thiết kế kiến trúc, viết narrative, refactor gắn kết chặt) sẽ **tệ hơn** khi chia thành đơn vị cô lập. Fan-out song song cũng tạo **lỗi tương quan** — verification chỉ giúp nếu reviewer có prompt/bằng chứng/vai *khác*.

### I4. Knowledge graph ở quy mô production

Phần Tuần 14 build là notebook-scale (6–10 tài liệu, in-memory). Lên hàng nghìn tài liệu cần thêm:

- **Blocking trước khi resolve**: nhét 10.000 entity vào một prompt thì thất bại. Gom candidate bằng tín hiệu **rẻ** (trùng token tên, overlap, embedding) thành block 50–100, chỉ để model phân xử *trong* block. Đây là pattern chung: **model cho phần cần phán xét, logic tất định cho mọi thứ còn lại.**
- **Incremental update**: tài liệu mới → resolve **với canonical set đã có** (không phải với nhau), chỉ thêm edge mới; re-summarize một entity **chỉ khi** tập tài liệu nguồn của nó đổi thật. Graph **tích luỹ**, không rebuild.
- **Storage**: NetworkX ổn tới vài trăm nghìn edge. Quá đó → property graph (Neo4j/Neptune) hoặc **3 bảng Postgres** (`entities`, `relations`, `aliases`) + recursive CTE. Code extraction/resolution **không đổi** — chỉ đổi lớp persistence.
- **Chunking tài liệu dài**: cắt theo **ranh giới mục/đoạn** (semantic), không theo số token, để entity và quan hệ của nó nằm cùng chunk; overlap một đoạn; dedupe entity giữa các chunk trước khi resolve.
- **Bốn tín hiệu monitoring**: *extraction rate* (đột ngột giảm = corpus lệch domain), *resolution compression ratio* (~1.0 = tên nhất quán; >2.0 = resolution đang có giá trị), *graph connectivity* (số component tăng = mất link cross-document), *query latency*.
- **Ba kỷ luật vận hành**: (1) **đọc tay 1 node mỗi ngày** — kiểm profile với tài liệu nguồn, verify provenance; khi bạn không giải thích được vì sao một edge tồn tại, hiểu biết của bạn đã tụt sau graph; (2) **cap volume mỗi run** (chống một batch trùng lặp nổ chi phí); (3) **version hoá schema** cùng graph.

**Hai failure mode chết người**: *silent entity loss* (tên không khớp cluster nào thì biến mất → phải fallback cluster 1 phần tử) và *false merge* (gộp sai hai người → mọi traversal downstream nhiễm bẩn → resolution phải giữ alias, evidence, confidence, và **đảo được**).

### I5. Kỷ luật production: budget, gaming, và thước đo cuối

**Complexity budget** — khai báo *trước* mỗi run: max model calls, max sub-agents, max concurrent workers, max tool calls, max wall-clock, max tokens, max chi phí, max retries, và **bằng chứng tối thiểu để được finalize**. Hết budget → trả artifact tốt nhất hiện có + issue chưa xử lý + **lý do dừng**. Tuyệt đối không giấu partial failure sau một câu trả lời trôi chảy.

**Metric bị game**: ratchet chỉ cải thiện thứ nó **thấy được**. Có thể giảm val loss mà tăng chi phí inference, giảm robustness, hoặc overfit chính eval set. Luôn giữ ràng buộc phụ (memory, throughput, stability, generalization).

**Sáu câu hỏi chọn kiến trúc**: (1) success có verify được? — không thì đừng bắt đầu bằng autonomy; (2) các bước có ổn định? — có thì chain; (3) subtask độc lập? — có thì parallelize; (4) cần giữ nhánh thay thế? — có thì DAG; (5) facts phải sống qua run? — có thì persist graph, đừng dựa vào transcript; (6) chịu được chi phí/latency? — đặt budget trước khi thêm worker.

**Thước đo cuối cùng của một hệ thống đáng tin:**

> *Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record.*

Khi câu đó **đúng** — loop, swarm, DAG, KG là các cơ chế engineering compose được. Khi nó **sai** — thêm agent chỉ làm tăng độ mờ đục. Đây là câu bạn tự kiểm ở Tuần 15.

---

## Tóm tắt ưu tiên (nếu thời gian hẹp)

1. **Bắt buộc**: KV cache (B1), RoPE (A1), RMSNorm/SwiGLU (A2–A3), GQA (A4), gradient accumulation (D), bits-per-byte (H) — đây là khoảng cách lớn nhất giữa "GPT-2 2019" và "LLM bạn dùng hằng ngày". Với Phase 3: 5 tầng engineering (I1) + 4 điều kiện của ratchet loop (I2) + complexity budget (I5).
2. **Nên có**: MoE (A7), quantization internals (B4), Muon (D1), full alignment pipeline (G), BPE training (E), 5 workflow patterns (I3), blocking + incremental update cho KG (I4).
3. **Để dành**: MLA (A5), sliding window (A6), speculative decoding (B3), TP/PP/FSDP (F), Dynamic Workflows ở quy mô 1.000 sub-agent (I3) — đào khi cần.

> **Neo nguồn nhanh:** paper mở (RoPE/GQA/MLA/MoE/FlashAttention — kiến trúc hiện đại) · `nanoGPT/train.py` (training dynamics) + HF Ultra-Scale Playbook (parallelism) · FareedKhan `src/post_training` (alignment) · nanochat `gpt.py`/`engine.py`/`optim.py`/`tok_train.py` (full-stack hiện đại) · [`../docs/`](../docs/) 2 PDF Graph-Engineering + sơ đồ 5 tầng (agentic/graph).
