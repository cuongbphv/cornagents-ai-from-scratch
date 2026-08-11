# Appendix — Kiến thức nâng cao cần bổ sung (Gap Analysis)

> **Vì sao có file này.** Lộ trình gốc (Tuần 1–15) dựng một model **cỡ GPT-2 (kiến trúc 2019)** rồi chuyển sang ứng dụng. Khi rà soát lại 4 nguồn — Raschka `rasbt/LLMs-from-scratch` (kèm thư mục *Bonus Material*), `FareedKhan-dev/train-llm-from-scratch`, blog `gilesthomas.com/llm-from-scratch` (đã tới part 33), và `karpathy/nanochat` — có một loạt chủ đề **các model hiện đại (Llama 3, Qwen3, DeepSeek, gpt-oss) dùng nhưng GPT-2 không có**, cộng với các kỹ thuật train/inference/eval mà 3 nguồn kia đã ghi lại. File này gom chúng lại thành một "appendix" để học sau khi đã nắm GPT-2, và được neo vào đúng tuần liên quan.
>
> Cách dùng: đọc song song với tuần tương ứng (cột *Học ở tuần*). Mỗi mục có công thức/ý chính + nguồn để đào sâu. Đây là tài liệu tham khảo, không phải checklist bắt buộc — ưu tiên A và B nếu thời gian hẹp.

**Mục lục**

- [A. Kiến trúc hiện đại: từ GPT-2 (2019) đến Llama/Qwen (2024–2025)](#a-kiến-trúc-hiện-đại)
- [B. Tối ưu inference (sinh text nhanh & rẻ)](#b-tối-ưu-inference)
- [C. Attention ở quy mô lớn](#c-attention-ở-quy-mô-lớn)
- [D. Training dynamics — loạt "Interventions" của Giles](#d-training-dynamics)
- [E. Tokenizer: train BPE from scratch](#e-tokenizer-train-bpe-from-scratch)
- [F. Scale & Parallelism](#f-scale--parallelism)
- [G. Alignment & Reasoning đầy đủ](#g-alignment--reasoning-đầy-đủ)
- [H. Evaluation đúng cách](#h-evaluation-đúng-cách)

---

## A. Kiến trúc hiện đại

> **Học ở tuần:** 3–4 (sau khi đã code attention + GPT-2). Nguồn lõi: rasbt *Bonus Material* (`KV Cache`, `Grouped-Query Attention`, `Multi-Head Latent Attention`, `Sliding Window Attention`, `Mixture-of-Experts`, walkthrough **Llama 3** & **Qwen3 dense/MoE**, **gpt-oss**); nanochat `nanochat/gpt.py`.

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

Nén K,V xuống một **vector tiềm ẩn (latent) chiều thấp** rồi mới chiếu ngược ra khi cần. Mục tiêu giống GQA (giảm KV cache) nhưng giữ chất lượng gần MHA. Đây là điểm sáng kiến trúc của DeepSeek-V2/V3; rasbt có chương từ-đầu cho cả MLA.

### A6. Sliding Window Attention

Mỗi token chỉ attend tới \(w\) token gần nhất (cửa sổ trượt) thay vì toàn bộ quá khứ → chi phí tuyến tính theo độ dài. Mistral/Qwen dùng xen kẽ lớp full-attention và sliding-window để cân bằng tầm xa và chi phí.

### A7. MoE — Mixture of Experts

Thay một FFN dày bằng **nhiều FFN "expert"**; một **router** chọn top-\(k\) expert cho mỗi token (ví dụ 8 trên 256). Tổng tham số rất lớn nhưng **tham số *active* mỗi token nhỏ** → "dung lượng" lớn với chi phí tính toán thấp. Cần lo **load balancing** (tránh dồn token vào ít expert). Qwen3-MoE, DeepSeek, gpt-oss đều theo hướng này. rasbt có chương MoE from scratch.

---

## B. Tối ưu inference

> **Học ở tuần:** 4 (sau khi sinh text) và 8 (local inference). Nguồn: rasbt *Bonus* `KV Cache`, `Memory-efficient Model Weight Loading`; nanochat `engine.py` (KV cache), `scripts/chat_*`.

### B1. KV Cache — bắt buộc phải hiểu

Khi sinh text tự hồi quy, mỗi bước chỉ thêm **1 token mới**, nhưng nếu tính lại attention cho toàn bộ chuỗi mỗi bước thì lãng phí \(O(n^2)\). **KV cache** lưu lại K,V của các token đã sinh; bước sau chỉ tính K,V cho token mới và attend vào cache → mỗi bước thành \(O(n)\). Đây là lý do GQA/MQA/MLA quan trọng: **bộ nhớ KV cache** \(\approx 2 \cdot n_{layers}\cdot n_{kv\_heads}\cdot d_{head}\cdot \text{seq} \cdot \text{dtype}\) — và là nút thắt VRAM khi context dài (rất liên quan tới giới hạn 8GB của 3070 Ti).

### B2. Sampling — điều khiển đầu ra

Từ logits → phân phối, các chiến lược:

- **Greedy / argmax**: luôn chọn token xác suất cao nhất → lặp, nhàm.
- **Temperature** \(T\): chia logits cho \(T\) trước softmax. \(T<1\) sắc nét hơn (an toàn), \(T>1\) đa dạng hơn (sáng tạo/rủi ro).
- **Top-k**: chỉ lấy mẫu trong \(k\) token cao nhất.
- **Top-p (nucleus)**: lấy tập token nhỏ nhất có tổng xác suất \(\ge p\).
- Thực tế thường kết hợp temperature + top-p. (Raschka ch.5 giới thiệu temperature & top-k; phần này mở rộng thêm top-p.)

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

> **Học ở tuần:** 3 (mở rộng từ "attention heads are dumb" của Giles part 13–14). Nguồn: Giles part 14 (complexity at scale).

### C1. Vì sao self-attention là \(O(n^2)\)

Ma trận score có shape \((\text{seq}\times\text{seq})\) → bộ nhớ và tính toán tăng **bình phương** theo độ dài context. Đây là rào cản chính cho context dài, và là động lực cho sliding-window (A6), MLA (A5), và FlashAttention.

### C2. FlashAttention (khái niệm)

Không *vật chất hoá* ma trận \(n\times n\) trong HBM. Nó **tiling** (chia khối) Q,K,V, tính softmax theo kiểu *online/streaming* trong SRAM, cộng dồn kết quả → cùng đầu ra toán học nhưng **giảm I/O bộ nhớ** mạnh, nhanh hơn và tiết kiệm VRAM. PyTorch gói sẵn qua `F.scaled_dot_product_attention` (chọn backend flash khi đủ điều kiện). Nắm: *cùng kết quả, khác cách dùng bộ nhớ*.

---

## D. Training dynamics

> **Học ở tuần:** 5 (pretraining). Nguồn: **Giles parts 32a–32m** ("Interventions") — chuỗi thực nghiệm đo từng can thiệp; nanochat `optim.py` (Muon), `common.py` (COMPUTE_DTYPE).

Giles train **7+ model** GPT-2-small trên RTX 3090 và đo ảnh hưởng từng can thiệp. Bài học cô đọng:

- **Gradient clipping** (32b): cắt norm gradient (vd. max_norm=1.0) → giảm loss-spike; cải thiện nhẹ nhưng "rabbit hole" hơn tưởng.
- **Bỏ dropout** (32c): với pretraining 1-epoch trên data lớn, **bỏ dropout lại tốt hơn** (dropout hợp cho fine-tune data nhỏ, dễ overfit).
- **Attention bias** (32d): thêm bias cho Q/K/V **không giúp** → modern models bỏ bias.
- **Learning rate** (32e): warmup tuyến tính → cosine decay; LR là siêu tham số nhạy nhất.
- **Weight decay** (32f): regularize, thường ~0.1; không áp lên bias/norm.
- **Weight tying** (32g): chia sẻ trọng số embedding ↔ output head; tiết kiệm tham số nhưng modern models lớn thường **không** tie.
- **float32 vs AMP** (32h): mixed precision (bf16) nhanh + đỡ VRAM, gần như không hại loss cuối.
- **Noise/variance** (32i): nhiều "cải thiện" nằm trong **nhiễu** giữa các lần chạy — phải chạy nhiều seed mới biết tín hiệu thật. *Bài học phương pháp luận quan trọng nhất.*
- **Gradient accumulation** (32k): cộng dồn gradient qua nhiều micro-batch để đạt **effective batch** lớn trên VRAM nhỏ — chìa khoá cho 8GB.

### D1. Optimizers: AdamW vs Muon

AdamW là mặc định (momentum + adaptive LR + decoupled weight decay). **Muon** (nanochat dùng cho ma trận 2D) **orthogonalize** bản cập nhật bằng vài bước Newton-Schulz → hội tụ nhanh hơn ở pretraining; embedding/head vẫn dùng AdamW. Đây là một trong các yếu tố giúp nanochat "speedrun" GPT-2 nhanh.

### D2. Mixed precision & dtype

bf16 (Ampere+), fp16 (cần `GradScaler` chống underflow), fp8 (Hopper, nanochat leaderboard #2 dùng fp8). nanochat quản lý precision **tường minh** qua một biến `COMPUTE_DTYPE` thay vì autocast — trọng số fp32 cho optimizer, cast xuống compute-dtype khi forward.

---

## E. Tokenizer: train BPE from scratch

> **Học ở tuần:** 3 (mở rộng ch.2). Nguồn: nanochat `tok_train.py` + `tok_eval.py`; rasbt *Bonus* "BPE from scratch".

Lộ trình gốc *dùng* tiktoken (đã train sẵn). Bước sâu hơn là **tự train** một BPE tokenizer kiểu GPT-4:

1. Bắt đầu từ byte-level (256 token cơ sở) → không bao giờ OOV.
2. Lặp: đếm cặp byte/token kề nhau xuất hiện nhiều nhất → **merge** thành token mới → lặp tới `vocab_size`.
3. Dùng **regex split pattern** (kiểu GPT-4) để tách số/chữ/khoảng trắng hợp lý trước khi merge.
4. **Đánh giá**: *compression rate* = bytes/token (cao = nén tốt). nanochat `tok_eval.py` đo chỉ số này.

Hiểu tokenizer giải thích nhiều "bug" nổi tiếng: đếm chữ "r" trong "strawberry", toán trên số nhiều chữ số, khoảng trắng/căn lề.

---

## F. Scale & Parallelism

> **Học ở tuần:** 5 (cloud run). Nguồn: Giles part 29 (DDP cloud); HF *Ultra-Scale Playbook*; nanochat `torchrun`.

- **DDP (Data Parallel)**: nhân bản model trên N GPU, mỗi GPU một phần batch, **all-reduce** gradient. Giles part 29 train base model trên 8×A100 bằng DDP. Đây là mức song song đầu tiên cần biết.
- **Tensor Parallel (TP)**: chia *trong* một lớp (ma trận) qua nhiều GPU — cho model không vừa 1 GPU.
- **Pipeline Parallel (PP)**: chia *theo lớp* thành các stage.
- **ZeRO / FSDP**: shard optimizer state / gradient / param qua GPU để giảm bộ nhớ (DeepSpeed ZeRO-1/2/3, PyTorch FSDP).
- **MFU** (Model FLOPs Utilization): % FLOP lý thuyết thực sự dùng được — thước đo hiệu quả train (nanochat theo dõi `train/mfu`).

Với bạn (1 GPU 8GB local): chủ yếu dùng **gradient accumulation** (D) ở local; **DDP** chỉ khi thuê multi-GPU cloud cho lần pretrain.

---

## G. Alignment & Reasoning đầy đủ

> **Học ở tuần:** 6 (mở rộng). Nguồn: **FareedKhan-dev `src/post_training/`** (SFT → Reward Model → PPO → DPO → GRPO, pure PyTorch trên Alpaca/Dolly/HH-RLHF/UltraFeedback/GSM8K); Raschka `reasoning-from-scratch`; nanochat `chat_sft.py`, `chat_rl.py`.

Pipeline đầy đủ "base → aligned reasoning model":

```
Pretrain  →  Midtrain  →  SFT  →  Reward Model  →  PPO / DPO  →  GRPO / RLVR
(dự đoán   (dạy format   (bắt    (học chấm điểm   (RL tối ưu   (RL cho reasoning,
 token)     hội thoại,    chước   ưu tiên giữa     reward)      reward kiểm chứng
            tool, special  phản    cặp output)                   được — toán/code)
            tokens)        hồi tốt)
```

- **Midtrain** (nanochat): bước *giữa* pretrain và SFT — dạy model định dạng hội thoại, special tokens, dùng tool, một ít kiến thức. Khái niệm này **không có** trong sách Raschka gốc.
- **Reward Model (RM)**: train một model chấm điểm; FareedKhan implement from scratch.
- **PPO**: RL kinh điển của RLHF, cần RM + critic + KL với policy gốc.
- **DPO**: bỏ RM/PPO, tối ưu trực tiếp từ cặp (chosen, rejected) — đơn giản & ổn định hơn (đã có công thức ở Tuần 6).
- **GRPO/RLVR**: *Group Relative Policy Optimization* — bỏ critic, chuẩn hoá reward theo **nhóm sample**; **RLVR** = reward *kiểm chứng được* (đáp án toán đúng/sai, test code pass) → nền của reasoning models (o1/R1-style).
- **Tool-use RL** (nanochat): model học gọi Python để đếm/tính (vd. "đếm r trong strawberry"), reward khi ra kết quả đúng.

---

## H. Evaluation đúng cách

> **Học ở tuần:** 5, 7, 10, 13. Nguồn: Giles part 21 (perplexity), part 30 (LLM-as-judge); nanochat `core_eval.py` (CORE/DCLM), `loss_eval.py` (bits-per-byte); tasks `mmlu/arc/gsm8k/humaneval`.

- **Cross-entropy loss / Perplexity** \(\text{PPL}=e^{L}\): đo trên ngôn ngữ; nhưng **phụ thuộc vocab/tokenizer** nên khó so chéo model.
- **Bits-per-byte (bpb)**: chuẩn hoá loss về *byte* → **so sánh được** giữa các tokenizer/model khác nhau. nanochat dùng bpb thay loss thô. *Nên biết khi so model của bạn với GPT-2.*
- **CORE score (DCLM)**: tổ hợp nhiều benchmark; nanochat đo "time-to-GPT-2" theo CORE (GPT-2 = 0.2565).
- **Benchmark chuẩn**: MMLU (kiến thức rộng, trắc nghiệm), ARC (khoa học), GSM8K (toán tiểu học), HumanEval (code). nanochat có sẵn các task này.
- **LLM-as-judge** (Giles part 30): dùng một LLM mạnh chấm output — tiện nhưng **nhiều bẫy** (thiên vị độ dài, vị trí, tự khen). Giles cho thấy *loss thấp hơn không đảm bảo hữu ích hơn* trong thực tế → đừng tin một chỉ số duy nhất.

---

## Tóm tắt ưu tiên (nếu thời gian hẹp)

1. **Bắt buộc**: KV cache (B1), RoPE (A1), RMSNorm/SwiGLU (A2–A3), GQA (A4), gradient accumulation (D), bits-per-byte (H) — đây là khoảng cách lớn nhất giữa "GPT-2 2019" và "LLM bạn dùng hằng ngày".
2. **Nên có**: MoE (A7), quantization internals (B4), Muon (D1), full alignment pipeline (G), BPE training (E).
3. **Để dành**: MLA (A5), sliding window (A6), speculative decoding (B3), TP/PP/FSDP (F) — đào khi cần.

> **Neo nguồn nhanh:** rasbt *Bonus Material* (kiến trúc hiện đại from scratch) · Giles 32a–32m (training dynamics) + 29 (DDP) + 21/30 (eval) · FareedKhan `src/post_training` (alignment) · nanochat `gpt.py`/`engine.py`/`optim.py`/`tok_train.py` (full-stack hiện đại).
