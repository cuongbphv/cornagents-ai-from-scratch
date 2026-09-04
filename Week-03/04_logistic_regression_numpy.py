"""
Tuần 3, Logistic regression bằng NumPy, train bằng gradient descent, không dùng thư viện ML.

    python Week-03/04_logistic_regression_numpy.py

Việc TỰ làm: điền `sigmoid`, `nll_loss`, `grad`. Kiểm gradient bằng sai phân (Tuần 2)
trước khi train. Đây là mạng neural một lớp; Tuần 4 bạn sẽ viết lại nó bằng PyTorch
và Tuần 5 tự viết autograd để không phải tính `grad` bằng tay nữa.

Nguồn: Vũ Hữu Tiệp Chương 14 (trang 165-179, hàm mất mát và cách tối ưu); Shalizi
mục 11.2 (trang 257); Mehlig mục 5.3 (trang 79, gradient descent cho đơn vị tuyến tính).
"""
from __future__ import annotations

import numpy as np


def make_data(n: int = 400, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Hai cụm Gaussian 2 chiều, nhãn 0/1. Thêm cột 1 để gộp bias vào w."""
    rng = np.random.default_rng(seed)
    x0 = rng.normal([-1.0, -1.0], 0.8, size=(n // 2, 2))
    x1 = rng.normal([1.0, 1.0], 0.8, size=(n // 2, 2))
    X = np.vstack([x0, x1])
    y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
    X = np.hstack([X, np.ones((n, 1))])
    return X, y


def sigmoid(z: np.ndarray) -> np.ndarray:
    """TODO: 1 / (1 + exp(-z)). Nghĩ xem vì sao kết quả luôn nằm trong (0, 1)."""
    raise NotImplementedError


def nll_loss(w: np.ndarray, X: np.ndarray, y: np.ndarray) -> float:
    """Negative log-likelihood trung bình của Bernoulli.

    TODO: -mean( y log p + (1 - y) log(1 - p) ) với p = sigmoid(X w).
    Đây chính là binary cross-entropy. Tuần 2 mục MLE giải thích vì sao.
    """
    raise NotImplementedError


def grad(w: np.ndarray, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """TODO: gradient của nll_loss theo w. Kết quả gọn: X^T (p - y) / n."""
    raise NotImplementedError


def numerical_grad(w: np.ndarray, X: np.ndarray, y: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    g = np.zeros_like(w)
    for i in range(w.size):
        e = np.zeros_like(w); e[i] = eps
        g[i] = (nll_loss(w + e, X, y) - nll_loss(w - e, X, y)) / (2 * eps)
    return g


def main() -> None:
    X, y = make_data()
    w = np.zeros(X.shape[1])
    print("gradcheck sai lệch tối đa:", float(np.max(np.abs(grad(w, X, y) - numerical_grad(w, X, y)))))
    lr = 0.5
    for step in range(1, 301):
        w -= lr * grad(w, X, y)
        if step % 50 == 0:
            acc = float(np.mean((sigmoid(X @ w) > 0.5) == y))
            print(f"step {step:>3}: loss = {nll_loss(w, X, y):.4f}, accuracy = {acc:.3f}")


if __name__ == "__main__":
    main()
