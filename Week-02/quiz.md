# Tuần 2 — Quiz: Backprop từ đầu + mental model Transformer

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Trong micrograd, mỗi đối tượng Value lưu những gì và làm gì khi backward()?

## Câu 2 (Trắc nghiệm)

backward() duyệt đồ thị theo thứ tự nào?

- **A.** Thứ tự ngẫu nhiên
- **B.** Thứ tự topo NGƯỢC (từ output về input)
- **C.** Theo thứ tự khởi tạo biến
- **D.** Theo độ lớn của grad

## Câu 3 (Tự luận)

Vì sao self-attention là 'permutation-equivariant' và điều đó buộc ta phải thêm gì?

## Câu 4 (Trắc nghiệm)

Đạo hàm của tanh(x) là gì (hay gặp khi tự code backward)?

- **A.** tanh(x)
- **B.** 1 - tanh^2(x)
- **C.** x(1-x)
- **D.** e^x / (1+e^x)

## Câu 5 (Trắc nghiệm)

Khi một biến được dùng ở NHIỀU nhánh của đồ thị, gradient của nó được xử lý thế nào?

- **A.** Lấy gradient lớn nhất
- **B.** Cộng dồn (+=) gradient từ tất cả các nhánh
- **C.** Ghi đè bằng gradient cuối cùng
- **D.** Lấy trung bình

## Câu 6 (Tự luận)

Bigram model trong makemore làm gì, và liên hệ thế nào với một mạng neural 1 lớp?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
