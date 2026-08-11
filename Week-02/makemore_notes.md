# makemore — Khung ghi chú (Karpathy Lecture 2–4)

> makemore: model sinh tên ký tự-the-ký tự. Đi từ bigram (đếm) → neural net → MLP.
> Tự code theo video, ghi lại bằng lời mình. Chỗ TODO là phần điền sau khi làm.

## 0. Dữ liệu

- Dataset: file `names.txt` (~32k tên). Tải từ repo `karpathy/makemore`.
- Vocab: 26 chữ cái + token đặc biệt `.` (đánh dấu đầu/cuối tên).

## 1. Bigram model — phiên bản ĐẾM

Ý tưởng: `P(ký tự kế | ký tự hiện tại)` = đếm số lần cặp (a→b) xuất hiện, rồi chuẩn hóa.

- [ ] Xây ma trận đếm `N` shape `(27, 27)`.
- [ ] Chuẩn hóa từng hàng thành xác suất `P`.
- [ ] Sinh tên bằng cách sample từ `P`.
- [ ] Đánh giá bằng **negative log-likelihood** trung bình.

TODO ghi chú: NLL bạn đo được = ______ . Vì sao dùng NLL thay vì accuracy? ______

## 2. Bigram model — phiên bản NEURAL NET

Cùng bài toán nhưng học bằng gradient descent:

- [ ] One-hot encode ký tự input (shape `(N, 27)`).
- [ ] 1 lớp Linear: `logits = x @ W` với `W` shape `(27, 27)`.
- [ ] `softmax(logits)` → xác suất.
- [ ] Loss = cross-entropy (≈ NLL). Train bằng gradient descent.
- [ ] Kiểm chứng: loss của net hội tụ về ≈ loss của bản đếm.

TODO: tại sao 2 cách lại cho loss gần nhau? ______

## 3. MLP (theo Bengio 2003)

Mở rộng context: dùng **nhiều** ký tự trước để dự đoán ký tự kế.

- [ ] `block_size` (vd. 3): nhìn 3 ký tự để đoán ký tự thứ 4.
- [ ] **Embedding** mỗi ký tự thành vector (vd. 10 chiều) → lookup table `C`.
- [ ] Nối các embedding, qua hidden layer (tanh), rồi output 27 logits.
- [ ] Train minibatch + theo dõi loss train/val.
- [ ] Thử learning rate khác nhau (tìm "thung lũng" lr tốt).

TODO: embedding khác one-hot ở điểm nào? Vì sao tốt hơn khi vocab lớn? ______

## 4. Liên hệ tới LLM (preview)

- Embedding ở đây = **token embedding** trong GPT (Tuần 3–4).
- Dự đoán ký tự kế = bản thu nhỏ của **next-token prediction** — chính là pretraining (Tuần 5).
- MLP + phi tuyến chính là **feed-forward block** trong transformer.

## 5. Tự kiểm tra (nhờ Claude quiz)

- [ ] Vì sao cần token `.` đầu/cuối?
- [ ] Cross-entropy quan hệ thế nào với NLL?
- [ ] Embedding lookup thực chất là phép toán gì? (gợi ý: nhân one-hot với ma trận)
- [ ] Vì sao mở rộng context (block_size) giúp model tốt hơn nhưng tốn hơn?
