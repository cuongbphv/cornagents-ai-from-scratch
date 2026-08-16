# Cầu nối toán — làm quen lại trước lý thuyết Tuần 1

> Dành cho người **lâu không học toán** hoặc chuyển từ web/dev. **Không thêm chủ đề mới** — chỉ ôn chậm đúng 5 thứ Tuần 1 sẽ dùng: ký hiệu, log/exp, dot product, nhân ma trận, chain rule, softmax, cross-entropy.
>
> Không cần PyTorch. Máy tính cầm tay hoặc `python -c "..."` là đủ.
>
> Số trong file này đã tính bằng `math` của Python 3.11 ngày **2026-08-16**. Tự tính tay rồi đối chiếu; đừng đọc đáp án trước.

---

## Ai nên làm file này, ai được nhảy

**Làm file này** nếu một trong các câu sau khiến bạn phải tra cứu:

- Σ, `aᵢ`, `eˣ`, `ln` nhìn không quen.
- Chưa nhân được ma trận `2×3` với `3×2` bằng tay.
- Chưa tính được đạo hàm `f(x) = (2x+1)²` bằng chain rule.

**Nhảy sang [`01_check_gpu.py`](01_check_gpu.py)** nếu checklist toán trong [`../Week-00/prerequisites_vi.md`](../Week-00/prerequisites_vi.md) §4 (matmul tay + chain rule) làm được không cần mở lại công thức.

Cổng cuối file: **trượt thì ở lại đây**, chưa mở [`02_theory_notes.md`](02_theory_notes.md).

Thời lượng: khoảng **3–6 giờ**. Người quên toán nên cộng thêm vào ~10–12 giờ còn lại của tuần (tổng khoảng 15–20 giờ), không cố nhét vào một buổi.

Luyện thêm (stdlib, không cần PyTorch): [`00_math_bridge_practice.py`](00_math_bridge_practice.py).

---

## 1. Ký hiệu — đọc công thức như đọc code

| Ký hiệu | Đọc như | Ví dụ |
|---|---|---|
| `aᵢ` | phần tử thứ *i* của danh sách `a` (đếm từ 1 trong công thức toán; Python đếm từ 0) | `a = [2, 5, 9]` → `a₁ = 2`, `a₂ = 5` |
| `Σᵢ aᵢ` | cộng mọi phần tử | `Σᵢ [2, 5, 9] = 16` |
| `a ∈ Rⁿ` | `a` là vector *n* số thực | `[1, 0, -2]` ∈ R³ |
| `e` | hằng số ≈ **2.718** (`math.e`) | cơ số của mũ/log trong ML |
| `eˣ` / `exp(x)` | e mũ x | `e⁰ = 1`, `e¹ ≈ 2.718` |
| `ln x` / `log x` | logarit **cơ số e** | `ln 1 = 0`, `ln e = 1` |
| `∂L/∂w` | đạo hàm riêng: L thay đổi bao nhiêu khi **chỉ mình** w nhúc nhích (các biến khác giữ nguyên) | dùng từ mục 4 |

Trong PyTorch và trong các tuần sau, `torch.log` / `log` **là ln**, không phải log₁₀. File này dùng `ln` cho khỏi nhầm.

**Vì sao cần e và ln?** Softmax lấy `e^{logit}`. Cross-entropy lấy `−ln(p_đúng)`. Hai hàm ngược nhau: `ln(eˣ) = x`, `e^{ln x} = x` (với x > 0).

```
e^0 = 1
e^1 ≈ 2.718
e^2 ≈ 7.389
ln(1) = 0
ln(e) = 1
−ln(0.1) ≈ 2.303
```

Bài 1 — tính tay (máy tính được):

1. `Σ` của `2 + 4 + 6`
2. `e⁰` và `ln 1` (không cần máy)
3. `−ln(0.1)` — khoảng bao nhiêu?

<details>
<summary>Đáp án mục 1</summary>

1. 12
2. 1 và 0
3. ≈ 2.303 (`math.log(0.1)` rồi đổi dấu)

</details>

---

## 2. Dot product — cộng các tích từng cặp

Hai list **cùng số phần tử**:

```
a · b = a₁b₁ + a₂b₂ + … + aₙbₙ
```

Đó là một số, không phải list. Với độ dài vector cố định, càng “cùng hướng” thì tích càng lớn; vuông góc thì ra 0 (công thức đầy đủ `a · b = |a||b|cos θ` nằm ở `02_theory_notes.md` §1.1 — chưa cần bây giờ). Tuần 3: attention score = `query · key`.

Ví dụ làm sẵn: `a = [1, 2, 3]`, `b = [4, 5, 6]`

```
1·4 + 2·5 + 3·6 = 4 + 10 + 18 = 32
```

Bài 2 — tính tay:

1. `[2, 0] · [3, 1]`
2. `[1, 0] · [0, 1]`
3. `[1, 2, 3] · [4, 5, 6]` (làm lại, không nhìn ví dụ)

<details>
<summary>Đáp án mục 2</summary>

1. `2·3 + 0·1 = 6`
2. `1·0 + 0·1 = 0` (hai trục vuông góc)
3. 32

</details>

---

## 3. Nhân ma trận — nhiều dot product xếp thành bảng

`C = A @ B` chỉ hợp lệ khi **chiều trong khớp**:

```
A: (m × k)   @   B: (k × n)   →   C: (m × n)
```

Ô `Cᵢⱼ` = dot product **hàng i của A** với **cột j của B**.

Ví dụ làm sẵn — `A` là `2×3`, `B` là `3×2`:

```
A = | 1  2  3 |      B = |  7   8 |
    | 4  5  6 |          |  9  10 |
                         | 11  12 |
```

```
C₁₁ = 1·7 + 2·9 + 3·11 = 7 + 18 + 33 = 58
C₁₂ = 1·8 + 2·10 + 3·12 = 8 + 20 + 36 = 64
C₂₁ = 4·7 + 5·9 + 6·11 = 28 + 45 + 66 = 139
C₂₂ = 4·8 + 5·10 + 6·12 = 32 + 50 + 72 = 154
```

```
C = |  58   64 |
    | 139  154 |     shape (2 × 2)
```

`A (2×3) @ (2×4)` **lỗi**: chiều trong 3 ≠ 2. Trong code đó là `RuntimeError` / `mat1 and mat2 shapes cannot be multiplied`.

Một `nn.Linear` sau này cũng chỉ là `y = x @ Wᵀ + b` — cùng một phép nhân này.

Bài 3 — tính tay:

1. Shape của `(2×3) @ (3×2)`? Của `(2×3) @ (2×4)`?
2. Với A, B ở ví dụ trên, `C₂₁` bằng bao nhiêu? (tính lại, không nhìn)
3. `[1, 2] @ | 3 |`  (hàng 1×2 nhân cột 2×1) ra shape gì và giá trị nào?
            `| 4 |`

<details>
<summary>Đáp án mục 3</summary>

1. `(2×2)`. Phép thứ hai không nhân được.
2. 139
3. Shape `(1×1)` — một số: `1·3 + 2·4 = 11`

</details>

---

## 4. Chain rule — đạo hàm hàm hợp

Đạo hàm = độ dốc. Gradient = đủ mọi độ dốc theo từng tham số. Training đi **ngược** gradient:

```
w ← w − lr · (∂L/∂w)
```

**Chain rule:** nếu `L = f(g(w))` thì

```
∂L/∂w = (∂L/∂g) · (∂g/∂w)
```

Backprop (Tuần 2) = lặp lại đúng một dòng này từ loss về từng layer.

**Quy tắc đạo hàm tối thiểu** — ba dòng này đủ cho mọi bài trong file (quên hết calculus cũng chỉ cần nhớ lại đúng chừng này):

```
(xⁿ)'     = n·xⁿ⁻¹      ví dụ: (x²)' = 2x, (u²)' = 2u
(ax + b)' = a           ví dụ: (3w + 1)' = 3, (2x + 1)' = 2
(c)'      = 0           hằng số không nhúc nhích → độ dốc 0
```

Ví dụ làm sẵn — `f(x) = (2x + 1)²` tại `x = 1` (đúng câu checklist prerequisites):

```
u = 2x + 1 = 3
f = u² = 9
∂f/∂u = 2u = 6
∂u/∂x = 2
∂f/∂x = 6 · 2 = 12
```

Hai lớp siêu nhỏ — `y = 3w + 1`, `L = y²`, tại `w = 1`:

```
y = 4
L = 16
∂L/∂y = 2y = 8
∂y/∂w = 3
∂L/∂w = 8 · 3 = 24
```

Một bước gradient descent — `L = w²`, `w = 5`, `lr = 0.1`:

```
∂L/∂w = 2w = 10
w ← 5 − 0.1 · 10 = 4
```

Bài 4 — tính tay:

1. `f(x) = (2x + 1)²` tại `x = 1` — `∂f/∂x`?
2. `y = 3w + 1`, `L = y²`, tại `w = 1` — `∂L/∂w`?
3. `L = w²`, `w = 5`, `lr = 0.1` — `w` sau 1 bước GD?

<details>
<summary>Đáp án mục 4</summary>

1. 12
2. 24
3. 4

</details>

---

## 5. Softmax — từ điểm số thô sang “xác suất”

Logits = điểm thô (âm dương tùy ý). Softmax biến chúng thành số trong `(0, 1)` **tổng = 1**:

```
softmax(z)ᵢ = e^{zᵢ} / Σⱼ e^{zⱼ}
```

Ví dụ làm sẵn — `z = [1, 2, 3]`:

```
e¹ ≈ 2.718
e² ≈ 7.389
e³ ≈ 20.086
tổng ≈ 30.193

p ≈ [0.0900, 0.2447, 0.6652]
```

Ô lớn nhất (logit 3) nhận xác suất lớn nhất. Dùng ở hai chỗ: token tiếp theo, và **attention weights** (Tuần 3).

**Trừ max trước khi mũ** — cùng kết quả, tránh `e^{1000}` tràn số:

```
z − 3 = [−2, −1, 0]
```

`e^{zᵢ − max}` / tổng vẫn ra `[0.0900, 0.2447, 0.6652]` (đã kiểm 2026-08-16).

Bài 5 — tính tay (máy tính được):

1. Softmax có tổng bằng mấy?
2. Với `z = [1, 2, 3]`, phần tử nào của `p` lớn nhất?
3. Softmax của `[1, 2, 3]` và của `[1, 2, 3] − 3` có bằng nhau không?

<details>
<summary>Đáp án mục 5</summary>

1. 1
2. Phần tử ứng với logit 3 ≈ 0.6652
3. Bằng nhau (tử và mẫu cùng chia `e^{max}`)

</details>

---

## 6. Cross-entropy — phạt khi sai mà tự tin

Nhãn one-hot / một chỉ số lớp đúng: chỉ còn

```
CE = − ln(p_đúng)
```

- `p_đúng → 1` → CE → 0
- `p_đúng → 0` → CE → rất lớn

Nối ví dụ softmax: nhãn đúng là lớp có logit 3 (`p ≈ 0.6652`):

```
CE = −ln(0.6652) ≈ 0.4077
```

(Ở [`02_theory_notes.md`](02_theory_notes.md) §3.2 con số là ≈ 0.4076 vì tính trên p chưa làm tròn `0.66524…`; ở đây tính trên `0.6652` đã làm tròn. Cả hai đều đúng — lệch 0.0001 là do làm tròn, không phải lỗi.)

Nếu model chỉ cho `p_đúng = 0.1` thì `CE ≈ 2.303` — phạt nặng hơn.

`nn.CrossEntropyLoss` **đã gộp** softmax + ln + đổi dấu. Đưa **logits** vào, không softmax trước. Chi tiết nằm ở [`02_theory_notes.md`](02_theory_notes.md) §3.2 — học sau khi qua cổng dưới.

Bài 6 — tính tay (máy tính được):

1. `p_đúng = 1` → CE?
2. `p_đúng = 0.1` → CE ≈ ?
3. `p_đúng = 0.6652` → CE ≈ ?

<details>
<summary>Đáp án mục 6</summary>

1. `−ln(1) = 0`
2. ≈ 2.303
3. ≈ 0.4077

</details>

---

## 7. Cổng — chưa qua thì chưa mở lý thuyết

Làm **không nhìn đáp án**. Sai một câu → ôn lại đúng mục, đừng sang `02_theory_notes.md`.

- [ ] Nhân `A (2×3)` với `B (3×2)` ở mục 3, viết đủ 4 ô và shape `(2×2)`
- [ ] Chain rule: `f(x) = (2x+1)²` tại `x = 1` ra **12**
- [ ] Nói được: softmax tổng = 1; CE = `−ln(p_đúng)`
- [ ] `e⁰ = 1`, `ln 1 = 0`, và `log` trong ML là **ln**

Qua cổng:

1. Chạy [`00_math_bridge_practice.py`](00_math_bridge_practice.py) (đoán trước, Enter sau).
2. [`01_check_gpu.py`](01_check_gpu.py) — 5 phút.
3. [`02_theory_notes.md`](02_theory_notes.md) — cùng 5 chủ đề, thêm PyTorch.

Cùng một việc, lần này bằng code: [`04_math_practice.py`](04_math_practice.py) (cần PyTorch) — để sau khi đọc lý thuyết.
