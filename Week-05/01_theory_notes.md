# Lý thuyết Tuần 5 — Pretraining: loop, schedule, precision, checkpoint

> Đọc trước khi điền TODO trong [`02_train_loop.py`](02_train_loop.py). Số liệu kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11; nguồn cuối file. Cần nắm training loop 5 bước (Tuần 1) và GPT model (Tuần 4).

---

## 1. Pretraining loop = loop Tuần 1 + dữ liệu ở quy mô khác

Bài toán duy nhất: **đoán token kế tiếp**. Với batch `(B, T)`, model cho logits `(B, T, V)`; cross-entropy tính trên **mọi vị trí** cùng lúc (mỗi vị trí i có nhãn là token i+1 — sliding window Tuần 3). Không cần nhãn tay — "nhãn" chính là văn bản.

```python
logits = model(xb)                                    # (B, T, V)
loss = F.cross_entropy(logits.flatten(0, 1), yb.flatten())
```

**Perplexity** = `exp(loss)`: loss 3.5 → PPL ≈ 33.1 ("phân vân giữa ~33 lựa chọn"); loss 0 → PPL 1 (kiểm chứng 2026-08-11). Mốc so sánh trong README: GPT-2 gốc loss ~3.5 trên miền dữ liệu tương đương.

## 2. Train/val split — biết mình đang học hay đang thuộc lòng

Cắt corpus thành train/val (ví dụ 90/10), đo val loss định kỳ. Train loss giảm mà val loss tăng = memorize. Lưu ý pretrain 1-epoch trên corpus lớn hầu như không kịp overfit — đó là lý do nanoGPT để dropout 0 khi pretrain (mục nâng cao D).

## 3. LR schedule — warmup + cosine decay

```
it < warmup:  lr = max_lr · (it+1)/warmup            (tăng tuyến tính)
sau đó:       lr = min_lr + 0.5·(1+cos(π·tiến_độ))·(max_lr − min_lr)
```

Giá trị kiểm chứng với `max_lr=6e-4, min_lr=6e-5, warmup=100, max_it=1000`: it=0 → 6.0e-6; it=100 → 6.0e-4 (đỉnh); it=550 → 3.3e-4 (lưng chừng cosine); it=1000 → 6.0e-5 (đáy). [Suy luận] Warmup giúp tránh bước cập nhật quá lớn khi các thống kê moment của AdamW chưa ổn định ở những step đầu — lập luận phổ biến, hiệu quả cụ thể phải nhìn loss curve của chính bạn.

## 4. Gradient clipping — cầu chì chống loss spike

Chặn **norm toàn cục** của gradient về ngưỡng (thường 1.0), giữ nguyên hướng:

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
```

Kiểm chứng: gradient `[30, 40]` (norm 50) sau clip thành `[0.6, 0.8]` (norm 1.0) — cùng hướng, ngắn lại. Gọi **sau** `backward()`, **trước** `step()`.

## 5. Mixed precision — vì sao bf16 là mặc định thời nay

Số đo từ `torch.finfo` (kiểm chứng 2026-08-11):

| dtype | max | eps (độ mịn) |
|-------|-----|--------------|
| float16 | 65,504 | 9.8e-4 |
| bfloat16 | 3.39e38 | 7.8e-3 |

- **fp16**: mịn hơn nhưng max chỉ 65,504 → dễ overflow → cần **GradScaler**.
- **bf16**: range bằng fp32 → không cần scaler, code đơn giản hơn; đổi lại kém mịn. GPU Ampere (3070 Ti) trở lên hỗ trợ bf16.

```python
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    logits = model(xb); loss = ...
```

## 6. Gradient accumulation — batch to trên VRAM nhỏ

Effective batch (token/update) = `micro_batch × seq_len × accum_steps`. Mục tiêu README ~524,288 token/update: với micro-batch 1 × seq 1024 → cần **512** accum steps; micro-batch 2 → 256 (số học, tự kiểm). Cách làm: cộng dồn `loss/accum_steps` qua `backward()` nhiều lần, `step()` + `zero_grad()` mỗi `accum_steps` lần — chính là tận dụng tính chất grad **cộng dồn** đã học ở Tuần 2.

## 7. Checkpointing — không mất công train vì một lần rớt điện/cloud

Lưu đủ 3 thứ mới resume đúng: `model.state_dict()`, `optimizer.state_dict()` (AdamW mang 2 giá trị moment cho MỖI tham số — thiếu nó resume sẽ khựng), và `step` (để LR schedule tiếp đúng chỗ). Lưu định kỳ + giữ bản `best_val`. Nguyên tắc chạy cloud: **smoke test local vài trăm step xác nhận loss giảm rồi mới thuê máy** — xem [`03_cloud_run_notes.md`](03_cloud_run_notes.md).

## 8. Tiếng Việt trong tuần này

- **Model chỉ biết ngôn ngữ có trong corpus pretrain.** FineWeb/FineWeb-Edu trong task tuần này thiên tiếng Anh — model bạn pretrain ra sẽ không đọc được tiếng Việt, và đó là kỳ vọng đúng. Muốn có khả năng tiếng Việt phải có corpus Việt trong pretrain (hoặc dùng base đa ngôn ngữ rồi fine-tune — hướng của Tuần 8–9; nguồn corpus VN license sạch: xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)).
- **Ngân sách token lệch theo ngôn ngữ:** cùng 1 GB văn bản, tiếng Việt sinh ra nhiều token hơn tiếng Anh với tokenizer thiên Anh (fertility đo ở Tuần 3) → "1B token" tiếng Việt chứa **ít nội dung hơn** 1B token tiếng Anh. Khi đọc bất kỳ báo cáo pretrain đa ngôn ngữ nào, hỏi ngay: token đếm bằng tokenizer nào?
- **So sánh chéo ngôn ngữ/tokenizer thì bỏ perplexity, dùng bits-per-byte** (mục nâng cao H): PPL phụ thuộc tokenizer — cùng một văn bản, tokenizer khác nhau cho PPL khác nhau dù model "giỏi" như nhau; bits-per-byte chuẩn hóa theo byte nên so được.

## 9. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| karpathy/nanoGPT (`train.py`, MIT) | https://github.com/karpathy/nanoGPT | 3, 4, 5, 6 |

(llm.c Discussion #481 và HF Ultra-Scale Playbook: link trong README nguồn học — nội dung chi phí/thời gian trong đó là **ảnh chụp thời điểm viết**, kiểm tra lại giá trước khi thuê máy.)

## Sau khi đọc xong

1. Điền TODO trong [`02_train_loop.py`](02_train_loop.py): loss → split/eval → schedule → clip → autocast → accumulation → checkpoint (đúng thứ tự đó, chạy được từng tầng rồi mới thêm tầng sau).
2. Smoke test local trên text public-domain nhỏ — bằng chứng: loss giảm qua các step, ghi số vào nhật ký.
3. Chuẩn bị cloud run theo [`03_cloud_run_notes.md`](03_cloud_run_notes.md); train thật; viết [`04_loss_analysis.md`](04_loss_analysis.md) so với GPT-2.
4. Làm [`quiz.md`](quiz.md); mục nâng cao D/F/H đọc sau khi loop chạy được.
