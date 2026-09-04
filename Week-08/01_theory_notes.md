# Lý thuyết Tuần 8: Pretraining: loop, schedule, precision, checkpoint

> Đọc trước khi điền TODO trong [`02_train_loop.py`](02_train_loop.py). Số liệu kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11; nguồn cuối file. Cần nắm training loop 5 bước (Tuần 4) và GPT model (Tuần 7).

---

## 1. Pretraining loop = loop Tuần 4 + dữ liệu ở quy mô khác

Bài toán duy nhất: **đoán token kế tiếp**. Với batch `(B, T)`, model cho logits `(B, T, V)`; cross-entropy tính trên **mọi vị trí** cùng lúc (mỗi vị trí i có nhãn là token i+1, sliding window Tuần 6). Không cần nhãn tay, "nhãn" chính là văn bản.

```python
logits = model(xb)                                    # (B, T, V)
loss = F.cross_entropy(logits.flatten(0, 1), yb.flatten())
```

**Perplexity** = `exp(loss)`: loss 3.5 → PPL ≈ 33.1 ("phân vân giữa ~33 lựa chọn"); loss 0 → PPL 1 (kiểm chứng 2026-08-11). Mốc so sánh trong README: GPT-2 gốc loss ~3.5 trên miền dữ liệu tương đương.

## 2. Train/val split: biết mình đang học hay đang thuộc lòng

Cắt corpus thành train/val (ví dụ 90/10), đo val loss định kỳ. Train loss giảm mà val loss tăng = memorize. Lưu ý pretrain 1-epoch trên corpus lớn hầu như không kịp overfit, đó là lý do nanoGPT để dropout 0 khi pretrain (mục nâng cao D).

## 3. LR schedule: warmup + cosine decay

```
it < warmup:  lr = max_lr · (it+1)/warmup            (tăng tuyến tính)
sau đó:       lr = min_lr + 0.5·(1+cos(π·tiến_độ))·(max_lr − min_lr)
```

Giá trị kiểm chứng với `max_lr=6e-4, min_lr=6e-5, warmup=100, max_it=1000`: it=0 → 6.0e-6; it=100 → 6.0e-4 (đỉnh); it=550 → 3.3e-4 (lưng chừng cosine); it=1000 → 6.0e-5 (đáy). [Suy luận] Warmup giúp tránh bước cập nhật quá lớn khi các thống kê moment của AdamW chưa ổn định ở những step đầu, lập luận phổ biến, hiệu quả cụ thể phải nhìn loss curve của chính bạn.

## 4. Gradient clipping: cầu chì chống loss spike

Chặn **norm toàn cục** của gradient về ngưỡng (thường 1.0), giữ nguyên hướng:

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
```

Kiểm chứng: gradient `[30, 40]` (norm 50) sau clip thành `[0.6, 0.8]` (norm 1.0): cùng hướng, ngắn lại. Gọi **sau** `backward()`, **trước** `step()`.

## 5. Mixed precision: vì sao bf16 là mặc định thời nay

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

## 6. Gradient accumulation: batch to trên VRAM nhỏ

Effective batch (token/update) = `micro_batch × seq_len × accum_steps`. Mục tiêu README ~524,288 token/update: với micro-batch 1 × seq 1024 → cần **512** accum steps; micro-batch 2 → 256 (số học, tự kiểm). Cách làm: cộng dồn `loss/accum_steps` qua `backward()` nhiều lần, `step()` + `zero_grad()` mỗi `accum_steps` lần, chính là tận dụng tính chất grad **cộng dồn** đã học ở Tuần 5.

## 7. Checkpointing: không mất công train vì một lần rớt điện/cloud

Lưu đủ 3 thứ mới resume đúng: `model.state_dict()`, `optimizer.state_dict()` (AdamW mang 2 giá trị moment cho MỖI tham số, thiếu nó resume sẽ khựng), và `step` (để LR schedule tiếp đúng chỗ). Lưu định kỳ + giữ bản `best_val`. Nguyên tắc chạy cloud: **smoke test local vài trăm step xác nhận loss giảm rồi mới thuê máy**: xem [`03_cloud_run_notes.md`](03_cloud_run_notes.md).

## 8. Tiếng Việt trong tuần này

- **Model chỉ biết ngôn ngữ có trong corpus pretrain.** FineWeb/FineWeb-Edu trong task tuần này thiên tiếng Anh, model bạn pretrain ra sẽ không đọc được tiếng Việt, và đó là kỳ vọng đúng. Nhân tiện, paper FineWeb (PDF trong repo, xem bảng Nguồn) đáng một buổi đọc: FineWeb là "a 15-trillion token dataset derived from 96 Common Crawl snapshots", FineWeb-Edu là subset giáo dục 1.3T token, và các tác giả tài liệu hóa từng quyết định lọc/dedup của mình, muốn biết một corpus web-scale được "nấu" ra sao thì hiếm chỗ nào kể kỹ hơn. Muốn có khả năng tiếng Việt phải có corpus Việt trong pretrain (hoặc dùng base đa ngôn ngữ rồi fine-tune, hướng của Tuần 11-12; nguồn corpus VN license sạch: xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md)).
- **Ngân sách token lệch theo ngôn ngữ:** cùng 1 GB văn bản, tiếng Việt sinh ra nhiều token hơn tiếng Anh với tokenizer thiên Anh (fertility đo ở Tuần 6) → "1B token" tiếng Việt chứa **ít nội dung hơn** 1B token tiếng Anh. Khi đọc bất kỳ báo cáo pretrain đa ngôn ngữ nào, hỏi ngay: token đếm bằng tokenizer nào?
- **So sánh chéo ngôn ngữ/tokenizer thì bỏ perplexity, dùng bits-per-byte** (mục nâng cao H): PPL phụ thuộc tokenizer, cùng một văn bản, tokenizer khác nhau cho PPL khác nhau dù model "giỏi" như nhau; bits-per-byte chuẩn hóa theo byte nên so được.

## 9. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| karpathy/nanoGPT (`train.py`, MIT) | https://github.com/karpathy/nanoGPT | 3, 4, 5, 6 |
| Penedo et al. 2024, The FineWeb Datasets (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2406.17557, PDF local: [`../docs/papers/2406.17557_fineweb-datasets.pdf`](../docs/papers/2406.17557_fineweb-datasets.pdf) | 8 |

(llm.c Discussion #481 và HF Ultra-Scale Playbook: link trong README nguồn học, nội dung chi phí/thời gian trong đó là **ảnh chụp thời điểm viết**, kiểm tra lại giá trước khi thuê máy.)

## Sau khi đọc xong

1. Điền TODO trong [`02_train_loop.py`](02_train_loop.py): loss → split/eval → schedule → clip → autocast → accumulation → checkpoint (đúng thứ tự đó, chạy được từng tầng rồi mới thêm tầng sau).
2. Smoke test local trên text public-domain nhỏ, bằng chứng: loss giảm qua các step, ghi số vào nhật ký.
3. Chuẩn bị cloud run theo [`03_cloud_run_notes.md`](03_cloud_run_notes.md); train thật; viết [`04_loss_analysis.md`](04_loss_analysis.md) so với GPT-2.
4. Làm [`quiz.md`](quiz.md); mục nâng cao D/F/H đọc sau khi loop chạy được.

## 10. Entropy, perplexity, scaling law và cách đọc loss curve

Mục này gom ba câu hỏi người pretrain lần đầu hay gặp: perplexity thực ra là gì, loss giảm đến đâu thì dừng, và vì sao model lớn hơn với dữ liệu nhiều hơn lại tốt hơn.

**Từ entropy đến perplexity.** SLP3 mục 3.7 (trang 85) cho định nghĩa entropy của biến ngẫu nhiên X trên tập χ với phân phối p: H(X) = −Σ p(x) log₂ p(x) (eq. 3.32), đo bằng bit khi dùng log cơ số 2. Cách hiểu trực quan họ đưa: entropy là **cận dưới của số bit cần để mã hóa một quyết định** theo sơ đồ mã tối ưu, minh họa bằng ví dụ đặt cược tám con ngựa của Cover và Thomas. Perplexity "actually arises from the information-theoretic concept of cross-entropy", và điều đó giải thích "otherwise mysterious properties of perplexity", như vì sao lại là nghịch đảo xác suất. Nối với mục 1 ở trên: loss L của bạn là cross-entropy trung bình trên token tính bằng nat, nên PPL = e^L; nếu tính bằng bit thì PPL = 2^H. Bits per byte ở mục nâng cao H chỉ là cùng con số chia cho số byte thay vì số token, để so được hai model dùng tokenizer khác nhau (xem thí nghiệm fertility tiếng Việt ở Tuần 6).

**Đọc loss curve bằng khung train, validation, test.** Fleuret mô tả protocol chuẩn (*Little Book* mục 3.6, trang 47): training set để tối ưu tham số, test set để đánh giá, và một validation set tách rời cả hai để chọn siêu tham số (kiến trúc, learning rate, hệ số regularization). Động học thường thấy: **training loss giảm chừng nào optimizer còn chạy, còn validation loss có thể đạt cực tiểu sau một số epoch rồi tăng lại**, đó là dấu hiệu overfitting. [Suy luận] Với lần pretrain của tuần này trên một mẫu FineWeb-Edu, số token chạy qua nhỏ hơn kích thước mẫu nên bạn khó thấy nhánh tăng; nhưng khi smoke test local trên text nhỏ, bạn sẽ thấy nó rõ, và đó là cơ hội tốt để tập nhận diện trước khi đốt tiền cloud. Ghi cả hai đường vào `04_loss_analysis.md`, không chỉ đường train.

**Scaling law.** Xiao và Zhu (*Foundations of LLMs* mục 2.2.4, trang 63) tóm lại: scaling law mô tả quan hệ giữa hiệu năng và các thuộc tính của training như kích thước model, lượng compute và lượng dữ liệu. Họ dẫn Hestness et al. 2017: hiệu năng là hàm dạng power-law của lượng dữ liệu, với ba pha, cải thiện chậm khi dữ liệu còn ít, rồi nhanh, rồi chậm lại. Họ cũng ghi rằng quan điểm truyền thống trong NLP cho rằng lợi ích sẽ biến mất khi scale đủ lớn, nhưng kết quả gần đây cho thấy cả model đóng và mở "can benefit from more data, even though trillions of tokens have already been used for training". Fleuret nói gọn cùng ý (mục 3.7, trang 51) và dẫn Kaplan et al. 2020. Hai paper Scaling Laws và Chinchilla trong kệ paper là nguồn gốc của các con số; mục này chỉ để bạn đặt lần chạy 124M của mình vào đúng chỗ trên đường cong: rất nhỏ, và mục tiêu là hiểu cơ chế, không phải đuổi số.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **Perplexity định nghĩa từ đâu.** SLP3 mục 3.3 (trang 76) giải thích vì sao không dùng xác suất thô của tập test: "the probability of a test set gets smaller the longer the text. It's useful to have a metric that is per-word, normalized by length", và perplexity là hàm của xác suất chuẩn hóa đó, dùng cho cả n-gram và LLM. Mục 3.7 (trang 85) nối perplexity với entropy, cùng ý với bits per byte ở mục nâng cao H. MacKay chương 4 Source Coding Theorem là nền lý thuyết của phép nối đó.
- **Pretraining là self-supervised.** SLP3 mục 7.7 (trang 201): "We call such a model self-supervised because we don't have to add any special gold labels to the data; the natural sequence of words is its own supervision!" Loss là cross-entropy trên vocab, eq. 7.53, đúng loss trong `02_train_loop.py`.
- **Scale.** Fleuret mục 3.7 (trang 51): hiệu năng "improves with the amount of data according to remarkable scaling laws, as long as the model size increases correspondingly [Kaplan et al., 2020]". Xiao và Zhu, *Foundations of LLMs* mục 2.2 Training at Scale (trang 56): pre-training có thể cần "trillions of tokens" (Table 2.3 của sách), nhưng "larger training datasets do not mean better training results"; mục 2.2.1 bàn chuẩn bị dữ liệu, cùng câu hỏi với paper FineWeb trong kệ paper.
- **Regularization và optimization ở mạng sâu.** Prince, UDL 9.2 Implicit regularization (trang 141); Goodfellow chương 8 Optimization for Training Deep Models (HTML).
