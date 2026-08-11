# Tuần 1 — Đáp án & Giải thích: Toán nền tảng + PyTorch

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Một nn.Linear(in, out) thực chất tính gì?

- **A.** y = x @ W + b với W có shape (in, out)
- **B.** y = x @ W^T + b với W lưu shape (out, in) ✅
- **C.** y = W @ x luôn luôn, không có bias
- **D.** y = softmax(x @ W)

**Đáp án: B**

**Giải thích:** PyTorch lưu weight shape (out, in), nên forward là y = x @ W^T + b. Đây là khối tuyến tính cơ bản lặp lại khắp transformer.

## Câu 2 (Trắc nghiệm)

Mục đích chính của softmax là gì?

- **A.** Chuẩn hoá vector về độ dài 1
- **B.** Biến một vector logits thành phân phối xác suất (mọi phần tử dương, tổng = 1) ✅
- **C.** Loại bỏ giá trị âm như ReLU
- **D.** Tính gradient của cross-entropy

**Đáp án: B**

**Giải thích:** softmax(z)_i = e^{z_i} / sum_j e^{z_j}: mũ hoá làm mọi giá trị dương, chia tổng làm chúng cộng lại bằng 1 → phân phối xác suất trên các lớp/token.

## Câu 3 (Tự luận)

Chain rule liên quan thế nào tới backpropagation?

**Trả lời mẫu:** Backprop = áp dụng chain rule lan ngược qua đồ thị tính toán. Đạo hàm của loss theo một tham số ở lớp sâu = tích các đạo hàm cục bộ dọc đường đi: dL/dw = dL/dg · dg/dw. Mỗi lớp chỉ cần biết đạo hàm cục bộ của nó và nhận gradient từ lớp sau, nhân vào, rồi truyền tiếp về trước.

**Giải thích:** Đây là toàn bộ ý tưởng của autograd: lưu đồ thị forward, rồi nhân dồn đạo hàm cục bộ theo chiều ngược lại.

## Câu 4 (Trắc nghiệm)

Cross-entropy loss L_CE = -sum_i y_i log(y_hat_i) đo điều gì?

- **A.** Khoảng cách Euclid giữa dự đoán và nhãn
- **B.** Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật — phạt nặng khi gán xác suất thấp cho lớp đúng ✅
- **C.** Số token dự đoán sai
- **D.** Phương sai của logits

**Đáp án: B**

**Giải thích:** Với nhãn one-hot, L_CE = -log(xác suất gán cho lớp đúng). Gán xác suất gần 1 cho lớp đúng → loss ~0; gần 0 → loss rất lớn.

## Câu 5 (Trắc nghiệm)

Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?

- **A.** (B, T, D) ✅
- **B.** (B, 1, D)
- **C.** Lỗi — không broadcast được
- **D.** (B, T, 1)

**Đáp án: A**

**Giải thích:** Broadcasting căn phải các chiều; chiều bằng 1 được 'kéo dài'. (B,1,D) và (1,T,D) → (B,T,D). Hiểu broadcasting là chìa khoá đọc code attention.

## Câu 6 (Tự luận)

torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?

**Trả lời mẫu:** requires_grad=True đánh dấu một tensor cần theo dõi để tính gradient (tham số train được). torch.no_grad() là context tắt việc xây đồ thị autograd cho mọi phép tính bên trong — dùng khi inference/đánh giá hoặc cập nhật tham số thủ công, để tiết kiệm bộ nhớ và tránh tính gradient thừa.

**Giải thích:** Quên no_grad() khi eval/generate là lỗi VRAM phổ biến, nhất là trên card 8GB.

## Câu 7 (Trắc nghiệm)

Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?

- **A.** Luôn là khoảng cách giữa hai điểm
- **B.** Độ 'cùng hướng' / tương đồng — lớn khi hai vector cùng hướng ✅
- **C.** Góc tuyệt đối tính bằng độ
- **D.** Tổng bình phương các phần tử

**Đáp án: B**

**Giải thích:** a·b = |a||b|cosθ. Trong attention, query·key chính là điểm tương đồng dùng để quyết định token nào 'chú ý' tới token nào.
