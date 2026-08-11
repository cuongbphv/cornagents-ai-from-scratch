# Tuần 5 — Pretraining: training loop + một lần chạy GPT-2 thật (cloud)

> Phase 1 — Deep Internals. Tuần giá trị cao. Hiểu vòng lặp pretraining, rồi thực sự pretrain một model nhỏ.

## Mục tiêu

- Hiểu **pretraining loop**, cross-entropy/perplexity, **LR scheduling**, checkpointing.
- Thực sự **pretrain** một model nhỏ.

## Nguồn học

- `karpathy/nanoGPT` — `train.py` (gradient clipping, LR warmup+decay, weight decay, mixed precision, grad accumulation đều có trong đó).
- Karpathy — **llm.c "Reproduce GPT-2 124M"** (Discussion #481).
- HF **Ultra-Scale Playbook** (gradient accumulation / parallelism).

## Nhiệm vụ (Task)

1. Train **local** trên một text nhỏ thuộc public domain (vd. một truyện ngắn từ Project Gutenberg) → validate vòng lặp trên 3070 Ti.
2. Sau đó chạy **pretraining GPT-2-small thật trên CLOUD** với FineWeb / FineWeb-Edu.

## Deliverable

Checkpoint base-model nhỏ + write-up **so sánh loss curve** của bạn với GPT-2 gốc.

## Thời lượng

~12–15 giờ (chưa kể thời gian train không cần ngồi canh).

## Phần cứng & chi phí (quan trọng)

- **Local 3070 Ti**: chỉ để validate loop + model tí hon. 8GB → micro-batch 1–2, seq len 1024, gradient accumulation ~16–64 để đạt effective batch ~0.5M token (Karpathy target ~524,288 tokens/update).
- **Cloud cho lần chạy thật**:
  - RunPod RTX 4090 từ **$0.34/hr** (Community) — chạy vài giờ.
  - Karpathy llm.c: Lambda 8×A100 (~$14/hr/node), ~90 phút ≈ **$20** (Discussion #481).
- **Caveat**: ước lượng thời gian cho 3070 Ti là extrapolation, KHÔNG phải benchmark đo thật — chạy **smoke test ngắn** trước khi commit chạy dài. *Trigger lên cloud:* khi run local dự kiến > ~24h.

> ⚠️ Giá cloud biến động (marketplace). Kiểm tra lại tại thời điểm deploy. Từ VN truy cập được; lưu ý phương thức thanh toán (thẻ quốc tế) + latency.

---

## Checklist tiến độ

- [ ] Code training loop: batch → logits → cross-entropy loss → backward → step
- [ ] Thêm train/val split + đánh giá loss định kỳ
- [ ] Thêm LR warmup + cosine decay
- [ ] Thêm gradient clipping + mixed precision (autocast) + grad accumulation
- [ ] Thêm checkpointing (lưu/khôi phục optimizer + model + step)
- [ ] Smoke test local trên text public-domain nhỏ — xác nhận loss giảm
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

- **D Training dynamics** — các can thiệp trong `nanoGPT/train.py`: gradient clipping, **dropout=0 khi pretrain 1-epoch**, weight decay, weight tying, mixed precision; và mục noise/variance: nhiều "cải thiện" nằm trong nhiễu — phải chạy nhiều seed.
- **D1 Optimizer** — AdamW vs **Muon** (nanochat dùng cho ma trận 2D, hội tụ nhanh hơn).
- **D2** — bf16/fp16(GradScaler)/**fp8**, quản lý dtype tường minh kiểu nanochat.
- **F Parallelism** — **DDP** (torchrun trong nanoGPT/llm.c), TP/PP/ZeRO/FSDP, **MFU**.
- **H Eval** — dùng **bits-per-byte** (so sánh được giữa tokenizer) thay vì loss thô khi so với GPT-2; **CORE/DCLM**.

> Nguồn: `nanoGPT/train.py`; HF *Ultra-Scale Playbook*; nanochat `optim.py`, `loss_eval.py`, `core_eval.py`.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `train_loop.py` | Skeleton pretraining loop (TODO) |
| `cloud_run_notes.md` | Quy trình thuê GPU + chạy cloud + checklist chi phí |
| `loss_analysis.md` | Template write-up so sánh loss curve (deliverable) |
