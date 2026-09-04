# Tuần 4, Quiz: PyTorch core: từ NumPy sang tensor, autograd, training loop

> Tự kiểm tra **trước** khi xem solution. Tổng **10** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Một nn.Linear(in, out) thực chất tính gì?

- **A.** y = x @ W + b với W có shape (in, out)
- **B.** y = x @ W^T + b với W lưu shape (out, in)
- **C.** y = W @ x luôn luôn, không có bias
- **D.** y = softmax(x @ W)

## Câu 2 (Trắc nghiệm)

Mục đích chính của softmax là gì?

- **A.** Chuẩn hoá vector về độ dài 1
- **B.** Biến một vector logits thành phân phối xác suất (mọi phần tử dương, tổng = 1)
- **C.** Loại bỏ giá trị âm như ReLU
- **D.** Tính gradient của cross-entropy

## Câu 3 (Tự luận)

Chain rule liên quan thế nào tới backpropagation?

## Câu 4 (Trắc nghiệm)

Cross-entropy loss L_CE = -sum_i y_i log(y_hat_i) đo điều gì?

- **A.** Khoảng cách Euclid giữa dự đoán và nhãn
- **B.** Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật, phạt nặng khi gán xác suất thấp cho lớp đúng
- **C.** Số token dự đoán sai
- **D.** Phương sai của logits

## Câu 5 (Trắc nghiệm)

Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?

- **A.** (B, T, D)
- **B.** (B, 1, D)
- **C.** Lỗi, không broadcast được
- **D.** (B, T, 1)

## Câu 6 (Tự luận)

torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?

## Câu 7 (Trắc nghiệm)

Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?

- **A.** Luôn là khoảng cách giữa hai điểm
- **B.** Độ 'cùng hướng' / tương đồng, lớn khi hai vector cùng hướng
- **C.** Góc tuyệt đối tính bằng độ
- **D.** Tổng bình phương các phần tử

## Câu 8 (Tự luận)

Ở Tuần 3 bạn viết logistic regression bằng NumPy với hàm grad tự tính và kiểm bằng sai phân. Khi viết lại bằng PyTorch, dòng nào thay cho hàm grad, dòng nào thay cho phép cập nhật w -= lr * grad, và vì sao xuất hiện thêm bước zero_grad() mà vòng lặp NumPy không cần?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

nanoGPT đặt dropout = 0.0 cho pretraining với comment 'for pretraining 0 is good, for finetuning try 0.1+'. Khung nào của Tuần 3 giải thích lựa chọn này?

- **A.** Dropout làm chậm GPU nên bỏ khi có nhiều dữ liệu
- **B.** Pretraining chạy trên dữ liệu rất lớn, thường dưới một epoch, nên estimation error nhỏ và regularization kiểu dropout ít cần; fine-tune trên dữ liệu nhỏ dễ overfit nên cần regularization hơn
- **C.** Dropout chỉ hoạt động với LayerNorm
- **D.** Dropout không tương thích với bf16

## Nâng cao 2 (Tự luận)

Vì sao PyTorch cộng dồn gradient vào .grad thay vì ghi đè, và kỹ thuật nào trong nanoGPT dựa trực tiếp vào hành vi đó?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
