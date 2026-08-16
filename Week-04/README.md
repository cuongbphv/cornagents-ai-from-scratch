# Tuần 4 — Lắp ráp & chạy mô hình GPT

> Phase 1 — Deep Internals. Ghép mọi mảnh thành kiến trúc GPT-2 hoàn chỉnh và sinh text.

## Mục tiêu

- Build đầy đủ kiến trúc **GPT-2**: layer norm, GELU FFN, residual/shortcut, transformer block.
- Sinh text (ban đầu từ model chưa train).

## Nguồn học

- `karpathy/nanoGPT` — `model.py` (kiến trúc GPT-2 đầy đủ) + hàm `from_pretrained` (load weights GPT-2).
- Paper GPT-2 "Language Models are Unsupervised Multitask Learners"; paper Layer Normalization (arXiv 1607.06450), GELU (arXiv 1606.08415).
- Karpathy — **nanoGPT** (`github.com/karpathy/nanoGPT`) làm tham chiếu chéo.
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm nguồn đã xác minh 2026-08-11).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md) — LayerNorm, GELU, FFN, residual, đếm tham số 124M.
2. [`02_gpt_model.py`](02_gpt_model.py) — TỰ lắp ráp GPTModel (deliverable).
3. [`03_load_weights_notes.md`](03_load_weights_notes.md) — load trọng số GPT-2, sinh text mạch lạc.
4. [`quiz.md`](quiz.md) — quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

- Khởi tạo config **124M**.
- **Load trọng số GPT-2 pretrained của OpenAI** (tham chiếu cách `nanoGPT` làm trong `from_pretrained`) để xác nhận kiến trúc đúng.
- Sinh text.

## Deliverable

Mô hình GPT của bạn sinh **text mạch lạc** từ trọng số GPT-2 đã load.

## Thời lượng

~10–12 giờ.

## Phần cứng

3070 Ti (inference 124M nằm gọn trong 8GB).

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` — chạy lại được mọi snippet trong đó
- [ ] Code `LayerNorm` từ đầu (hiểu mean/var, scale γ + shift β)
- [ ] Code `GELU` activation
- [ ] Code `FeedForward` (Linear → GELU → Linear, mở rộng 4×)
- [ ] Ghép `MultiHeadAttention` (Tuần 3) vào `TransformerBlock` + residual + pre-LN
- [ ] Lắp `GPTModel`: token emb + pos emb → N blocks → final LN → out head
- [ ] Verify số tham số ≈ 124M
- [ ] Load trọng số GPT-2 OpenAI, map đúng tên layer
- [ ] Sinh text mạch lạc → xác nhận kiến trúc đúng
- [ ] Claude review phần load weights (dễ sai mapping)

## Config GPT-2 small (124M)

```
vocab_size      = 50257
context_length  = 1024
emb_dim         = 768
n_heads         = 12
n_layers        = 12
drop_rate       = 0.1
qkv_bias        = True   # GPT-2 dùng bias ở QKV
```

## 🚀 Bổ sung nâng cao (GPT-2 → kiến trúc hiện đại)

Sau khi lắp xong GPT-2, đối chiếu với Llama 3/Qwen3 trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md):

- **A2 RMSNorm** (thay LayerNorm — bỏ mean & bias), **A3 SwiGLU FFN** (gated, thay GELU-4×), **bỏ bias** ở Linear.
- **A7 MoE** — thay 1 FFN dày bằng nhiều expert + router top-k (Qwen3-MoE, gpt-oss).
- **B1 KV cache** + **B2 Sampling** (temperature/top-k/**top-p**) — cho phần sinh text.
- **Bài tập KV cache có sẵn trong repo**: cuối [`02_gpt_model.py`](02_gpt_model.py) có section 🚀 EXT-TODO 1–3 — thêm `generate_with_kv_cache` (mỗi bước chỉ feed token mới, append K,V per-layer) + assert cached vs uncached ra cùng dãy token (greedy). Lý thuyết ở [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) §B1.
- **Bài tập RoPE có sẵn trong repo**: [`02_gpt_model.py`](02_gpt_model.py) EXT-TODO 4–5 — viết `precompute_rope_freqs` + `apply_rope` (xoay cặp chiều xen kẽ bằng cos/sin) rồi check bằng số: pos 0 là identity, dot product q·k chỉ phụ thuộc khoảng cách tương đối (m − n). Lý thuyết ở [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) §A1.
- **Bài tập MoE toy có sẵn trong repo**: [`02_gpt_model.py`](02_gpt_model.py) EXT-TODO 6–7 — `MoEFeedForward` (4 expert, router top-2) + aux load-balancing loss kiểu Switch Transformer; check output giữ nguyên shape và aux_loss là scalar > 0. Toy độc lập, KHÔNG thay FFN trong skeleton chính. Lý thuyết ở [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) §A7.

> Bài tập hay: fork model GPT-2 của bạn, thay LayerNorm→RMSNorm và GELU-FFN→SwiGLU, so số tham số. Nguồn: paper RMSNorm (arXiv 1910.07467) + GLU Variants/SwiGLU (arXiv 2002.05202); implementation Llama/Qwen trong HF `transformers`; nanochat `gpt.py`.

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| — | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: LayerNorm, GELU, FFN, residual, param count |
| 2 | `02_gpt_model.py` | Skeleton LayerNorm/GELU/FFN/Block/GPTModel (TODO) |
| 3 | `03_load_weights_notes.md` | Hướng dẫn + checklist load trọng số GPT-2 |
| 4 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
