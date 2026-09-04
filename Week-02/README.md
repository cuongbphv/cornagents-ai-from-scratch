# Tuần 2: Giải tích vector, xác suất, tối ưu hóa

> Phase 0: Nền tảng toán và ML. Ba mảnh toán còn lại mà mọi training loop đều đứng trên: đạo hàm nhiều biến và chain rule (để có backprop), xác suất (để hiểu loss là kỳ vọng và batch là mẫu), và gradient descent (để hiểu vì sao learning rate quyết định hội tụ hay nổ).

## Mục tiêu

- Tính được gradient của một hàm nhiều biến bằng tay và kiểm lại bằng sai phân số.
- Phát biểu được chain rule dạng ma trận (Jacobian) và chỉ ra nó là toàn bộ ý tưởng của backprop.
- Dùng đúng ba tiên đề xác suất, sum rule, product rule, và công thức Bayes trên một bài toán đếm được.
- Giải thích được luật số lớn và định lý giới hạn trung tâm bằng mô phỏng, và nối chúng sang câu "loss trên batch là ước lượng của loss kỳ vọng".
- Chỉ ra cross-entropy là negative log-likelihood, tức MLE.
- Tự cài gradient descent, thấy tận mắt điểm khởi đầu và step size quyết định kết quả.

## Nguồn học

Chi tiết chương và số trang in ở [`../docs/books/README.md`](../docs/books/README.md), mục Tuần 2. Tóm tắt:

- *Mathematics for Machine Learning*: chương 5 Vector Calculus, chương 6 Probability and Distributions, chương 7 Continuous Optimization.
- *Elementary Probability for Applications* (Rick Durrett): mục 1.1.1 tiên đề, 4.4 luật số lớn, 4.5 định lý giới hạn trung tâm, 5.3 công thức Bayes.
- *Machine Learning cơ bản* (Vũ Hữu Tiệp): chương 2 Giải tích ma trận, chương 3 Ôn tập xác suất, chương 4 MLE và MAP, chương 12 Gradient descent.
- *Deep Learning cơ bản* (Nguyễn Thanh Tuấn): mục 3.3 gradient descent, cách giải thích trực quan.
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md). Mọi ví dụ số đã chạy kiểm chứng bằng NumPy 2.5.0 ngày 2026-09-04.

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): đọc theo ba phần, giải tích, xác suất, tối ưu.
2. [`02_calculus_probability_lab.py`](02_calculus_probability_lab.py): bảy thí nghiệm, đoán trước rồi chạy.
3. [`03_gradient_descent.py`](03_gradient_descent.py): tự điền đạo hàm và bước cập nhật (deliverable chính).
4. [`04_cheat_sheet.md`](04_cheat_sheet.md): cheat sheet một trang bạn tự viết (deliverable).
5. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Hai file này do `scripts/generate_quiz.py` sinh ra nên giữ nguyên tên, không đánh số.)*

## Nhiệm vụ (Task)

1. Điền hai chỗ `TODO` trong `03_gradient_descent.py`, chạy, và trả lời hai câu hỏi trong docstring: điểm khởi đầu nào rơi vào cực tiểu thấp hơn, và step size nào làm phân kỳ.
2. Viết một hàm `numerical_gradient` của riêng bạn (không nhìn lab), rồi dùng nó kiểm tra gradient của hàm f(x₁, x₂) = x₁² x₂ + x₁ x₂³ tại một điểm bạn chọn.
3. Tự làm bài xét nghiệm y tế bằng công thức Bayes với con số bạn tự đặt, và giải thích vì sao kết quả nhỏ hơn trực giác.

## Deliverables

1. `03_gradient_descent.py` chạy được, kèm output và câu trả lời hai câu hỏi.
2. `04_cheat_sheet.md` một trang, bốn mục: gradient và chain rule, tiên đề và Bayes, luật số lớn và CLT, MLE và gradient descent.

## Thời lượng

Khoảng 12 đến 14 giờ. Phần xác suất thường tốn nhiều thời gian hơn bạn nghĩ.

## Phần cứng

Bất kỳ máy nào chạy được Python và NumPy.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` phần A (đạo hàm, gradient, chain rule, Jacobian)
- [ ] Đọc MML 5.2 và 5.3; đọc Vũ Hữu Tiệp 2.6 về kiểm tra đạo hàm
- [ ] Chạy `gradcheck`, `chain`, `jacobian` trong lab, hiểu vì sao sai lệch cỡ 1e-9
- [ ] Đọc `01_theory_notes.md` phần B (tiên đề, biến ngẫu nhiên, Bayes, luật số lớn, CLT)
- [ ] Đọc Durrett 1.1.1, 4.4, 4.5, 5.3; đọc MML Table 6.1 để phân biệt pmf, pdf, cdf
- [ ] Chạy `lln`, `clt`, `bayes` trong lab, tự làm lại bài Bayes với số của bạn
- [ ] Đọc `01_theory_notes.md` phần C (MLE, gradient descent, step size, convex)
- [ ] Đọc MML 7.1 và Vũ Hữu Tiệp chương 12
- [ ] Chạy `mle` trong lab; hiểu vì sao NLL tại nghiệm MLE nhỏ hơn tại điểm khác
- [ ] Điền `TODO` trong `03_gradient_descent.py` và trả lời hai câu hỏi trong docstring
- [ ] Viết `04_cheat_sheet.md` bằng lời của mình
- [ ] Tự kiểm tra: giải thích cho Claude vì sao cross-entropy là negative log-likelihood

## Cách dùng Claude làm bạn học (Tuần 2)

- Dán bài xét nghiệm y tế bạn tự đặt số và nhờ Claude kiểm tra từng bước Bayes, rồi nhờ đặt một bài khác để bạn giải.
- Sau khi điền `03_gradient_descent.py`, dán code và nhờ Claude chỉ ra chỗ có thể sai dấu hoặc sai step size.
- Nhờ Claude cho một hàm hai biến mới, bạn tính gradient bằng tay rồi kiểm bằng hàm sai phân của bạn.

## Bổ sung nâng cao

Tuần này cố ý không có mục nâng cao. Nếu bạn muốn đọc định nghĩa xác suất theo độ đo, mở *Probability: Theory and Examples* (Durrett) chương 1, nhưng lộ trình này không cần đến mức đó.

## File trong folder này

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: gradient, chain rule, tiên đề xác suất, Bayes, LLN, CLT, MLE, gradient descent |
| 2 | `02_calculus_probability_lab.py` | Bảy thí nghiệm NumPy có dẫn trang sách |
| 3 | `03_gradient_descent.py` | Skeleton gradient descent, bạn tự điền (deliverable) |
| 4 | `04_cheat_sheet.md` | Cheat sheet một trang bạn tự viết (deliverable) |
| 5 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
