# Tuần 5, Đáp án & Giải thích: Backprop từ đầu + mental model Transformer

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Trong micrograd, mỗi đối tượng Value lưu những gì và làm gì khi backward()?

**Trả lời mẫu:** Mỗi Value lưu: data (giá trị forward), grad (đạo hàm của output cuối theo nó, khởi tạo 0), và một hàm _backward() biết cách đẩy gradient về các 'cha' của nó. Forward dựng đồ thị; backward() sắp xếp topo các node, set grad của output = 1, rồi gọi _backward() theo thứ tự ngược để nhân dồn chain rule.

**Giải thích:** Đây là lõi của mọi autograd engine (kể cả PyTorch), chỉ khác quy mô.

## Câu 2 (Trắc nghiệm)

backward() duyệt đồ thị theo thứ tự nào?

- **A.** Thứ tự ngẫu nhiên
- **B.** Thứ tự topo NGƯỢC (từ output về input) (đáp án đúng)
- **C.** Theo thứ tự khởi tạo biến
- **D.** Theo độ lớn của grad

**Đáp án: B**

**Giải thích:** Phải xử lý một node sau khi đã cộng xong mọi gradient đến từ các node phía sau nó → duyệt topo ngược.

## Câu 3 (Tự luận)

Vì sao self-attention là 'permutation-equivariant' và điều đó buộc ta phải thêm gì?

**Trả lời mẫu:** Score giữa token i và j chỉ là q_i·k_j, không chứa thông tin vị trí; W_Q, W_K, W_V dùng chung cho mọi vị trí. Nếu hoán vị thứ tự token đầu vào, đầu ra hoán vị y hệt, model không phân biệt 'chó cắn người' với 'người cắn chó'. Vì vậy phải thêm positional encoding (absolute learned ở GPT-2, hoặc RoPE ở model hiện đại) để đưa thông tin thứ tự vào.

**Giải thích:** Đây là lý do tồn tại của positional embedding, không có nó, transformer mù thứ tự.

## Câu 4 (Trắc nghiệm)

Đạo hàm của tanh(x) là gì (hay gặp khi tự code backward)?

- **A.** tanh(x)
- **B.** 1 - tanh^2(x) (đáp án đúng)
- **C.** x(1-x)
- **D.** e^x / (1+e^x)

**Đáp án: B**

**Giải thích:** tanh'(x) = 1 - tanh^2(x). Tự viết local gradient cho tanh/relu/exp là bài tập cốt lõi của micrograd.

## Câu 5 (Trắc nghiệm)

Khi một biến được dùng ở NHIỀU nhánh của đồ thị, gradient của nó được xử lý thế nào?

- **A.** Lấy gradient lớn nhất
- **B.** Cộng dồn (+=) gradient từ tất cả các nhánh (đáp án đúng)
- **C.** Ghi đè bằng gradient cuối cùng
- **D.** Lấy trung bình

**Đáp án: B**

**Giải thích:** Theo quy tắc tổng của chain rule, gradient từ các đường khác nhau phải CỘNG dồn. Quên += (dùng =) là bug micrograd kinh điển.

## Câu 6 (Tự luận)

Bigram model trong makemore làm gì, và liên hệ thế nào với một mạng neural 1 lớp?

**Trả lời mẫu:** Bigram dự đoán ký tự tiếp theo chỉ dựa trên ký tự hiện tại. Bản 'đếm' xây ma trận tần suất (c_i → c_{i+1}) rồi chuẩn hoá thành xác suất. Bản neural tương đương: one-hot ký tự đầu vào @ một ma trận trọng số → logits → softmax; train bằng cross-entropy sẽ hội tụ về cùng phân phối với bản đếm. Đây là cầu nối từ thống kê đếm sang học bằng gradient.

**Giải thích:** Karpathy dùng bigram để cho thấy 'neural net' chỉ là cách tổng quát hoá của đếm tần suất.

## Câu 7 (Tự luận)

Bạn vừa điền xong _backward cho các phép trong micrograd nhưng chưa muốn phụ thuộc PyTorch để kiểm. Hãy mô tả cách dùng sai phân trung tâm của Tuần 2 để kiểm gradient của một Value, và nói vì sao nên kiểm bằng cách này trước khi chạy 03_check_grad.py.

**Trả lời mẫu:** Dựng biểu thức f từ các Value, gọi f.backward() để có a.grad. Rồi nhúc nhích a.data thêm ε (khoảng 1e-6), tính lại f thành f_plus; trừ ε, tính f_minus; so (f_plus − f_minus) / 2ε với a.grad, lệch dưới khoảng 1e-6 là khớp. Làm trước để tách hai nguồn lỗi: nếu sai phân khớp mà PyTorch lệch thì lỗi nằm ở cách gọi PyTorch trong 03_check_grad.py, còn nếu sai phân đã lệch thì lỗi nằm trong _backward của bạn.

**Giải thích:** Sai phân trung tâm là công cụ kiểm độc lập duy nhất không cần thư viện. Kỹ năng này dùng lại mỗi khi bạn tự viết một phép đạo hàm, kể cả ở Tuần 6 khi viết attention.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Backward của micrograd duyệt đồ thị theo thứ tự topo đảo ngược. Vì sao thứ tự này là bắt buộc, không chỉ là tiện?

- **A.** Vì Python yêu cầu duyệt tập hợp theo thứ tự
- **B.** Vì khi một node phát gradient xuống toán hạng, gradient của chính nó phải đã được cộng đủ từ mọi nhánh phía trên; thứ tự topo đảo ngược bảo toàn điều đó (đáp án đúng)
- **C.** Vì thứ tự topo giúp giảm bộ nhớ
- **D.** Vì tanh chỉ khả vi theo thứ tự đó

**Đáp án: B**

**Giải thích:** Đây là chain rule trên đồ thị (MML mục 5.6, trang 159; UDL mục 7.4, trang 103). Nếu một node có fan-out và bạn duyệt sai thứ tự, nó sẽ phát gradient chưa đầy đủ xuống dưới.

## Nâng cao 2 (Tự luận)

Weight tying trong nanoGPT gán wte.weight = lm_head.weight. Hãy giải thích ảnh hưởng lên số tham số và lên gradient của ma trận embedding.

**Trả lời mẫu:** Số tham số giảm đúng bằng vocab_size × d vì chỉ còn một ma trận; khi đếm tham số GPT-2 124M ở Tuần 7 không được đếm hai lần. Về gradient, ma trận này nhận gradient từ hai đường: đường embedding (input) và đường unembedding (logits), và autograd cộng dồn hai phần đó, đúng cơ chế += của micrograd với node dùng ở nhiều nhánh.

**Giải thích:** Dòng code kiểm trên repo karpathy/nanoGPT ngày 2026-09-04: self.transformer.wte.weight = self.lm_head.weight.
