# Tuần 5 — Pretraining: training loop + một lần chạy GPT-2 thật (cloud) (Raschka ch.5)

> Phase 1 — Deep Internals. Tuần giá trị cao. Hiểu vòng lặp pretraining, rồi thực sự pretrain một model nhỏ.

## Mục tiêu

- Hiểu **pretraining loop**, cross-entropy/perplexity, **LR scheduling**, checkpointing.
- Thực sự **pretrain** một model nhỏ.

## Nguồn học

- Raschka — **ch.5** (Pretraining on unlabeled data) + **Appendix D** (bells & whistles).
- Giles Thomas — parts **20–29** (training, cross-entropy) + mini-series "Interventions" (gradient clipping, dropout, LR, weight decay, weight tying, mixed precision — parts **32a–32m**).
- Karpathy — nanoGPT / **llm.c "Reproduce GPT-2 124M"**.
- HF **Ultra-Scale Playbook** (gradient accumulation / parallelism).

## Nhiệm vụ (Task)

1. Train **local** trên dataset nhỏ "The Verdict" → validate vòng lặp trên 3070 Ti.
2. Sau đó chạy **pretraining GPT-2-small thật trên CLOUD** với FineWeb / FineWeb-Edu.

## Deliverable

Checkpoint base-model nhỏ + write-up **so sánh loss curve** của bạn với GPT-2 gốc (theo phong cách Giles).

## Thời lượng

~12–15 giờ (chưa kể thời gian train không cần ngồi canh).

## Phần cứng & chi phí (quan trọng)

- **Local 3070 Ti**: chỉ để validate loop + model tí hon. 8GB → micro-batch 1–2, seq len 1024, gradient accumulation ~16–64 để đạt effective batch ~0.5M token (Karpathy target ~524,288 tokens/update).
- **Cloud cho lần chạy thật**:
  - RunPod RTX 4090 từ **$0.34/hr** (Community) — chạy vài giờ.
  - Lambda 8×A100 (~$14/hr/node) → reproduce trong <4h, ~**$35** (chi phí Giles ghi nhận).
  - Karpathy llm.c: 8×A100 ~90 phút ≈ **$20**.
- **Caveat**: ước lượng thời gian cho 3070 Ti là extrapolation, KHÔNG phải benchmark đo thật — chạy **smoke test ngắn** trước khi commit chạy dài. *Trigger lên cloud:* khi run local dự kiến > ~24h.

> ⚠️ Giá cloud biến động (marketplace). Kiểm tra lại tại thời điểm deploy. Từ VN truy cập được; lưu ý phương thức thanh toán (thẻ quốc tế) + latency.

---

## Checklist tiến độ

- [ ] Code training loop: batch → logits → cross-entropy loss → backward → step
- [ ] Thêm train/val split + đánh giá loss định kỳ
- [ ] Thêm LR warmup + cosine decay
- [ ] Thêm gradient clipping + mixed precision (autocast) + grad accumulation
- [ ] Thêm checkpointing (lưu/khôi phục optimizer + model + step)
- [ ] Smoke test local trên "The Verdict" — xác nhận loss giảm
- [ ] Chọn cloud provider + chuẩn bị dataset (FineWeb-Edu sample)
- [ ] Chạy pretrain thật trên cloud → lưu checkpoint
- [ ] Vẽ loss curve, so với GPT-2 gốc (~3.5) — viết `loss_analysis.md`

## Mẹo bộ nhớ 8GB (nếu thử local)

```
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```
+ gradient checkpointing, micro-batch nhỏ, seq len ≤1024.

## 🚀 Bổ sung nâng cao (training dynamics + scale)

Pretraining là nơi nhiều thủ thuật "ăn tiền". Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md):

- **D Interventions (Giles 32a–32m)** — đo từng can thiệp: gradient clipping, **bỏ dropout** (tốt hơn cho pretrain 1-epoch), weight decay, weight tying, mixed precision; và **D (mục noise/variance 32i)**: nhiều "cải thiện" nằm trong nhiễu — phải chạy nhiều seed.
- **D1 Optimizer** — AdamW vs **Muon** (nanochat dùng cho ma trận 2D, hội tụ nhanh hơn).
- **D2** — bf16/fp16(GradScaler)/**fp8**, quản lý dtype tường minh kiểu nanochat.
- **F Parallelism** — **DDP** (Giles part 29, 8×A100), TP/PP/ZeRO/FSDP, **MFU**.
- **H Eval** — dùng **bits-per-byte** (so sánh được giữa tokenizer) thay vì loss thô khi so với GPT-2; **CORE/DCLM**.

> Nguồn: Giles parts 21, 29, 32a–32m; HF *Ultra-Scale Playbook*; nanochat `optim.py`, `loss_eval.py`, `core_eval.py`.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `train_loop.py` | Skeleton pretraining loop (TODO) |
| `cloud_run_notes.md` | Quy trình thuê GPU + chạy cloud + checklist chi phí |
| `loss_analysis.md` | Template write-up so sánh loss curve (deliverable) |
