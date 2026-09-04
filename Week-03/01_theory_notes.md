# Lý thuyết Tuần 3: Nền tảng ML và lý thuyết học

> Tài liệu lý thuyết tự chứa cho Tuần 3. Nguồn chính: Shalev-Shwartz và Ben-David, *Understanding Machine Learning* (viết tắt UML); Tong Zhang, *Mathematical Analysis of Machine Learning Algorithms*; MML chương 8 và 9; Shalizi chương 3; Mehlig chương 5 và 6. Số trang là trang in của bản PDF trong `books/` (xem [`../docs/books/README.md`](../docs/books/README.md)). Tuần này không có số liệu chạy sẵn: các con số bạn sẽ tự sinh ra từ [`02_erm_lab.py`](02_erm_lab.py) và [`04_logistic_regression_numpy.py`](04_logistic_regression_numpy.py).

---

## 1. Khung học thống kê

UML mở đầu bằng một mô hình hình thức (mục 2.1, trang 33). Learner nhận vào:

- một **domain set** X, tập các đối tượng cần gán nhãn, mỗi đối tượng thường là một vector đặc trưng;
- một **label set** Y, ban đầu chỉ xét hai nhãn {0, 1};
- **training data** S = ((x₁, y₁), ..., (x_m, y_m)), một dãy hữu hạn cặp trong X × Y.

Điều learner **không** biết: phân phối D sinh ra x, và hàm gán nhãn f. UML nhấn mạnh điểm này ở trang 35: "The learner is blind to the underlying distribution D over the world and to the labeling function f. ... The only way the learner can interact with the environment is through observing the training set."

Tong Zhang viết cùng khung bằng ký hiệu kỳ vọng (mục 1.1, trang 2): với hàm dự đoán f(w, ·) tham số w và loss L, **training loss** là (1/n) Σ L(f(ŵ, Xᵢ), Yᵢ) trên mẫu, còn **test loss** (generalization error) là E_{(X,Y)∼D} L(f(ŵ, X), Y) trên phân phối. Giả định chuẩn là mẫu i.i.d. từ D và dữ liệu test cũng từ D.

MML nói cùng chuyện theo ngôn ngữ dữ liệu: mỗi ví dụ là một vector D chiều gọi là feature, attribute hay covariate, N ví dụ xếp thành bảng (MML mục 8.1, trang 253).

## 2. Empirical Risk Minimization

Vì không biết D, learner chỉ tính được lỗi trên mẫu. UML định nghĩa **training error**, còn gọi là empirical error hay empirical risk:

```
L_S(h) = |{ i ∈ [m] : h(xᵢ) ≠ yᵢ }| / m          (UML eq. 2.2, trang 35)
```

**Empirical Risk Minimization** (ERM) chọn h làm L_S(h) nhỏ nhất. Tong Zhang viết ERM dạng tham số: ŵ = argmin_w Σᵢ L(f(w, Xᵢ), Yᵢ) (eq. 1.1, trang 2). MML mục 8.2 (trang 259) tách ERM thành bốn câu hỏi: lớp hàm nào được phép, đo lỗi trên training data thế nào, làm sao để tốt trên dữ liệu chưa thấy, và tìm trong không gian model bằng thủ tục gì.

ERM không giới hạn gì sẽ **overfit**: một giả thuyết nhớ hết mẫu có L_S = 0 nhưng lỗi thật cao. Giải pháp của UML (mục 2.3, trang 36) là chọn trước một **lớp giả thuyết** H, gọi là inductive bias, rồi làm ERM trong H. Mehlig mô tả cùng hiện tượng ở mạng neural: mạng nhiều neuron hơn có thể khớp cả những chi tiết chỉ có trong training set, như nhiễu, và không có ý nghĩa tổng quát (Mehlig mục 6.4, trang 101). Vũ Hữu Tiệp chương 8 (trang 91) định nghĩa ngắn: overfitting là mô hình quá khớp với dữ liệu huấn luyện, không mô tả tốt dữ liệu ngoài training set.

Lab [`02_erm_lab.py`](02_erm_lab.py) cho bạn thấy điều này: cùng 20 điểm, đa thức bậc 15 có training loss nhỏ nhất nhưng validation loss lớn, đa thức bậc 3 hoặc 5 cân bằng hơn. Con số cụ thể bạn tự chạy ra.

## 3. Tách lỗi: approximation và estimation

UML mục 5.2 (trang 64) tách lỗi thật của giả thuyết ERM h_S thành hai phần:

```
L_D(h_S) = ε_app + ε_est,   ε_app = min_{h∈H} L_D(h),   ε_est = L_D(h_S) − ε_app     (UML eq. 5.7)
```

- **Approximation error** ε_app: lỗi nhỏ nhất đạt được trong H. Nó "does not depend on the sample size and is determined by the hypothesis class chosen. Enlarging the hypothesis class can decrease the approximation error" (UML trang 64).
- **Estimation error** ε_est: phần trả giá vì chỉ có mẫu hữu hạn. Lớp H càng lớn thì phần này càng dễ lớn.

Tong Zhang nói gọn hai lực kéo ở mục 1.4 (trang 5): muốn training error nhỏ thì cần model biểu đạt mạnh hơn, không gian tham số lớn hơn; nhưng model càng biểu đạt thì khoảng cách giữa training error và test error càng lớn. Cách nói phổ biến hơn là **bias và variance**. Nguyễn Thanh Tuấn định nghĩa bằng tiếng Việt: bias là độ lệch giữa trung bình dự đoán và giá trị thật, variance là độ phân tán của các dự đoán (*Deep Learning cơ bản* mục 12.3, trang 181). [Suy luận] Approximation error ứng với bias, estimation error ứng với variance; hai cách nói không trùng khít hoàn toàn nhưng cùng một trực giác. Phép đối chiếu này là cách đọc của tôi, không phải phát biểu của UML hay Tong Zhang.

Đây là khung để đọc mọi loss curve về sau. Ở Tuần 8, train loss giảm mà val loss tăng là estimation error đang thắng. Ở Tuần 11 và 12, paper "LoRA Learns Less and Forgets Less" đo đúng trade-off này trên model 7B.

## 4. PAC learnability và VC-dimension (mức nhận diện)

UML Definition 3.1 (trang 43): lớp H là **PAC learnable** nếu tồn tại hàm m_H(ε, δ) và một thuật toán học sao cho, với mọi ε, δ ∈ (0, 1), mọi phân phối D, mọi hàm nhãn f (dưới giả định realizable), khi chạy trên m ≥ m_H(ε, δ) mẫu i.i.d., thuật toán trả về h có L_{(D,f)}(h) ≤ ε với xác suất ít nhất 1 − δ. UML giải thích hai tham số: ε là phần "approximately correct", δ là phần "probably". Tên PAC do Valiant đặt năm 1984; Tong Zhang nhắc lại lịch sử này ở mục 3.1 (trang 29).

Câu hỏi tiếp theo là lớp nào PAC learnable. UML chương 4 chứng minh mọi lớp hữu hạn đều học được (mục 4.2, trang 55). Với lớp vô hạn, thước đo là **VC-dimension**: kích thước lớn nhất của một tập C ⊂ X mà H có thể shatter, tức gán được mọi cách nhãn (UML Definition 6.5, trang 70). UML Theorem 6.6 cùng trang: lớp có VC-dimension vô hạn thì không PAC learnable; và chiều ngược lại cũng đúng, VC-dimension hữu hạn thì học được.

Ở lộ trình này bạn chỉ cần nhận diện khái niệm. Mạng neural hiện đại có số tham số vượt xa số mẫu mà vẫn generalize, điều lý thuyết VC không giải thích được; Tong Zhang bàn ở mục 11.7 "Double Descent and Benign Overfitting" (trang 245), và Roberts, Yaida đề xuất một cách tiếp cận khác hẳn (mục 0.1, trang 2). Đọc hai chỗ đó sau Tuần 8, khi bạn đã chạy pretrain thật.

## 5. Validation, hold-out, cross-validation

Ước lượng lỗi thật cần dữ liệu chưa dùng để chọn model. UML mục 11.2 (trang 146 đến 147) so hai cách: bound từ VC-dimension phụ thuộc d và m, còn bound từ validation set độc lập chỉ phụ thuộc kích thước m_v của validation set, chính xác hơn, nhưng tốn thêm mẫu. Vì tách một phần dữ liệu ra tương đương với chọn validation set độc lập, phần đó gọi là **hold out set**.

Shalizi nói thẳng hơn về kỷ luật (mục 3.4, trang 81): "we absolutely, positively, cannot use any of the validation data in estimating the model." Nếu chỉ có một tập dữ liệu, chia ngẫu nhiên thành training và testing rồi làm y như có validation set thật (mục 3.4.1, cùng trang). **Cross-validation** lặp lại việc chia đó nhiều lần để giảm nhiễu của ước lượng. Mehlig mục 6.4 (trang 101) dùng cùng thuật ngữ cho mạng neural.

Ba tập, ba vai trò: train để khớp tham số, validation để chọn siêu tham số hoặc chọn model, test chỉ chạm một lần cuối để báo cáo. Ở Tuần 11, bạn so base và fine-tuned trên held-out set; ở Tuần 14, RAGAS cần eval set riêng; ở Tuần 18, rubric capstone là một validation protocol. Cùng một nguyên tắc từ đầu đến cuối.

## 6. Hai model cổ điển bạn tự code

**Linear regression** là ERM với squared loss trên lớp hàm affine (MML Example 8.1, trang 259). Nghiệm là phép chiếu trực giao của Tuần 1 mục 5, và MML mục 9.2.1 (trang 293) chỉ ra cùng nghiệm đó là MLE khi nhiễu Gaussian. Vũ Hữu Tiệp chương 7 (trang 83) trình bày bằng tiếng Việt kèm code.

**Logistic regression** đổi đầu ra thành xác suất qua sigmoid và dùng loss là negative log-likelihood của Bernoulli, tức binary cross-entropy (Vũ Hữu Tiệp chương 14, trang 165 đến 177; Shalizi mục 11.2, trang 257). Không còn nghiệm đóng, phải dùng gradient descent của Tuần 2. Gradient gọn: Xᵀ(p − y)/n. Mehlig mục 5.3 (trang 79) viết cùng bước cập nhật cho đơn vị tuyến tính dưới tên energy function và learning rate. Bạn cài toàn bộ trong [`04_logistic_regression_numpy.py`](04_logistic_regression_numpy.py); đó là mạng neural một lớp.

## 7. Cầu nối sang Tuần 4 và Tuần 5

Tuần 4 viết lại logistic regression và một MLP bằng PyTorch: `nn.Linear` là ánh xạ tuyến tính của Tuần 1, `F.cross_entropy` là NLL của Tuần 2, `optimizer.step()` là gradient descent của Tuần 2, và train, val split là mục 5 của tuần này. Tuần 5 tự viết autograd, tức là tự động hóa chain rule của Tuần 2 mục A3. Mehlig mục 6.1 (trang 91) trình bày backprop cho mạng nhiều lớp đúng bằng chain rule trên energy function; đọc trước để Tuần 5 không bỡ ngỡ.

## Tóm tắt bằng một bảng

| Khái niệm | Một câu | Nguồn |
|---|---|---|
| Khung học thống kê | X, Y, D không biết, mẫu S, giả thuyết h | UML 2.1 tr. 33; Zhang 1.1 tr. 2 |
| Empirical risk, ERM | Lỗi trên mẫu; chọn h làm nó nhỏ nhất | UML eq. 2.2 tr. 35; Zhang eq. 1.1 |
| Inductive bias | Giới hạn H trước để ERM không overfit | UML 2.3 tr. 36 |
| Error decomposition | L_D(h_S) = ε_app + ε_est | UML eq. 5.7 tr. 64 |
| Bias, variance | Độ lệch trung bình và độ phân tán của dự đoán | Nguyễn Thanh Tuấn 12.3 tr. 181 |
| PAC | Đúng đến ε với xác suất 1 − δ, đủ mẫu m_H(ε, δ) | UML Def 3.1 tr. 43 |
| VC-dimension | Tập lớn nhất H shatter được; hữu hạn thì học được | UML Def 6.5 tr. 70 |
| Validation | Không dùng validation data để ước lượng model | Shalizi 3.4 tr. 81; UML 11.2 tr. 146 |
| Linear, logistic regression | Phép chiếu; sigmoid + NLL + gradient descent | MML Ex 8.1 tr. 259; VHT ch.14 tr. 165 |

## Nguồn

- Shai Shalev-Shwartz, Shai Ben-David. *Understanding Machine Learning: From Theory to Algorithms*. Cambridge University Press, 2014. Bản PDF cá nhân tại trang tác giả.
- Tong Zhang. *Mathematical Analysis of Machine Learning Algorithms*. Bản prepublication, Cambridge University Press.
- Deisenroth, Faisal, Ong. *Mathematics for Machine Learning*. Chương 8, 9.
- Cosma Rohilla Shalizi. *Advanced Data Analysis from an Elementary Point of View*. Chương 3, 11.
- Bernhard Mehlig. *Machine learning with neural networks*. arXiv 1901.05639. Mục 5.3, 6.1, 6.4.
- Vũ Hữu Tiệp. *Machine Learning cơ bản*. Chương 5, 7, 8, 14. Nguyễn Thanh Tuấn. *Deep Learning cơ bản*. Mục 12.3.
- Daniel A. Roberts, Sho Yaida. *The Principles of Deep Learning Theory*. arXiv 2106.10165. Mục 0.1.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **ERM viết theo MLE.** Murphy tổng quát hóa MLE bằng cách thay log loss bằng loss bất kỳ: L(θ) = (1/N) Σ ℓ(yₙ, θ; xₙ) (PML1 eq. 4.60, trang 115), và gọi đó là empirical risk minimization "since it is the expected loss where the expectation is taken wrt the empirical distribution". Đây là cầu nối giữa công thức ERM của UML (mục 2) và NLL của Tuần 2.
- **Logistic regression từ góc xác suất.** Bishop viết p(C₁|φ) = σ(wᵀφ) (PRML eq. 4.87, trang 205) và nhấn mạnh "this model is known as logistic regression, although it should be emphasized that this is a model for classification rather than regression". Mục 4.3.4 (trang 209) mở rộng lên nhiều lớp, đúng phiên bản bạn dùng ở Tuần 4 với `CrossEntropyLoss`.
- **Logistic regression từ góc NLP.** Jurafsky và Martin dành cả chương 4 cho logistic regression trên văn bản: 4.5 cross-entropy loss (trang 101), 4.6 gradient descent (trang 103), 4.10 test sets và cross-validation (trang 115). Đọc mục 4.10 song song với mục 5 ở trên để thấy cùng kỷ luật validation được nói bằng ngôn ngữ NLP.
