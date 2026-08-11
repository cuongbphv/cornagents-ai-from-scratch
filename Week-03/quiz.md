# Tuần 3 — Quiz: Tokenization, embeddings, attention từ đầu

> Tự kiểm tra **trước** khi xem solution. Tổng **7** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Vì sao trong scaled dot-product attention ta chia cho sqrt(d_k)?

- **A.** Để tiết kiệm bộ nhớ
- **B.** Để chuẩn hoá vector về độ dài 1
- **C.** Để giữ phương sai của score ổn định, tránh softmax bão hoà làm gradient triệt tiêu
- **D.** Để score luôn dương

## Câu 2 (Tự luận)

Causal mask làm gì và cài đặt thế nào?

## Câu 3 (Trắc nghiệm)

Token embedding và positional embedding được kết hợp thế nào trong GPT-2?

- **A.** Nối (concatenate) lại
- **B.** Cộng vào nhau (cùng chiều d_model)
- **C.** Nhân element-wise
- **D.** Chỉ dùng token embedding

## Câu 4 (Trắc nghiệm)

Ma trận attention scores (trước khi nhân V) có shape nào với input (batch, seq, d)?

- **A.** (batch, seq, d)
- **B.** (batch, seq, seq)
- **C.** (batch, d, d)
- **D.** (seq, seq)

## Câu 5 (Tự luận)

[Nâng cao] RoPE khác với positional embedding tuyệt đối của GPT-2 thế nào?

## Câu 6 (Trắc nghiệm)

[Nâng cao] Mục đích chính của Grouped-Query Attention (GQA) so với Multi-Head Attention?

- **A.** Tăng số head để chính xác hơn
- **B.** Cho các nhóm head chia sẻ chung K,V để GIẢM kích thước KV cache khi inference
- **C.** Bỏ hoàn toàn key và value
- **D.** Thay softmax bằng sigmoid

## Câu 7 (Trắc nghiệm)

[Nâng cao] Độ phức tạp bộ nhớ/tính toán của self-attention thường (full) theo độ dài seq n là?

- **A.** O(n)
- **B.** O(n log n)
- **C.** O(n^2)
- **D.** O(1)

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
