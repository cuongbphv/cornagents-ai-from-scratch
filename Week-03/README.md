# Tuần 3: Nền tảng ML và lý thuyết học

> Phase 0: Nền tảng toán và ML (tuần cuối). Tuần này trả lời câu hỏi "học từ dữ liệu nghĩa là gì" bằng ngôn ngữ chính xác: phân phối D không biết, chỉ có mẫu S, chọn giả thuyết bằng empirical risk minimization, và trả giá bằng khoảng cách giữa lỗi trên mẫu và lỗi thật. Bạn cũng tự code hai model cổ điển bằng NumPy để Tuần 4 vào PyTorch không bị lạ.

## Mục tiêu

- Phát biểu được khung học thống kê: domain X, nhãn Y, phân phối D, mẫu S, giả thuyết h, lỗi thật L_D(h) và lỗi mẫu L_S(h).
- Giải thích ERM và vì sao ERM không giới hạn lớp giả thuyết thì overfit.
- Tách lỗi thành approximation error và estimation error, và nối sang cách nói bias và variance.
- Nêu định nghĩa PAC learnability và VC-dimension ở mức nhận diện, không cần chứng minh.
- Dùng đúng train, validation, test: biết điều gì tuyệt đối không được làm với validation data.
- Tự code linear regression bằng phép chiếu và logistic regression bằng gradient descent.

## Nguồn học

Chi tiết chương và số trang in ở [`../docs/books/README.md`](../docs/books/README.md), mục Tuần 3. Tóm tắt:

- *Understanding Machine Learning: From Theory to Algorithms* (Shalev-Shwartz, Ben-David): mục 2.1 đến 2.3, định nghĩa 3.1, chương 5, định nghĩa 6.5, mục 11.2. Nguồn chính cho lý thuyết.
- *Mathematical Analysis of Machine Learning Algorithms* (Tong Zhang): mục 1.1, 1.4, 3.1. Cách viết gọn bằng kỳ vọng.
- *Mathematics for Machine Learning*: chương 8 When Models Meet Data, chương 9 Linear Regression.
- *Advanced Data Analysis from an Elementary Point of View* (Shalizi): mục 3.2 đến 3.4 về lỗi trong và ngoài mẫu, cross-validation.
- *Machine learning with neural networks* (Mehlig): mục 5.3, 6.1, 6.4.
- *Machine Learning cơ bản* (Vũ Hữu Tiệp): chương 5, 7, 8, 14. *Deep Learning cơ bản* (Nguyễn Thanh Tuấn): mục 12.3 bias và variance.
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): đọc mục 1 đến 4 trước khi chạy code.
2. [`02_erm_lab.py`](02_erm_lab.py): điền `fit_poly` và `empirical_risk`, đọc bảng train loss và val loss theo bậc đa thức.
3. [`03_learning_theory_notes.md`](03_learning_theory_notes.md): ghi lại bằng lời của bạn năm khái niệm và câu trả lời từ lab (deliverable).
4. [`04_logistic_regression_numpy.py`](04_logistic_regression_numpy.py): điền sigmoid, loss, gradient, kiểm gradient, rồi train (deliverable).
5. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Hai file này do `scripts/generate_quiz.py` sinh ra nên giữ nguyên tên, không đánh số.)*

## Nhiệm vụ (Task)

1. Hoàn thành `02_erm_lab.py`. Trả lời: bậc nào tốt nhất trên train, bậc nào tốt nhất trên validation, và giải thích bằng error decomposition.
2. Hoàn thành `04_logistic_regression_numpy.py`. Gradient phải qua kiểm tra sai phân trước khi train.
3. Viết `03_learning_theory_notes.md`.

## Deliverables

1. Hai file `.py` chạy được kèm output.
2. `03_learning_theory_notes.md` với năm khái niệm viết bằng lời của bạn: ERM, overfitting, error decomposition, PAC, validation.

## Thời lượng

Khoảng 12 đến 14 giờ.

## Phần cứng

Bất kỳ máy nào chạy được Python và NumPy.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` mục 1 và 2 (khung học thống kê, ERM)
- [ ] Đọc UML 2.1 đến 2.3 và Tong Zhang 1.1
- [ ] Đọc `01_theory_notes.md` mục 3 (error decomposition, bias và variance)
- [ ] Đọc UML 5.2; đọc Nguyễn Thanh Tuấn 12.3 để có cách nói tiếng Việt
- [ ] Đọc `01_theory_notes.md` mục 4 (PAC, VC-dimension, ở mức nhận diện)
- [ ] Đọc `01_theory_notes.md` mục 5 (validation, cross-validation); đọc Shalizi 3.4
- [ ] Điền và chạy `02_erm_lab.py`, ghi câu trả lời vào `03_learning_theory_notes.md`
- [ ] Điền `04_logistic_regression_numpy.py`, gradcheck lệch dưới 1e-6, rồi train
- [ ] Đọc `01_theory_notes.md` mục 6 và 7 (hai model cổ điển, cầu nối sang deep learning)
- [ ] Hoàn thành `03_learning_theory_notes.md`
- [ ] Tự kiểm tra: giải thích cho Claude vì sao không được chọn model bằng test set

## Cách dùng Claude làm bạn học (Tuần 3)

- Dán Definition 3.1 (PAC Learnability) và nhờ Claude giải thích vai trò của ε và δ bằng ví dụ đời thường, rồi bạn diễn đạt lại.
- Dán bảng train loss và val loss của bạn, nhờ Claude hỏi ngược bạn ba câu về lý do.
- Sau khi tự code logistic regression, dán code nhờ Claude soát dấu của gradient và cách xử lý số khi sigmoid bão hòa.

## Bổ sung nâng cao

Tuần này cố ý không có mục nâng cao trong `advanced_topics_vi.md`. Cầu nối sang lý thuyết deep learning: đọc mục 0.1 của *The Principles of Deep Learning Theory* (Roberts, Yaida) để biết vì sao lý thuyết học cổ điển chưa đủ cho mạng rất rộng và rất sâu; quay lại chương 1 và 2 của sách đó sau Tuần 8.

## File trong folder này

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: khung học thống kê, ERM, error decomposition, PAC, validation, hai model cổ điển |
| 2 | `02_erm_lab.py` | Overfitting bằng mắt trên đa thức bậc tăng dần (bạn điền) |
| 3 | `03_learning_theory_notes.md` | Ghi chú năm khái niệm bằng lời của bạn (deliverable) |
| 4 | `04_logistic_regression_numpy.py` | Logistic regression NumPy, gradient tự tính (deliverable) |
| 5 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
