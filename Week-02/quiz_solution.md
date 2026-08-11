# Tuần 2 — Đáp án & Giải thích: Backprop từ đầu + mental model Transformer

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Trong micrograd, mỗi đối tượng Value lưu những gì và làm gì khi backward()?

**Trả lời mẫu:** Mỗi Value lưu: data (giá trị forward), grad (đạo hàm của output cuối theo nó, khởi tạo 0), và một hàm _backward() biết cách đẩy gradient về các 'cha' của nó. Forward dựng đồ thị; backward() sắp xếp topo các node, set grad của output = 1, rồi gọi _backward() theo thứ tự ngược để nhân dồn chain rule.

**Giải thích:** Đây là lõi của mọi autograd engine (kể cả PyTorch), chỉ khác quy mô.

## Câu 2 (Trắc nghiệm)

backward() duyệt đồ thị theo thứ tự nào?

- **A.** Thứ tự ngẫu nhiên
- **B.** Thứ tự topo NGƯỢC (từ output về input) ✅
- **C.** Theo thứ tự khởi tạo biến
- **D.** Theo độ lớn của grad

**Đáp án: B**

**Giải thích:** Phải xử lý một node sau khi đã cộng xong mọi gradient đến từ các node phía sau nó → duyệt topo ngược.

## Câu 3 (Tự luận)

Vì sao self-attention là 'permutation-equivariant' và điều đó buộc ta phải thêm gì?

**Trả lời mẫu:** Score giữa token i và j chỉ là q_i·k_j, không chứa thông tin vị trí; W_Q, W_K, W_V dùng chung cho mọi vị trí. Nếu hoán vị thứ tự token đầu vào, đầu ra hoán vị y hệt — model không phân biệt 'chó cắn người' với 'người cắn chó'. Vì vậy phải thêm positional encoding (absolute learned ở GPT-2, hoặc RoPE ở model hiện đại) để đưa thông tin thứ tự vào.

**Giải thích:** Đây là lý do tồn tại của positional embedding — không có nó, transformer mù thứ tự.

## Câu 4 (Trắc nghiệm)

Đạo hàm của tanh(x) là gì (hay gặp khi tự code backward)?

- **A.** tanh(x)
- **B.** 1 - tanh^2(x) ✅
- **C.** x(1-x)
- **D.** e^x / (1+e^x)

**Đáp án: B**

**Giải thích:** tanh'(x) = 1 - tanh^2(x). Tự viết local gradient cho tanh/relu/exp là bài tập cốt lõi của micrograd.

## Câu 5 (Trắc nghiệm)

Khi một biến được dùng ở NHIỀU nhánh của đồ thị, gradient của nó được xử lý thế nào?

- **A.** Lấy gradient lớn nhất
- **B.** Cộng dồn (+=) gradient từ tất cả các nhánh ✅
- **C.** Ghi đè bằng gradient cuối cùng
- **D.** Lấy trung bình

**Đáp án: B**

**Giải thích:** Theo quy tắc tổng của chain rule, gradient từ các đường khác nhau phải CỘNG dồn. Quên += (dùng =) là bug micrograd kinh điển.

## Câu 6 (Tự luận)

Bigram model trong makemore làm gì, và liên hệ thế nào với một mạng neural 1 lớp?

**Trả lời mẫu:** Bigram dự đoán ký tự tiếp theo chỉ dựa trên ký tự hiện tại. Bản 'đếm' xây ma trận tần suất (c_i → c_{i+1}) rồi chuẩn hoá thành xác suất. Bản neural tương đương: one-hot ký tự đầu vào @ một ma trận trọng số → logits → softmax; train bằng cross-entropy sẽ hội tụ về cùng phân phối với bản đếm. Đây là cầu nối từ thống kê đếm sang học bằng gradient.

**Giải thích:** Karpathy dùng bigram để cho thấy 'neural net' chỉ là cách tổng quát hoá của đếm tần suất.
