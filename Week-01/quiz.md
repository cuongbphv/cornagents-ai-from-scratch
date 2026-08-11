# Tuần 1 — Quiz: Toán nền tảng + PyTorch

> Tự kiểm tra **trước** khi xem solution. Tổng **7** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

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
- **B.** Độ 'bất ngờ' của phân phối dự đoán so với nhãn thật — phạt nặng khi gán xác suất thấp cho lớp đúng
- **C.** Số token dự đoán sai
- **D.** Phương sai của logits

## Câu 5 (Trắc nghiệm)

Cộng tensor shape (B, 1, D) với (1, T, D) bằng broadcasting cho ra shape nào?

- **A.** (B, T, D)
- **B.** (B, 1, D)
- **C.** Lỗi — không broadcast được
- **D.** (B, T, 1)

## Câu 6 (Tự luận)

torch.no_grad() và requires_grad khác nhau thế nào, dùng khi nào?

## Câu 7 (Trắc nghiệm)

Dot product giữa hai vector đo điều gì (ý nghĩa cho attention)?

- **A.** Luôn là khoảng cách giữa hai điểm
- **B.** Độ 'cùng hướng' / tương đồng — lớn khi hai vector cùng hướng
- **C.** Góc tuyệt đối tính bằng độ
- **D.** Tổng bình phương các phần tử

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
