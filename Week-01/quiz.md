# Tuần 1, Quiz: Đại số tuyến tính và hình học giải tích

> Tự kiểm tra **trước** khi xem solution. Tổng **19** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Khi nhân hai ma trận A có chiều (m, k) và B có chiều (k, n), kết quả A @ B có chiều nào, và điều kiện nào phải thỏa để phép nhân hợp lệ?

- **A.** Kết quả có chiều (m, n); chiều trong k của A phải khớp với chiều đầu của B
- **B.** Kết quả có chiều (k, k); chỉ cần A và B cùng số phần tử
- **C.** Kết quả có chiều (m, k); B phải khả nghịch
- **D.** Kết quả có chiều (n, m); hai ma trận phải vuông

## Câu 2 (Trắc nghiệm)

Vì sao phép nhân ma trận nói chung không giao hoán, tức là A @ B thường khác B @ A?

- **A.** Vì máy tính làm tròn số theo thứ tự khác nhau
- **B.** Vì định thức của tích thay đổi theo thứ tự
- **C.** Vì mỗi ma trận là một ánh xạ tuyến tính, và hợp hai ánh xạ phụ thuộc thứ tự thực hiện, ví dụ xoay rồi kéo dãn khác kéo dãn rồi xoay
- **D.** Vì chỉ ma trận vuông mới nhân được theo cả hai chiều

## Câu 3 (Tự luận)

Hãy giải thích bằng lời của bạn vì sao dot product giữa hai vector đo được mức độ cùng hướng của chúng, và nêu hai chỗ trong lộ trình sẽ dùng lại ý này.

## Câu 4 (Trắc nghiệm)

Ba vector v1 = [1, 0, 1], v2 = [0, 1, 1] và v3 = v1 + v2 được xếp thành cột của một ma trận 3×3. Hạng của ma trận đó là bao nhiêu và vì sao?

- **A.** Không xác định được nếu chưa tính định thức
- **B.** Hạng bằng 1 vì cả ba vector đều có phần tử cuối bằng 1 hoặc 2
- **C.** Hạng bằng 2 vì v3 là tổ hợp tuyến tính của v1 và v2, nên ba vector chỉ trải ra một mặt phẳng
- **D.** Hạng bằng 3 vì ma trận có 3 cột

## Câu 5 (Trắc nghiệm)

Khi giải hệ A x = b vô nghiệm bằng least squares, công thức x̂ = (AᵀA)⁻¹Aᵀb cho ra điều gì, và ta kiểm tra kết quả bằng cách nào?

- **A.** Cho ra vector riêng của AᵀA; kiểm bằng định thức
- **B.** Cho ra nghịch đảo của A; kiểm bằng cách nhân A với kết quả
- **C.** Cho ra hệ số của phép chiếu trực giao b lên không gian cột của A; kiểm bằng cách xem phần dư b − A x̂ có trực giao với mọi cột của A không
- **D.** Cho ra nghiệm chính xác của hệ; kiểm bằng cách thay vào thấy A x̂ = b

## Câu 6 (Tự luận)

Một ma trận 6×5 có giá trị kỳ dị xấp xỉ [4.98, 2.17, 0.02, 0.02, 0.005]. Bạn kết luận gì về hạng hiệu dụng của nó, và điều này liên quan thế nào đến LoRA ở Tuần 9 và Tuần 11?

## Câu 7 (Trắc nghiệm)

Một ma trận A kích thước 2×4 có hạng rk(A) = 2, xem như ánh xạ tuyến tính Φ: R⁴ → R². Không gian nghiệm của Ax = 0 (kernel) có số chiều bằng bao nhiêu, và vì sao?

- **A.** 1, vì hạng 2 trừ đi số chiều của không gian đích là 2 và cộng thêm một chiều cho vector 0.
- **B.** 0, vì A có hạng đầy đủ theo hàng nên hệ Ax = 0 chỉ có nghiệm tầm thường x = 0.
- **C.** 4, vì kernel luôn là toàn bộ không gian nguồn khi số cột lớn hơn số hàng của ma trận.
- **D.** 2, vì theo định lý rank-nullity dim(ker Φ) + dim(Im Φ) = dim(V) = 4 và dim(Im Φ) = rk(A) = 2.

## Câu 8 (Trắc nghiệm)

MML nói rằng mọi inner product đều sinh ra một norm qua ‖x‖ = √⟨x, x⟩, nhưng điều ngược lại không đúng. Phát biểu nào sau đây đúng với nội dung sách?

- **A.** Norm Euclid ‖x‖₂ là ví dụ về một norm không được sinh ra từ bất kỳ inner product nào.
- **B.** Mọi norm trên Rⁿ đều được sinh ra từ đúng một inner product duy nhất, nên hai khái niệm tương đương.
- **C.** Norm Manhattan ‖x‖₁ là ví dụ về một norm không được sinh ra từ bất kỳ inner product nào.
- **D.** Norm chỉ được định nghĩa khi có inner product, nên không tồn tại norm nào ngoài norm sinh từ inner product.

## Câu 9 (Trắc nghiệm)

Trong Ví dụ 3.7 của MML, hai vector x = [1, 1]ᵀ và y = [−1, 1]ᵀ trực giao theo dot product. Nếu đổi sang inner product ⟨x, y⟩ = xᵀ diag(2, 1) y thì điều gì xảy ra?

- **A.** Chúng vẫn trực giao, vì trực giao là tính chất hình học của hai vector, không phụ thuộc inner product.
- **B.** Inner product này không hợp lệ vì ma trận diag(2, 1) không đối xứng xác định dương, nên không thể tính góc.
- **C.** Chúng trở thành cùng phương, vì ma trận diag(2, 1) kéo giãn trục thứ nhất gấp đôi làm hai vector trùng hướng.
- **D.** Chúng không còn trực giao nữa: cos ω = −1/3 và góc xấp xỉ 109,5°, cho thấy trực giao phụ thuộc inner product đã chọn.

## Câu 10 (Trắc nghiệm)

Cho A là ma trận trực giao (AAᵀ = AᵀA = I). Khi biến đổi hai vector x, y bằng A, độ dài ‖Ax‖ và góc giữa Ax và Ay thay đổi thế nào so với x, y ban đầu?

- **A.** Cả độ dài và góc đều giữ nguyên, vì xᵀAᵀAy = xᵀy; A biểu diễn phép xoay (có thể kèm lật).
- **B.** Độ dài giữ nguyên nhưng góc có thể thay đổi tùy theo hướng của x và y so với các cột của A.
- **C.** Độ dài được nhân với định thức của A còn góc được giữ nguyên, nên A chỉ là phép co giãn đều.
- **D.** Góc giữ nguyên nhưng độ dài bị nhân với căn bậc hai của số chiều n do chuẩn hóa cột.

## Câu 11 (Trắc nghiệm)

Chiếu vector x = [1, 1, 1]ᵀ lên đường thẳng qua gốc có vector chỉ phương b = [1, 2, 2]ᵀ (dùng dot product). Điểm chiếu π_U(x) là gì?

- **A.** [1, 1, 1]ᵀ, vì x đã có tọa độ dương như b nên nó nằm sẵn trong không gian con U.
- **B.** (5/9)·[1, 2, 2]ᵀ, vì hệ số chiếu λ = bᵀx/‖b‖² = 5/9 và π_U(x) = λb.
- **C.** (5/3)·[1, 2, 2]ᵀ, vì hệ số chiếu chính là bᵀx = 5 rồi chia cho ‖b‖ = 3.
- **D.** (1/3)·[1, 2, 2]ᵀ, vì hệ số chiếu là bᵀx chia cho ‖b‖ = 3.

## Câu 12 (Trắc nghiệm)

Ma trận A = [[4, 2], [1, 3]] có trace bằng 7 và định thức bằng 10. Dựa vào tính chất tổng và tích các trị riêng, cặp trị riêng của A là gì?

- **A.** λ₁ = 4 và λ₂ = 3, vì trị riêng của ma trận vuông luôn là các phần tử nằm trên đường chéo chính.
- **B.** λ₁ = 1 và λ₂ = 6, vì tổng bằng 7 và đây là hai số nguyên dương duy nhất thỏa điều kiện tổng.
- **C.** λ₁ = 2 và λ₂ = 5, vì chúng có tổng 7 bằng trace và tích 10 bằng định thức của A.
- **D.** λ₁ = −2 và λ₂ = −5, vì đa thức đặc trưng λ² + 7λ + 10 có hai nghiệm âm.

## Câu 13 (Trắc nghiệm)

Xét A₁ = [[9, 6], [6, 5]] và A₂ = [[9, 6], [6, 3]]. Cả hai đều đối xứng. Phát biểu nào đúng về tính xác định dương của chúng?

- **A.** A₂ xác định dương còn A₁ không, vì định thức của A₂ nhỏ hơn nên dạng toàn phương của nó bị chặn tốt hơn.
- **B.** Cả hai đều xác định dương vì mọi phần tử đều dương và ma trận đối xứng thì trị riêng luôn dương.
- **C.** A₁ xác định dương vì xᵀA₁x = (3x₁ + 2x₂)² + x₂² > 0 với x ≠ 0; A₂ thì không, vì xᵀA₂x = (3x₁ + 2x₂)² − x₂² âm tại x = [2, −3]ᵀ.
- **D.** Không ma trận nào xác định dương, vì phần tử ngoài đường chéo 6 lớn hơn phần tử đường chéo 5 và 3.

## Câu 14 (Trắc nghiệm)

Cho x = [3, −4, 1]ᵀ. Bộ giá trị (‖x‖₁, ‖x‖₂, ‖x‖∞) theo định nghĩa các chuẩn ℓp là gì?

- **A.** (0, √26, 4), vì chuẩn ℓ1 là tổng đại số các phần tử nên với vector này 3 − 4 + 1 = 0.
- **B.** (8, 26, 4), vì chuẩn ℓ2 được định nghĩa là tổng bình phương các phần tử và không lấy căn bậc hai.
- **C.** (8, √26, 4), vì ℓ1 là tổng trị tuyệt đối, ℓ2 là căn của tổng bình phương, ℓ∞ là trị tuyệt đối lớn nhất.
- **D.** (8, √26, 3), vì chuẩn vô cùng lấy phần tử đầu tiên của vector, không lấy trị tuyệt đối lớn nhất.

## Câu 15 (Tự luận)

MML dùng ảnh Stonehenge 1432×1910 để minh họa xấp xỉ hạng thấp. Hãy nêu cách viết A thành tổng các ma trận hạng 1, cho biết xấp xỉ hạng 5 cần lưu bao nhiêu số so với ảnh gốc, rồi áp dụng cùng phép tính cho ma trận hiệu chỉnh LoRA kích thước d×k với hạng r.

## Câu 16 (Tự luận)

MML lưu ý rằng số chiều của một không gian vector không nhất thiết bằng số phần tử trong mỗi vector. Hãy giải thích nhận xét này qua ví dụ trong sách, nêu ba cách phát biểu tương đương của một cơ sở, và cho biết vì sao ý này quan trọng khi bạn nhìn một ma trận embedding có 768 cột.

## Câu 17 (Tự luận)

Tính cosine của góc giữa x = [1, 1]ᵀ và y = [1, 2]ᵀ theo Ví dụ 3.6 của MML, nêu giá trị góc xấp xỉ, rồi giải thích vì sao trong RAG người ta dùng cosine similarity (chia dot product cho tích hai norm) thay vì dùng dot product thô.

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Định lý Eckart-Young (MML Theorem 4.25) nói gì về xấp xỉ hạng k của một ma trận, và điều đó được LoRA khai thác thế nào?

- **A.** Xấp xỉ hạng thấp chỉ đúng với ma trận đối xứng
- **B.** Mọi ma trận đều có hạng bằng số cột, nên không thể xấp xỉ hạng thấp
- **C.** Eckart-Young chỉ áp dụng cho ma trận vuông
- **D.** Giữ k giá trị kỳ dị lớn nhất của SVD cho xấp xỉ hạng k tốt nhất theo chuẩn Frobenius và chuẩn phổ; LoRA đặt cược rằng ma trận hiệu chỉnh khi fine-tune có hạng hiệu dụng thấp nên chỉ cần học tích B·A hạng r

## Nâng cao 2 (Tự luận)

Vì sao ma trận Gram AᵀA luôn nửa xác định dương, và tính chất này xuất hiện ở đâu trong công thức phép chiếu least squares?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
