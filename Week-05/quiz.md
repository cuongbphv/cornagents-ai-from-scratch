# Tuần 5, Quiz: Backprop từ đầu + mental model Transformer

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

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

## Câu 7 (Tự luận)

Bạn vừa điền xong _backward cho các phép trong micrograd nhưng chưa muốn phụ thuộc PyTorch để kiểm. Hãy mô tả cách dùng sai phân trung tâm của Tuần 2 để kiểm gradient của một Value, và nói vì sao nên kiểm bằng cách này trước khi chạy 03_check_grad.py.

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Backward của micrograd duyệt đồ thị theo thứ tự topo đảo ngược. Vì sao thứ tự này là bắt buộc, không chỉ là tiện?

- **A.** Vì Python yêu cầu duyệt tập hợp theo thứ tự
- **B.** Vì khi một node phát gradient xuống toán hạng, gradient của chính nó phải đã được cộng đủ từ mọi nhánh phía trên; thứ tự topo đảo ngược bảo toàn điều đó
- **C.** Vì thứ tự topo giúp giảm bộ nhớ
- **D.** Vì tanh chỉ khả vi theo thứ tự đó

## Nâng cao 2 (Tự luận)

Weight tying trong nanoGPT gán wte.weight = lm_head.weight. Hãy giải thích ảnh hưởng lên số tham số và lên gradient của ma trận embedding.

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
