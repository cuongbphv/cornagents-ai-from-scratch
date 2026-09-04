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
