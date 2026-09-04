# Tuần 3, Quiz: Nền tảng ML và lý thuyết học

> Tự kiểm tra **trước** khi xem solution. Tổng **8** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Trong khung học thống kê của Shalev-Shwartz và Ben-David, learner được biết gì và không được biết gì?

- **A.** Biết phân phối D và hàm nhãn f, chỉ không biết tập test
- **B.** Biết training data S gồm các cặp (x, y); không biết phân phối D sinh ra x và hàm gán nhãn f
- **C.** Biết phân phối D nhưng không biết training data
- **D.** Biết mọi thứ trừ kích thước mẫu m

## Câu 2 (Trắc nghiệm)

Empirical Risk Minimization trên toàn bộ các hàm có thể có thì dẫn đến hậu quả gì, và lý thuyết đề xuất cách khắc phục nào?

- **A.** Dẫn đến underfitting; khắc phục bằng cách tăng learning rate
- **B.** Dẫn đến overfitting vì một hàm nhớ hết mẫu có lỗi mẫu bằng 0 nhưng lỗi thật cao; khắc phục bằng cách giới hạn trước lớp giả thuyết H, gọi là inductive bias
- **C.** Không có hậu quả gì nếu dữ liệu đủ sạch
- **D.** Dẫn đến chi phí tính toán cao; khắc phục bằng GPU

## Câu 3 (Tự luận)

Hãy viết công thức tách lỗi của giả thuyết ERM thành approximation error và estimation error, rồi giải thích mỗi thành phần phụ thuộc vào điều gì.

## Câu 4 (Trắc nghiệm)

Trong định nghĩa PAC learnability, hai tham số ε và δ lần lượt mang ý nghĩa gì?

- **A.** ε là learning rate, δ là kích thước batch
- **B.** ε là độ chính xác cho phép của giả thuyết trả về (phần 'approximately correct'), δ là xác suất thất bại được chấp nhận (phần 'probably')
- **C.** ε là số mẫu, δ là số chiều của dữ liệu
- **D.** ε là lỗi trên training set, δ là lỗi trên test set

## Câu 5 (Trắc nghiệm)

Điều gì tuyệt đối không được làm với validation data, và vì sao?

- **A.** Không được vẽ đồ thị trên validation data vì tốn thời gian
- **B.** Không được dùng validation data để ước lượng hay chọn tham số model, vì khi đó ước lượng lỗi trên nó không còn độc lập và không còn là ước lượng không chệch của lỗi thật
- **C.** Không được chia validation data ngẫu nhiên vì làm mất thứ tự thời gian
- **D.** Không được để validation data nhỏ hơn 50% dữ liệu

## Câu 6 (Tự luận)

Logistic regression khác linear regression ở những điểm nào về đầu ra, hàm loss và cách giải, và vì sao có thể gọi nó là mạng neural một lớp?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Shalev-Shwartz và Ben-David tách lỗi của giả thuyết ERM thành ε_app + ε_est. Khi bạn tăng hạng r của LoRA ở Tuần 11, thành phần nào của phân tích này có xu hướng thay đổi theo hướng nào?

- **A.** Cả hai đều giảm vì model mạnh hơn
- **B.** ε_app giảm vì lớp giả thuyết rộng hơn, còn ε_est có xu hướng tăng vì mẫu hữu hạn phải ước lượng nhiều tham số hơn
- **C.** Chỉ ε_est giảm
- **D.** Không thành phần nào đổi vì LoRA không đổi lớp giả thuyết

## Nâng cao 2 (Tự luận)

Tại sao Shalev-Shwartz và Ben-David nói bound ước lượng từ validation set độc lập chính xác hơn bound từ VC-dimension, và cái giá của cách đó là gì?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
