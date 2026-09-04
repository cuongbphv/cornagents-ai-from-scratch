# Tuần 5, Đáp án & Giải thích: Backprop từ đầu + mental model Transformer

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Trong micrograd, mỗi đối tượng Value lưu những gì và làm gì khi backward()?

**Trả lời mẫu:** Mỗi Value lưu: data (giá trị forward), grad (đạo hàm của output cuối theo nó, khởi tạo 0), và một hàm _backward() biết cách đẩy gradient về các 'cha' của nó. Forward dựng đồ thị; backward() sắp xếp topo các node, set grad của output = 1, rồi gọi _backward() theo thứ tự ngược để nhân dồn chain rule.

**Giải thích:** Đây là lõi của mọi autograd engine (kể cả PyTorch), chỉ khác quy mô.

## Câu 2 (Trắc nghiệm)

backward() duyệt đồ thị theo thứ tự nào?

- **A.** Thứ tự topo NGƯỢC (từ output về input) (đáp án đúng)
- **B.** Theo độ lớn của grad
- **C.** Thứ tự ngẫu nhiên
- **D.** Theo thứ tự khởi tạo biến

**Đáp án: A**

**Giải thích:** Phải xử lý một node sau khi đã cộng xong mọi gradient đến từ các node phía sau nó → duyệt topo ngược.

## Câu 3 (Tự luận)

Vì sao self-attention là 'permutation-equivariant' và điều đó buộc ta phải thêm gì?

**Trả lời mẫu:** Score giữa token i và j chỉ là q_i·k_j, không chứa thông tin vị trí; W_Q, W_K, W_V dùng chung cho mọi vị trí. Nếu hoán vị thứ tự token đầu vào, đầu ra hoán vị y hệt, model không phân biệt 'chó cắn người' với 'người cắn chó'. Vì vậy phải thêm positional encoding (absolute learned ở GPT-2, hoặc RoPE ở model hiện đại) để đưa thông tin thứ tự vào.

**Giải thích:** Đây là lý do tồn tại của positional embedding, không có nó, transformer mù thứ tự.

## Câu 4 (Trắc nghiệm)

Đạo hàm của tanh(x) là gì (hay gặp khi tự code backward)?

- **A.** e^x / (1+e^x)
- **B.** 1 - tanh^2(x) (đáp án đúng)
- **C.** tanh(x)
- **D.** x(1-x)

**Đáp án: B**

**Giải thích:** tanh'(x) = 1 - tanh^2(x). Tự viết local gradient cho tanh/relu/exp là bài tập cốt lõi của micrograd.

## Câu 5 (Trắc nghiệm)

Khi một biến được dùng ở NHIỀU nhánh của đồ thị, gradient của nó được xử lý thế nào?

- **A.** Lấy trung bình
- **B.** Lấy gradient lớn nhất
- **C.** Ghi đè bằng gradient cuối cùng
- **D.** Cộng dồn (+=) gradient từ tất cả các nhánh (đáp án đúng)

**Đáp án: D**

**Giải thích:** Theo quy tắc tổng của chain rule, gradient từ các đường khác nhau phải CỘNG dồn. Quên += (dùng =) là bug micrograd kinh điển.

## Câu 6 (Tự luận)

Bigram model trong makemore làm gì, và liên hệ thế nào với một mạng neural 1 lớp?

**Trả lời mẫu:** Bigram dự đoán ký tự tiếp theo chỉ dựa trên ký tự hiện tại. Bản 'đếm' xây ma trận tần suất (c_i → c_{i+1}) rồi chuẩn hoá thành xác suất. Bản neural tương đương: one-hot ký tự đầu vào @ một ma trận trọng số → logits → softmax; train bằng cross-entropy sẽ hội tụ về cùng phân phối với bản đếm. Đây là cầu nối từ thống kê đếm sang học bằng gradient.

**Giải thích:** Karpathy dùng bigram để cho thấy 'neural net' chỉ là cách tổng quát hoá của đếm tần suất.

## Câu 7 (Tự luận)

Bạn vừa điền xong _backward cho các phép trong micrograd nhưng chưa muốn phụ thuộc PyTorch để kiểm. Hãy mô tả cách dùng sai phân trung tâm của Tuần 2 để kiểm gradient của một Value, và nói vì sao nên kiểm bằng cách này trước khi chạy 03_check_grad.py.

**Trả lời mẫu:** Dựng biểu thức f từ các Value, gọi f.backward() để có a.grad. Rồi nhúc nhích a.data thêm ε (khoảng 1e-6), tính lại f thành f_plus; trừ ε, tính f_minus; so (f_plus − f_minus) / 2ε với a.grad, lệch dưới khoảng 1e-6 là khớp. Làm trước để tách hai nguồn lỗi: nếu sai phân khớp mà PyTorch lệch thì lỗi nằm ở cách gọi PyTorch trong 03_check_grad.py, còn nếu sai phân đã lệch thì lỗi nằm trong _backward của bạn.

**Giải thích:** Sai phân trung tâm là công cụ kiểm độc lập duy nhất không cần thư viện. Kỹ năng này dùng lại mỗi khi bạn tự viết một phép đạo hàm, kể cả ở Tuần 6 khi viết attention.

## Câu 8 (Trắc nghiệm)

Trong backward pass của UDL mục 7.4 với mạng ReLU, đạo hàm ∂h_3/∂f_2 của activation theo pre-activation được xử lý thế nào để cài đặt hiệu quả?

- **A.** Nó là ma trận đường chéo với 1 tại các vị trí f_2 > 0 và 0 ở nơi khác; thay vì nhân ma trận, ta rút vector đường chéo I[f_2 > 0] và nhân từng phần tử. (đáp án đúng)
- **B.** Nó là ma trận đầy đủ D_3 × D_3 phải nhân với Ω^T ở mỗi lớp, và Prince xem đây là bước tốn kém nhất của toàn bộ backward pass.
- **C.** Nó bằng hằng số 1 vì ReLU tuyến tính trên miền dương, nên đạo hàm này được bỏ qua và backward pass chỉ còn phép nhân với Ω^T.
- **D.** Nó là ma trận đường chéo với giá trị bằng chính f_2, vì đạo hàm ReLU tỉ lệ với độ lớn của pre-activation tại mỗi đơn vị ẩn.

**Đáp án: A**

**Giải thích:** Prince viết đạo hàm này "will be a diagonal matrix since each activation only depends on the corresponding pre-activation"; với ReLU các phần tử đường chéo là 0 nơi f_2 < 0 và 1 nơi khác (Figure 7.6), và "Rather than multiply by this matrix, we extract the diagonal terms as a vector I[f_2 > 0] and pointwise multiply, which is more efficient." Đây chính là phép ⊙ trong công thức 7.25 và là cách _backward của ReLU trong micrograd hoạt động. (UDL mục 7.4, tr. 105)

## Câu 9 (Trắc nghiệm)

UDL mục 7.4.1 kết luận backpropagation "extremely efficient" về tính toán nhưng nêu một nhược điểm. Nhược điểm đó là gì?

- **A.** Chỉ áp dụng được cho mạng tính toán tuần tự, không mở rộng được cho đồ thị tính toán có nhánh như residual connection.
- **B.** Không hiệu quả về bộ nhớ vì toàn bộ giá trị trung gian của forward pass phải được lưu lại, điều này có thể giới hạn kích cỡ model có thể train. (đáp án đúng)
- **C.** Tốn tính toán vì mỗi lớp cần nhân ma trận hai lần trong backward pass, nên chi phí gấp đôi forward pass và tăng theo độ sâu mạng.
- **D.** Không ổn định về số học vì phép nhân với ma trận chuyển vị Ω^T làm mất độ chính xác số thực ở các lớp sâu của mạng.

**Đáp án: B**

**Giải thích:** Prince viết bước tốn nhất của cả forward và backward pass chỉ là nhân ma trận (với Ω và Ω^T), nhưng "it is not memory efficient; the intermediate values in the forward pass must all be stored, and this can limit the size of the model we can train." Lựa chọn về đồ thị có nhánh sai vì mục 7.4.3 nói backprop vẫn áp dụng cho mọi đồ thị tính toán không có chu trình. Đây là gốc của lỗi hết VRAM khi tăng batch hay độ dài chuỗi. (UDL mục 7.4.1, tr. 106)

## Câu 10 (Trắc nghiệm)

He initialization trong UDL mục 7.5.1 đặt phương sai trọng số σ²_Ω = 2/D_h. Hệ số 2 trong công thức này đến từ đâu?

- **A.** Vì bias được khởi tạo bằng 0 nên mất đi một nửa nguồn phương sai của pre-activation, và phương sai trọng số phải gấp đôi để bù lại.
- **B.** Vì có hai ma trận trọng số (một cho forward, một cho backward) cần cân bằng, nên phương sai được nhân đôi để bù cho cả hai chiều.
- **C.** Vì ReLU cắt bỏ khoảng nửa số pre-activation, nên moment bậc hai E[h_j²] chỉ bằng nửa phương sai σ²_f; hệ số 2 bù lại để phương sai giữ nguyên qua lớp. (đáp án đúng)
- **D.** Vì mỗi lớp có D_h đầu vào và D_h đầu ra, tổng cộng 2D_h kết nối, và phương sai được chia đều cho toàn bộ số kết nối đó để cân bằng hai phía.

**Đáp án: C**

**Giải thích:** Prince giả sử phân phối pre-activation ở lớp trước đối xứng quanh 0, nên "half of these pre-activations will be clipped by the ReLU function, and the second moment E[h_j²] will be half the variance σ²_f"; từ đó σ²_{f'} = (1/2) D_h σ²_Ω σ²_f (công thức 7.31). Muốn phương sai không đổi qua lớp thì σ²_Ω = 2/D_h (công thức 7.32), gọi là He initialization. (UDL mục 7.5.1, tr. 110)

## Câu 11 (Trắc nghiệm)

Bishop (PRML mục 5.3.3) so sánh backpropagation với sai phân hữu hạn để tính gradient. Theo Bishop, vì sao không dùng sai phân hữu hạn khi huấn luyện, nhưng nó vẫn giữ một vai trò quan trọng trong thực hành?

- **A.** Vì sai phân cần O(W²) phép tính do phải nhiễu từng trọng số riêng lẻ, còn backprop chỉ O(W); nhưng so với sai phân trung tâm là cách kiểm tra mạnh cho code backprop. (đáp án đúng)
- **B.** Vì sai phân chỉ tính được đạo hàm theo đầu vào chứ không theo trọng số, nên nó chỉ hữu ích để tính ma trận Jacobian của một mạng đã huấn luyện xong.
- **C.** Vì sai phân đòi hỏi lưu toàn bộ giá trị trung gian giống backprop nhưng chậm gấp đôi, nên chỉ được dùng để kiểm tra khi bộ nhớ GPU còn dư nhiều.
- **D.** Vì sai phân có sai số O(ε) không thể giảm thêm dù chọn ε nhỏ, nên nó chỉ được dùng cho các hàm kích hoạt không khả vi tại một điểm như ReLU.

**Đáp án: A**

**Giải thích:** Bishop viết mỗi forward propagation tốn O(W) và có W trọng số phải nhiễu riêng lẻ, "so that the overall scaling is O(W²)"; sai phân trung tâm (công thức 5.69) có sai số O(ε²) chứ không phải O(ε) không giảm được. Tuy vậy "a comparison of the derivatives calculated by backpropagation with those obtained using central differences provides a powerful check on the correctness of any software implementation of the backpropagation algorithm". Đây là phép kiểm gradient bạn dùng cho micrograd. (Bishop mục 5.3.3, tr. 247)

## Câu 12 (Trắc nghiệm)

MML mục 5.6.2 trình bày automatic differentiation có forward mode và reverse mode. Hai chế độ khác nhau ở điểm nào, và vì sao huấn luyện mạng neural dùng reverse mode?

- **A.** Hai chế độ chỉ khác thứ tự nhân các Jacobian nhờ tính kết hợp của phép nhân ma trận; khi chiều đầu vào lớn hơn nhiều chiều nhãn, reverse mode rẻ hơn hẳn. (đáp án đúng)
- **B.** Reverse mode cho kết quả chính xác hơn về số học, còn forward mode tích lũy sai số làm tròn qua từng lớp nên không dùng được cho các mạng sâu nhiều lớp.
- **C.** Reverse mode không cần lưu giá trị trung gian của forward pass, trong khi forward mode phải lưu toàn bộ đồ thị tính toán nên tốn bộ nhớ hơn.
- **D.** Forward mode chỉ áp dụng cho hàm một biến còn reverse mode cho hàm nhiều biến; mạng neural có rất nhiều tham số nên bắt buộc dùng reverse mode.

**Đáp án: A**

**Giải thích:** MML viết "the forward and reverse mode differ in the order of multiplication. Due to the associativity of matrix multiplication" ta có thể nhóm (dy/db · db/da) · da/dx (reverse, công thức 5.120) hoặc dy/db · (db/da · da/dx) (forward, 5.121); reverse mode lan truyền gradient ngược chiều dòng dữ liệu. Với mạng neural, "where the input dimensionality is often much higher than the dimensionality of the labels, the reverse mode is computationally significantly cheaper than the forward mode". (MML mục 5.6.2, tr. 162)

## Câu 13 (Trắc nghiệm)

Theo công thức (5.53) của Bishop, đạo hàm ∂E_n/∂w_ji của lỗi theo một trọng số trong mạng feed-forward bằng gì?

- **A.** Hiệu y_j - t_j nhân với w_ji, một công thức áp dụng chung cho cả đơn vị ẩn lẫn đơn vị đầu ra của mạng.
- **B.** Tổng các δ_k của mọi đơn vị k mà đơn vị j gửi kết nối tới, nhân với h'(a_j), và không phụ thuộc vào activation z_i.
- **C.** Tích của δ_j (lỗi tại đơn vị ở đầu ra của kết nối) với z_i (activation ở đầu vào của kết nối), cùng dạng với model tuyến tính. (đáp án đúng)
- **D.** Tích của δ_i ở đầu vào của kết nối với z_j ở đầu ra của kết nối, vì tín hiệu lỗi được nhân ngược chiều dòng dữ liệu.

**Đáp án: C**

**Giải thích:** Bishop định nghĩa δ_j ≡ ∂E_n/∂a_j (5.51), có ∂a_j/∂w_ji = z_i (5.52), suy ra ∂E_n/∂w_ji = δ_j z_i (5.53): "the required derivative is obtained simply by multiplying the value of δ for the unit at the output end of the weight by the value of z for the unit at the input end of the weight". Lựa chọn về tổng Σ w_kj δ_k nhân h'(a_j) là công thức tính δ_j cho đơn vị ẩn (5.56), không phải đạo hàm theo trọng số. Trong micrograd, đây là _backward của phép nhân: grad của trọng số bằng grad đầu ra nhân giá trị đầu vào. (Bishop mục 5.3.1, tr. 243)

## Câu 14 (Tự luận)

Trong Example 5.14 của MML, biến trung gian c = a + b được dùng bởi cả d = sqrt(c) và e = cos(c). Hãy viết ∂f/∂c theo chain rule như MML và giải thích vì sao micrograd phải dùng `self.grad +=` thay vì `self.grad =` trong _backward.

**Trả lời mẫu:** Vì c có hai node con d và e, ∂f/∂c = (∂f/∂d)(∂d/∂c) + (∂f/∂e)(∂e/∂c) = 1 · 1/(2 sqrt(c)) + 1 · (-sin c). Tổng quát, gradient của một biến bằng tổng đóng góp qua mọi node con có nó làm parent. Trong micrograd, mỗi node con gọi _backward riêng và cộng phần đóng góp của mình vào grad của parent; nếu dùng phép gán thì phần của node con chạy trước sẽ bị ghi đè, cho gradient sai.

**Giải thích:** MML viết ∂f/∂c = (∂f/∂d)(∂d/∂c) + (∂f/∂e)(∂e/∂c) (công thức 5.135) và sau khi thay đạo hàm cơ bản: ∂f/∂c = 1 · 1/(2√c) + 1 · (-sin(c)) (5.139). Công thức tổng quát 5.145 viết ∂f/∂x_i là tổng trên mọi x_j có x_i thuộc Pa(x_j). Vì thế gradient tại một node là tổng theo các node con, ứng với phép cộng dồn trong micrograd. (MML mục 5.6.2, tr. 163)

## Câu 15 (Tự luận)

Figure 7.7 của UDL xét mạng 50 lớp ẩn, D_h = 100 đơn vị mỗi lớp, đầu vào chuẩn tắc, khởi tạo trọng số theo phân phối chuẩn với năm phương sai σ²_Ω thuộc {0.001, 0.01, 0.02, 0.1, 1.0}. Mô tả điều xảy ra với phương sai activation ở forward pass và phương sai gradient ở backward pass cho ba trường hợp σ²_Ω = 0.02, lớn hơn 0.02, nhỏ hơn 0.02, và nêu tên hai hiện tượng tương ứng.

**Trả lời mẫu:** Với σ²_Ω = 2/D_h = 0.02 (He initialization) phương sai activation giữ ổn định qua các lớp. Với giá trị lớn hơn (0.1, 1.0) phương sai tăng nhanh theo độ sâu; với giá trị nhỏ hơn (0.01, 0.001) phương sai giảm nhanh (trục log). Backward pass tiếp tục đúng xu hướng đó: khởi tạo lớn hơn 0.02 làm độ lớn gradient tăng nhanh khi đi ngược về các lớp đầu (exploding gradient), khởi tạo nhỏ hơn làm gradient teo dần (vanishing gradient).

**Giải thích:** Chú thích Figure 7.7: "For He initialization (σ²_Ω = 2/D_h = 0.02), the variance is stable. However, for larger values, it increases rapidly, and for smaller values, it decreases rapidly (note log scale)"; phương sai gradient ở backward pass "continues this trend", và hai trường hợp được gọi là "the exploding gradient and vanishing gradient problems, respectively". Đây là lý do bạn phải chọn std khởi tạo cho nn.Linear trong GPT của mình thay vì để ngẫu nhiên tùy ý. (UDL mục 7.5, tr. 110)

## Câu 16 (Tự luận)

Bishop (PRML mục 5.3) nhấn mạnh thuật ngữ backpropagation trong tài liệu neural network được dùng với nhiều nghĩa khác nhau, và ông tách quá trình huấn luyện thành hai giai đoạn riêng biệt. Hai giai đoạn đó là gì, Bishop dùng chữ backpropagation cho giai đoạn nào, và chúng tương ứng với dòng lệnh nào trong training loop micrograd hoặc PyTorch của bạn?

**Trả lời mẫu:** Giai đoạn một: tính đạo hàm của hàm lỗi theo trọng số, bằng cách lan truyền lỗi ngược qua mạng; Bishop dành riêng chữ backpropagation cho giai đoạn này. Giai đoạn hai: dùng các đạo hàm đó để tính lượng điều chỉnh trọng số, ví dụ bằng gradient descent (Rumelhart et al. 1986) hoặc các phương pháp tối ưu mạnh hơn. Trong code, giai đoạn một là loss.backward() (điền .grad), giai đoạn hai là vòng cập nhật p.data -= lr * p.grad hay optimizer.step(). Bishop lưu ý hai giai đoạn độc lập: backprop áp dụng được cho nhiều loại mạng và hàm lỗi khác, còn bước cập nhật có thể thay bằng optimizer bất kỳ.

**Giải thích:** Bishop viết: "In the first stage, the derivatives of the error function with respect to the weights must be evaluated ... we shall use the term backpropagation specifically to describe the evaluation of derivatives. In the second stage, the derivatives are then used to compute the adjustments to be made to the weights." Ông nhấn mạnh "It is important to recognize that the two stages are distinct" và giai đoạn hai có thể dùng "a variety of optimization schemes, many of which are substantially more powerful than simple gradient descent". (Bishop mục 5.3, tr. 241)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Backward của micrograd duyệt đồ thị theo thứ tự topo đảo ngược. Vì sao thứ tự này là bắt buộc, không chỉ là tiện?

- **A.** Vì Python yêu cầu duyệt tập hợp theo thứ tự
- **B.** Vì tanh chỉ khả vi theo thứ tự đó
- **C.** Vì thứ tự topo giúp giảm bộ nhớ
- **D.** Vì khi một node phát gradient xuống toán hạng, gradient của chính nó phải đã được cộng đủ từ mọi nhánh phía trên; thứ tự topo đảo ngược bảo toàn điều đó (đáp án đúng)

**Đáp án: D**

**Giải thích:** Đây là chain rule trên đồ thị (MML mục 5.6, trang 159; UDL mục 7.4, trang 103). Nếu một node có fan-out và bạn duyệt sai thứ tự, nó sẽ phát gradient chưa đầy đủ xuống dưới.

## Nâng cao 2 (Tự luận)

Weight tying trong nanoGPT gán wte.weight = lm_head.weight. Hãy giải thích ảnh hưởng lên số tham số và lên gradient của ma trận embedding.

**Trả lời mẫu:** Số tham số giảm đúng bằng vocab_size × d vì chỉ còn một ma trận; khi đếm tham số GPT-2 124M ở Tuần 7 không được đếm hai lần. Về gradient, ma trận này nhận gradient từ hai đường: đường embedding (input) và đường unembedding (logits), và autograd cộng dồn hai phần đó, đúng cơ chế += của micrograd với node dùng ở nhiều nhánh.

**Giải thích:** Dòng code kiểm trên repo karpathy/nanoGPT ngày 2026-09-04: self.transformer.wte.weight = self.lm_head.weight.
