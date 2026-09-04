# Lý thuyết Tuần 4: PyTorch core trên nền toán Phase 0

> Cách đọc: mục 0 là bảng map NumPy của Tuần 1-3 sang PyTorch, đọc trước. Mục 1 đến 3 là ôn toán, mỗi mục dẫn về đúng chỗ đã học ở Tuần 1 và 2; nếu bạn vừa học xong Phase 0 thì đọc nhanh. Mục 4 là phần mới của tuần. Đọc file này song song với tutorial chính thức của PyTorch (link ở cuối, đã xác minh ngày 2026-08-11). Đọc xong mục nào thì sang [`03_math_cheat_sheet.md`](03_math_cheat_sheet.md) **tự viết lại mục đó bằng lời mình**: đó mới là deliverable. Mọi ví dụ số trong file này đã được chạy kiểm chứng bằng PyTorch 2.5.1 ngày 2026-08-11; bạn nên tự chạy lại từng snippet.
>
> Ký hiệu, log hay nhân ma trận tay còn lạ dù đã qua Tuần 1-3: quay lại [`00_math_bridge.md`](00_math_bridge.md) ôn nhanh rồi mới đọc tiếp.

---

## 0. Từ NumPy sang PyTorch: cùng toán, đổi công cụ

Ba tuần Phase 0 bạn đã viết mọi thứ bằng NumPy. Bảng này nối từng việc đã làm với API PyTorch sẽ dùng từ tuần này.

| Việc bạn đã làm | Ở đâu | PyTorch tương ứng |
|---|---|---|
| Tạo mảng, nhân ma trận, đọc chiều | Tuần 1 lab `shape`, `matmul` | `torch.tensor`, `@`, `.shape`; thêm `.to(device)` và `.dtype` |
| Nghiệm least squares bằng `np.linalg.solve` | Tuần 1 lab `proj` | `torch.linalg.solve`, `torch.linalg.lstsq` |
| SVD, trị riêng | Tuần 1 lab `svd`, `pd` | `torch.linalg.svd`, `torch.linalg.eigh` |
| Gradient giải tích, kiểm bằng sai phân trung tâm | Tuần 2 lab `gradcheck` | `loss.backward()` điền `.grad`; `torch.autograd.gradcheck` làm việc kiểm |
| Chain rule viết tay | Tuần 2 mục A3, lab `chain` | Autograd áp chain rule ngược trên đồ thị (mục 2.3) |
| Jacobian của A x là A | Tuần 2 lab `jacobian` | Backward của `nn.Linear` chỉ nhân với Wᵀ |
| NLL của Gaussian, MLE | Tuần 2 lab `mle` | `nn.MSELoss` (Gaussian) và `nn.CrossEntropyLoss` (categorical) đều là NLL |
| `gradient_descent_1d` với step size | Tuần 2 `03_gradient_descent.py` | `torch.optim.SGD(lr=...)`, `optimizer.step()`; `lr` là step size γ của MML 7.1 |
| Logistic regression: `sigmoid`, `nll_loss`, `grad` | Tuần 3 `04_logistic_regression_numpy.py` | `nn.Linear(2, 1)` + `nn.BCEWithLogitsLoss`, gradient do autograd |
| Tách train và validation | Tuần 3 mục 5 | Không có API riêng; tự tách trước khi train, như phần 1 của `05_train_mlp.py` |

Điều duy nhất thật sự mới về mặt khái niệm: PyTorch **ghi lại đồ thị tính toán** khi bạn tính forward, để `backward()` có đường đi ngược. Tuần 5 bạn sẽ tự viết cơ chế đó.

## 1. Linear Algebra

### 1.1 Vector & dot product

Vector là dãy số `a ∈ Rⁿ`. **Dot product** giữa hai vector cùng chiều:

```
a · b = Σᵢ aᵢbᵢ
```

```python
import torch
a = torch.tensor([1., 2., 3.])
b = torch.tensor([4., 5., 6.])
a @ b            # 1*4 + 2*5 + 3*6 = 32.0
```

**Ý nghĩa hình học** (Tuần 1 mục 4, MML Example 3.6): `a · b = |a||b|cos(θ)`: hai vector càng "cùng hướng" thì dot product càng lớn. Đây chính là lý do attention (Tuần 6) dùng `query · key` làm điểm liên quan: token nào có key "cùng hướng" với query thì được chú ý nhiều hơn.

### 1.2 Matrix multiply & quy tắc shape

`C = A @ B` với `A: (m×k)`, `B: (k×n)` → `C: (m×n)`. **Chiều trong (`k`) phải khớp**, chiều ngoài quyết định shape kết quả. Đây là quy tắc chiều Tuần 1 mục 2, giờ trên tensor.

```
Cᵢⱼ = Σₖ AᵢₖBₖⱼ    (dot product của hàng i trong A với cột j trong B)
```

```python
A = torch.randn(2, 3)
B = torch.randn(3, 4)
(A @ B).shape    # (2, 4)
# A @ torch.randn(2, 4) → RuntimeError: chiều trong 3 ≠ 2
```

Kỹ năng sống còn của cả 18 tuần: **nhìn code là đọc được shape chảy qua từng phép tính**. Gặp bug shape, in `x.shape` tại từng bước.

### 1.3 `nn.Linear` chính là matmul

`nn.Linear(in_features, out_features)` là một ánh xạ tuyến tính (Tuần 1 mục 1) cộng thêm vector dịch, thực hiện `y = x @ Wᵀ + b`. PyTorch lưu weight theo shape `(out, in)`:

```python
lin = torch.nn.Linear(3, 5)
lin.weight.shape                       # (5, 3), (out, in)
x = torch.randn(1, 3)
manual = x @ lin.weight.T + lin.bias   # bằng đúng lin(x)
```

Một MLP chỉ là chuỗi `Linear → activation → Linear → ...`: tức là chuỗi matmul xen kẽ hàm phi tuyến.

### 1.4 Broadcasting

Broadcasting là thứ NumPy đã làm ngầm trong các lab Phase 0; giờ gọi tên nó. Khi hai tensor khác shape, PyTorch so shape **từ phải sang trái**; mỗi cặp chiều hợp lệ khi bằng nhau, hoặc một bên là 1, hoặc một bên thiếu (được coi là 1). Chiều size 1 / thiếu sẽ được "kéo dài" ảo.

```python
M = torch.randn(2, 5, 4)
v = torch.randn(4)
(M + v).shape    # (2, 5, 4), v cộng vào MỌI vị trí (2,5)
```

Broadcasting tiện nhưng là nguồn bug thầm lặng: phép cộng "chạy được" không có nghĩa là đúng ý bạn. Khi nghi ngờ, viết rõ shape mong đợi ra comment.

### 1.5 Transpose

`Aᵀ` đổi hàng ↔ cột: `(m×n) → (n×m)`. Trong PyTorch: `A.T` (2 chiều) hoặc `A.transpose(dim0, dim1)` (chọn cặp chiều, quan trọng từ Tuần 6 khi thao tác tensor `(batch, head, seq, dim)`).

---

## 2. Calculus: nền của backprop

Toàn bộ mục này bạn đã học ở Tuần 2 phần A và phần C; ở đây chỉ gắn API.

### 2.1 Đạo hàm & gradient

Đạo hàm `f'(x)` = độ dốc: f thay đổi bao nhiêu khi x nhúc nhích một lượng nhỏ. Với hàm nhiều biến `L(w₁,...,wₙ)` (loss theo toàn bộ tham số model), **gradient** là vector mọi đạo hàm riêng:

```
∇L = [∂L/∂w₁, ..., ∂L/∂wₙ]
```

∇L chỉ **hướng tăng nhanh nhất** của L. Training đi ngược lại, **gradient descent**:

```
w ← w − lr · ∂L/∂w
```

`lr` (learning rate) là bước chân, chính là step size γ của MML mục 7.1 mà bạn đã thấy làm phân kỳ với 1.1 và hội tụ với 0.1 trong `03_gradient_descent.py` Tuần 2.

### 2.2 Chain rule: linh hồn của backprop

Tuần 2 mục A3 bạn kiểm chain rule bằng sai phân trên hàm (5.109) của MML. Nếu `L = f(g(w))` thì:

```
∂L/∂w = (∂L/∂g) · (∂g/∂w)
```

**Ví dụ tự tính tay được:** `f(x) = (3x + 2)²` tại `x = 1`.
- Đặt `u = 3x + 2` → `f = u²`.
- `∂f/∂u = 2u = 2·5 = 10`; `∂u/∂x = 3`.
- Chain rule: `∂f/∂x = 10 · 3 = 30`.

Kiểm chứng bằng autograd:

```python
x = torch.tensor(1., requires_grad=True)
f = (3*x + 2)**2
f.backward()
x.grad    # 30.0, khớp tính tay
```

Bạn vẫn có thể kiểm bằng sai phân trung tâm như Tuần 2: `((3*1.000001+2)**2 - (3*0.999999+2)**2) / 2e-6` cho 30.0 tới sáu chữ số. Autograd không thay thế kỹ năng kiểm đó; nó chỉ tiết kiệm công viết đạo hàm.

Một neural network là hàm hợp rất sâu: `L = loss(layerₙ(...layer₂(layer₁(x))...))`. **Backprop = chain rule áp dụng lan ngược từ loss về từng layer**, nhân dồn các đạo hàm cục bộ. Không có gì huyền bí hơn thế.

### 2.3 Autograd làm gì cho bạn

- Mỗi phép tính trên tensor có `requires_grad=True` được ghi vào một **computation graph**.
- `loss.backward()` chạy ngược graph đó, tính `∂loss/∂param` cho mọi tham số, **cộng dồn** vào `param.grad`.
- `optimizer.step()` dùng các `.grad` để cập nhật tham số.
- `optimizer.zero_grad()` xóa grad cũ, bắt buộc mỗi step, vì PyTorch cộng dồn grad (thiết kế có chủ đích, phục vụ gradient accumulation).
- `with torch.no_grad():` tắt ghi graph, dùng khi eval/inference cho nhanh và đỡ tốn bộ nhớ.

Chi tiết đầy đủ: trang **Autograd mechanics** trong docs (link cuối file).

---

## 3. Probability: softmax & cross-entropy

### 3.1 Softmax

Biến vector điểm số thô (**logits**) thành phân phối xác suất, tức một pmf theo Table 6.1 của MML (Tuần 2 mục B2):

```
softmax(z)ᵢ = e^{zᵢ} / Σⱼ e^{zⱼ}
```

```python
z = torch.tensor([1., 2., 3.])
torch.softmax(z, dim=0)    # [0.0900, 0.2447, 0.6652], tổng = 1.0
```

- Mỗi giá trị ∈ (0,1), tổng = 1 → đọc được như xác suất.
- **Ổn định số học:** `e^{1000}` tràn số. Trừ `max(z)` trước khi mũ, kết quả không đổi (tử và mẫu cùng chia `e^{max}`) nhưng hết overflow. Các hàm PyTorch đã làm sẵn việc này.
- Xuất hiện ở hai nơi trong LLM: lớp output (xác suất token tiếp theo) và **attention weights** (Tuần 6).

### 3.2 Cross-entropy loss

Đây là negative log-likelihood của Tuần 2 mục B6 áp cho phân phối categorical; bản hai lớp của nó là `nll_loss` bạn tự viết cho logistic regression ở Tuần 3. Đo độ lệch giữa phân phối dự đoán `p` và nhãn thật `y`:

```
CE = − Σᵢ yᵢ log(pᵢ)
```

Với nhãn dạng index/one-hot, chỉ còn một số hạng: `CE = − log(p_đúng)`.

Ví dụ nối tiếp mục 3.1: nếu nhãn đúng là lớp có logit 3, phần tử thứ ba, tức index 2 khi đếm từ 0 như PyTorch (xác suất dự đoán 0.6652): thì `CE = −log(0.66524…) ≈ 0.4076` (tính trên p chưa làm tròn; xem chú thích trong [`00_math_bridge.md`](00_math_bridge.md) §6). Dự đoán đúng và tự tin → loss tiến về 0; sai mà tự tin (`p_đúng` gần 0) → `−log` bùng nổ → phạt rất nặng.

**Bẫy kinh điển:** `nn.CrossEntropyLoss` của PyTorch **đã gộp softmax + log + NLL**: đưa thẳng **logits** vào, KHÔNG softmax trước (softmax hai lần cho kết quả sai mà không báo lỗi).

### 3.3 Preview: perplexity (Tuần 8)

`perplexity = exp(cross_entropy)`: hiểu nôm na: "trung bình model phân vân giữa bao nhiêu lựa chọn". CE = 0 → PPL = 1 (chắc chắn tuyệt đối). Đây là metric chuẩn khi pretrain language model.

---

## 4. PyTorch core: từ tensor đến training loop

### 4.1 Tensor

Mảng n chiều + dtype + device:

```python
x = torch.randn(2, 3)              # ngẫu nhiên chuẩn, dtype mặc định float32
x = x.to("cuda")                   # chuyển lên GPU (đã xác nhận bằng 01_check_gpu.py)
x.shape, x.dtype, x.device
```

Hai tensor muốn tính với nhau phải **cùng device**: lỗi "expected all tensors to be on the same device" sẽ là bạn đồng hành quen mặt.

### 4.2 `nn.Module`: khuôn của mọi model

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, d_in, d_hidden, d_out):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, d_hidden),
            nn.ReLU(),
            nn.Linear(d_hidden, d_out),
        )

    def forward(self, x):
        return self.net(x)   # trả về logits, KHÔNG softmax ở đây (xem 3.2)
```

- `__init__`: khai báo layer (tham số tự động được đăng ký qua `self.`).
- `forward`: định nghĩa luồng tính. Gọi `model(x)` chứ đừng gọi `model.forward(x)` trực tiếp.
- `model.parameters()` trả mọi tham số, đưa cho optimizer.
- Từ GPT (Tuần 7) đến agent stack, mọi model đều là `nn.Module` lồng nhau. Nắm chắc ở đây là nắm mãi.

### 4.3 Giải phẫu training loop: 5 bước bất biến

```python
model = MLP(2, 32, 2).to(device)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for step in range(num_steps):
    xb, yb = get_batch()               # dữ liệu lên đúng device
    logits = model(xb)                 # 1. forward
    loss = loss_fn(logits, yb)         # 2. tính loss
    opt.zero_grad()                    # 3. xóa grad cũ (vì grad CỘNG DỒN)
    loss.backward()                    # 4. backward, chain rule tự động
    opt.step()                         # 5. cập nhật tham số
```

So với vòng lặp trong `04_logistic_regression_numpy.py` Tuần 3: bước 4 thay cho hàm `grad` viết tay, bước 5 thay cho dòng `w -= lr * grad(...)`, bước 3 là thứ mới vì PyTorch cộng dồn gradient. Training loop của GPT Tuần 8 hay QLoRA Tuần 12 vẫn đúng 5 bước này, chỉ khác model, data và vài kỹ thuật quanh nó. Thuộc lòng khung này trước khi sang Tuần 5.

### 4.4 Từ logistic regression sang MLP

Logistic regression là `nn.Linear(2, 1)` nối với sigmoid và BCE loss: một lớp giả thuyết chỉ gồm các đường thẳng chia mặt phẳng. Dữ liệu two moons trong `05_train_mlp.py` không tách được bằng một đường thẳng, nên logistic regression bị chặn ở accuracy thấp dù train bao lâu. Chèn một `nn.Linear(2, 32)` và `ReLU` vào giữa là mở rộng lớp giả thuyết H; theo error decomposition của Tuần 3 mục 3, approximation error giảm hẳn; [Suy luận] với 800 điểm train, estimation error chưa đáng kể, và accuracy held-out 1.000 đo được trong lời giải mẫu là bằng chứng gián tiếp. Đó là toàn bộ lý do MLP thắng trong bài này, và cũng là câu bạn cần viết được bằng lời mình.

**Tự kiểm tra hiểu:** giải thích được vì sao đổi chỗ bước 3 lên trước bước 1 vẫn chạy đúng, nhưng bỏ hẳn bước 3 thì loss sẽ hỏng như thế nào.

---

## 5. Cầu nối tới Transformer (preview Tuần 6)

Attention, trái tim của Transformer, chỉ dùng đúng những thứ ở trên:

1. Attention score = **dot product** `query · key` (mục 1.1; góc giữa hai vector, Tuần 1 mục 4).
2. Chia `√d_k` cho ổn định, rồi **softmax** → trọng số (mục 3.1).
3. Output = trọng số nhân **matmul** với value (mục 1.2).

Nắm chắc dot product + softmax + matmul + chain rule ở tuần này thì Tuần 6 sẽ "click" thay vì choáng.

---

## 6. Nguồn chính thức (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| PyTorch, Learn the Basics (Tensors → Autograd → Optimization Loop) | https://docs.pytorch.org/tutorials/beginner/basics/intro.html | 1, 2.3, 4 |
| PyTorch, Deep Learning: A 60 Minute Blitz | https://docs.pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html | 2, 4 |
| PyTorch docs, Autograd mechanics | https://docs.pytorch.org/docs/stable/notes/autograd.html | 2.3 |
| PyTorch docs, `torch.nn.Module` | https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html | 4.2 |

Ghi chú: `pytorch.org/tutorials` hiện redirect 301 sang `docs.pytorch.org` (kiểm tra 2026-08-11): hai địa chỉ là một. Phần toán (mục 1-3) đã được dạy có trích dẫn sách ở Tuần 1 và 2 (MML chương 2-7, Vũ Hữu Tiệp chương 1-4, Durrett); ở đây chỉ kiểm chứng lại bằng các snippet chạy được.

## Sau khi đọc xong

1. Chạy lại từng snippet trong file này (gõ tay, đừng copy).
2. Sang [`03_math_cheat_sheet.md`](03_math_cheat_sheet.md) viết lại bằng lời mình, mỗi công thức ghi tuần đã học và API tương ứng.
3. Luyện với [`04_math_practice.py`](04_math_practice.py): đoán trước, chạy sau.
4. Tự code [`05_train_mlp.py`](05_train_mlp.py): phần 2 viết lại logistic regression Tuần 3, phần 3 chồng lớp ẩn thành MLP, cùng khung 5 bước ở mục 4.3.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **Cross-entropy là cực tiểu KL.** Prince trình bày cross-entropy như việc "minimize the distance (KL divergence) between these two distributions": phân phối thực nghiệm của mẫu và phân phối của model (UDL Figure 5.12 và mục 5.7, trang 71). Mục 5.1 (trang 56) đi từ maximum likelihood, mục 5.2 (trang 60) cho "công thức chung" để dựng loss: chọn phân phối cho đầu ra, để mạng dự đoán tham số của phân phối đó, rồi lấy NLL. Đây là cách nhìn gọn nhất cho mục 3.2 ở trên.
- **Optimizer trong training loop.** UDL chương 6: 6.1 gradient descent (trang 77), 6.2 SGD (trang 83), 6.3 momentum (trang 86), 6.4 Adam (trang 88). Khi bạn đổi `torch.optim.SGD` sang `Adam` trong `05_train_mlp.py`, đây là chỗ đọc để biết mình đổi gì.
- **Cùng nội dung, ngắn hơn.** Fleuret, *The Little Book of Deep Learning* mục 3.1 Losses (trang 25): cross-entropy tính từ logit, mỗi thành phần đầu ra "interpreted as the logarithm of a non-normalized probability, or logit". Goodfellow chương 6 Deep Feedforward Networks và chương 8 Optimization (đọc HTML tại deeplearningbook.org) là bản đầy đủ nhất, nhưng dài.
