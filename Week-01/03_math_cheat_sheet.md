# Math Cheat Sheet cho LLM — Tuần 1

> Bản nháp khởi tạo. **Hãy tự viết lại / bổ sung bằng lời của mình** — đó mới là deliverable thật. Giữ thuật ngữ tiếng Anh.

## 1. Linear Algebra

**Vector & dot product.** Với `a, b ∈ R^n`: `a · b = Σ aᵢ bᵢ`. Đo độ "giống hướng" giữa 2 vector → là nền tảng của **attention score** (query · key).

**Matrix multiply.** `C = A @ B`, với `A: (m×k)`, `B: (k×n)` → `C: (m×n)`. Quy tắc shape: chiều trong phải khớp (`k`).
- `Cᵢⱼ = Σₖ Aᵢₖ Bₖⱼ` (dot product của hàng i với cột j).
- Trong NN: một `nn.Linear(in, out)` thực chất là `y = x @ Wᵀ + b`.

**Broadcasting (PyTorch).** Khi shape khác nhau, PyTorch tự "kéo dài" chiều có size 1. Vd. `(B, T, D) + (D,)` → cộng vào mọi vị trí. Nắm chắc để tránh bug shape.

**Transpose.** `Aᵀ` đổi hàng ↔ cột; `(m×n) → (n×m)`.

## 2. Calculus (nền của backprop)

**Đạo hàm = độ dốc.** `f'(x)` cho biết f thay đổi bao nhiêu khi x nhúc nhích.

**Gradient.** Với hàm nhiều biến `L(w₁,...,wₙ)`, gradient `∇L = [∂L/∂w₁, ..., ∂L/∂wₙ]` chỉ hướng tăng nhanh nhất. Training đi **ngược** gradient (gradient descent): `w ← w − lr · ∂L/∂w`.

**Chain rule** (linh hồn của backprop). Nếu `L = f(g(w))` thì
`∂L/∂w = (∂L/∂g) · (∂g/∂w)`.
Backprop = áp dụng chain rule lan ngược qua từng layer, nhân dồn các đạo hàm cục bộ.

**Autograd (PyTorch).** `loss.backward()` tự tính mọi `∂loss/∂param` và lưu vào `param.grad`. `optimizer.step()` dùng các grad đó cập nhật tham số. `optimizer.zero_grad()` xóa grad cũ (vì PyTorch *cộng dồn* grad).

## 3. Probability

**Softmax.** Biến vector logits `z` thành phân phối xác suất:
`softmax(z)ᵢ = e^{zᵢ} / Σⱼ e^{zⱼ}`. Tổng = 1, mỗi giá trị ∈ (0,1).
- Mẹo số học: trừ `max(z)` trước khi mũ để tránh overflow.
- Dùng ở: output classifier, và **attention weights**.

**Cross-entropy loss.** Đo khoảng cách giữa phân phối dự đoán `p` và nhãn thật `y`:
`CE = − Σᵢ yᵢ log(pᵢ)`. Với nhãn dạng one-hot/index → `CE = − log(p_đúng)`.
- Dự đoán càng tự tin & đúng → loss càng nhỏ; sai & tự tin → loss lớn.
- `nn.CrossEntropyLoss` **đã gộp** softmax + log + NLL → đưa thẳng **logits** vào, đừng softmax trước.

**Perplexity** (gặp ở Tuần 5): `exp(cross_entropy)` — "trung bình model phân vân giữa bao nhiêu lựa chọn".

## 4. Cầu nối tới Transformer (preview Tuần 3)

- Attention score = **dot product** giữa query và key → đo độ liên quan.
- Chia cho `√d_k` để ổn định, rồi **softmax** → trọng số.
- Output = tổng có trọng số của các value vector (lại là **matrix multiply**).

→ Cả attention thực chất chỉ là dot product + softmax + matmul. Nắm 3 thứ này là nắm gốc.

## 5. Tự kiểm tra (nhờ Claude quiz)

- [ ] Giải thích tại sao `nn.Linear` dùng `Wᵀ`.
- [ ] Vì sao phải `zero_grad()` mỗi step?
- [ ] Vì sao trừ `max` trong softmax?
- [ ] Cross-entropy khác gì MSE, và tại sao hợp cho phân loại?
- [ ] Viết chain rule cho một mạng 2 layer trên giấy.
