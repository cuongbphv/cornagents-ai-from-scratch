# Lý thuyết Tuần 2: Giải tích vector, xác suất, tối ưu hóa

> Tài liệu lý thuyết tự chứa cho Tuần 2, chia ba phần A, B, C. Nguồn chính: MML chương 5, 6, 7; Durrett *Elementary Probability for Applications* (EP4A); Vũ Hữu Tiệp chương 2, 3, 4, 12. Số trang là trang in của bản PDF trong `books/` (xem [`../docs/books/README.md`](../docs/books/README.md)). Mọi con số dưới đây là output của [`02_calculus_probability_lab.py`](02_calculus_probability_lab.py), chạy bằng NumPy 2.5.0 ngày 2026-09-04.

---

## Phần A: Giải tích vector

### A1. Đạo hàm riêng và gradient

Với hàm f từ ℝⁿ vào ℝ, đạo hàm riêng theo x_i là tốc độ thay đổi của f khi chỉ x_i nhúc nhích. Gradient gom tất cả đạo hàm riêng lại. MML chọn quy ước gradient là **vector hàng**, và giải thích lý do: "First, we can consistently generalize the gradient to vector-valued functions f: ℝⁿ → ℝᵐ (then the gradient becomes a matrix). Second, we can immediately apply the multi-variate chain rule without paying attention to the dimension of the gradient" (MML mục 5.2, trang 147). PyTorch trả gradient cùng chiều với tham số, tức là vector cột theo cách nhìn này; hai quy ước chỉ khác nhau một phép chuyển vị.

Ví dụ 5.7 trong MML (trang 147): f(x₁, x₂) = x₁² x₂ + x₁ x₂³ có ∂f/∂x₁ = 2x₁x₂ + x₂³ và ∂f/∂x₂ = x₁² + 3x₁x₂². Tại (1, 2), gradient là [12, 13].

### A2. Kiểm tra đạo hàm bằng số

Sai phân trung tâm (f(x + εe_i) − f(x − εe_i)) / 2ε xấp xỉ đạo hàm riêng thứ i. Vũ Hữu Tiệp mục 2.6 (trang 36, Code 2.1) dùng đúng cách này để kiểm mọi công thức đạo hàm trước khi tin. Thí nghiệm `gradcheck`: gradient giải tích [12, 13] và gradient số [12, 13] lệch nhau 9.9e-10. Ở Tuần 5, bạn sẽ dùng lại đúng kỹ thuật này để kiểm micrograd đối chiếu PyTorch.

### A3. Chain rule

Nếu f = g(h(x)) thì df/dx = (dg/dh)(dh/dx). MML tính một ví dụ dài ở mục 5.6 (trang 159), hàm (5.109): f(x) = √(x² + exp(x²)) + cos(x² + exp(x²)). Thí nghiệm `chain` kiểm đạo hàm theo chain rule tại x = 0.5 là −1.360431, sai phân số cho cùng giá trị. MML viết ngay sau đó rằng backpropagation "is a special case of a general technique in numerical analysis called automatic differentiation". Đó là toàn bộ điều Tuần 5 sẽ cài.

### A4. Jacobian và ánh xạ tuyến tính

Với f từ ℝⁿ vào ℝᵐ, gradient là ma trận m×n gọi là Jacobian (MML mục 5.3, trang 149). Với f(x) = A x, Jacobian chính là A. Thí nghiệm `jacobian` xác nhận điều này bằng sai phân. Vì thế backward của một lớp Linear chỉ là nhân gradient với Wᵀ, không có gì bí hiểm.

---

## Phần B: Xác suất

### B1. Ba tiên đề và cách hiểu bằng tần số

Durrett phát biểu: xác suất là hàm gán số cho sự kiện, thỏa (i) 0 ≤ P(A) ≤ 1, (ii) P(Ω) = 1, (iii) A, B rời nhau thì P(A ∪ B) = P(A) + P(B), và (iv) mở rộng (iii) cho dãy vô hạn sự kiện rời nhau (EP4A mục 1.1.1, trang 4). Ông giải thích các tiên đề bằng cách hiểu tần số: "if we repeat an experiment a large number of times then the fraction of times the event A occurs will be close to P(A)", công thức (1.1) cùng trang, và nói thêm rằng đây sẽ là một định lý, luật số lớn.

### B2. Biến ngẫu nhiên, pmf, pdf, cdf

Tài liệu ML dùng chữ "distribution" cho ba thứ khác nhau. MML tách rõ ở Table 6.1 (trang 183): với biến rời rạc, P(X = x) là hàm khối xác suất (pmf); với biến liên tục, p(x) là hàm mật độ (pdf) và P(X ≤ x) là hàm phân phối tích lũy (cdf). Mật độ có thể lớn hơn 1, chỉ cần tích phân bằng 1 (MML công thức 6.19, cùng trang). Khi Tuần 4 nói softmax cho ra "phân phối trên token", đó là một pmf.

### B3. Sum rule, product rule, Bayes

Sum rule: p(x) = Σ_y p(x, y). Product rule: p(x, y) = p(y | x) p(x). Bayes suy ra từ hai quy tắc đó (MML mục 6.3, trang 183 đến 186). Durrett dạy Bayes qua ví dụ trước rồi mới cho công thức (EP4A mục 5.3, trang 118).

Thí nghiệm `bayes`: bệnh có tỉ lệ 1%, xét nghiệm nhạy 95%, dương tính giả 5%. P(bệnh | dương tính) = 0.161, không phải 90% như trực giác. Lý do: số người khỏe dương tính giả (5% của 99%) đông hơn số người bệnh dương tính thật (95% của 1%).

### B4. Kỳ vọng, phương sai, luật số lớn

Cho X₁, X₂, ... độc lập cùng phân phối, kỳ vọng μ, phương sai σ². Trung bình mẫu X̄ₙ có kỳ vọng μ và phương sai σ²/n. Luật số lớn yếu: với mọi ε > 0, P(|X̄ₙ − μ| > ε) tiến về 0 khi n tiến ra vô cùng (EP4A Theorem 4.7, trang 93).

Thí nghiệm `lln` với xúc xắc công bằng (μ = 3.5, P(mặt 6) = 1/6 ≈ 0.1667):

| n | trung bình mẫu | tần số mặt 6 |
|---|---|---|
| 10 | 3.1000 | 0.1000 |
| 1 000 | 3.5030 | 0.1610 |
| 100 000 | 3.4999 | 0.1659 |

Nối sang training: loss trên một batch là trung bình mẫu của loss kỳ vọng trên phân phối dữ liệu. Batch nhỏ thì ước lượng nhiễu, batch lớn thì sát hơn, đúng theo phương sai σ²/n. Vì loss mỗi batch là một trung bình mẫu với phương sai σ²/n, loss curve ở Tuần 8 nhấp nhô ngay cả khi model không đổi; các nguồn nhiễu khác (learning rate, dữ liệu không đồng nhất) bàn ở tuần đó.

### B5. Định lý giới hạn trung tâm

Chuẩn hóa (Sₙ − nμ)/(σ√n) tiến về phân phối chuẩn N(0, 1) (EP4A Theorem 4.9, trang 95). Durrett cho bảng Φ(1) = 0.8413, nên P(−1 ≤ Z ≤ 1) = 2Φ(1) − 1 = 0.6826. Thí nghiệm `clt` với tổng 50 xúc xắc, 20 000 lần, cho 0.7015. Con số lệch khoảng 0.02 không phải nhiễu mô phỏng: với 20 000 lần thử, độ lệch chuẩn của một tỉ lệ quanh 0.68 là √(0.68 · 0.32 / 20000) ≈ 0.0033, nhỏ hơn mức lệch nhiều lần. Phần lệch đến từ việc định lý chỉ đúng ở giới hạn n tiến ra vô cùng trong khi n = 50, và từ việc so một biến rời rạc với phân phối liên tục; bạn tự kiểm bằng cách tăng n trong lab và xem sai lệch có giảm không. Đây là ví dụ để bạn tập nhìn sai số mô phỏng thay vì tin một số duy nhất.

### B6. Gaussian và MLE

Gaussian là phân phối trung tâm của ML vì CLT và vì nó tính được bằng tay (MML mục 6.5, trang 197). **Maximum likelihood estimation** tìm tham số θ làm xác suất quan sát được dữ liệu lớn nhất (Vũ Hữu Tiệp mục 4.2, trang 53). MML nhắc một điểm hay bị nhầm: "The likelihood p(y | x, θ) is not a probability distribution in θ" (MML mục 9.2.1, trang 293). Trong thực hành ta cực tiểu **negative log-likelihood** (NLL) vì log biến tích thành tổng và không đổi vị trí cực trị.

Thí nghiệm `mle`: 10 000 mẫu từ N(2.0, 0.5²) cho μ_ML = 2.0 và σ_ML = 0.5017; NLL trung bình tại nghiệm MLE là 0.7292, tại (1.5, 0.5) là 1.2292. Cross-entropy ở Tuần 4 là NLL của phân phối categorical: cùng một ý tưởng, đổi phân phối.

---

## Phần C: Tối ưu hóa

### C1. Gradient descent

Cập nhật x_{t+1} = x_t − γ ∇f(x_t). Gradient chỉ hướng tăng nhanh nhất, nên đi ngược gradient thì giảm f, nhưng "not how far (this is called the step-size)" (MML mục 7.1, trang 227). MML dùng hàm x⁴ + 7x³ + 5x² − 17x + 3 (Figure 7.2, cùng trang) để chỉ ra điểm khởi đầu quyết định rơi vào cực tiểu nào; ở x > −1, gradient đưa về cực tiểu bên phải, có giá trị hàm cao hơn. Bạn sẽ tự tái hiện điều này trong [`03_gradient_descent.py`](03_gradient_descent.py).

Nguyễn Thanh Tuấn giải thích cùng ý bằng đồ thị y = x²: trị tuyệt đối của đạo hàm càng lớn thì đồ thị càng dốc, đạo hàm âm thì hàm đang giảm (*Deep Learning cơ bản* mục 3.3, trang 50 đến 51). Vũ Hữu Tiệp chương 12 (trang 140 đến 155) đi từ GD một biến, nhiều biến, đến momentum, Nesterov và SGD.

### C2. Step size

Step size quá nhỏ thì chậm, quá lớn thì phân kỳ (MML trang 228). Trên f(x) = x² với đạo hàm 2x, lr = 0.1 hội tụ, lr = 1.1 làm |x| tăng theo cấp số nhân. Skeleton `demo_step_size` để bạn tự thấy. Ở Tuần 8, warmup và cosine decay là cách điều khiển step size theo thời gian.

### C3. Convex

Với hàm lồi, mọi cực tiểu cục bộ là cực tiểu toàn cục, nên điểm khởi đầu không còn quan trọng (MML nêu ở mục 7.1, trang 227, và trình bày đầy đủ ở mục 7.3, trang 236). Loss của mạng neural nhiều lớp không lồi; đó là lý do khởi tạo trọng số và lịch learning rate được bàn nhiều ở Tuần 8.

---

## Tóm tắt bằng một bảng

| Khái niệm | Một câu | Nguồn | Dùng ở tuần |
|---|---|---|---|
| Gradient, chain rule | Đạo hàm nhiều biến; hợp hàm thì nhân đạo hàm | MML 5.2 tr. 147; 5.6 tr. 159 | 5 |
| Kiểm tra đạo hàm | Sai phân trung tâm, lệch cỡ 1e-9 là tốt | Vũ Hữu Tiệp 2.6 tr. 36 | 5 |
| Tiên đề xác suất | Không âm, tổng bằng 1, cộng tính | EP4A 1.1.1 tr. 4 | 4 |
| pmf, pdf, cdf | Ba thứ hay bị gọi chung là "distribution" | MML Table 6.1 tr. 183 | 4 |
| Bayes | Đảo chiều điều kiện, cần prior | EP4A 5.3 tr. 118; MML 6.3 | 13 |
| Luật số lớn | Trung bình mẫu tiến về kỳ vọng, phương sai σ²/n | EP4A Thm 4.7 tr. 93 | 8 |
| CLT | Tổng chuẩn hóa tiến về N(0,1) | EP4A Thm 4.9 tr. 95 | 8 |
| MLE, NLL | Cross-entropy là NLL | VHT 4.2 tr. 53; MML 9.2.1 tr. 293 | 4, 8 |
| Gradient descent | Ngược gradient, step size quyết định | MML 7.1 tr. 227; VHT ch.12 | 8 |

## Nguồn

- Deisenroth, Faisal, Ong. *Mathematics for Machine Learning*. Chương 5, 6, 7, 9.2.1.
- Rick Durrett. *Elementary Probability for Applications*, version 2.4, 2021. Mục 1.1.1, 4.4, 4.5, 5.3.
- Vũ Hữu Tiệp. *Machine Learning cơ bản*. Chương 2, 3, 4, 12.
- Nguyễn Thanh Tuấn. *Deep Learning cơ bản*, v2, 2020. Mục 3.3.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- Định nghĩa chặt của entropy và KL nằm ở MacKay: ông định nghĩa entropy của một ensemble là "the average Shannon information content of an outcome", H(X) = Σ P(x) log 1/P(x) (ITILA eq. 2.35, trang 32), và relative entropy D_KL(P‖Q) = Σ P(x) log P(x)/Q(x) thỏa bất đẳng thức Gibbs D_KL ≥ 0 "with equality only if P = Q" (eq. 2.45-2.46, trang 34). Đây là lý do cross-entropy ở mục B6 có đáy: cross-entropy = entropy của dữ liệu + KL, nên nhỏ nhất khi model trùng phân phối thật. Murphy viết cùng định nghĩa bằng kỳ vọng, H(X) = −E[log p(X)] (PML1 eq. 6.1, trang 207), và nhắc KL là divergence chứ không phải metric vì không đối xứng (PML1 6.2, trang 213).
- Định nghĩa gốc của hàm lồi lấy từ Boyd và Vandenberghe: f lồi khi miền xác định lồi và f(θx + (1−θ)y) ≤ θf(x) + (1−θ)f(y) với mọi θ ∈ [0, 1] (Convex Optimization eq. 3.1, trang 67); mọi hàm affine vừa lồi vừa lõm. Đây là định nghĩa mà MML 7.3 (mục C3 ở trên) dựa vào.
- Information theory theo cách trình bày của Bishop nằm ở PRML mục 1.6 (trang 48) và 1.6.1 relative entropy (trang 55); đây là cách trình bày thứ ba, đi từ "lượng thông tin của một sự kiện" tới KL; đọc nếu hai cách trên chưa thấm.
