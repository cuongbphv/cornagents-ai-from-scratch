"""
Tuần 2, Tự cài gradient descent bằng NumPy trên hai hàm nhỏ.

Việc cần TỰ làm (deliverable): điền hai chỗ đánh dấu TODO rồi chạy:

    python Week-02/03_gradient_descent.py

Nguồn: MML mục 7.1 (trang 227-233) cho gradient descent và step size; Vũ Hữu Tiệp
Chương 12 (trang 140-160) cho GD một biến, nhiều biến, momentum, SGD; Nguyễn Thanh Tuấn
mục 3.3 (trang 50-55) cho cách giải thích trực quan trên y = x^2.
"""
from __future__ import annotations

import numpy as np


def quartic(x: float) -> float:
    """Hàm ví dụ Figure 7.2 trong MML (trang 227): x^4 + 7x^3 + 5x^2 - 17x + 3. Có hai cực tiểu."""
    return x**4 + 7 * x**3 + 5 * x**2 - 17 * x + 3


def quartic_grad(x: float) -> float:
    # TODO: viết đạo hàm của quartic theo x. Kiểm lại bằng sai phân trước khi dùng.
    raise NotImplementedError("Điền đạo hàm của x^4 + 7x^3 + 5x^2 - 17x + 3")


def gradient_descent_1d(grad_fn, x0: float, lr: float, steps: int) -> list[float]:
    """Trả về danh sách các x_t. MML (7.4): x_{t+1} = x_t - gamma * grad f(x_t)."""
    xs = [x0]
    for _ in range(steps):
        # TODO: một bước cập nhật
        raise NotImplementedError("Điền bước cập nhật gradient descent")
    return xs


def demo_two_minima() -> None:
    """Cùng một hàm, hai điểm khởi đầu, rơi vào hai cực tiểu khác nhau (MML trang 227).

    Câu hỏi: khởi đầu ở x0 = -10 và x0 = 0, điểm nào rơi vào cực tiểu có giá trị hàm thấp hơn?
    """
    for x0 in (-10.0, 0.0):
        xs = gradient_descent_1d(quartic_grad, x0, lr=0.001, steps=2000)
        print(f"x0={x0:>5}: x cuối = {xs[-1]:.4f}, f = {quartic(xs[-1]):.4f}")


def demo_step_size() -> None:
    """Step size quá lớn thì phân kỳ, quá nhỏ thì chậm (MML trang 228, Vũ Hữu Tiệp 12.2).

    Trên f(x) = x^2 với đạo hàm 2x: lr = 0.1 hội tụ, lr = 1.1 nổ.
    """
    for lr in (0.1, 0.5, 1.1):
        xs = gradient_descent_1d(lambda x: 2 * x, 5.0, lr=lr, steps=20)
        status = "phân kỳ" if abs(xs[-1]) > 5 else "hội tụ"
        print(f"lr={lr}: x sau 20 bước = {xs[-1]:.4e} ({status})")


if __name__ == "__main__":
    demo_two_minima()
    demo_step_size()
