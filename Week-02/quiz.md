# Tuần 2, Quiz: Giải tích vector, xác suất, tối ưu hóa

> Tự kiểm tra **trước** khi xem solution. Tổng **20** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Với hàm f(x₁, x₂) = x₁²x₂ + x₁x₂³, gradient tại điểm (1, 2) bằng bao nhiêu?

- **A.** [12, 13]
- **B.** [5, 9]
- **C.** [12, 7]
- **D.** [4, 13]

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

- **A.** Loss trên batch là trung bình mẫu của loss kỳ vọng, có phương sai tỉ lệ với 1/n, nên batch nhỏ cho loss curve nhấp nhô hơn batch lớn
- **B.** Loss trên batch chỉ hội tụ khi learning rate giảm về 0
- **C.** Loss trên batch không liên quan đến loss kỳ vọng vì dữ liệu không độc lập
- **D.** Loss trên batch luôn bằng loss kỳ vọng, nên loss curve phải trơn

## Câu 5 (Tự luận)

Vì sao cross-entropy loss được xem là negative log-likelihood, và vì sao người ta cực tiểu negative log-likelihood thay vì cực đại likelihood trực tiếp?

## Câu 6 (Trắc nghiệm)

Trên hàm f(x) = x² với đạo hàm 2x, chạy gradient descent từ x₀ = 5 với step size 1.1 thì điều gì xảy ra sau 20 bước, và vì sao?

- **A.** Phân kỳ, vì mỗi bước nhân x với (1 − 2 × 1.1) = −1.2 nên trị tuyệt đối tăng theo cấp số nhân
- **B.** Hội tụ về 0 vì hàm lồi nên mọi step size đều được
- **C.** Dừng ngay tại x = 5 vì gradient bằng 0
- **D.** Dao động quanh 0 với biên độ không đổi

## Câu 7 (Trắc nghiệm)

Theo MacKay (ITILA eq. 2.45-2.46), relative entropy D_KL(P‖Q) luôn không âm và chỉ bằng 0 khi P = Q. Điều này nói gì về giá trị nhỏ nhất mà cross-entropy loss có thể đạt khi train một model?

- **A.** Cross-entropy không có đáy vì log không bị chặn
- **B.** Cross-entropy nhỏ nhất bằng KL divergence
- **C.** Cross-entropy nhỏ nhất bằng entropy của phân phối dữ liệu, đạt được khi phân phối model trùng phân phối thật, vì cross-entropy = entropy + KL
- **D.** Cross-entropy có thể xuống 0 với mọi dữ liệu nếu train đủ lâu

## Câu 8 (Trắc nghiệm)

Theo quy ước numerator layout của MML, Jacobian của hàm f: R³ → R² có kích thước nào, và gradient của hàm vô hướng g: Rⁿ → R được viết là vector hàng hay cột?

- **A.** Jacobian 3×2 và gradient là vector cột n×1, vì mỗi cột ứng với một đầu ra của f.
- **B.** Jacobian 2×3 và gradient là vector hàng 1×n, vì các phần tử của f xác định hàng, các biến x xác định cột.
- **C.** Jacobian 2×2 và gradient là vector cột n×1, vì số hàng và cột đều bằng số chiều đầu ra.
- **D.** Jacobian 3×3 và gradient là vector hàng 1×n, vì Jacobian luôn vuông để có thể lấy định thức.

## Câu 9 (Trắc nghiệm)

Cho f(x₁, x₂) = x₁² + 2x₂ với x₁ = sin t và x₂ = cos t. Áp dụng chain rule nhiều biến, df/dt bằng bao nhiêu?

- **A.** 2 sin t cos t + 2 cos t, vì đạo hàm của cos t là cos t và của sin t là cos t.
- **B.** 2 cos t − 2 sin t, vì chỉ cần lấy đạo hàm từng biến theo t rồi cộng lại, bỏ qua các đạo hàm riêng của f.
- **C.** sin 2t + 2, vì 2 sin t cos t = sin 2t và đạo hàm của 2x₂ theo t là hằng số 2.
- **D.** 2 sin t (cos t − 1), vì df/dt = (∂f/∂x₁)(∂x₁/∂t) + (∂f/∂x₂)(∂x₂/∂t) = 2 sin t cos t − 2 sin t.

## Câu 10 (Trắc nghiệm)

MML phân biệt forward mode và reverse mode của automatic differentiation qua thứ tự nhân trong dy/dx = (dy/db)(db/da)(da/dx). Vì sao reverse mode (backpropagation) được ưu tiên khi huấn luyện mạng neural?

- **A.** Vì forward mode cần lưu toàn bộ đồ thị tính toán trong bộ nhớ, còn reverse mode không cần lưu giá trị trung gian.
- **B.** Vì reverse mode cho gradient chính xác hơn về số học, còn forward mode chỉ là xấp xỉ sai phân hữu hạn.
- **C.** Vì reverse mode là cách duy nhất áp dụng được chain rule cho các hàm hợp có nhiều hơn hai tầng.
- **D.** Vì trong mạng neural số chiều đầu vào thường lớn hơn nhiều số chiều nhãn, nên nhân từ phía đầu ra ngược về rẻ hơn đáng kể.

## Câu 11 (Trắc nghiệm)

Khi kiểm tra đạo hàm bằng số, Vũ Hữu Tiệp khuyên dùng công thức hai phía (f(x + ε) − f(x − ε))/(2ε) thay cho công thức một phía (f(x + ε) − f(x))/ε. Lý do bằng khai triển Taylor là gì?

- **A.** Hai công thức có cùng sai số O(ε) nhưng công thức hai phía tính nhanh gấp đôi vì chỉ cần một lần gọi hàm.
- **B.** Công thức hai phía có sai số O(ε) còn công thức một phía có sai số O(ε²), nên hai phía ổn định hơn khi ε lớn.
- **C.** Công thức hai phía triệt tiêu số hạng bậc hai f''(x)ε/2 nên sai số chỉ còn O(ε²), trong khi công thức một phía có sai số O(ε).
- **D.** Công thức hai phía đúng tuyệt đối với mọi đa thức bậc ba, còn công thức một phía chỉ đúng với hàm tuyến tính.

## Câu 12 (Trắc nghiệm)

Nguyễn Thanh Tuấn chạy gradient descent trên f(x) = x² từ x = 10 với learning_rate = 0,1. Sau mỗi bước x được cập nhật thế nào, và sau 10 bước x xấp xỉ bao nhiêu?

- **A.** x ← x − 0,1·2x, tức nhân với 0,8 mỗi bước; sau 10 bước x ≈ 1,07.
- **B.** x ← x − 0,1·x², tức trừ đi 10 ở bước đầu; sau 10 bước x đã về đúng 0.
- **C.** x ← x − 0,1·x, tức nhân với 0,9 mỗi bước; sau 10 bước x ≈ 3,49.
- **D.** x ← 0,1·2x, tức nhân với 0,2 mỗi bước; sau 10 bước x ≈ 10⁻⁶.

## Câu 13 (Trắc nghiệm)

MML tách bạch pmf, pdf và cdf trong Bảng 6.1. Phát biểu nào sau đây đúng?

- **A.** Giá trị của hàm mật độ p(x) (pdf) có thể lớn hơn 1, miễn là tích phân của nó trên toàn miền bằng 1.
- **B.** Giá trị của hàm khối xác suất P(X = x) (pmf) có thể lớn hơn 1 khi biến rời rạc có ít trạng thái.
- **C.** pdf và cdf là hai tên gọi của cùng một hàm, khác nhau ở chỗ cdf được chuẩn hóa để nhận giá trị trong [0, 1].
- **D.** Hàm phân phối tích lũy P(X ≤ x) (cdf) chỉ định nghĩa cho biến rời rạc, còn biến liên tục chỉ có pdf.

## Câu 14 (Trắc nghiệm)

Bốn phân phối trên 4 trạng thái: p₁ = [0,25; 0,25; 0,25; 0,25], p₂ = [0,5; 0,5; 0; 0], p₃ = [1; 0; 0; 0], p₄ = [0,7; 0,1; 0,1; 0,1]. Phân phối nào có entropy lớn nhất và giá trị đó là bao nhiêu bit?

- **A.** p₂, với entropy 1 bit, vì hai trạng thái có xác suất 0 làm giảm bậc tự do và tăng độ bất định.
- **B.** p₁, với entropy log₂ 4 = 2 bit, vì phân phối đều là phân phối có entropy lớn nhất trên K trạng thái.
- **C.** p₄, với entropy khoảng 1,36 bit, vì nó vừa có một trạng thái nổi trội vừa giữ được ba trạng thái hiếm.
- **D.** p₃, với entropy 4 bit, vì toàn bộ khối lượng dồn vào một trạng thái nên lượng thông tin của trạng thái đó lớn nhất.

## Câu 15 (Tự luận)

Vì sao MML nói chi phí tính gradient bằng backpropagation "có độ phức tạp tương đương với chi phí tính chính hàm số", dù biểu thức đạo hàm viết tường minh (công thức 5.110) dài hơn hàm gốc rất nhiều? Trình bày cơ chế tái sử dụng trong chuỗi ∂L/∂θᵢ.

## Câu 16 (Tự luận)

MML mô tả hiện tượng gradient descent "zigzag" trong thung lũng dài và hẹp. Hãy giải thích hiện tượng này bằng condition number, nêu hai heuristic điều chỉnh step size mà sách trích từ Toussaint (2012), và cho biết momentum thay đổi công thức cập nhật ra sao.

## Câu 17 (Tự luận)

Trong ước lượng MLE cho phân phối chuẩn một chiều (Vũ Hữu Tiệp, Ví dụ 3, Chương 4), kết quả cho µ và σ² là gì? Nêu hai lý do MML đưa ra cho việc lấy log của likelihood trước khi tối ưu, và liên hệ với cách bạn sẽ cài cross-entropy ở Tuần 4.

## Câu 18 (Tự luận)

Xem loss trên một minibatch như trung bình X̄ₙ của n biến độc lập cùng phân phối, kỳ vọng µ và phương sai σ². Durrett cho biết gì về E X̄ₙ, var(X̄ₙ) và về phân phối giới hạn của (Sₙ − nµ)/(σ√n)? Từ đó suy ra điều gì khi bạn tăng batch size từ 16 lên 64?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Theo RoFormer (arXiv 2104.09864) và cách MML định nghĩa góc giữa hai vector, vì sao xoay cả query và key theo vị trí lại làm điểm attention chỉ phụ thuộc khoảng cách tương đối?

- **A.** Vì RoPE cộng vector vị trí vào embedding như GPT-2
- **B.** Vì tích vô hướng của hai vector đã xoay góc mθ và nθ chỉ phụ thuộc hiệu góc (m−n)θ, do phép xoay bảo toàn độ dài và góc tương đối giữa hai vector
- **C.** Vì phép xoay làm mọi vector có cùng độ dài
- **D.** Vì key không bị xoay, chỉ query bị xoay

## Nâng cao 2 (Tự luận)

MacKay và Murphy đều định nghĩa KL divergence. Vì sao KL không phải một metric, và điều đó có nghĩa gì khi PPO dùng KL(policy ‖ reference) làm ràng buộc?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
