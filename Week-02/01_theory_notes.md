# Lý thuyết Tuần 2 — Backprop từ đầu + mental model Transformer

> Đọc file này trước khi tự build [`02_micrograd.py`](02_micrograd.py). Mọi ví dụ số đã chạy kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11 (tự chạy lại từng snippet). Nguồn dẫn ở cuối file — tất cả đã xác minh truy cập được cùng ngày.

---

## 1. Autograd engine — backprop không có gì huyền bí

### 1.1 Computation graph

Mọi biểu thức là một **đồ thị**: node = giá trị, cạnh = phép toán. Ví dụ `f = (a*b + c).tanh() * d`:

```
a ─┐
   ×──┐
b ─┘  +──tanh──┐
c ────┘        ×── f
d ─────────────┘
```

Forward đi xuôi tính giá trị. **Backward đi ngược, mỗi node nhân "grad từ trên rơi xuống" với đạo hàm cục bộ của phép toán tạo ra nó** (chain rule, ôn Tuần 1 mục 2.2) rồi đẩy tiếp xuống toán hạng.

### 1.2 Node `Value` cần đúng 4 thứ

Đây là toàn bộ thiết kế của micrograd (và về bản chất, của `torch.autograd`):

| Trường | Vai trò |
|--------|---------|
| `data` | giá trị số (forward) |
| `grad` | `∂output_cuối/∂self`, khởi tạo 0 |
| `_backward` | closure: cộng grad vào các toán hạng tạo ra node này |
| `_prev` | các node cha trực tiếp (để duyệt ngược) |

### 1.3 Đạo hàm cục bộ của từng phép — chỉ cần thuộc bảng này

Với `out` là kết quả và `g = out.grad` (grad từ trên rơi xuống):

| Phép | Forward | `_backward` (cộng dồn vào grad) |
|------|---------|------------------------------|
| `out = a + b` | `a.data + b.data` | `a.grad += 1·g`; `b.grad += 1·g` — phép cộng **phát** grad nguyên vẹn |
| `out = a * b` | `a.data * b.data` | `a.grad += b.data·g`; `b.grad += a.data·g` — grad chéo qua toán hạng kia |
| `out = tanh(a)` | `tanh(a.data)` | `a.grad += (1 − out.data²)·g` |
| `out = relu(a)` | `max(0, a.data)` | `a.grad += (1 if a.data > 0 else 0)·g` |

Kiểm chứng `tanh` bằng PyTorch (đã chạy 2026-08-11): tại `x = 0.5`, `tanh(x) = 0.4621`, autograd cho grad `0.7864`, đúng bằng `1 − 0.4621² = 0.7864`.

### 1.4 Vì sao là `+=` chứ không phải `=` — bug kinh điển nhất

Một node có thể được **dùng nhiều lần** (fan-out). Ví dụ `f = a * a`: node `a` xuất hiện ở cả hai toán hạng, mỗi nhánh đóng góp một phần đạo hàm, phải **cộng dồn**:

```python
a = torch.tensor(3., requires_grad=True)
f = a * a
f.backward()
a.grad    # 6.0 = a + a — hai nhánh cộng lại, không phải 3.0
```

Nếu `_backward` của bạn dùng `=`, biểu thức có node tái sử dụng sẽ ra grad sai **một cách im lặng**. Đây cũng chính là lý do PyTorch cộng dồn grad và bắt bạn `zero_grad()` mỗi step (Tuần 1, mục 2.3).

### 1.5 `backward()` toàn cục = topological sort + chain rule

1. Duyệt DFS từ node output, xếp mọi node theo **topological order** (con đứng sau cha).
2. Đặt `output.grad = 1.0` (vì `∂f/∂f = 1`).
3. Đi **ngược** danh sách topo, gọi `_backward()` của từng node.

Thứ tự topo bảo đảm khi một node phát grad xuống thì grad của chính nó đã được cộng đủ từ mọi nhánh phía trên. Sau khi điền xong TODO trong [`02_micrograd.py`](02_micrograd.py), chạy [`03_check_grad.py`](03_check_grad.py) — script so sánh grad của bạn với `torch.autograd` trên cùng biểu thức, khớp tới `1e-5` mới đạt.

---

## 2. makemore: bigram → neural net → MLP

Bài toán: sinh tên người từng ký tự một — tức một **language model tối giản**, cùng bản chất với GPT (Tuần 4–5) chỉ khác quy mô.

### 2.1 Bigram đếm (không học gì cả)

`P(ký_tự_kế | ký_tự_hiện_tại)`: đếm ma trận `N (27×27)` (26 chữ + token `.` đầu/cuối), chuẩn hóa từng hàng thành xác suất. Đánh giá bằng **NLL trung bình** = chính là cross-entropy Tuần 1: `−mean(log P(ký_tự_đúng))`. Dùng NLL chứ không dùng accuracy vì ta chấm cả **độ tự tin** của phân phối, không chỉ đoán trúng/trượt.

### 2.2 Bigram neural net — cùng model, học bằng gradient

Thay bảng đếm bằng ma trận trọng số `W (27×27)`:

```
one_hot(ký_tự) @ W → logits → softmax → P → NLL → backward → cập nhật W
```

Nhận xét then chốt: `one_hot(i) @ W` **chính là lấy hàng i của W** — phép "tra bảng embedding" chẳng qua là matmul với one-hot. Train hội tụ thì `W` tiến về đúng `log(N)` của phiên bản đếm — hai cách nhìn của cùng một model.

### 2.3 MLP theo Bengio 2003 — thêm ngữ cảnh, thêm embedding

Bigram chỉ nhìn 1 ký tự trước. Paper "A Neural Probabilistic Language Model" (Bengio et al., JMLR 2003 — link cuối file) đưa ra khung mà mọi LM hiện đại vẫn theo:

1. Mỗi ký tự → **embedding vector** (bảng tra `C (27×d)`, học được).
2. Ghép embedding của `k` ký tự ngữ cảnh → MLP → logits 27 lớp.
3. Vẫn cross-entropy + gradient descent.

Ghi kết quả NLL đo được của từng phiên bản vào [`04_makemore_notes.md`](04_makemore_notes.md) — số phải là số bạn tự đo, kèm ngày.

---

## 3. Mental model Transformer — dựng TRƯỚC khi code (Tuần 3)

### 3.1 Bức tranh một câu

Transformer xử lý chuỗi vector token **song song**. Mỗi layer, từng token "hỏi" mọi token khác (attention) rồi tự biến đổi (MLP). Attention trả lời: *"tôi nên trộn thông tin của những token nào, mỗi token bao nhiêu?"* — trọng số trộn tính từ dot product query·key (nền Tuần 1, mục 1.1), qua softmax (mục 3.1).

### 3.2 Permutation-equivariance — attention "mù" thứ tự

`W_Q, W_K, W_V` **dùng chung cho mọi vị trí**, và score `qᵢ·kⱼ` không chứa i, j. Hệ quả: **hoán vị token đầu vào thì output bị hoán vị đúng theo cách đó** (equivariant) — model không hề biết token nào đứng trước token nào.

Kiểm chứng bằng code (đã chạy 2026-08-11, `atol=1e-6`):

```python
def attn(x):                                   # self-attention tối giản
    return torch.softmax(x @ x.T, dim=-1) @ x

X = torch.randn(5, 8)
perm = torch.tensor([2, 0, 4, 1, 3])
torch.allclose(attn(X[perm]), attn(X)[perm])   # True — hoán vị input = hoán vị output
```

Phân biệt với **permutation-invariant** (sum, mean: đổi thứ tự input, output *không đổi*). Attention là equivariant, không phải invariant.

### 3.3 Vì thế cần positional information

"Chó cắn người" ≠ "người cắn chó", nhưng với attention thuần hai chuỗi này chỉ là hoán vị của nhau. Giải pháp: **tiêm thông tin vị trí vào input** — GPT-2 cộng positional embedding học được vào token embedding (bạn sẽ code ở Tuần 3); các model mới dùng RoPE (Tuần 3, mục nâng cao A1). Viết lại toàn bộ lập luận mục 3 này bằng lời mình vào [`05_attention_writeup.md`](05_attention_writeup.md) — đó là deliverable thứ hai của tuần.

---

## 4. Nguồn chính thức (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | License / loại | Dùng cho mục |
|-------|-----|----------------|--------------|
| karpathy/micrograd | https://github.com/karpathy/micrograd | MIT | 1 |
| karpathy/makemore | https://github.com/karpathy/makemore | MIT | 2 |
| Bengio et al. 2003 — A Neural Probabilistic Language Model | https://www.jmlr.org/papers/v3/bengio03a.html | JMLR truy cập mở | 2.3 |
| The Annotated Transformer (Harvard NLP) | https://nlp.seas.harvard.edu/annotated-transformer/ | web mở | 3 |
| Vaswani et al. 2017 — Attention Is All You Need | https://arxiv.org/abs/1706.03762 | arXiv mở | 3 |

## Sau khi đọc xong

1. Tự điền TODO trong [`02_micrograd.py`](02_micrograd.py) — dùng bảng đạo hàm mục 1.3, nhớ `+=`.
2. Chạy [`03_check_grad.py`](03_check_grad.py) đối chiếu PyTorch — khớp `1e-5` mới đạt.
3. Làm makemore theo [`04_makemore_notes.md`](04_makemore_notes.md), ghi NLL đo được.
4. Viết [`05_attention_writeup.md`](05_attention_writeup.md) bằng lời mình, nhờ Claude review.
5. Làm [`quiz.md`](quiz.md), đối chiếu [`quiz_solution.md`](quiz_solution.md).
