# Tuần 4 — Lắp ráp & chạy mô hình GPT (Raschka ch.4)

> Phase 1 — Deep Internals. Ghép mọi mảnh thành kiến trúc GPT-2 hoàn chỉnh và sinh text.

## Mục tiêu

- Build đầy đủ kiến trúc **GPT-2**: layer norm, GELU FFN, residual/shortcut, transformer block.
- Sinh text (ban đầu từ model chưa train).

## Nguồn học

- Raschka — **ch.4** (Implementing a GPT model from scratch).
- Giles Thomas — parts **15–19** (layer norm, feed-forward, residuals, kết thúc ch.4).
- Karpathy — **nanoGPT** (`github.com/karpathy/nanoGPT`) làm tham chiếu chéo.

## Nhiệm vụ (Task)

- Khởi tạo config **124M**.
- **Load trọng số GPT-2 pretrained của OpenAI** (như sách hướng dẫn) để xác nhận kiến trúc đúng.
- Sinh text.

## Deliverable

Mô hình GPT của bạn sinh **text mạch lạc** từ trọng số GPT-2 đã load.

## Thời lượng

~10–12 giờ.

## Phần cứng

3070 Ti (inference 124M nằm gọn trong 8GB).

---

## Checklist tiến độ

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

> Bài tập hay: fork model GPT-2 của bạn, thay LayerNorm→RMSNorm và GELU-FFN→SwiGLU, so số tham số. Nguồn: rasbt walkthrough **Llama 3** & **Qwen3 dense/MoE**, **gpt-oss**; nanochat `gpt.py`.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `gpt_model.py` | Skeleton LayerNorm/GELU/FFN/Block/GPTModel (TODO) |
| `load_weights_notes.md` | Hướng dẫn + checklist load trọng số GPT-2 |
