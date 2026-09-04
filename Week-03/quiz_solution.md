# Tuần 3, Đáp án & Giải thích: Nền tảng ML và lý thuyết học

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Trong khung học thống kê của Shalev-Shwartz và Ben-David, learner được biết gì và không được biết gì?

- **A.** Biết phân phối D và hàm nhãn f, chỉ không biết tập test
- **B.** Biết training data S gồm các cặp (x, y); không biết phân phối D sinh ra x và hàm gán nhãn f (đáp án đúng)
- **C.** Biết phân phối D nhưng không biết training data
- **D.** Biết mọi thứ trừ kích thước mẫu m

**Đáp án: B**

**Giải thích:** UML mục 2.1 (trang 33) và câu ở trang 35: learner 'mù' với D và f, cách duy nhất tương tác với thế giới là qua training set. Vì thế lỗi thật L_D(h) không tính được, chỉ tính được lỗi trên mẫu.

## Câu 2 (Trắc nghiệm)

Empirical Risk Minimization trên toàn bộ các hàm có thể có thì dẫn đến hậu quả gì, và lý thuyết đề xuất cách khắc phục nào?

- **A.** Dẫn đến underfitting; khắc phục bằng cách tăng learning rate
- **B.** Dẫn đến overfitting vì một hàm nhớ hết mẫu có lỗi mẫu bằng 0 nhưng lỗi thật cao; khắc phục bằng cách giới hạn trước lớp giả thuyết H, gọi là inductive bias (đáp án đúng)
- **C.** Không có hậu quả gì nếu dữ liệu đủ sạch
- **D.** Dẫn đến chi phí tính toán cao; khắc phục bằng GPU

**Đáp án: B**

**Giải thích:** UML mục 2.2 định nghĩa empirical risk (eq. 2.2, trang 35) và mục 2.3 (trang 36) đưa ra ERM với inductive bias. Lab 02_erm_lab.py cho thấy đa thức bậc cao có train loss thấp nhất nhưng validation loss lớn.

## Câu 3 (Tự luận)

Hãy viết công thức tách lỗi của giả thuyết ERM thành approximation error và estimation error, rồi giải thích mỗi thành phần phụ thuộc vào điều gì.

**Trả lời mẫu:** L_D(h_S) = ε_app + ε_est, với ε_app = min over h in H của L_D(h) và ε_est = L_D(h_S) − ε_app (UML eq. 5.7, trang 64). Approximation error là lỗi nhỏ nhất đạt được trong lớp H, không phụ thuộc kích thước mẫu, chỉ phụ thuộc H; mở rộng H làm nó giảm. Estimation error là phần trả giá vì chỉ có mẫu hữu hạn; H càng lớn thì phần này càng dễ lớn. Cách nói bias và variance là phiên bản trực giác của cùng trade-off.

**Giải thích:** Đây là khung để đọc mọi loss curve về sau: train loss giảm mà validation loss tăng nghĩa là estimation error đang thắng.

## Câu 4 (Trắc nghiệm)

Trong định nghĩa PAC learnability, hai tham số ε và δ lần lượt mang ý nghĩa gì?

- **A.** ε là learning rate, δ là kích thước batch
- **B.** ε là độ chính xác cho phép của giả thuyết trả về (phần 'approximately correct'), δ là xác suất thất bại được chấp nhận (phần 'probably') (đáp án đúng)
- **C.** ε là số mẫu, δ là số chiều của dữ liệu
- **D.** ε là lỗi trên training set, δ là lỗi trên test set

**Đáp án: B**

**Giải thích:** UML Definition 3.1 (trang 43): với m ≥ m_H(ε, δ) mẫu i.i.d., thuật toán trả về h có lỗi thật không quá ε với xác suất ít nhất 1 − δ. Hai xấp xỉ này là không tránh được vì mẫu hữu hạn và ngẫu nhiên.

## Câu 5 (Trắc nghiệm)

Điều gì tuyệt đối không được làm với validation data, và vì sao?

- **A.** Không được vẽ đồ thị trên validation data vì tốn thời gian
- **B.** Không được dùng validation data để ước lượng hay chọn tham số model, vì khi đó ước lượng lỗi trên nó không còn độc lập và không còn là ước lượng không chệch của lỗi thật (đáp án đúng)
- **C.** Không được chia validation data ngẫu nhiên vì làm mất thứ tự thời gian
- **D.** Không được để validation data nhỏ hơn 50% dữ liệu

**Đáp án: B**

**Giải thích:** Shalizi mục 3.4 (trang 81): 'we absolutely, positively, cannot use any of the validation data in estimating the model.' UML mục 11.2 (trang 146) chỉ ra bound từ validation set độc lập chính xác hơn bound VC, nhưng chỉ khi nó thật sự độc lập.

## Câu 6 (Tự luận)

Logistic regression khác linear regression ở những điểm nào về đầu ra, hàm loss và cách giải, và vì sao có thể gọi nó là mạng neural một lớp?

**Trả lời mẫu:** Linear regression trả về số thực, dùng squared loss, và có nghiệm đóng bằng phép chiếu trực giao (MML Example 8.1, trang 259). Logistic regression đưa đầu ra qua sigmoid để thành xác suất trong (0, 1), dùng negative log-likelihood của Bernoulli tức binary cross-entropy, và không có nghiệm đóng nên phải dùng gradient descent với gradient Xᵀ(p − y)/n (Vũ Hữu Tiệp chương 14, trang 165). Nó là một lớp tuyến tính nối với một hàm kích hoạt phi tuyến và một loss, đúng cấu trúc tối giản của một mạng neural.

**Giải thích:** Tuần 4 viết lại đúng model này bằng nn.Linear và F.binary_cross_entropy trong PyTorch, rồi chồng thêm lớp để thành MLP.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Shalev-Shwartz và Ben-David tách lỗi của giả thuyết ERM thành ε_app + ε_est. Khi bạn tăng hạng r của LoRA ở Tuần 11, thành phần nào của phân tích này có xu hướng thay đổi theo hướng nào?

- **A.** Cả hai đều giảm vì model mạnh hơn
- **B.** ε_app giảm vì lớp giả thuyết rộng hơn, còn ε_est có xu hướng tăng vì mẫu hữu hạn phải ước lượng nhiều tham số hơn (đáp án đúng)
- **C.** Chỉ ε_est giảm
- **D.** Không thành phần nào đổi vì LoRA không đổi lớp giả thuyết

**Đáp án: B**

**Giải thích:** UML mục 5.2 (trang 64): approximation error chỉ phụ thuộc H, estimation error là giá của mẫu hữu hạn. Tăng r mở rộng H. Kết quả thực nghiệm phụ thuộc dữ liệu; đây là khung để đọc, không phải dự đoán chắc.

## Nâng cao 2 (Tự luận)

Tại sao Shalev-Shwartz và Ben-David nói bound ước lượng từ validation set độc lập chính xác hơn bound từ VC-dimension, và cái giá của cách đó là gì?

**Trả lời mẫu:** Bound VC phụ thuộc VC-dimension d và kích thước mẫu m, còn bound từ validation set chỉ phụ thuộc kích thước m_v của validation set với sai số cỡ căn(log(2/δ)/(2m_v)), không phụ thuộc độ phức tạp của lớp giả thuyết (UML mục 11.2, trang 146-147). Cái giá là cần thêm mẫu độc lập ngoài mẫu đã dùng để train, và tuyệt đối không dùng validation data để ước lượng model (Shalizi mục 3.4, trang 81).

**Giải thích:** Đây là lý do mọi tuần eval về sau đều đòi held-out set riêng, kể cả eval set RAGAS ở Tuần 14.
