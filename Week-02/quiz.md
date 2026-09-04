# Tuần 2, Quiz: Giải tích vector, xác suất, tối ưu hóa

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Với hàm f(x₁, x₂) = x₁²x₂ + x₁x₂³, gradient tại điểm (1, 2) bằng bao nhiêu?

- **A.** [4, 13]
- **B.** [12, 13]
- **C.** [12, 7]
- **D.** [5, 9]

## Câu 2 (Tự luận)

Hãy mô tả cách bạn kiểm tra một công thức gradient bằng số, và giải thích vì sao kỹ thuật này sẽ hữu ích ở Tuần 5 khi tự viết autograd.

## Câu 3 (Trắc nghiệm)

Một bệnh có tỉ lệ 1% trong dân số. Xét nghiệm phát hiện đúng 95% người bệnh và báo dương tính giả ở 5% người khỏe. Một người nhận kết quả dương tính thì xác suất thực sự mắc bệnh gần với con số nào?

- **A.** Khoảng 95%
- **B.** Khoảng 50%
- **C.** Khoảng 16%
- **D.** Khoảng 1%

## Câu 4 (Trắc nghiệm)

Luật số lớn nói gì về loss tính trên một batch trong training, và điều đó giải thích hiện tượng nào trên loss curve?

- **A.** Loss trên batch luôn bằng loss kỳ vọng, nên loss curve phải trơn
- **B.** Loss trên batch là trung bình mẫu của loss kỳ vọng, có phương sai tỉ lệ với 1/n, nên batch nhỏ cho loss curve nhấp nhô hơn batch lớn
- **C.** Loss trên batch không liên quan đến loss kỳ vọng vì dữ liệu không độc lập
- **D.** Loss trên batch chỉ hội tụ khi learning rate giảm về 0

## Câu 5 (Tự luận)

Vì sao cross-entropy loss được xem là negative log-likelihood, và vì sao người ta cực tiểu negative log-likelihood thay vì cực đại likelihood trực tiếp?

## Câu 6 (Trắc nghiệm)

Trên hàm f(x) = x² với đạo hàm 2x, chạy gradient descent từ x₀ = 5 với step size 1.1 thì điều gì xảy ra sau 20 bước, và vì sao?

- **A.** Hội tụ về 0 vì hàm lồi nên mọi step size đều được
- **B.** Dao động quanh 0 với biên độ không đổi
- **C.** Phân kỳ, vì mỗi bước nhân x với (1 − 2 × 1.1) = −1.2 nên trị tuyệt đối tăng theo cấp số nhân
- **D.** Dừng ngay tại x = 5 vì gradient bằng 0

## Câu 7 (Trắc nghiệm)

Theo MacKay (ITILA eq. 2.45-2.46), relative entropy D_KL(P‖Q) luôn không âm và chỉ bằng 0 khi P = Q. Điều này nói gì về giá trị nhỏ nhất mà cross-entropy loss có thể đạt khi train một model?

- **A.** Cross-entropy có thể xuống 0 với mọi dữ liệu nếu train đủ lâu
- **B.** Cross-entropy nhỏ nhất bằng entropy của phân phối dữ liệu, đạt được khi phân phối model trùng phân phối thật, vì cross-entropy = entropy + KL
- **C.** Cross-entropy không có đáy vì log không bị chặn
- **D.** Cross-entropy nhỏ nhất bằng KL divergence

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Theo RoFormer (arXiv 2104.09864) và cách MML định nghĩa góc giữa hai vector, vì sao xoay cả query và key theo vị trí lại làm điểm attention chỉ phụ thuộc khoảng cách tương đối?

- **A.** Vì phép xoay làm mọi vector có cùng độ dài
- **B.** Vì tích vô hướng của hai vector đã xoay góc mθ và nθ chỉ phụ thuộc hiệu góc (m−n)θ, do phép xoay bảo toàn độ dài và góc tương đối giữa hai vector
- **C.** Vì RoPE cộng vector vị trí vào embedding như GPT-2
- **D.** Vì key không bị xoay, chỉ query bị xoay

## Nâng cao 2 (Tự luận)

MacKay và Murphy đều định nghĩa KL divergence. Vì sao KL không phải một metric, và điều đó có nghĩa gì khi PPO dùng KL(policy ‖ reference) làm ràng buộc?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
