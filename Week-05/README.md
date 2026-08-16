# Tuần 5 — Pretraining: training loop + một lần chạy GPT-2 thật (cloud)

> Phase 1 — Deep Internals. Tuần giá trị cao. Hiểu vòng lặp pretraining, rồi thực sự pretrain một model nhỏ.

## Mục tiêu

- Hiểu **pretraining loop**, cross-entropy/perplexity, **LR scheduling**, checkpointing.
- Thực sự **pretrain** một model nhỏ.

## Nguồn học

- `karpathy/nanoGPT` — `train.py` (gradient clipping, LR warmup+decay, weight decay, mixed precision, grad accumulation đều có trong đó).
- Karpathy — **llm.c "Reproduce GPT-2 124M"** (Discussion #481).
- HF **Ultra-Scale Playbook** (gradient accumulation / parallelism).
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm nguồn đã xác minh 2026-08-11).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md) — loop, LR schedule, clipping, mixed precision, accumulation, checkpoint.
2. [`02_train_loop.py`](02_train_loop.py) — TỰ code pretraining loop, smoke test local.
3. [`05_data_dedup.py`](05_data_dedup.py) — exact dedup + MinHash + quality filter kiểu FineWeb. **Làm trước cloud run — lọc data chính là bước đầu của pretraining thật.** (Lý thuyết: `01_theory_notes.md` §10.)
4. [`03_cloud_run_notes.md`](03_cloud_run_notes.md) — quy trình thuê GPU + chạy thật.
5. [`04_loss_analysis.md`](04_loss_analysis.md) — write-up so sánh loss curve (deliverable).
6. [`quiz.md`](quiz.md) — quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

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

- [ ] Đọc `01_theory_notes.md` — chạy lại được mọi snippet trong đó
- [ ] Code training loop: batch → logits → cross-entropy loss → backward → step
- [ ] Thêm train/val split + đánh giá loss định kỳ
- [ ] Thêm LR warmup + cosine decay
- [ ] Thêm gradient clipping + mixed precision (autocast) + grad accumulation
- [ ] Thêm checkpointing (lưu/khôi phục optimizer + model + step)
- [ ] Smoke test local trên text public-domain nhỏ — xác nhận loss giảm
- [ ] Chọn cloud provider + chuẩn bị dataset (FineWeb-Edu sample)
- [ ] Chạy pretrain thật trên cloud → lưu checkpoint
- [ ] Vẽ loss curve, so với GPT-2 gốc (~3.5) — viết `04_loss_analysis.md`

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

## 🚀 Extension: DDP hands-on trên cloud 2×GPU

> Chủ repo xác nhận 2026-08-16: sẵn sàng thuê GPU cloud, chi phí không phải blocker.

Sau khi `02_train_loop.py` chạy ổn 1 GPU, thuê một instance **2 GPU** và chạy chính loop đó qua DDP:

```bash
torchrun --nproc_per_node=2 02_train_loop.py
```

Các bước sửa tối thiểu (theo tutorial DDP chính thức của PyTorch, đã xác minh URL 2026-08-16):

1. **`init_process_group`** — khởi tạo process group (backend `nccl` cho GPU) đầu chương trình; đọc `RANK`/`LOCAL_RANK`/`WORLD_SIZE` từ env do `torchrun` set, `destroy_process_group()` khi xong.
2. **`DistributedSampler`** — "chunks the input data across all distributed processes" (nguyên văn tutorial) để 2 GPU không train trùng data; nếu loop tự cắt batch bằng `randint` thì thay bằng chia shard theo rank.
3. **Wrap model** — `model = DDP(model, device_ids=[local_rank])`; gradient tự đồng bộ trong `backward()`.

Đo **tokens/giây** với 1 GPU vs 2 GPU (cùng effective batch) và ghi kết quả vào [`03_cloud_run_notes.md`](03_cloud_run_notes.md). [Suy luận] Kỳ vọng gần 2× nhưng thường thấp hơn do chi phí giao tiếp gradient — số thật của bạn mới là bằng chứng.

Lý thuyết nền: [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) §F (DDP, TP/PP/ZeRO/FSDP, MFU).

> Nguồn (đã fetch xác minh nội dung 2026-08-16):
> - PyTorch — *Multi GPU training with DDP* (init_process_group, DistributedSampler, wrap DDP): https://docs.pytorch.org/tutorials/beginner/ddp_series_multigpu.html
> - PyTorch — *Getting Started with Distributed Data Parallel* (torchrun launch): https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| — | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: loop, schedule, precision, checkpoint |
| 2 | `02_train_loop.py` | Skeleton pretraining loop (TODO) |
| 3 | `03_cloud_run_notes.md` | Quy trình thuê GPU + chạy cloud + checklist chi phí |
| 4 | `04_loss_analysis.md` | Template write-up so sánh loss curve (deliverable) |
| 5 | `05_data_dedup.py` | Skeleton data curation: exact dedup + MinHash + quality filter (TODO) — làm trước cloud run |
| 6 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
