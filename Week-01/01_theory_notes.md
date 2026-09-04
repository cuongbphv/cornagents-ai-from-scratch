# Lý thuyết Tuần 1: Đại số tuyến tính và hình học giải tích

> Tài liệu lý thuyết tự chứa cho Tuần 1. Nguồn chính là *Mathematics for Machine Learning* (viết tắt MML) chương 2, 3, 4 và *Machine Learning cơ bản* (Vũ Hữu Tiệp) chương 1; số trang ghi theo trang in của bản PDF trong `books/` (xem [`../docs/books/README.md`](../docs/books/README.md)). Mọi kết quả số trong file này lấy từ output của [`02_linear_algebra_lab.py`](02_linear_algebra_lab.py), chạy bằng NumPy 2.5.0 ngày 2026-09-04. Bạn nên tự chạy lại.

---

## 1. Ma trận là gì, và vì sao cách định nghĩa lại quan trọng

MML định nghĩa ma trận rất khô: "With m, n ∈ ℕ a real-valued (m, n) matrix A is an m·n-tuple of elements a_ij, i = 1, ..., m, j = 1, ..., n, which is ordered according to a rectangular scheme consisting of m rows and n columns" (MML, Definition 2.1, trang 22). Định nghĩa này chỉ nói ma trận là một bảng số. Cách nhìn hữu ích hơn nằm ở mục 2.7 (trang 48): mỗi ma trận là một **ánh xạ tuyến tính** Φ: V → W, và ngược lại, khi đã chọn cơ sở thì mỗi ánh xạ tuyến tính có đúng một ma trận biểu diễn.

Hệ quả bạn sẽ dùng suốt lộ trình: nhân hai ma trận là **hợp hai ánh xạ**. Vì hợp ánh xạ không giao hoán, nhân ma trận cũng không giao hoán. Thí nghiệm `matmul` trong lab: xoay 90 độ rồi kéo dãn trục x gấp 2 đưa vector [1, 0] thành [0, 1]; kéo dãn trước rồi xoay sau đưa nó thành [0, 2]. Hai ma trận tích khác nhau.

Ở Tuần 4, `nn.Linear(in, out)` là đúng một ánh xạ tuyến tính (cộng thêm một vector dịch b). Ở Tuần 6, ba ma trận W_Q, W_K, W_V trong attention là ba ánh xạ tuyến tính áp lên cùng một vector token. Nếu bạn đọc chúng như bảng số, code sẽ khó hiểu; đọc chúng như phép biến đổi không gian thì dễ hơn nhiều.

## 2. Quy tắc chiều

A có chiều (m, k), B có chiều (k, n), thì A @ B có chiều (m, n). Chiều trong (k) phải khớp; chiều ngoài quyết định kết quả. Phần tử (i, j) của tích là dot product của hàng i trong A với cột j trong B (MML, công thức 2.13, trang 22; Vũ Hữu Tiệp mục 1.3, trang 13).

Thí nghiệm `shape`: A(2,3) @ B(3,4) cho (2,4); A(2,3) @ C(2,4) báo lỗi vì 3 khác 2. Kỹ năng đọc chiều chảy qua từng phép tính là kỹ năng bạn cần nhất khi debug attention ở Tuần 6, nơi tensor có bốn chiều (batch, head, seq, dim).

## 3. Độc lập tuyến tính, cơ sở, hạng

Một tập vector gọi là độc lập tuyến tính khi không vector nào viết được thành tổ hợp tuyến tính của các vector còn lại (MML mục 2.5, trang 40). Số vector độc lập tối đa trong không gian cột của một ma trận gọi là **hạng** (MML mục 2.6, trang 47).

Thí nghiệm `rank`: ba vector v1 = [1, 0, 1], v2 = [0, 1, 1], v3 = v1 + v2 xếp thành ma trận 3×3 có hạng 2 và định thức 0. Ba vector đó chỉ trải ra một mặt phẳng trong ℝ³, nên ma trận không khả nghịch.

Vì sao cần biết: ở Tuần 9 và Tuần 11, LoRA thay ma trận hiệu chỉnh ΔW bằng tích B·A với hạng r rất nhỏ so với chiều d. Câu hỏi "hạng r = 8 có đủ không" chỉ có nghĩa khi bạn hiểu hạng là gì.

## 4. Norm, dot product, góc

**Norm** là hàm gán cho mỗi vector một độ dài, thỏa ba tính chất: thuần nhất tuyệt đối ‖λx‖ = |λ|‖x‖, bất đẳng thức tam giác, và xác định dương (MML, Definition 3.1, trang 71). Hai norm hay gặp: L1 (tổng trị tuyệt đối) và L2 (Euclid). Thí nghiệm `norm`: vector [3, −4] có L1 = 7 và L2 = 5.

**Dot product** x·y = Σ x_i y_i là một inner product, và góc giữa hai vector được tính từ nó:

```
cos ω = ⟨x, y⟩ / (‖x‖ ‖y‖)
```

MML tính ví dụ x = [1, 1], y = [1, 2]: cos ω = 3/√10, góc xấp xỉ 0.32 rad, khoảng 18 độ (MML, Example 3.6, trang 77). Lab cho cos ω = 0.9487, góc 0.3218 rad, tức 18.4 độ.

Hai vector **trực giao** khi inner product bằng 0 (MML, Definition 3.7, trang 77). Ví dụ [1, 2] và [2, −1] có dot product 0.

Ở Tuần 6, điểm attention giữa query q và key k là q·k (rồi chia √d_k): token nào có key cùng hướng với query thì được chú ý nhiều. Ở Tuần 13, cosine similarity giữa embedding câu hỏi và embedding đoạn văn quyết định đoạn nào được retrieve. Cả hai đều là công thức góc ở trên.

## 5. Phép chiếu trực giao và least squares

Chiếu vector b lên không gian cột của A cho ra điểm trong không gian đó gần b nhất. Với A có các cột độc lập, phép chiếu là

```
π(b) = A (Aᵀ A)⁻¹ Aᵀ b
```

(MML mục 3.8, trang 81 đến 91). Hệ số x̂ = (Aᵀ A)⁻¹ Aᵀ b chính là nghiệm least squares của hệ A x = b khi hệ vô nghiệm, và phần dư b − A x̂ trực giao với mọi cột của A.

Thí nghiệm `proj`: khớp đường thẳng y = a + b·t qua ba điểm (0, 1), (1, 2), (2, 2) cho [a, b] = [1.1667, 0.5], khớp với `np.linalg.lstsq`, và Aᵀ(b − A x̂) bằng 0. Ở Tuần 3, linear regression là đúng phép chiếu này, và MML chương 9 mục 9.4 gọi thẳng nó là "Maximum Likelihood as Orthogonal Projection".

## 6. Trị riêng và vector riêng

Với ma trận vuông A, số λ là **trị riêng** và vector x khác 0 là **vector riêng** tương ứng khi A x = λ x (MML, Definition 4.6, trang 105). Nói bằng lời: vector riêng là hướng mà ánh xạ A chỉ kéo dãn, không xoay.

Thí nghiệm `svd` phần đầu: ma trận đối xứng [[2, 1], [1, 2]] có trị riêng 1 và 3. Ma trận đối xứng luôn chéo hóa được với vector riêng trực chuẩn (MML, Theorem 4.21).

Ma trận Gram AᵀA luôn nửa xác định dương, vì xᵀAᵀAx = ‖Ax‖² ≥ 0 (Vũ Hữu Tiệp mục 1.13, trang 24). Thí nghiệm `pd` cho ba trị riêng đều dương. Ma trận này xuất hiện trong công thức phép chiếu ở mục 5 và trong PCA.

## 7. SVD và xấp xỉ hạng thấp

Eigendecomposition đòi ma trận vuông. **Singular value decomposition** (SVD) áp dụng cho mọi ma trận và luôn tồn tại: với A ∈ ℝ^{m×n} hạng r, A = U Σ Vᵀ, trong đó U và V trực giao, Σ chỉ có các giá trị kỳ dị σ₁ ≥ σ₂ ≥ ... ≥ σ_r > 0 trên đường chéo (MML, Theorem 4.22, trang 119). MML dẫn lại Strang gọi SVD là "fundamental theorem of linear algebra" vì tính phổ quát này.

Giữ lại k giá trị kỳ dị lớn nhất cho ta ma trận hạng k gần A nhất theo chuẩn Frobenius và chuẩn phổ. Đó là định lý Eckart-Young (MML, Theorem 4.25, trang 131). Thí nghiệm `svd` phần sau: một ma trận 6×5 sinh ra từ tích hạng 2 cộng nhiễu 0.01 có giá trị kỳ dị [4.9786, 2.1737, 0.0235, 0.0156, 0.0049]. Hai giá trị đầu lớn, ba giá trị sau gần bằng 0, đúng như "hạng thật" là 2. Giữ hạng 2 cho sai số Frobenius 0.0286, cùng bậc với nhiễu.

Đây là trực giác đứng sau LoRA (Tuần 9 và 11): nếu ma trận hiệu chỉnh cần học có "hạng hiệu dụng" thấp, thì học B·A với hạng r nhỏ mất rất ít thông tin. Paper LoRA gốc (arXiv 2106.09685, link ở [`../docs/papers/README.md`](../docs/papers/README.md)) đặt đúng giả thuyết này.

## 8. Tóm tắt bằng một bảng

| Khái niệm | Định nghĩa ngắn | Nguồn | Dùng ở tuần |
|---|---|---|---|
| Ma trận là ánh xạ tuyến tính | Nhân ma trận là hợp ánh xạ, không giao hoán | MML 2.7, tr. 48 | 4, 6 |
| Hạng | Số cột độc lập tuyến tính | MML 2.6, tr. 47 | 9, 11 |
| Norm, góc | cos ω = ⟨x,y⟩/(‖x‖‖y‖) | MML Def 3.1 tr. 71; Ex 3.6 tr. 77 | 6, 13 |
| Phép chiếu | x̂ = (AᵀA)⁻¹Aᵀb | MML 3.8, tr. 81 | 3 |
| Trị riêng | A x = λ x | MML Def 4.6, tr. 105 | 3 (PCA) |
| SVD, Eckart-Young | A = UΣVᵀ; giữ k σ lớn nhất là xấp xỉ hạng k tốt nhất | MML Thm 4.22 tr. 119; Thm 4.25 tr. 131 | 9, 11 |

## Nguồn

- Deisenroth, Faisal, Ong. *Mathematics for Machine Learning*. Cambridge University Press, 2020. PDF miễn phí tại mml-book.github.io (kiểm 2026-09-04). Chương 2, 3, 4.
- Vũ Hữu Tiệp. *Machine Learning cơ bản*. Bản 27/03/2018, repo tiepvupsu/ebookMLCB (CC BY-SA 4.0). Chương 1.
- Ankur Moitra. *Algorithmic Aspects of Machine Learning*. Chương 2 (đọc thêm).
