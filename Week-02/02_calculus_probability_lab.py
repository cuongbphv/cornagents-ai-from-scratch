"""
Tuần 2, Bài thực hành giải tích vector và xác suất bằng NumPy.

Chạy từng mục sau khi đọc mục tương ứng trong 01_theory_notes.md:

    python Week-02/02_calculus_probability_lab.py            # tất cả
    python Week-02/02_calculus_probability_lab.py gradcheck  # một mục

Nguồn cho từng mục ghi trong docstring (tên sách, mục, số trang in).
"""
from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=4, suppress=True)


def f_and_grad(x: np.ndarray) -> tuple[float, np.ndarray]:
    """f(x1, x2) = x1^2 x2 + x1 x2^3, Example 5.7 trong MML (trang 147).

    Gradient giải tích: df/dx1 = 2 x1 x2 + x2^3 ; df/dx2 = x1^2 + 3 x1 x2^2.
    """
    x1, x2 = x
    value = x1**2 * x2 + x1 * x2**3
    grad = np.array([2 * x1 * x2 + x2**3, x1**2 + 3 * x1 * x2**2])
    return float(value), grad


def numerical_gradient(fn, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Vũ Hữu Tiệp mục 2.6 (trang 36), Code 2.1: kiểm tra đạo hàm bằng sai phân trung tâm.

    (f(x + eps e_i) - f(x - eps e_i)) / (2 eps) cho từng chiều i.
    """
    g = np.zeros_like(x, dtype=float)
    for i in range(x.size):
        e = np.zeros_like(x, dtype=float)
        e[i] = eps
        g[i] = (fn(x + e)[0] - fn(x - e)[0]) / (2 * eps)
    return g


def gradcheck() -> None:
    """MML Example 5.7 (trang 147) + Vũ Hữu Tiệp 2.6 (trang 36): gradient giải tích phải khớp gradient số."""
    x = np.array([1.0, 2.0])
    _, g_analytic = f_and_grad(x)
    g_numeric = numerical_gradient(f_and_grad, x)
    print("gradient giải tích :", g_analytic)
    print("gradient số        :", g_numeric)
    print("sai lệch tối đa    :", float(np.max(np.abs(g_analytic - g_numeric))))


def chain_rule_scalar() -> None:
    """MML mục 5.6 (trang 159), hàm (5.109): f(x) = sqrt(x^2 + exp(x^2)) + cos(x^2 + exp(x^2)).

    Sách tính df/dx bằng chain rule, ta kiểm lại bằng số tại x = 0.5.
    """
    def f(x: float) -> float:
        a = x**2 + np.exp(x**2)
        return float(np.sqrt(a) + np.cos(a))

    def df(x: float) -> float:
        a = x**2 + np.exp(x**2)
        da = 2 * x + 2 * x * np.exp(x**2)
        return float(da * (1 / (2 * np.sqrt(a)) - np.sin(a)))

    x0, eps = 0.5, 1e-6
    print("df/dx theo chain rule tại 0.5 :", round(df(x0), 6))
    print("df/dx theo sai phân            :", round((f(x0 + eps) - f(x0 - eps)) / (2 * eps), 6))


def jacobian_of_linear_map() -> None:
    """MML mục 5.3 (trang 149): Jacobian của f(x) = A x chính là A.

    Đây là lý do backward của một lớp Linear chỉ là nhân với W (Tuần 5).
    """
    rng = np.random.default_rng(0)
    A = rng.standard_normal((3, 2))
    x = rng.standard_normal(2)
    J = np.zeros((3, 2))
    eps = 1e-6
    for i in range(2):
        e = np.zeros(2); e[i] = eps
        J[: i] = (A @ (x + e) - A @ (x - e)) / (2 * eps)
    print("Jacobian số khớp A không?", np.allclose(J, A))


def law_of_large_numbers() -> None:
    """Durrett EP4A Thm 4.7 (trang 93): trung bình mẫu hội tụ về kỳ vọng khi n lớn.

    Xúc xắc công bằng có kỳ vọng 3.5. Theo (1.1) trang 4, tần số tương đối tiến về xác suất.
    """
    rng = np.random.default_rng(42)
    for n in (10, 1_000, 100_000):
        rolls = rng.integers(1, 7, size=n)
        print(f"n={n:>7}: trung bình mẫu = {rolls.mean():.4f}, tần số mặt 6 = {(rolls == 6).mean():.4f}")


def central_limit_theorem() -> None:
    """Durrett EP4A Thm 4.9 (trang 95): (S_n - n mu) / (sigma sqrt n) tiến về chuẩn N(0, 1).

    Xúc xắc: mu = 3.5, sigma^2 = 35/12. Với n = 50, xác suất chuẩn hóa nằm trong [-1, 1]
    phải gần 2 Phi(1) - 1 = 0.6826 (bảng Phi ở trang 95: Phi(1) = 0.8413).
    """
    rng = np.random.default_rng(7)
    n, trials = 50, 20_000
    mu, sigma = 3.5, np.sqrt(35 / 12)
    sums = rng.integers(1, 7, size=(trials, n)).sum(axis=1)
    z = (sums - n * mu) / (sigma * np.sqrt(n))
    print("P(-1 <= Z <= 1) mô phỏng =", round(float(np.mean((z >= -1) & (z <= 1))), 4), "; lý thuyết 2*0.8413-1 =", round(2 * 0.8413 - 1, 4))


def bayes_formula() -> None:
    """Durrett EP4A mục 5.3 (trang 118) và MML mục 6.3 (trang 183-186): công thức Bayes.

    Bài toán xét nghiệm: tỉ lệ bệnh 1%, độ nhạy 95%, dương tính giả 5%.
    Hỏi P(bệnh | dương tính) là bao nhiêu? Nhiều người đoán khoảng 90%.
    """
    p_d = 0.01
    p_pos_given_d = 0.95
    p_pos_given_nd = 0.05
    p_pos = p_pos_given_d * p_d + p_pos_given_nd * (1 - p_d)
    print("P(bệnh | dương tính) =", round(p_pos_given_d * p_d / p_pos, 4))


def mle_gaussian() -> None:
    """Vũ Hữu Tiệp mục 4.2 (trang 53) và MML 9.2.1 (trang 293): MLE của Gaussian.

    Cực đại log-likelihood cho mu_ML = trung bình mẫu, sigma^2_ML = phương sai mẫu (chia n).
    Negative log-likelihood chính là loss mà Tuần 4 và Tuần 8 sẽ gọi là cross-entropy.
    """
    rng = np.random.default_rng(3)
    data = rng.normal(loc=2.0, scale=0.5, size=10_000)
    mu_ml = data.mean()
    var_ml = ((data - mu_ml) ** 2).mean()
    print("mu_ML =", round(float(mu_ml), 4), "; sigma_ML =", round(float(np.sqrt(var_ml)), 4), "(giá trị thật 2.0 và 0.5)")

    def nll(mu: float, sigma: float) -> float:
        return float(np.mean(0.5 * np.log(2 * np.pi * sigma**2) + (data - mu) ** 2 / (2 * sigma**2)))

    print("NLL tại (mu_ML, sigma_ML) =", round(nll(mu_ml, np.sqrt(var_ml)), 4), "; NLL tại (1.5, 0.5) =", round(nll(1.5, 0.5), 4))


LABS = {
    "gradcheck": gradcheck,
    "chain": chain_rule_scalar,
    "jacobian": jacobian_of_linear_map,
    "lln": law_of_large_numbers,
    "clt": central_limit_theorem,
    "bayes": bayes_formula,
    "mle": mle_gaussian,
}

if __name__ == "__main__":
    picked = sys.argv[1:] or list(LABS)
    for name in picked:
        print(f"\n=== {name}: {LABS[name].__doc__.strip().splitlines()[0]}")
        LABS[name]()
