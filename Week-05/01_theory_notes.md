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

- **Model chỉ biết ngôn ngữ có trong corpus pretrain.** FineWeb/FineWeb-Edu trong task tuần này thiên tiếng Anh — model bạn pretrain ra sẽ không đọc được tiếng Việt, và đó là kỳ vọng đúng. Nhân tiện, paper FineWeb (PDF trong repo, xem bảng Nguồn) đáng một buổi đọc: FineWeb là "a 15-trillion token dataset derived from 96 Common Crawl snapshots", FineWeb-Edu là subset giáo dục 1.3T token, và các tác giả tài liệu hóa từng quyết định lọc/dedup của mình — muốn biết một corpus web-scale được "nấu" ra sao thì hiếm chỗ nào kể kỹ hơn. Muốn có khả năng tiếng Việt phải có corpus Việt trong pretrain (hoặc dùng base đa ngôn ngữ rồi fine-tune — hướng của Tuần 8–9; nguồn corpus VN license sạch: xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)).
- **Ngân sách token lệch theo ngôn ngữ:** cùng 1 GB văn bản, tiếng Việt sinh ra nhiều token hơn tiếng Anh với tokenizer thiên Anh (fertility đo ở Tuần 3) → "1B token" tiếng Việt chứa **ít nội dung hơn** 1B token tiếng Anh. Khi đọc bất kỳ báo cáo pretrain đa ngôn ngữ nào, hỏi ngay: token đếm bằng tokenizer nào?
- **So sánh chéo ngôn ngữ/tokenizer thì bỏ perplexity, dùng bits-per-byte** (mục nâng cao H): PPL phụ thuộc tokenizer — cùng một văn bản, tokenizer khác nhau cho PPL khác nhau dù model "giỏi" như nhau; bits-per-byte chuẩn hóa theo byte nên so được.

## 9. Scaling laws — compute/data/params trade-off

Hai paper trả lời câu hỏi "model bao nhiêu tham số, train bao nhiêu token thì đáng đồng compute": cả hai đã xác minh abstract trên arXiv ngày 2026-08-16 (link-only trong [`../docs/papers/README.md`](../docs/papers/README.md), gắn Tuần 5).

**Kaplan et al. 2020 (arXiv 2001.08361):** loss của language model giảm theo **power law** với cả 3 đại lượng — số tham số, kích thước dataset, lượng compute — "with some trends spanning more than seven orders of magnitude" (nguyên văn abstract). Kết luận thời đó: model lớn sample-efficient hơn, nên ưu tiên tăng tham số, dừng train trước khi hội tụ.

**Hoffmann et al. 2022 — "Chinchilla" (arXiv 2203.15556):** đo lại kỹ hơn và sửa kết luận trên: "for compute-optimal training, the model size and the number of training tokens should be scaled equally" (nguyên văn abstract) — tức đa số model đời trước bị **thiếu token** so với kích thước. Bằng chứng trong paper (Table 1, kiểm bản HTML ar5iv 2026-08-16): Chinchilla 70B tham số / 1.4T token — chia ra đúng **20 token/tham số** (số học, tự kiểm); Table 3 chiếu 67B → 1.5T token ≈ 22 token/tham số. Lưu ý paper **không phát biểu** con số "20 token/param" thành quy tắc — đó là tỷ lệ cộng đồng rút ra từ các bảng trên, và nó chỉ đúng quanh vùng compute paper đã fit.

**Áp vào chính tuần này** (số học, tự kiểm):

```
GPT-2-small:  124M tham số × ~20 token/tham số ≈ 2.5B token  (mốc Chinchilla-optimal)
llm.c #481:   train 124M trên 10B token FineWeb (nguyên văn discussion, kiểm 2026-08-16)
              → 10B / 124M ≈ 81 token/tham số — gấp ~4× mốc Chinchilla
```

Nghĩa là run tham chiếu của tuần này là **"over-token"** theo chuẩn Chinchilla. [Suy luận] Vì sao vẫn hợp lý: Chinchilla-optimal chỉ tối ưu loss **cho một budget compute train cố định**; nếu thứ bạn quan tâm là chất lượng của model nhỏ khi **inference** (chạy được trên máy yếu), train quá mốc vẫn tiếp tục hạ loss — trả thêm compute lúc train để đổi lấy model nhỏ mà tốt hơn. Đây là diễn giải từ chính power law của Kaplan (loss vẫn giảm theo data khi chưa hội tụ), không phải khẳng định của riêng paper nào về run 10B token này.

Bài học thực dụng khi đọc README các model đời nay: thấy "8B params, 15T tokens" đừng thắc mắc "sao train lố thế" — họ cố ý over-train vì tối ưu chi phí inference, không phải tối ưu compute train theo Chinchilla.

## 10. Data curation & dedup — làm thật trước khi train

Mua GPU giờ mới là nửa việc; nửa kia là **dữ liệu cho GPU ăn**. Paper FineWeb (PDF local, xem bảng Nguồn; đọc bản PDF ngày 2026-08-16) dành hẳn các mục 3.4–3.6 để ablate từng quyết định lọc/dedup — hiếm tài liệu mở nào kể kỹ như vậy.

**Vì sao dedup quan trọng — và không phải "càng dedup càng tốt".** FineWeb §3.4: dedup MinHash **toàn cục** trên cả 96 snapshot loại tới 90% dữ liệu ở các snapshot cũ nhưng model "showed little improvement over a model trained on the non-deduplicated data" (nguyên văn); kiểm tra lại thì phần dữ liệu bị giữ lại của snapshot cũ "contains more ads, incoherent lists of keywords and generally badly formatted text" hơn phần bị loại. Chuyển sang dedup **từng snapshot độc lập** thì điểm benchmark mới cải thiện (Fig. 5). Bài học: dedup là để loại các **cụm trùng lặp khổng lồ**, không phải để vắt kiệt mọi cặp na ná nhau.

**Exact vs near-dup:**
- *Exact dup*: hai document giống hệt nhau sau chuẩn hóa (lowercase, gộp whitespace) → bắt bằng **hash** (SHA-256 trên văn bản chuẩn hóa), chi phí O(n).
- *Near-dup*: cùng nội dung nhưng lệch vài câu (boilerplate, ngày tháng, template) — hash thường bó tay, cần đo **độ giống tập hợp** (Jaccard trên các shingle).

**MinHash intuition:** so Jaccard trực tiếp mọi cặp document thì quá đắt. Thay vào đó, băm mỗi shingle qua n hàm hash; với mỗi hàm, chỉ giữ **giá trị nhỏ nhất** trên toàn document → được signature n số. Tính chất then chốt: xác suất hai document cho cùng min-value ở một hàm hash **bằng đúng Jaccard** của hai tập shingle — nên tỷ lệ vị trí trùng nhau trong signature là ước lượng Jaccard. FineWeb §3.4 dùng 5-gram (mức từ), 112 hàm hash chia 14 bucket × 8, "targeting documents that are at least 75% similar" (nguyên văn).

**Quality filter heuristic** (FineWeb §3.6 — 3 filter sống sót sau ablation, kèm ngưỡng): loại document có tỷ lệ dòng kết thúc bằng dấu câu ≤ 0.12; tỷ lệ ký tự nằm trong các dòng lặp ≥ 0.1; tỷ lệ dòng ngắn hơn 30 ký tự ≥ 0.67. Cách họ tìm ngưỡng: so **histogram** của metric trên tập "chất lượng cao" vs "thấp" rồi chọn điểm cắt — không phải số thiêng, sang ngôn ngữ/miền khác phải tự tune lại.

**Làm thật:** [`05_data_dedup.py`](05_data_dedup.py) — pipeline mini đủ 3 tầng (exact dedup → MinHash near-dedup → quality filter) trên file text bất kỳ hoặc mẩu FineWeb-Edu, in số giữ/loại từng bước. Làm **trước** khi thuê cloud: lọc data chính là bước đầu của pretraining thật.

## 11. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| karpathy/nanoGPT (`train.py`, MIT) | https://github.com/karpathy/nanoGPT | 3, 4, 5, 6 |
| Penedo et al. 2024 — The FineWeb Datasets (CC BY 4.0, kiểm 2026-08-12; §3.4–3.6 đọc lại từ PDF 2026-08-16) | https://arxiv.org/abs/2406.17557 — PDF local: [`../docs/papers/2406.17557_fineweb-datasets.pdf`](../docs/papers/2406.17557_fineweb-datasets.pdf) | 8, 10 |
| Kaplan et al. 2020 — Scaling Laws for Neural Language Models (abstract kiểm 2026-08-16) | https://arxiv.org/abs/2001.08361 | 9 |
| Hoffmann et al. 2022 — Training Compute-Optimal Large Language Models (abstract + ar5iv kiểm 2026-08-16) | https://arxiv.org/abs/2203.15556 | 9 |
| karpathy/llm.c Discussion #481 — "Reproduce GPT-2 124M" (kiểm 2026-08-16) | https://github.com/karpathy/llm.c/discussions/481 | 9 |

(llm.c Discussion #481 và HF Ultra-Scale Playbook: link trong README nguồn học — nội dung chi phí/thời gian trong đó là **ảnh chụp thời điểm viết**, kiểm tra lại giá trước khi thuê máy.)

## Sau khi đọc xong

1. Điền TODO trong [`02_train_loop.py`](02_train_loop.py): loss → split/eval → schedule → clip → autocast → accumulation → checkpoint (đúng thứ tự đó, chạy được từng tầng rồi mới thêm tầng sau).
2. Smoke test local trên text public-domain nhỏ — bằng chứng: loss giảm qua các step, ghi số vào nhật ký.
3. Điền TODO trong [`05_data_dedup.py`](05_data_dedup.py) (mục 10) và chạy trên một file text nhỏ — thấy số giữ/loại từng bước, làm trước cloud run.
4. Chuẩn bị cloud run theo [`03_cloud_run_notes.md`](03_cloud_run_notes.md); train thật; viết [`04_loss_analysis.md`](04_loss_analysis.md) so với GPT-2.
5. Tự tính lại hai phép chia của mục 9 (2.5B và ~81 token/tham số) và đối chiếu với số token bạn thật sự train — biết mình đang ở đâu trên trục Chinchilla.
6. Làm [`quiz.md`](quiz.md); mục nâng cao D/F/H đọc sau khi loop chạy được.
