"""
00_math_bridge_practice.py — luyện tay theo 00_math_bridge.md.

Chỉ dùng stdlib (math). Không cần PyTorch.

    python Week-01/00_math_bridge_practice.py
    python Week-01/00_math_bridge_practice.py --self-test

Cách học: đọc câu → đoán ra giấy → Enter → so đáp án.
Số đã đối chiếu với 00_math_bridge.md (tính 2026-08-16).
"""

from __future__ import annotations

import math
import sys


def log(msg: str) -> None:
    try:
        print(msg)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((msg + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()


def ask(n: int, section: str, question: str, hint: str) -> None:
    log("\n" + "=" * 64)
    log(f" Câu {n}  ·  {section}")
    log("=" * 64)
    log(question.strip())
    log(f"\n  >>> TỰ ĐOÁN: {hint}")
    if "--self-test" not in sys.argv:
        input("  (nhấn Enter để xem đáp án) ")


def show(label: str, value, explain: str) -> None:
    log(f"  → {label}: {value}")
    log(f"    {explain}")


def q1_sigma() -> None:
    ask(1, "Ký hiệu · Σ", "Σ của 2 + 4 + 6 bằng bao nhiêu?", "cộng hết các số")
    show("Σ", 2 + 4 + 6, "12. Σ = vòng for cộng dồn.")


def q2_ln() -> None:
    ask(
        2,
        "Ký hiệu · ln",
        "e⁰ = ?   ln(1) = ?   −ln(0.1) ≈ ?   (log trong ML là ln)",
        "1 ; 0 ; khoảng 2.3",
    )
    show("e⁰", math.exp(0), "e mũ 0 luôn = 1.")
    show("ln(1)", math.log(1), "ln 1 = 0.")
    show("−ln(0.1)", round(-math.log(0.1), 3), "≈ 2.303. Đây là CE khi p_đúng = 0.1.")


def q3_dot() -> None:
    ask(3, "Dot product", "[1, 2, 3] · [4, 5, 6] = ?", "1*4 + 2*5 + 3*6")
    dot = 1 * 4 + 2 * 5 + 3 * 6
    show("dot", dot, "32. Attention score (Tuần 3) cũng chỉ là phép này.")


def q4_dot_ortho() -> None:
    ask(4, "Dot product", "[1, 0] · [0, 1] = ? Ý nghĩa?", "vuông góc → ?")
    show("dot", 1 * 0 + 0 * 1, "0. Hai hướng vuông góc → tích vô hướng = 0.")


def q5_matmul_shape() -> None:
    ask(
        5,
        "Matmul · shape",
        "(2×3) @ (3×2) ra shape gì? (2×3) @ (2×4) có nhân được không?",
        "(m×k)@(k×n)→(m×n); chiều trong phải khớp",
    )
    show("shape", "(2, 2)", "Chiều trong 3 khớp.")
    show("(2×3)@(2×4)", "không nhân được", "Chiều trong 3 ≠ 2.")


def q6_matmul_cell() -> None:
    ask(
        6,
        "Matmul · một ô",
        "A hàng 1 = [1,2,3], B cột 1 = [7,9,11]. C₁₁ = ?",
        "dot của hàng với cột",
    )
    c11 = 1 * 7 + 2 * 9 + 3 * 11
    show("C₁₁", c11, "7+18+33 = 58. Mỗi ô của C là một dot product.")


def q7_chain() -> None:
    ask(
        7,
        "Chain rule",
        "f(x) = (2x+1)² tại x=1. ∂f/∂x = ?",
        "u=2x+1; (∂f/∂u)·(∂u/∂x)",
    )
    x = 1
    u = 2 * x + 1
    dfdx = (2 * u) * 2
    show("u", u, "2*1+1 = 3")
    show("∂f/∂x", dfdx, "2u * 2 = 12. Đúng câu checklist prerequisites.")


def q8_two_layer() -> None:
    ask(
        8,
        "Chain rule · 2 lớp",
        "y=3w+1, L=y², w=1. ∂L/∂w = ?",
        "(∂L/∂y)·(∂y/∂w) = 2y * 3",
    )
    w = 1
    y = 3 * w + 1
    dldw = (2 * y) * 3
    show("y", y, "4")
    show("∂L/∂w", dldw, "8*3 = 24. Backprop = lặp đúng phép nhân này.")


def q9_gd() -> None:
    ask(
        9,
        "Gradient descent",
        "L=w², w=5, lr=0.1. w mới sau 1 bước = ?",
        "w ← w − lr·(2w)",
    )
    w = 5 - 0.1 * (2 * 5)
    show("w", w, "5 − 1 = 4. Đi ngược gradient.")


def q10_softmax() -> None:
    ask(
        10,
        "Softmax",
        "z=[1,2,3]. Softmax tổng = ? Phần tử lớn nhất ≈ ?",
        "tổng 1; ≈ 0.665 ứng với logit 3",
    )
    z = [1.0, 2.0, 3.0]
    ex = [math.exp(v) for v in z]
    s = sum(ex)
    p = [e / s for e in ex]
    show("tổng", round(sum(p), 6), "1.0")
    show("p", [round(v, 4) for v in p], "[0.0900, 0.2447, 0.6652] — khớp 00_math_bridge.md")


def q11_ce() -> None:
    ask(
        11,
        "Cross-entropy",
        "p_đúng = 0.6652. CE = −ln(p) ≈ ?",
        "khoảng 0.41",
    )
    ce = -math.log(0.6652)
    show("CE", round(ce, 4), "≈ 0.4077. p=1 → CE=0; p nhỏ → CE lớn.")


def main() -> int:
    log("Cầu nối toán Tuần 1 — đoán trước, Enter sau. Không cần PyTorch.")
    for fn in (
        q1_sigma,
        q2_ln,
        q3_dot,
        q4_dot_ortho,
        q5_matmul_shape,
        q6_matmul_cell,
        q7_chain,
        q8_two_layer,
        q9_gd,
        q10_softmax,
        q11_ce,
    ):
        fn()
    log("\n" + "=" * 64)
    log(" Xong 11 câu. Sai chỗ nào → mở lại đúng mục trong 00_math_bridge.md.")
    log(" Qua cổng rồi mới sang 01_check_gpu.py → 02_theory_notes.md.")
    log("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
