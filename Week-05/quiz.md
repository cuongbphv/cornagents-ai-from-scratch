# Tuần 5, Quiz: Backprop từ đầu + mental model Transformer

> Tự kiểm tra **trước** khi xem solution. Tổng **18** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Trong micrograd, mỗi đối tượng Value lưu những gì và làm gì khi backward()?

## Câu 2 (Trắc nghiệm)

backward() duyệt đồ thị theo thứ tự nào?

- **A.** Thứ tự topo NGƯỢC (từ output về input)
- **B.** Theo độ lớn của grad
- **C.** Thứ tự ngẫu nhiên
- **D.** Theo thứ tự khởi tạo biến

## Câu 3 (Tự luận)

Vì sao self-attention là 'permutation-equivariant' và điều đó buộc ta phải thêm gì?

## Câu 4 (Trắc nghiệm)

Đạo hàm của tanh(x) là gì (hay gặp khi tự code backward)?

- **A.** e^x / (1+e^x)
- **B.** 1 - tanh^2(x)
- **C.** tanh(x)
- **D.** x(1-x)

## Câu 5 (Trắc nghiệm)

Khi một biến được dùng ở NHIỀU nhánh của đồ thị, gradient của nó được xử lý thế nào?

- **A.** Lấy trung bình
- **B.** Lấy gradient lớn nhất
- **C.** Ghi đè bằng gradient cuối cùng
- **D.** Cộng dồn (+=) gradient từ tất cả các nhánh

## Câu 6 (Tự luận)

Bigram model trong makemore làm gì, và liên hệ thế nào với một mạng neural 1 lớp?

## Câu 7 (Tự luận)

Bạn vừa điền xong _backward cho các phép trong micrograd nhưng chưa muốn phụ thuộc PyTorch để kiểm. Hãy mô tả cách dùng sai phân trung tâm của Tuần 2 để kiểm gradient của một Value, và nói vì sao nên kiểm bằng cách này trước khi chạy 03_check_grad.py.

## Câu 8 (Trắc nghiệm)

Trong backward pass của UDL mục 7.4 với mạng ReLU, đạo hàm ∂h_3/∂f_2 của activation theo pre-activation được xử lý thế nào để cài đặt hiệu quả?

- **A.** Nó là ma trận đường chéo với 1 tại các vị trí f_2 > 0 và 0 ở nơi khác; thay vì nhân ma trận, ta rút vector đường chéo I[f_2 > 0] và nhân từng phần tử.
- **B.** Nó là ma trận đầy đủ D_3 × D_3 phải nhân với Ω^T ở mỗi lớp, và Prince xem đây là bước tốn kém nhất của toàn bộ backward pass.
- **C.** Nó bằng hằng số 1 vì ReLU tuyến tính trên miền dương, nên đạo hàm này được bỏ qua và backward pass chỉ còn phép nhân với Ω^T.
- **D.** Nó là ma trận đường chéo với giá trị bằng chính f_2, vì đạo hàm ReLU tỉ lệ với độ lớn của pre-activation tại mỗi đơn vị ẩn.

## Câu 9 (Trắc nghiệm)

UDL mục 7.4.1 kết luận backpropagation "extremely efficient" về tính toán nhưng nêu một nhược điểm. Nhược điểm đó là gì?

- **A.** Chỉ áp dụng được cho mạng tính toán tuần tự, không mở rộng được cho đồ thị tính toán có nhánh như residual connection.
- **B.** Không hiệu quả về bộ nhớ vì toàn bộ giá trị trung gian của forward pass phải được lưu lại, điều này có thể giới hạn kích cỡ model có thể train.
- **C.** Tốn tính toán vì mỗi lớp cần nhân ma trận hai lần trong backward pass, nên chi phí gấp đôi forward pass và tăng theo độ sâu mạng.
- **D.** Không ổn định về số học vì phép nhân với ma trận chuyển vị Ω^T làm mất độ chính xác số thực ở các lớp sâu của mạng.

## Câu 10 (Trắc nghiệm)

He initialization trong UDL mục 7.5.1 đặt phương sai trọng số σ²_Ω = 2/D_h. Hệ số 2 trong công thức này đến từ đâu?

- **A.** Vì bias được khởi tạo bằng 0 nên mất đi một nửa nguồn phương sai của pre-activation, và phương sai trọng số phải gấp đôi để bù lại.
- **B.** Vì có hai ma trận trọng số (một cho forward, một cho backward) cần cân bằng, nên phương sai được nhân đôi để bù cho cả hai chiều.
- **C.** Vì ReLU cắt bỏ khoảng nửa số pre-activation, nên moment bậc hai E[h_j²] chỉ bằng nửa phương sai σ²_f; hệ số 2 bù lại để phương sai giữ nguyên qua lớp.
- **D.** Vì mỗi lớp có D_h đầu vào và D_h đầu ra, tổng cộng 2D_h kết nối, và phương sai được chia đều cho toàn bộ số kết nối đó để cân bằng hai phía.

## Câu 11 (Trắc nghiệm)

Bishop (PRML mục 5.3.3) so sánh backpropagation với sai phân hữu hạn để tính gradient. Theo Bishop, vì sao không dùng sai phân hữu hạn khi huấn luyện, nhưng nó vẫn giữ một vai trò quan trọng trong thực hành?

- **A.** Vì sai phân cần O(W²) phép tính do phải nhiễu từng trọng số riêng lẻ, còn backprop chỉ O(W); nhưng so với sai phân trung tâm là cách kiểm tra mạnh cho code backprop.
- **B.** Vì sai phân chỉ tính được đạo hàm theo đầu vào chứ không theo trọng số, nên nó chỉ hữu ích để tính ma trận Jacobian của một mạng đã huấn luyện xong.
- **C.** Vì sai phân đòi hỏi lưu toàn bộ giá trị trung gian giống backprop nhưng chậm gấp đôi, nên chỉ được dùng để kiểm tra khi bộ nhớ GPU còn dư nhiều.
- **D.** Vì sai phân có sai số O(ε) không thể giảm thêm dù chọn ε nhỏ, nên nó chỉ được dùng cho các hàm kích hoạt không khả vi tại một điểm như ReLU.

## Câu 12 (Trắc nghiệm)

MML mục 5.6.2 trình bày automatic differentiation có forward mode và reverse mode. Hai chế độ khác nhau ở điểm nào, và vì sao huấn luyện mạng neural dùng reverse mode?

- **A.** Hai chế độ chỉ khác thứ tự nhân các Jacobian nhờ tính kết hợp của phép nhân ma trận; khi chiều đầu vào lớn hơn nhiều chiều nhãn, reverse mode rẻ hơn hẳn.
- **B.** Reverse mode cho kết quả chính xác hơn về số học, còn forward mode tích lũy sai số làm tròn qua từng lớp nên không dùng được cho các mạng sâu nhiều lớp.
- **C.** Reverse mode không cần lưu giá trị trung gian của forward pass, trong khi forward mode phải lưu toàn bộ đồ thị tính toán nên tốn bộ nhớ hơn.
- **D.** Forward mode chỉ áp dụng cho hàm một biến còn reverse mode cho hàm nhiều biến; mạng neural có rất nhiều tham số nên bắt buộc dùng reverse mode.

## Câu 13 (Trắc nghiệm)

Theo công thức (5.53) của Bishop, đạo hàm ∂E_n/∂w_ji của lỗi theo một trọng số trong mạng feed-forward bằng gì?

- **A.** Hiệu y_j - t_j nhân với w_ji, một công thức áp dụng chung cho cả đơn vị ẩn lẫn đơn vị đầu ra của mạng.
- **B.** Tổng các δ_k của mọi đơn vị k mà đơn vị j gửi kết nối tới, nhân với h'(a_j), và không phụ thuộc vào activation z_i.
- **C.** Tích của δ_j (lỗi tại đơn vị ở đầu ra của kết nối) với z_i (activation ở đầu vào của kết nối), cùng dạng với model tuyến tính.
- **D.** Tích của δ_i ở đầu vào của kết nối với z_j ở đầu ra của kết nối, vì tín hiệu lỗi được nhân ngược chiều dòng dữ liệu.

## Câu 14 (Tự luận)

Trong Example 5.14 của MML, biến trung gian c = a + b được dùng bởi cả d = sqrt(c) và e = cos(c). Hãy viết ∂f/∂c theo chain rule như MML và giải thích vì sao micrograd phải dùng `self.grad +=` thay vì `self.grad =` trong _backward.

## Câu 15 (Tự luận)

Figure 7.7 của UDL xét mạng 50 lớp ẩn, D_h = 100 đơn vị mỗi lớp, đầu vào chuẩn tắc, khởi tạo trọng số theo phân phối chuẩn với năm phương sai σ²_Ω thuộc {0.001, 0.01, 0.02, 0.1, 1.0}. Mô tả điều xảy ra với phương sai activation ở forward pass và phương sai gradient ở backward pass cho ba trường hợp σ²_Ω = 0.02, lớn hơn 0.02, nhỏ hơn 0.02, và nêu tên hai hiện tượng tương ứng.

## Câu 16 (Tự luận)

Bishop (PRML mục 5.3) nhấn mạnh thuật ngữ backpropagation trong tài liệu neural network được dùng với nhiều nghĩa khác nhau, và ông tách quá trình huấn luyện thành hai giai đoạn riêng biệt. Hai giai đoạn đó là gì, Bishop dùng chữ backpropagation cho giai đoạn nào, và chúng tương ứng với dòng lệnh nào trong training loop micrograd hoặc PyTorch của bạn?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Backward của micrograd duyệt đồ thị theo thứ tự topo đảo ngược. Vì sao thứ tự này là bắt buộc, không chỉ là tiện?

- **A.** Vì Python yêu cầu duyệt tập hợp theo thứ tự
- **B.** Vì tanh chỉ khả vi theo thứ tự đó
- **C.** Vì thứ tự topo giúp giảm bộ nhớ
- **D.** Vì khi một node phát gradient xuống toán hạng, gradient của chính nó phải đã được cộng đủ từ mọi nhánh phía trên; thứ tự topo đảo ngược bảo toàn điều đó

## Nâng cao 2 (Tự luận)

Weight tying trong nanoGPT gán wte.weight = lm_head.weight. Hãy giải thích ảnh hưởng lên số tham số và lên gradient của ma trận embedding.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
