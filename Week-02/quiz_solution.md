# Tuần 2, Đáp án & Giải thích: Giải tích vector, xác suất, tối ưu hóa

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Với hàm f(x₁, x₂) = x₁²x₂ + x₁x₂³, gradient tại điểm (1, 2) bằng bao nhiêu?

- **A.** [12, 13] (đáp án đúng)
- **B.** [5, 9]
- **C.** [12, 7]
- **D.** [4, 13]

**Đáp án: A**

**Giải thích:** Đạo hàm riêng theo x₁ là 2x₁x₂ + x₂³ = 4 + 8 = 12; theo x₂ là x₁² + 3x₁x₂² = 1 + 12 = 13 (MML Example 5.7, trang 147). Lab gradcheck xác nhận bằng sai phân với sai lệch cỡ 1e-9.

## Câu 2 (Tự luận)

Hãy mô tả cách bạn kiểm tra một công thức gradient bằng số, và giải thích vì sao kỹ thuật này sẽ hữu ích ở Tuần 5 khi tự viết autograd.

**Trả lời mẫu:** Dùng sai phân trung tâm: với từng chiều i, tính (f(x + εeᵢ) − f(x − εeᵢ)) / 2ε với ε khoảng 1e-6, rồi so với gradient giải tích; sai lệch cỡ 1e-8 trở xuống là khớp (Vũ Hữu Tiệp mục 2.6, trang 36). Ở Tuần 5, micrograd tự tính gradient qua chain rule; cách kiểm độc lập duy nhất là so với sai phân số hoặc với PyTorch.

**Giải thích:** Đây là công cụ debug rẻ nhất cho mọi phép đạo hàm bạn tự viết, kể cả khi đã dùng PyTorch.

## Câu 3 (Trắc nghiệm)

Một bệnh có tỉ lệ 1% trong dân số. Xét nghiệm phát hiện đúng 95% người bệnh và báo dương tính giả ở 5% người khỏe. Một người nhận kết quả dương tính thì xác suất thực sự mắc bệnh gần với con số nào?

- **A.** Khoảng 95%
- **B.** Khoảng 50%
- **C.** Khoảng 16% (đáp án đúng)
- **D.** Khoảng 1%

**Đáp án: C**

**Giải thích:** Theo công thức Bayes (Durrett EP4A mục 5.3, trang 118): P(bệnh | dương) = 0.95 × 0.01 / (0.95 × 0.01 + 0.05 × 0.99) ≈ 0.161. Số người khỏe bị dương tính giả đông hơn số người bệnh dương tính thật, nên kết quả nhỏ hơn trực giác rất nhiều.

## Câu 4 (Trắc nghiệm)

Luật số lớn nói gì về loss tính trên một batch trong training, và điều đó giải thích hiện tượng nào trên loss curve?

- **A.** Loss trên batch là trung bình mẫu của loss kỳ vọng, có phương sai tỉ lệ với 1/n, nên batch nhỏ cho loss curve nhấp nhô hơn batch lớn (đáp án đúng)
- **B.** Loss trên batch chỉ hội tụ khi learning rate giảm về 0
- **C.** Loss trên batch không liên quan đến loss kỳ vọng vì dữ liệu không độc lập
- **D.** Loss trên batch luôn bằng loss kỳ vọng, nên loss curve phải trơn

**Đáp án: A**

**Giải thích:** Trung bình mẫu X̄ₙ có kỳ vọng μ và phương sai σ²/n, và tiến về μ khi n lớn (Durrett EP4A Theorem 4.7, trang 93). Loss của một batch là đúng trung bình mẫu như vậy, nên kích thước batch điều khiển độ nhiễu của ước lượng.

## Câu 5 (Tự luận)

Vì sao cross-entropy loss được xem là negative log-likelihood, và vì sao người ta cực tiểu negative log-likelihood thay vì cực đại likelihood trực tiếp?

**Trả lời mẫu:** Maximum likelihood tìm tham số làm xác suất quan sát được dữ liệu lớn nhất (Vũ Hữu Tiệp mục 4.2, trang 53). Với phân phối categorical trên các lớp hoặc token, log-likelihood của nhãn đúng là log của xác suất model gán cho nhãn đó; đổi dấu và lấy trung bình ta được cross-entropy. Lấy log biến tích của nhiều mẫu thành tổng, dễ tính và ổn định số, còn đổi dấu chỉ để dùng thuật toán cực tiểu hóa; vị trí cực trị không đổi vì log đơn điệu tăng.

**Giải thích:** MML mục 9.2.1 (trang 293) nhắc thêm rằng likelihood không phải phân phối xác suất theo tham số θ; nó chỉ là một hàm của θ mà ta tối ưu.

## Câu 6 (Trắc nghiệm)

Trên hàm f(x) = x² với đạo hàm 2x, chạy gradient descent từ x₀ = 5 với step size 1.1 thì điều gì xảy ra sau 20 bước, và vì sao?

- **A.** Phân kỳ, vì mỗi bước nhân x với (1 − 2 × 1.1) = −1.2 nên trị tuyệt đối tăng theo cấp số nhân (đáp án đúng)
- **B.** Hội tụ về 0 vì hàm lồi nên mọi step size đều được
- **C.** Dừng ngay tại x = 5 vì gradient bằng 0
- **D.** Dao động quanh 0 với biên độ không đổi

**Đáp án: A**

**Giải thích:** Bước cập nhật x ← x − γ·2x = (1 − 2γ)x. Với γ = 1.1, hệ số là −1.2, trị tuyệt đối lớn hơn 1 nên |x| tăng mỗi bước. MML mục 7.1 (trang 227-228) bàn đúng chuyện step size quá lớn thì phân kỳ, quá nhỏ thì chậm; skeleton 03_gradient_descent.py cho bạn thấy tận mắt.

## Câu 7 (Trắc nghiệm)

Theo MacKay (ITILA eq. 2.45-2.46), relative entropy D_KL(P‖Q) luôn không âm và chỉ bằng 0 khi P = Q. Điều này nói gì về giá trị nhỏ nhất mà cross-entropy loss có thể đạt khi train một model?

- **A.** Cross-entropy không có đáy vì log không bị chặn
- **B.** Cross-entropy nhỏ nhất bằng KL divergence
- **C.** Cross-entropy nhỏ nhất bằng entropy của phân phối dữ liệu, đạt được khi phân phối model trùng phân phối thật, vì cross-entropy = entropy + KL (đáp án đúng)
- **D.** Cross-entropy có thể xuống 0 với mọi dữ liệu nếu train đủ lâu

**Đáp án: C**

**Giải thích:** Cross-entropy H(P, Q) = H(P) + D_KL(P‖Q). Vì KL ≥ 0 với đẳng thức khi P = Q (bất đẳng thức Gibbs, MacKay trang 34), đáy của loss là entropy của dữ liệu, không phải 0. Dữ liệu có nhiễu thì loss tốt nhất vẫn dương.

## Câu 8 (Trắc nghiệm)

Theo quy ước numerator layout của MML, Jacobian của hàm f: R³ → R² có kích thước nào, và gradient của hàm vô hướng g: Rⁿ → R được viết là vector hàng hay cột?

- **A.** Jacobian 3×2 và gradient là vector cột n×1, vì mỗi cột ứng với một đầu ra của f.
- **B.** Jacobian 2×3 và gradient là vector hàng 1×n, vì các phần tử của f xác định hàng, các biến x xác định cột. (đáp án đúng)
- **C.** Jacobian 2×2 và gradient là vector cột n×1, vì số hàng và cột đều bằng số chiều đầu ra.
- **D.** Jacobian 3×3 và gradient là vector hàng 1×n, vì Jacobian luôn vuông để có thể lấy định thức.

**Đáp án: B**

**Giải thích:** Định nghĩa 5.6: Jacobian của f: Rⁿ → Rᵐ là ma trận m×n với J(i, j) = ∂fᵢ/∂xⱼ; sách ghi rõ "we use the numerator layout of the derivative, i.e., the derivative df/dx of f ∈ Rᵐ with respect to x ∈ Rⁿ is an m × n matrix, where the elements of f define the rows and the elements of x define the columns" (MML mục 5.3, Định nghĩa 5.6, công thức 5.57-5.59, tr. 150). Gradient của hàm vô hướng là vector hàng 1×n (công thức 5.40); lý do chọn hàng là để áp dụng chain rule dạng nhân ma trận mà không phải lo chiều (MML mục 5.2, tr. 146-147)

## Câu 9 (Trắc nghiệm)

Cho f(x₁, x₂) = x₁² + 2x₂ với x₁ = sin t và x₂ = cos t. Áp dụng chain rule nhiều biến, df/dt bằng bao nhiêu?

- **A.** 2 sin t cos t + 2 cos t, vì đạo hàm của cos t là cos t và của sin t là cos t.
- **B.** 2 cos t − 2 sin t, vì chỉ cần lấy đạo hàm từng biến theo t rồi cộng lại, bỏ qua các đạo hàm riêng của f.
- **C.** sin 2t + 2, vì 2 sin t cos t = sin 2t và đạo hàm của 2x₂ theo t là hằng số 2.
- **D.** 2 sin t (cos t − 1), vì df/dt = (∂f/∂x₁)(∂x₁/∂t) + (∂f/∂x₂)(∂x₂/∂t) = 2 sin t cos t − 2 sin t. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Ví dụ 5.8 trong MML: df/dt = ∂f/∂x₁ · ∂x₁/∂t + ∂f/∂x₂ · ∂x₂/∂t = 2 sin t · cos t + 2 · (−sin t) = 2 sin t (cos t − 1) (công thức 5.50a-c). Dạng ma trận của cùng phép tính là gradient hàng [∂f/∂x₁ ∂f/∂x₂] nhân với cột [∂x₁/∂t; ∂x₂/∂t] (công thức 5.49); đây đúng là phép nhân mà autograd ở Tuần 5 thực hiện tại mỗi nút (MML mục 5.2.2, Ví dụ 5.8, công thức 5.49-5.50, tr. 148)

## Câu 10 (Trắc nghiệm)

MML phân biệt forward mode và reverse mode của automatic differentiation qua thứ tự nhân trong dy/dx = (dy/db)(db/da)(da/dx). Vì sao reverse mode (backpropagation) được ưu tiên khi huấn luyện mạng neural?

- **A.** Vì forward mode cần lưu toàn bộ đồ thị tính toán trong bộ nhớ, còn reverse mode không cần lưu giá trị trung gian.
- **B.** Vì reverse mode cho gradient chính xác hơn về số học, còn forward mode chỉ là xấp xỉ sai phân hữu hạn.
- **C.** Vì reverse mode là cách duy nhất áp dụng được chain rule cho các hàm hợp có nhiều hơn hai tầng.
- **D.** Vì trong mạng neural số chiều đầu vào thường lớn hơn nhiều số chiều nhãn, nên nhân từ phía đầu ra ngược về rẻ hơn đáng kể. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Sách viết: "Equation (5.120) would be the reverse mode because gradients are propagated backward through the graph" và "In the context of neural networks, where the input dimensionality is often much higher than the dimensionality of the labels, the reverse mode is computationally significantly cheaper than the forward mode". Cả hai mode đều cho gradient chính xác tới độ chính xác máy (khác với sai phân hữu hạn), và việc chọn thứ tự nhân dựa trên tính kết hợp của phép nhân ma trận (MML mục 5.6.2, công thức 5.119-5.121, tr. 161-162)

## Câu 11 (Trắc nghiệm)

Khi kiểm tra đạo hàm bằng số, Vũ Hữu Tiệp khuyên dùng công thức hai phía (f(x + ε) − f(x − ε))/(2ε) thay cho công thức một phía (f(x + ε) − f(x))/ε. Lý do bằng khai triển Taylor là gì?

- **A.** Hai công thức có cùng sai số O(ε) nhưng công thức hai phía tính nhanh gấp đôi vì chỉ cần một lần gọi hàm.
- **B.** Công thức hai phía có sai số O(ε) còn công thức một phía có sai số O(ε²), nên hai phía ổn định hơn khi ε lớn.
- **C.** Công thức hai phía triệt tiêu số hạng bậc hai f''(x)ε/2 nên sai số chỉ còn O(ε²), trong khi công thức một phía có sai số O(ε). (đáp án đúng)
- **D.** Công thức hai phía đúng tuyệt đối với mọi đa thức bậc ba, còn công thức một phía chỉ đúng với hàm tuyến tính.

**Đáp án: C**

**Giải thích:** Từ khai triển Taylor (2.19)-(2.20), sách thu được (f(x + ε) − f(x))/ε ≈ f'(x) + f''(x)ε/2 + ... = f'(x) + O(ε) (công thức 2.21) và (f(x + ε) − f(x − ε))/(2ε) ≈ f'(x) + f⁽³⁾(x)ε²/6 + ... = f'(x) + O(ε²) (công thức 2.22); "Khi ε rất nhỏ, O(ε²) ≪ O(ε), tức cách đánh giá sử dụng công thức 2.22 có sai số nhỏ hơn". Sách cũng lưu ý numerical gradient chỉ dùng để kiểm tra vì quá tốn kém với ma trận lớn, nên khi so sánh người ta giảm số chiều và số điểm dữ liệu (Vũ Hữu Tiệp mục 2.6.1-2.6.2, công thức 2.18-2.22, tr. 36-37)

## Câu 12 (Trắc nghiệm)

Nguyễn Thanh Tuấn chạy gradient descent trên f(x) = x² từ x = 10 với learning_rate = 0,1. Sau mỗi bước x được cập nhật thế nào, và sau 10 bước x xấp xỉ bao nhiêu?

- **A.** x ← x − 0,1·2x, tức nhân với 0,8 mỗi bước; sau 10 bước x ≈ 1,07. (đáp án đúng)
- **B.** x ← x − 0,1·x², tức trừ đi 10 ở bước đầu; sau 10 bước x đã về đúng 0.
- **C.** x ← x − 0,1·x, tức nhân với 0,9 mỗi bước; sau 10 bước x ≈ 3,49.
- **D.** x ← 0,1·2x, tức nhân với 0,2 mỗi bước; sau 10 bước x ≈ 10⁻⁶.

**Đáp án: A**

**Giải thích:** Với f'(x) = 2x, bước cập nhật là x = x − learning_rate·2x = 0,8x. Bảng trong sách liệt kê x sau từng lần: 8,00; 6,40; 5,12; 4,10; 3,28; 2,62; 2,10; 1,68; 1,34; 1,07 với f(x) giảm từ 64,00 xuống 1,15 (Nguyễn Thanh Tuấn mục 3.3.2, tr. 52). Sách cũng nêu ba trường hợp learning rate: nhỏ thì cần rất nhiều bước, hợp lý thì hội tụ sau số bước vừa phải, quá lớn thì overshoot và không về được cực tiểu (Nguyễn Thanh Tuấn mục 3.3.2, tr. 53)

## Câu 13 (Trắc nghiệm)

MML tách bạch pmf, pdf và cdf trong Bảng 6.1. Phát biểu nào sau đây đúng?

- **A.** Giá trị của hàm mật độ p(x) (pdf) có thể lớn hơn 1, miễn là tích phân của nó trên toàn miền bằng 1. (đáp án đúng)
- **B.** Giá trị của hàm khối xác suất P(X = x) (pmf) có thể lớn hơn 1 khi biến rời rạc có ít trạng thái.
- **C.** pdf và cdf là hai tên gọi của cùng một hàm, khác nhau ở chỗ cdf được chuẩn hóa để nhận giá trị trong [0, 1].
- **D.** Hàm phân phối tích lũy P(X ≤ x) (cdf) chỉ định nghĩa cho biến rời rạc, còn biến liên tục chỉ có pdf.

**Đáp án: A**

**Giải thích:** Sách viết ngay dưới Bảng 6.1 rằng "density can be greater than 1. However, it needs to hold that ∫ p(x)dx = 1" (công thức 6.19). Bảng 6.1 xếp: biến rời rạc có P(X = x) là pmf và không có "interval probability"; biến liên tục có p(x) là pdf và P(X ≤ x) là cdf. Sách cũng cảnh báo tài liệu ML dùng lẫn chữ "distribution" cho cả pmf, pdf và cdf. Điều này quan trọng khi đọc log-likelihood của mô hình liên tục: log p(x) dương không phải lỗi (MML mục 6.2-6.3, Bảng 6.1, công thức 6.19, tr. 183)

## Câu 14 (Trắc nghiệm)

Bốn phân phối trên 4 trạng thái: p₁ = [0,25; 0,25; 0,25; 0,25], p₂ = [0,5; 0,5; 0; 0], p₃ = [1; 0; 0; 0], p₄ = [0,7; 0,1; 0,1; 0,1]. Phân phối nào có entropy lớn nhất và giá trị đó là bao nhiêu bit?

- **A.** p₂, với entropy 1 bit, vì hai trạng thái có xác suất 0 làm giảm bậc tự do và tăng độ bất định.
- **B.** p₁, với entropy log₂ 4 = 2 bit, vì phân phối đều là phân phối có entropy lớn nhất trên K trạng thái. (đáp án đúng)
- **C.** p₄, với entropy khoảng 1,36 bit, vì nó vừa có một trạng thái nổi trội vừa giữ được ba trạng thái hiếm.
- **D.** p₃, với entropy 4 bit, vì toàn bộ khối lượng dồn vào một trạng thái nên lượng thông tin của trạng thái đó lớn nhất.

**Đáp án: B**

**Giải thích:** Tự tính theo định nghĩa: H(p₂) = 1 bit, H(p₃) = 0, H(p₄) ≈ 0,36 + 3·0,332 ≈ 1,36 bit (ba con số này tính tay từ công thức entropy, không in trong sách). MacKay định nghĩa H(X) = Σ P(x) log 1/P(x) với quy ước 0 × log 1/0 ≡ 0 (MacKay mục 2.4, công thức 2.35, tr. 32). Murphy: "The discrete distribution with maximum entropy is the uniform distribution. Hence for a K-ary random variable, the entropy is maximized if p(x = k) = 1/K; in this case, H(X) = log₂ K" (công thức 6.2), và phân phối suy biến có entropy 0 là giá trị nhỏ nhất (Murphy mục 6.1.1, công thức 6.1-6.2, tr. 207)

## Câu 15 (Tự luận)

Vì sao MML nói chi phí tính gradient bằng backpropagation "có độ phức tạp tương đương với chi phí tính chính hàm số", dù biểu thức đạo hàm viết tường minh (công thức 5.110) dài hơn hàm gốc rất nhiều? Trình bày cơ chế tái sử dụng trong chuỗi ∂L/∂θᵢ.

**Trả lời mẫu:** Backprop không khai triển biểu thức đạo hàm thành công thức đóng mà làm việc trên các biến trung gian của đồ thị tính toán. Với mạng K tầng, ∂L/∂θ_{K−1} = (∂L/∂f_K)(∂f_K/∂θ_{K−1}), rồi ∂L/∂θ_{K−2} = (∂L/∂f_K)(∂f_K/∂f_{K−1})(∂f_{K−1}/∂θ_{K−2}); phần tích đã tính cho tầng i+1 được dùng lại cho tầng i, mỗi tầng chỉ cần nhân thêm một đạo hàm cục bộ theo đầu vào và một theo tham số. Vì mỗi phép toán sơ cấp (cộng, nhân, exp, sin...) có đạo hàng cục bộ đơn giản, tổng số phép tính khi đi ngược tỉ lệ với số phép tính khi đi tiến. Đây chính là lý do một bước training gồm forward và backward chỉ tốn cỡ vài lần forward, không phụ thuộc số tham số theo kiểu bùng nổ.

**Giải thích:** Các công thức (5.115)-(5.118) cho ∂L/∂θᵢ = (∂L/∂f_K)(∂f_K/∂f_{K−1})···(∂f_{i+1}/∂θᵢ) và sách nói "Assuming, we have already computed the partial derivatives ∂L/∂θ_{i+1}, then most of the computation can be reused to compute ∂L/∂θᵢ" (MML mục 5.6.1, công thức 5.115-5.118, tr. 160). Ví dụ 5.14 với các biến trung gian a, b, c, d, e kết luận: "the computation required for calculating the derivative is of similar complexity as the computation of the function itself. This is quite counter-intuitive since the mathematical expression for the derivative ∂f/∂x (5.110) is significantly more complicated than the mathematical expression of the function f(x) in (5.109)" (MML mục 5.6.2, Ví dụ 5.14, công thức 5.122-5.142, tr. 160-163)

## Câu 16 (Tự luận)

MML mô tả hiện tượng gradient descent "zigzag" trong thung lũng dài và hẹp. Hãy giải thích hiện tượng này bằng condition number, nêu hai heuristic điều chỉnh step size mà sách trích từ Toussaint (2012), và cho biết momentum thay đổi công thức cập nhật ra sao.

**Trả lời mẫu:** Khi mặt mục tiêu cong mạnh theo một hướng và rất phẳng theo hướng khác, gradient gần như vuông góc với hướng ngắn nhất tới cực tiểu, nên các bước nhảy qua lại giữa hai vách thung lũng. Tốc độ hội tụ phụ thuộc condition number κ = σ_max(A)/σ_min(A), tỉ số giữa giá trị kỳ dị lớn nhất và nhỏ nhất, đo mức chênh giữa hướng cong nhất và hướng phẳng nhất; κ lớn là bài toán poorly conditioned. Hai heuristic: nếu giá trị hàm tăng sau một bước thì step size quá lớn, hoàn tác và giảm step size; nếu giá trị hàm giảm thì có thể tăng step size. Momentum thêm bộ nhớ vào cập nhật: x_{i+1} = xᵢ − γᵢ(∇f(xᵢ))ᵀ + αΔxᵢ với Δxᵢ = xᵢ − x_{i−1} và α ∈ [0, 1], làm mượt các bước dao động và trung bình hóa gradient nhiễu; đây là tổ tiên của các optimizer Tuần 4.

**Giải thích:** Sách viết: "For poorly conditioned convex problems, gradient descent increasingly 'zigzags' as the gradients point nearly orthogonally to the shortest direction to a minimum point" (MML mục 7.1, tr. 229); condition number κ = σ(A)_max/σ(A)_min "measures the ratio of the most curved direction versus the least curved direction" (MML mục 7.1.1, Ví dụ 7.2, tr. 230). Hai heuristic của Toussaint (2012) và công thức momentum (7.11)-(7.12) với α ∈ [0, 1] nằm ở cùng đoạn (MML mục 7.1.1-7.1.2, công thức 7.11-7.12, tr. 229-231)

## Câu 17 (Tự luận)

Trong ước lượng MLE cho phân phối chuẩn một chiều (Vũ Hữu Tiệp, Ví dụ 3, Chương 4), kết quả cho µ và σ² là gì? Nêu hai lý do MML đưa ra cho việc lấy log của likelihood trước khi tối ưu, và liên hệ với cách bạn sẽ cài cross-entropy ở Tuần 4.

**Trả lời mẫu:** Với các quan sát độc lập x₁, ..., x_N tuân theo N(µ, σ²), cực đại log-likelihood J(µ, σ) = −N log σ − Σ(xᵢ − µ)²/(2σ²) cho µ = (1/N)Σxᵢ (trung bình mẫu) và σ² = (1/N)Σ(xᵢ − µ)². MML nêu hai lý do lấy log: (a) tránh numerical underflow khi nhân N xác suất rất nhỏ, ví dụ không biểu diễn được các số cỡ 10⁻²⁵⁶; (b) log biến tích thành tổng, nên gradient là tổng các gradient riêng lẻ thay vì phải áp dụng quy tắc tích lặp lại N lần. Vì log là hàm tăng nghiêm ngặt, điểm cực đại của f và của log f trùng nhau. Cross-entropy ở Tuần 4 là negative log-likelihood trung bình trên batch, nên cả hai lý do này áp dụng trực tiếp.

**Giải thích:** Vũ Hữu Tiệp đưa J(µ, σ) ở công thức (4.23), giải ∂J/∂µ = 0 và ∂J/∂σ = 0 để được µ = Σxᵢ/N và σ² = Σ(xᵢ − µ)²/N (Vũ Hữu Tiệp mục 4.2, Ví dụ 3, công thức 4.20-4.26, tr. 56-57). MML: "the log-transformation is useful since (a) it does not suffer from numerical underflow, and (b) the differentiation rules will turn out simpler ... we cannot represent very small numbers, such as 10⁻²⁵⁶ ... the log-transform will turn the product into a sum of log-probabilities such that the corresponding gradient is a sum of individual gradients" (MML mục 9.2.1, Remark Log-Transformation, công thức 9.7-9.8, tr. 293)

## Câu 18 (Tự luận)

Xem loss trên một minibatch như trung bình X̄ₙ của n biến độc lập cùng phân phối, kỳ vọng µ và phương sai σ². Durrett cho biết gì về E X̄ₙ, var(X̄ₙ) và về phân phối giới hạn của (Sₙ − nµ)/(σ√n)? Từ đó suy ra điều gì khi bạn tăng batch size từ 16 lên 64?

**Trả lời mẫu:** E X̄ₙ = µ (X̄ₙ là ước lượng không chệch của µ) và var(X̄ₙ) = σ²/n, nên phương sai của trung bình giảm tỉ lệ nghịch với n; luật số lớn yếu (Định lý 4.7) nói P(|X̄ₙ − µ| > ε) → 0. Định lý giới hạn trung tâm (Định lý 4.9) nói (Sₙ − nµ)/(σ√n) hội tụ về phân phối chuẩn tắc, nên với n đủ lớn X̄ₙ xấp xỉ chuẩn quanh µ với độ lệch chuẩn σ/√n; theo bảng chuẩn, khoảng 68% xác suất nằm trong một độ lệch chuẩn và 95% trong hai. Tăng batch từ 16 lên 64 (gấp 4) làm var giảm 4 lần, tức độ lệch chuẩn của loss batch giảm một nửa: loss curve mượt hơn nhưng mỗi bước tốn gấp 4 lần tính toán (kết luận về loss curve áp dụng công thức phương sai σ²/n).

**Giải thích:** Durrett: "E X̄ₙ = µ, var(X̄ₙ) = σ²/n" (công thức 4.15), "X̄ₙ is an unbiased estimator of µ", và Định lý 4.7 (Weak law of Large Numbers): với mọi ε > 0, P(|X̄ₙ − µ| > ε) → 0 (Durrett EP4A mục 4.4, công thức 4.15, Định lý 4.7, tr. 93). Định lý 4.9 (CLT): P(a ≤ (Sₙ − nµ)/(σ√n) ≤ b) → ∫ₐᵇ e^{−x²/2}/√(2π) dx, kèm bảng Φ(1) = 0,8413, Φ(2) = 0,9772 và nhận xét 68%, 95%, dưới 0,3% (Durrett EP4A mục 4.5, Định lý 4.9, tr. 95). MML cũng viết loss huấn luyện dạng tổng L(θ) = Σ Lₙ(θ) và SGD dùng xấp xỉ nhiễu của gradient (MML mục 7.1.3, công thức 7.13-7.14, tr. 231)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Theo RoFormer (arXiv 2104.09864) và cách MML định nghĩa góc giữa hai vector, vì sao xoay cả query và key theo vị trí lại làm điểm attention chỉ phụ thuộc khoảng cách tương đối?

- **A.** Vì RoPE cộng vector vị trí vào embedding như GPT-2
- **B.** Vì tích vô hướng của hai vector đã xoay góc mθ và nθ chỉ phụ thuộc hiệu góc (m−n)θ, do phép xoay bảo toàn độ dài và góc tương đối giữa hai vector (đáp án đúng)
- **C.** Vì phép xoay làm mọi vector có cùng độ dài
- **D.** Vì key không bị xoay, chỉ query bị xoay

**Đáp án: B**

**Giải thích:** Đây là hình học Tuần 1 mục 4 (cos góc = inner product chia tích độ dài) áp lên cặp chiều được xoay. RoFormer viết RoPE 'encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation' (abstract).

## Nâng cao 2 (Tự luận)

MacKay và Murphy đều định nghĩa KL divergence. Vì sao KL không phải một metric, và điều đó có nghĩa gì khi PPO dùng KL(policy ‖ reference) làm ràng buộc?

**Trả lời mẫu:** KL(P‖Q) không đối xứng và không thỏa bất đẳng thức tam giác, nên chỉ là divergence, không phải metric (Murphy PML1 mục 6.2, trang 213; MacKay eq. 2.45, trang 34). Trong RLHF, chiều KL(π_θ ‖ π_ref) phạt policy đặt xác suất cao vào chỗ reference đặt xác suất thấp; đổi chiều sẽ phạt điều khác, nên khi đọc code alignment ở Tuần 10 phải nhìn rõ chiều nào được dùng.

**Giải thích:** Bất đẳng thức Gibbs KL ≥ 0 với đẳng thức khi hai phân phối trùng nhau là lý do KL dùng được như 'khoảng cách' dù không đối xứng.
