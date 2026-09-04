"""
Tuần 1, Bài thực hành đại số tuyến tính bằng NumPy.

Cách dùng: đọc từng mục trong 01_theory_notes.md, rồi chạy mục tương ứng ở đây.
Mỗi hàm in ra một kết quả nhỏ mà bạn nên đoán TRƯỚC khi chạy. Đoán sai thì quay lại
đọc đúng mục đó trong sách (tên sách và số trang ghi trong docstring của hàm).

    python Week-01/02_linear_algebra_lab.py            # chạy tất cả
    python Week-01/02_linear_algebra_lab.py rank svd   # chỉ chạy vài mục

Chỉ dùng NumPy để bạn thấy toán thuần, chưa dính PyTorch (PyTorch bắt đầu ở Tuần 4).
"""
from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=4, suppress=True)


def matmul_is_composition() -> None:
    """MML mục 2.7 (trang 48-61): ma trận là ánh xạ tuyến tính, nhân ma trận là hợp hai ánh xạ.

    Câu hỏi để tự trả lời trước khi chạy: nếu xoay 90 độ rồi kéo dãn trục x gấp 2,
    kết quả có giống kéo dãn trước rồi xoay sau không?
    """
    rotate90 = np.array([[0.0, -1.0], [1.0, 0.0]])
    stretch_x = np.array([[2.0, 0.0], [0.0, 1.0]])
    v = np.array([1.0, 0.0])
    print("xoay rồi kéo  :", stretch_x @ rotate90 @ v)
    print("kéo rồi xoay  :", rotate90 @ stretch_x @ v)
    print("hai ma trận tích có bằng nhau không?", np.allclose(stretch_x @ rotate90, rotate90 @ stretch_x))


def shape_rules() -> None:
    """MML Def 2.1 (trang 22) và Vũ Hữu Tiệp mục 1.3 (trang 13): quy tắc chiều của phép nhân.

    A có chiều (m, k), B có chiều (k, n) thì A @ B có chiều (m, n). Chiều trong phải khớp.
    """
    A = np.random.randn(2, 3)
    B = np.random.randn(3, 4)
    print("A(2,3) @ B(3,4) ->", (A @ B).shape)
    try:
        _ = A @ np.random.randn(2, 4)
    except ValueError as e:
        print("A(2,3) @ C(2,4) -> lỗi, vì chiều trong 3 khác 2:", str(e).split("(")[0].strip())


def rank_and_independence() -> None:
    """MML mục 2.5-2.6 (trang 40-47): độc lập tuyến tính, cơ sở, hạng.

    Ba vector trong R^3 nhưng vector thứ ba là tổng hai vector đầu, nên chúng chỉ trải
    ra một mặt phẳng. Hạng là 2, không phải 3.
    """
    v1 = np.array([1.0, 0.0, 1.0])
    v2 = np.array([0.0, 1.0, 1.0])
    v3 = v1 + v2
    M = np.stack([v1, v2, v3], axis=1)
    print("rank của [v1 v2 v1+v2] =", np.linalg.matrix_rank(M))
    print("det =", round(float(np.linalg.det(M)), 6), "(bằng 0 nên không khả nghịch)")


def norms_and_angles() -> None:
    """MML Def 3.1 (trang 71), Ex 3.6 và Def 3.7 (trang 77); Vũ Hữu Tiệp mục 1.14 (trang 26).

    Ví dụ 3.6 trong MML: x = [1, 1], y = [1, 2]. cos(góc) = 3 / sqrt(10), góc xấp xỉ 0.32 rad (khoảng 18 độ).
    """
    x = np.array([1.0, 1.0])
    y = np.array([1.0, 2.0])
    cos_w = x @ y / (np.linalg.norm(x) * np.linalg.norm(y))
    print("cos(góc) =", round(float(cos_w), 4), "; góc (rad) =", round(float(np.arccos(cos_w)), 4),
          "; góc (độ) =", round(float(np.degrees(np.arccos(cos_w))), 1))
    print("chuẩn L1 của [3, -4] =", np.linalg.norm([3.0, -4.0], 1), "; chuẩn L2 =", np.linalg.norm([3.0, -4.0]))
    print("hai vector trực giao [1, 2] và [2, -1] có dot product =", np.array([1.0, 2.0]) @ np.array([2.0, -1.0]))


def projection_least_squares() -> None:
    """MML mục 3.8 (trang 81-91): phép chiếu trực giao.

    Chiếu b lên không gian cột của A cho ra điểm gần b nhất trong không gian đó.
    Đây chính là nghiệm least squares của hệ A x = b khi hệ vô nghiệm.
    """
    A = np.array([[1.0, 0.0], [1.0, 1.0], [1.0, 2.0]])  # đường thẳng y = a + b t với t = 0, 1, 2
    b = np.array([1.0, 2.0, 2.0])
    x_hat = np.linalg.solve(A.T @ A, A.T @ b)  # công thức chiếu (A^T A)^{-1} A^T b
    print("hệ số least squares [a, b] =", x_hat)
    print("khớp với np.linalg.lstsq:", np.allclose(x_hat, np.linalg.lstsq(A, b, rcond=None)[0]))
    residual = b - A @ x_hat
    print("phần dư có trực giao với cột của A không?", np.allclose(A.T @ residual, 0.0))


def eigen_and_svd() -> None:
    """MML Def 4.6 (trang 105), Thm 4.22 SVD (trang 119), mục 4.6 xấp xỉ ma trận (trang 129).

    Ma trận đối xứng có trị riêng thực. SVD tồn tại cho mọi ma trận, kể cả không vuông.
    Giữ lại k giá trị kỳ dị lớn nhất cho ta xấp xỉ hạng k tốt nhất theo chuẩn Frobenius
    (định lý Eckart-Young, MML Thm 4.25). LoRA ở Tuần 9 và 11 dựa đúng vào ý này.
    """
    S = np.array([[2.0, 1.0], [1.0, 2.0]])
    vals, vecs = np.linalg.eigh(S)
    print("trị riêng của [[2,1],[1,2]] =", vals)
    print("kiểm tra S v = lambda v:", np.allclose(S @ vecs[: 1], vals[1] * vecs[: 1]))

    rng = np.random.default_rng(0)
    low_rank = rng.standard_normal((6, 2)) @ rng.standard_normal((2, 5))  # hạng 2 thật
    noisy = low_rank + 0.01 * rng.standard_normal((6, 5))
    U, s, Vt = np.linalg.svd(noisy)
    print("giá trị kỳ dị:", s)
    approx2 = (U[: :2] * s[:2]) @ Vt[:2]
    print("sai số Frobenius khi giữ hạng 2 =", round(float(np.linalg.norm(noisy - approx2)), 4))


def positive_definite() -> None:
    """Vũ Hữu Tiệp mục 1.13 (trang 24): ma trận xác định dương và ma trận Gram A^T A.

    A^T A luôn nửa xác định dương vì x^T A^T A x = ||A x||^2 >= 0.
    """
    rng = np.random.default_rng(1)
    A = rng.standard_normal((4, 3))
    G = A.T @ A
    print("trị riêng của Gram A^T A (đều >= 0):", np.linalg.eigvalsh(G))


LABS = {
    "matmul": matmul_is_composition,
    "shape": shape_rules,
    "rank": rank_and_independence,
    "norm": norms_and_angles,
    "proj": projection_least_squares,
    "svd": eigen_and_svd,
    "pd": positive_definite,
}

if __name__ == "__main__":
    picked = sys.argv[1:] or list(LABS)
    for name in picked:
        print(f"\n=== {name}: {LABS[name].__doc__.strip().splitlines()[0]}")
        LABS[name]()
