# Tuần 3 — Tokenization, embeddings, attention từ đầu (Raschka ch.2–3)

> Phase 1 — Deep Internals. **Đây là điểm cốt lõi về khái niệm — đi chậm.** Tự tay code toàn bộ stack attention.

## Mục tiêu

- Hiểu & code **BPE / data loading**, **token + positional embeddings**.
- Tự code **self-attention → causal attention → multi-head**, từng bước bằng tay.

## Nguồn học

- Raschka — **ch.2** (Working with text data) + **ch.3** (Coding attention mechanisms).
- Giles Thomas — parts **1–14** (đặc biệt: part 8 trainable self-attention, part 9 causal, part 12 multi-head, part 13 "attention heads are dumb").
- **The Annotated Transformer** (Harvard NLP, nlp.seas.harvard.edu).

## Nhiệm vụ (Task)

Tự code đầy đủ attention stack ch.3; **verify shape** với repo của sách.

## Deliverable

`multihead_attention.py` tự viết, **pass shape test** (`test_attention.py`) + ghi chú Claude review.

## Thời lượng

~12–15 giờ (crux khái niệm — đi chậm).

## Phần cứng

3070 Ti.

---

## Checklist tiến độ

- [ ] Đọc ch.2: BPE (dùng `tiktoken`), data loader, sliding window
- [ ] Hiểu token embedding vs positional embedding (cộng vào nhau)
- [ ] Code **simplified self-attention** (không trainable) — hiểu context vector
- [ ] Code **scaled dot-product attention** với `W_Q, W_K, W_V` trainable
- [ ] Thêm **causal mask** (tam giác trên = -inf) + dropout
- [ ] Mở rộng lên **multi-head** (chia/d_out hoặc stack head)
- [ ] Chạy `test_attention.py` → tất cả shape đúng
- [ ] Dán code cho Claude review so với Raschka

## Mốc shape cần nhớ

- Input embeddings: `(batch, seq_len, d_in)`
- Q/K/V: `(batch, seq_len, d_out)`
- Attention scores: `(batch, seq_len, seq_len)`
- Multi-head: `(batch, num_heads, seq_len, head_dim)` → gộp lại `(batch, seq_len, d_out)`

## 🚀 Bổ sung nâng cao (sau khi nắm attention GPT-2)

GPT-2 dùng **absolute positional embedding + MHA**. Các model hiện đại (Llama 3, Qwen3, DeepSeek) đổi gần hết. Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md), mục:

- **A1 RoPE** — xoay Q,K theo vị trí (thay vì cộng), score chỉ phụ thuộc khoảng cách tương đối.
- **A4 GQA/MQA** + **A5 MLA** — chia sẻ/nén K,V để **giảm KV cache**.
- **C1–C2** — vì sao attention là `O(n²)` và **FlashAttention** giải quyết bằng tiling (không vật chất hoá ma trận n×n).
- **B1 KV cache** — bắt buộc hiểu cho inference.
- **E** — tự **train BPE tokenizer** (nanochat `tok_train.py`) thay vì chỉ dùng tiktoken.

> Nguồn từ-đầu: rasbt *Bonus Material* (`Grouped-Query Attention`, `Multi-Head Latent Attention`, `Sliding Window Attention`); Giles part 14 (complexity at scale).

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `multihead_attention.py` | Skeleton self/causal/multi-head attention (TODO) |
| `test_attention.py` | Kiểm tra shape các bước attention |
