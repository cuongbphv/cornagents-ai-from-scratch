# Tuần 4, Đáp án & Giải thích: PyTorch core: từ NumPy sang tensor, autograd, training loop

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Một nn.Linear(in, out) thực chất tính gì?

- **A.** y = W @ x luôn luôn, không có bias
- **B.** y = x @ W + b với W có shape (in, out)
- **C.** y = softmax(x @ W)
- **D.** y = x @ W^T + b với W lưu shape (out, in) (đáp án đúng)

**Đáp án: D**

**Giải thích:** PyTorch lưu weight shape (out, in), nên forward là y = x @ W^T + b. Đây là khối tuyến tính cơ bản lặp lại khắp transformer.

## Câu 2 (Trắc nghiệm)

Mục đích chính của softmax là gì?

- **A.** Tính gradient của cross-entropy
- **B.** Biến một vector logits thành phân phối xác suất (mọi phần tử dương, tổng = 1) (đáp án đúng)
- **C.** Loại bỏ giá trị âm như ReLU
- **D.** Chuẩn hoá vector về độ dài 1

**Đáp án: B**

**Giải thích:** softmax(z)_i = e^{z_i} / sum_j e^{z_j}: mũ hoá làm mọi giá trị dương, chia tổng làm chúng cộng lại bằng 1 → phân phối xác suất trên các lớp/token.

## Câu 3 (Tự luận)

Chain rule liên quan thế nào tới backpropagation?

**Trả lời mẫu:** Backprop = áp dụng chain rule lan ngược qua đồ thị tính toán. Đạo hàm của loss theo một tham số ở lớp sâu = tích các đạo hàm cục bộ dọc đường đi: dL/dw = dL/dg · dg/dw. Mỗi lớp chỉ cần biết đạo hàm cục bộ của nó và nhận gradient từ lớp sau, nhân vào, rồi truyền tiếp về trước.

**Giải thích:** Đây là toàn bộ ý tưởng của autograd: lưu đồ thị forward, rồi nhân dồn đạo hàm cục bộ theo chiều ngược lại.

## Câu 4 (Trắc nghiệm)

Cross-entropy loss L_CE = -sum_i y_i log(y_hat_i) đo điều gì?

- **A.** Phương sai của logits
- **B.** Số token dự đoán sai
- **C.** Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật, phạt nặng khi gán xác suất thấp cho lớp đúng (đáp án đúng)
- **D.** Khoảng cách Euclid giữa dự đoán và nhãn

**Đáp án: C**

**Giải thích:** Với nhãn one-hot, L_CE = -log(xác suất gán cho lớp đúng). Gán xác suất gần 1 cho lớp đúng → loss ~0; gần 0 → loss rất lớn.

## Câu 5 (Trắc nghiệm)

Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?

- **A.** (B, 1, D)
- **B.** (B, T, 1)
- **C.** (B, T, D) (đáp án đúng)
- **D.** Lỗi, không broadcast được

**Đáp án: C**

**Giải thích:** Broadcasting căn phải các chiều; chiều bằng 1 được 'kéo dài'. (B,1,D) và (1,T,D) → (B,T,D). Hiểu broadcasting là chìa khoá đọc code attention.

## Câu 6 (Tự luận)

torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?

**Trả lời mẫu:** requires_grad=True đánh dấu một tensor cần theo dõi để tính gradient (tham số train được). torch.no_grad() là context tắt việc xây đồ thị autograd cho mọi phép tính bên trong, dùng khi inference/đánh giá hoặc cập nhật tham số thủ công, để tiết kiệm bộ nhớ và tránh tính gradient thừa.

**Giải thích:** Quên no_grad() khi eval/generate là lỗi VRAM phổ biến, nhất là trên card 8GB.

## Câu 7 (Trắc nghiệm)

Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?

- **A.** Độ 'cùng hướng' / tương đồng, lớn khi hai vector cùng hướng (đáp án đúng)
- **B.** Góc tuyệt đối tính bằng độ
- **C.** Tổng bình phương các phần tử
- **D.** Luôn là khoảng cách giữa hai điểm

**Đáp án: A**

**Giải thích:** a·b = |a||b|cosθ. Trong attention, query·key chính là điểm tương đồng dùng để quyết định token nào 'chú ý' tới token nào.

## Câu 8 (Tự luận)

Ở Tuần 3 bạn viết logistic regression bằng NumPy với hàm grad tự tính và kiểm bằng sai phân. Khi viết lại bằng PyTorch, dòng nào thay cho hàm grad, dòng nào thay cho phép cập nhật w -= lr * grad, và vì sao xuất hiện thêm bước zero_grad() mà vòng lặp NumPy không cần?

**Trả lời mẫu:** loss.backward() thay cho hàm grad: autograd áp chain rule ngược trên đồ thị tính toán và điền vào .grad của từng tham số. optimizer.step() thay cho w -= lr * grad, với lr là step size. Bước zero_grad() cần vì PyTorch cộng dồn gradient vào .grad qua các lần backward (thiết kế phục vụ gradient accumulation); vòng lặp NumPy tính gradient mới mỗi lần nên không có gì để xóa. Cách kiểm bằng sai phân của Tuần 2 vẫn dùng được để đối chiếu .grad.

**Giải thích:** Đây là toàn bộ 'phần mới' của Tuần 4: đổi công cụ, không đổi toán. Nếu bạn chỉ ra được ba dòng này thì đã nối xong Phase 0 với PyTorch.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

nanoGPT đặt dropout = 0.0 cho pretraining với comment 'for pretraining 0 is good, for finetuning try 0.1+'. Khung nào của Tuần 3 giải thích lựa chọn này?

- **A.** Dropout chỉ hoạt động với LayerNorm
- **B.** Dropout không tương thích với bf16
- **C.** Dropout làm chậm GPU nên bỏ khi có nhiều dữ liệu
- **D.** Pretraining chạy trên dữ liệu rất lớn, thường dưới một epoch, nên estimation error nhỏ và regularization kiểu dropout ít cần; fine-tune trên dữ liệu nhỏ dễ overfit nên cần regularization hơn (đáp án đúng)

**Đáp án: D**

**Giải thích:** Giá trị đọc từ nanoGPT/train.py ngày 2026-09-04. Lý giải theo error decomposition của UML mục 5.2 là suy luận của người viết dựa trên khung lý thuyết, không phải kết luận trong code.

## Nâng cao 2 (Tự luận)

Vì sao PyTorch cộng dồn gradient vào .grad thay vì ghi đè, và kỹ thuật nào trong nanoGPT dựa trực tiếp vào hành vi đó?

**Trả lời mẫu:** Cộng dồn cho phép gọi backward nhiều lần trên nhiều micro-batch rồi mới step một lần, tức gradient accumulation; nanoGPT có gradient_accumulation_steps = 5 * 8 với comment 'used to simulate larger batch sizes'. Hệ quả là mỗi lần bắt đầu tích lũy phải zero_grad, còn micrograd Tuần 5 cũng phải dùng += trong _backward vì một node có thể được dùng ở nhiều nhánh.

**Giải thích:** Trên card 8GB, gradient accumulation là cách duy nhất đạt effective batch lớn; hiểu cơ chế cộng dồn giúp tránh lỗi quên zero_grad.
