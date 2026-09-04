# Tuần 1: Đại số tuyến tính và hình học giải tích

> Phase 0: Nền tảng toán và ML. Tuần này bạn học đúng phần đại số tuyến tính mà mọi tuần sau sẽ dùng: ma trận là ánh xạ tuyến tính, dot product đo góc, phép chiếu giải least squares, và SVD cho biết một ma trận "thực sự" có bao nhiêu chiều. Không có PyTorch trong tuần này; PyTorch bắt đầu ở Tuần 4.

## Mục tiêu

- Đọc một phép nhân ma trận như một phép biến đổi không gian, và suy ra được chiều kết quả mà không cần chạy code.
- Giải thích được vì sao dot product đo độ cùng hướng, và vì sao cosine similarity là góc giữa hai vector.
- Tính được nghiệm least squares bằng phép chiếu trực giao và kiểm tra phần dư trực giao với không gian cột.
- Nêu được ý nghĩa của trị riêng, giá trị kỳ dị, và xấp xỉ hạng thấp, rồi nối nó sang câu hỏi "vì sao LoRA chỉ cần hạng r nhỏ".

## Nguồn học

Chi tiết chương và số trang in nằm ở [`../docs/books/README.md`](../docs/books/README.md), mục Tuần 1. Tóm tắt:

- *Mathematics for Machine Learning* (Deisenroth, Faisal, Ong): chương 2 Linear Algebra, chương 3 Analytic Geometry, chương 4 Matrix Decompositions. Đây là nguồn chính.
- *Machine Learning cơ bản* (Vũ Hữu Tiệp): chương 1 Ôn tập đại số tuyến tính, để có từ vựng tiếng Việt.
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md). Mọi ví dụ số trong đó đã chạy kiểm chứng bằng NumPy 2.5.0 ngày 2026-09-04.

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): đọc từng mục, mở đúng trang sách được dẫn khi cần chứng minh đầy đủ.
2. [`02_linear_algebra_lab.py`](02_linear_algebra_lab.py): mỗi hàm là một thí nghiệm nhỏ. Đoán kết quả trước, chạy sau.
3. [`03_cheat_sheet.md`](03_cheat_sheet.md): tự viết cheat sheet một trang bằng lời của bạn (deliverable).
4. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Hai file này do `scripts/generate_quiz.py` sinh ra nên giữ nguyên tên, không đánh số.)*

## Nhiệm vụ (Task)

Làm hết các thí nghiệm trong `02_linear_algebra_lab.py`, và với mỗi thí nghiệm, viết một câu giải thích kết quả vào cheat sheet. Sau đó tự giải hai bài tập nhỏ bằng NumPy, không dùng `np.linalg.lstsq` và không dùng `np.linalg.svd`:

1. Cho 5 điểm bất kỳ trên mặt phẳng, tìm đường thẳng least squares bằng công thức phép chiếu, rồi kiểm tra phần dư trực giao với không gian cột.
2. Cho một ma trận 4×3 hạng 2 cộng nhiễu nhỏ, dùng eigendecomposition của ma trận Gram để tìm hai hướng chính, và so với kết quả `np.linalg.svd`.

## Deliverables

1. `03_cheat_sheet.md` một trang, tự viết, có đủ bốn mục: ánh xạ tuyến tính, dot product và góc, phép chiếu, SVD.
2. Hai bài tập ở trên, lưu trong một file `.py` hoặc notebook của bạn, có output.

## Thời lượng

Khoảng 10 đến 12 giờ.

## Phần cứng

Bất kỳ máy nào chạy được Python và NumPy.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` mục 1 đến 3 (ánh xạ tuyến tính, quy tắc chiều, hạng)
- [ ] Đọc MML chương 2 mục 2.4 đến 2.7 khi cần chứng minh đầy đủ
- [ ] Đọc `01_theory_notes.md` mục 4 đến 5 (norm, dot product, góc, phép chiếu)
- [ ] Đọc MML chương 3 mục 3.1, 3.2, 3.4, 3.8
- [ ] Đọc `01_theory_notes.md` mục 6 đến 7 (trị riêng, SVD, xấp xỉ hạng thấp)
- [ ] Đọc MML chương 4 mục 4.2, 4.5, 4.6
- [ ] Chạy hết `02_linear_algebra_lab.py`, mỗi hàm đoán trước rồi chạy
- [ ] Làm bài tập 1: least squares bằng phép chiếu
- [ ] Làm bài tập 2: hai hướng chính từ ma trận Gram
- [ ] Viết `03_cheat_sheet.md` bằng lời của mình
- [ ] Tự kiểm tra: giải thích cho Claude vì sao cosine similarity là góc và vì sao SVD cho xấp xỉ hạng thấp tốt nhất

## Cách dùng Claude làm bạn học (Tuần 1)

- Dán một định nghĩa từ MML (ví dụ Def 3.7 Orthogonality) và nhờ Claude đặt ba câu hỏi kiểm tra bạn có hiểu không.
- Sau khi tự làm bài tập, dán code và nhờ Claude so với cách chuẩn. Đừng để Claude viết bản nháp đầu tiên.
- Nhờ Claude cho một ví dụ ma trận 2×2 rồi bạn vẽ tay ảnh của hình vuông đơn vị qua ma trận đó.

> Tiêu chí tự đánh giá: nếu chưa giải thích được một thành phần cho Claude bằng lời của mình, nghĩa là chưa học xong. Đó là tín hiệu để đi chậm lại.

## Bổ sung nâng cao

Tuần này cố ý không có mục nâng cao. Bảng neo trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) để trống cho Tuần 1 đến Tuần 5. Nếu còn thời gian, đọc thêm chương 2 (Nonnegative Matrix Factorization) trong sách của Moitra để thấy một phép phân rã ma trận có ý nghĩa thực tế.

## File trong folder này

Số ở đầu tên file là thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này: mục tiêu, nguồn, checklist |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: ánh xạ tuyến tính, norm, góc, phép chiếu, trị riêng, SVD |
| 2 | `02_linear_algebra_lab.py` | Bảy thí nghiệm NumPy, mỗi hàm dẫn đúng trang sách |
| 3 | `03_cheat_sheet.md` | Cheat sheet một trang bạn tự viết (deliverable) |
| 4 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
