"""
04_math_practice.py — Luyện tập tương tác theo 03_math_cheat_sheet.md (mục 1-4).

Cách dùng (LƯU Ý: shell có alias python -> python3.14, phải gọi venv trực tiếp):
    .venv/bin/python Week-01/04_math_practice.py

Cách học: với MỖI câu, đọc câu hỏi -> TỰ ĐOÁN đáp án ra giấy/miệng ->
nhấn Enter để chạy code và so sánh -> đọc 1 dòng giải thích.
Tự đoán TRƯỚC mới là chỗ học; xem luôn đáp án thì phí.
"""

import math
import torch

torch.manual_seed(0)  # tái lập kết quả


def ask(n, section, question, predict):
    print("\n" + "=" * 64)
    print(f" Câu {n}  ·  {section}")
    print("=" * 64)
    print(question.strip())
    print(f"\n  >>> TỰ ĐOÁN: {predict}")
    input("  (nhấn Enter để xem đáp án) ")


def show(label, value, explain):
    print(f"  → {label}: {value}")
    print(f"    {explain}")


# ─────────────────────────── 1. LINEAR ALGEBRA ───────────────────────────

def q1_dot_product():
    ask(1, "Linear Algebra · dot product",
        "a = [1,2,3], b = [4,5,6]. Tính a · b. Ý nghĩa con số này?",
        "a·b = 1*4 + 2*5 + 3*6 = ?")
    a = torch.tensor([1., 2., 3.])
    b = torch.tensor([4., 5., 6.])
    show("a @ b", (a @ b).item(),
         "Dot product = Σ aᵢbᵢ = 32. Đo độ 'cùng hướng' → nền tảng attention score (query·key).")


def q2_matmul_shape():
    ask(2, "Linear Algebra · matmul shape",
        "A: (2,3), B: (3,4). Shape của A @ B? Vì sao A @ (2,4) sẽ lỗi?",
        "(m×k)@(k×n) → (m×n); chiều trong k phải khớp")
    A, B = torch.randn(2, 3), torch.randn(3, 4)
    show("(A @ B).shape", tuple((A @ B).shape),
         "(2,3)@(3,4)→(2,4). A@(2,4) lỗi vì chiều trong 3≠2 (mat1/mat2 không khớp).")


def q3_nn_linear():
    ask(3, "Linear Algebra · nn.Linear",
        "nn.Linear(3,5) có đúng là y = x @ Wᵀ + b không? weight lưu shape nào?",
        "weight shape (out,in)=(5,3); y = x @ W.T + b")
    lin = torch.nn.Linear(3, 5)
    x = torch.randn(1, 3)
    manual = x @ lin.weight.T + lin.bias
    show("weight.shape", tuple(lin.weight.shape), "Lưu (out,in) nên cần transpose .T khi nhân.")
    show("allclose(lin(x), x@Wᵀ+b)", torch.allclose(lin(x), manual),
         "True → nn.Linear chính là x @ Wᵀ + b. Đó là lý do có Wᵀ.")


def q4_broadcasting():
    ask(4, "Linear Algebra · broadcasting",
        "(8,1,16) + (1,4,16) ra shape gì? Quy tắc broadcasting?",
        "căn từ phải sang trái; mỗi chiều bằng nhau HOẶC một bên =1")
    x, y = torch.randn(8, 1, 16), torch.randn(1, 4, 16)
    show("(x + y).shape", tuple((x + y).shape),
         "(8,4,16): chiều =1 bị 'kéo dài' để khớp. Đây là nguồn bug shape #1.")


def q5_matmul_vs_mul():
    ask(5, "Linear Algebra · @ vs *",
        "Với M (2,2): M @ M và M * M khác nhau thế nào?",
        "@ = nhân ma trận (dot theo hàng/cột); * = element-wise")
    M = torch.tensor([[1., 2.], [3., 4.]])
    show("M @ M", M.matmul(M).tolist(), "Matmul: hàng·cột.")
    show("M * M", (M * M).tolist(), "Element-wise: bình phương từng ô. Cùng shape, KHÁC nghĩa.")


# ─────────────────────────── 2. CALCULUS ───────────────────────────

def q6_grad_autograd():
    ask(6, "Calculus · gradient (autograd)",
        "L = w², tại w=3. dL/dw = ? autograd có cho đúng không?",
        "dL/dw = 2w = 6")
    w = torch.tensor(3.0, requires_grad=True)
    (w ** 2).backward()
    show("w.grad", w.grad.item(), "backward() tự tính ∂L/∂w = 2w = 6, lưu vào w.grad.")


def q7_chain_rule():
    ask(7, "Calculus · chain rule",
        "L = g², g = 3w+1, tại w=2. Dùng chain rule tính dL/dw.",
        "dL/dw = (dL/dg)(dg/dw) = (2g)(3) = 2*7*3 = 42")
    w = torch.tensor(2.0, requires_grad=True)
    g = 3 * w + 1
    (g ** 2).backward()
    show("w.grad", w.grad.item(),
         "Chain rule: 2*(3*2+1)*3 = 42. Backprop = chain rule lan ngược qua các layer.")


def q8_zero_grad():
    ask(8, "Calculus · vì sao zero_grad()",
        "Gọi backward() 2 lần liên tiếp KHÔNG zero_grad. w.grad ra sao?",
        "PyTorch CỘNG DỒN grad → grad bị nhân đôi")
    w = torch.tensor(3.0, requires_grad=True)
    (w ** 2).backward()
    (w ** 2).backward()  # không zero_grad giữa 2 lần
    show("w.grad (cộng dồn)", w.grad.item(),
         "6+6=12 (không phải 6). Vì vậy mỗi step phải optimizer.zero_grad().")


def q9_gd_step():
    ask(9, "Calculus · gradient descent",
        "w=5, L=w², lr=0.1. Sau 1 bước w ← w − lr·∂L/∂w, w mới = ?",
        "grad=2w=10; w = 5 − 0.1*10 = 4")
    w = torch.tensor(5.0, requires_grad=True)
    (w ** 2).backward()
    with torch.no_grad():
        w -= 0.1 * w.grad
    show("w sau 1 step", w.item(), "5 − 0.1*10 = 4. Đi NGƯỢC gradient để giảm loss.")


# ─────────────────────────── 3. PROBABILITY ───────────────────────────

def q10_softmax():
    ask(10, "Probability · softmax",
        "softmax([2,1,0]) — tổng các phần tử bằng mấy? phần tử nào lớn nhất?",
        "tổng = 1; logit lớn nhất (2.0) → xác suất cao nhất")
    z = torch.tensor([2., 1., 0.])
    p = torch.softmax(z, dim=0)
    show("softmax(z)", [round(v, 3) for v in p.tolist()], "Mỗi giá trị ∈(0,1).")
    show("tổng", round(p.sum().item(), 6), "= 1.0 → là phân phối xác suất.")


def q11_softmax_stable():
    ask(11, "Probability · softmax ổn định số học",
        "softmax(z) và softmax(z − max(z)) có bằng nhau? vì sao trừ max?",
        "bằng nhau; trừ max để tránh e^(số lớn) overflow")
    z = torch.tensor([1000., 1001., 1002.])
    naive_ok = torch.softmax(z, dim=0)
    shifted = torch.softmax(z - z.max(), dim=0)
    show("softmax(z − max)", [round(v, 3) for v in shifted.tolist()],
         "Cùng kết quả nhưng không overflow. PyTorch đã tự trừ max bên trong.")
    show("allclose", torch.allclose(naive_ok, shifted), "Toán học giống hệt, chỉ khác độ ổn định.")


def q12_cross_entropy():
    ask(12, "Probability · cross-entropy",
        "logits=[2,0.5,0.1], nhãn đúng=lớp 0. CrossEntropyLoss == −log(p_đúng)?",
        "CE = −log(softmax(logits)[0]); KHÔNG softmax trước khi đưa vào")
    logits = torch.tensor([[2.0, 0.5, 0.1]])
    target = torch.tensor([0])
    ce = torch.nn.functional.cross_entropy(logits, target)
    manual = -torch.log_softmax(logits, dim=1)[0, 0]
    show("cross_entropy", round(ce.item(), 4), "nn.CrossEntropyLoss đã gộp softmax+log+NLL.")
    show("−log(p_đúng)", round(manual.item(), 4), "Khớp → đưa thẳng LOGITS vào, đừng softmax trước.")


def q13_perplexity():
    ask(13, "Probability · perplexity (preview Tuần 5)",
        "cross_entropy = ln(4). perplexity = exp(CE) = ?",
        "exp(ln 4) = 4 → 'model phân vân giữa ~4 lựa chọn'")
    ce = torch.tensor(math.log(4))
    show("exp(CE)", round(torch.exp(ce).item(), 2), "Perplexity = exp(cross_entropy).")


# ─────────────────────── 4. CẦU NỐI TRANSFORMER ───────────────────────

def q14_attention():
    ask(14, "Bridge · self-attention = dot + scale + softmax + matmul",
        "Q,K,V shape (T=3, d_k=4). Shape của scores=Q@Kᵀ? của output?",
        "scores (T,T)=(3,3); softmax theo hàng (sum=1); output (T,d_k)=(3,4)")
    T, d_k = 3, 4
    Q, K, V = torch.randn(T, d_k), torch.randn(T, d_k), torch.randn(T, d_k)
    scores = Q @ K.T                      # dot product mọi cặp token
    weights = torch.softmax(scores / math.sqrt(d_k), dim=-1)   # scale + softmax
    out = weights @ V                     # tổng có trọng số của V (matmul)
    show("scores.shape", tuple(scores.shape), "Q@Kᵀ: độ liên quan giữa mọi cặp token.")
    show("weights mỗi hàng sum", [round(s, 4) for s in weights.sum(-1).tolist()],
         "=1 do softmax theo dim=-1.")
    show("output.shape", tuple(out.shape),
         "= (T,d_k). Attention CHỈ là dot product + softmax + matmul. Nắm 3 thứ = nắm gốc.")


def main():
    print("Luyện tập math cheat sheet — Tuần 1 (mục 1-4). Tự đoán trước, rồi Enter để so.")
    for fn in (q1_dot_product, q2_matmul_shape, q3_nn_linear, q4_broadcasting, q5_matmul_vs_mul,
               q6_grad_autograd, q7_chain_rule, q8_zero_grad, q9_gd_step,
               q10_softmax, q11_softmax_stable, q12_cross_entropy, q13_perplexity,
               q14_attention):
        fn()
    print("\n" + "=" * 64)
    print(" Xong 14 câu. Câu nào đoán sai = chỗ cần ôn lại trong cheat sheet.")
    print("=" * 64)


if __name__ == "__main__":
    main()
