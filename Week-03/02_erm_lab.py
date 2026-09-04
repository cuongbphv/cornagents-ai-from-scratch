"""
Tuần 3, Thấy overfitting bằng mắt: ERM trên đa thức bậc tăng dần.

    python Week-03/02_erm_lab.py

Việc TỰ làm: điền hàm `fit_poly` (nghiệm least squares, xem Tuần 1 mục phép chiếu) và
`empirical_risk`. Sau đó đọc bảng in ra và trả lời: bậc nào làm training loss nhỏ nhất,
bậc nào làm validation loss nhỏ nhất, và vì sao hai bậc đó khác nhau.

Nguồn: Shalev-Shwartz & Ben-David mục 2.2 (trang 35, eq. 2.2 empirical risk) và 11.2
(trang 146-151, validation); Shalizi mục 3.3-3.4 (trang 74-89); Vũ Hữu Tiệp Chương 8
(trang 91-100); Tong Zhang mục 1.1 (trang 2, training loss và test loss).
"""
from __future__ import annotations

import numpy as np


def make_data(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Hàm thật y = sin(2 pi x) cộng nhiễu Gaussian sigma = 0.2. Learner không biết hàm này."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(0.0, 1.0, size=n)
    y = np.sin(2 * np.pi * x) + 0.2 * rng.standard_normal(n)
    return x, y


def design_matrix(x: np.ndarray, degree: int) -> np.ndarray:
    """Cột j là x^j, j = 0..degree. Lớp giả thuyết H = đa thức bậc <= degree."""
    return np.vander(x, degree + 1, increasing=True)


def fit_poly(x: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    """ERM với squared loss trên lớp đa thức bậc <= degree.

    TODO: trả về hệ số w sao cho ||X w - y||^2 nhỏ nhất, với X = design_matrix(x, degree).
    Gợi ý: np.linalg.lstsq. Đây là empirical risk minimization đúng nghĩa trong UML eq. (2.2).
    """
    raise NotImplementedError


def empirical_risk(w: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    """Trung bình squared loss trên tập (x, y). TODO: cài theo Tong Zhang trang 2, training-loss."""
    raise NotImplementedError


def main() -> None:
    x_train, y_train = make_data(n=20, seed=0)
    x_val, y_val = make_data(n=200, seed=1)  # mẫu mới cùng phân phối, chỉ dùng để đo
    print(f"{'bậc':>4} | {'train loss':>10} | {'val loss':>9}")
    for degree in (0, 1, 3, 5, 9, 15):
        w = fit_poly(x_train, y_train, degree)
        print(f"{degree:>4} | {empirical_risk(w, x_train, y_train):>10.4f} | {empirical_risk(w, x_val, y_val):>9.4f}")
    print("\nCâu hỏi: bậc nào tốt nhất trên train, bậc nào tốt nhất trên val? Ghi câu trả lời vào 03_learning_theory_notes.md.")


if __name__ == "__main__":
    main()
