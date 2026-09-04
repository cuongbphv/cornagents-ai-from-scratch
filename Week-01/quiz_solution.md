# Tuần 1, Đáp án & Giải thích: Đại số tuyến tính và hình học giải tích

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Khi nhân hai ma trận A có chiều (m, k) và B có chiều (k, n), kết quả A @ B có chiều nào, và điều kiện nào phải thỏa để phép nhân hợp lệ?

- **A.** Kết quả có chiều (m, n); chiều trong k của A phải khớp với chiều đầu của B (đáp án đúng)
- **B.** Kết quả có chiều (k, k); chỉ cần A và B cùng số phần tử
- **C.** Kết quả có chiều (m, k); B phải khả nghịch
- **D.** Kết quả có chiều (n, m); hai ma trận phải vuông

**Đáp án: A**

**Giải thích:** Phần tử (i, j) của tích là dot product của hàng i trong A với cột j trong B, nên hai chiều trong phải bằng nhau và hai chiều ngoài quyết định chiều kết quả (MML công thức 2.13, trang 22).

## Câu 2 (Trắc nghiệm)

Vì sao phép nhân ma trận nói chung không giao hoán, tức là A @ B thường khác B @ A?

- **A.** Vì máy tính làm tròn số theo thứ tự khác nhau
- **B.** Vì định thức của tích thay đổi theo thứ tự
- **C.** Vì mỗi ma trận là một ánh xạ tuyến tính, và hợp hai ánh xạ phụ thuộc thứ tự thực hiện, ví dụ xoay rồi kéo dãn khác kéo dãn rồi xoay (đáp án đúng)
- **D.** Vì chỉ ma trận vuông mới nhân được theo cả hai chiều

**Đáp án: C**

**Giải thích:** MML mục 2.7 (trang 48) nhìn ma trận như ánh xạ tuyến tính. Thí nghiệm matmul trong lab: xoay 90 độ rồi kéo dãn trục x đưa [1, 0] thành [0, 1], còn kéo dãn trước rồi xoay đưa nó thành [0, 2].

## Câu 3 (Tự luận)

Hãy giải thích bằng lời của bạn vì sao dot product giữa hai vector đo được mức độ cùng hướng của chúng, và nêu hai chỗ trong lộ trình sẽ dùng lại ý này.

**Trả lời mẫu:** Với inner product là dot product, cos của góc giữa x và y bằng x·y chia cho tích hai độ dài (MML Example 3.6, trang 77). Khi hai vector cùng hướng, cos gần 1 và dot product lớn; khi vuông góc, dot product bằng 0 (MML Definition 3.7). Lộ trình dùng lại ở điểm attention q·k của Tuần 6 và ở cosine similarity giữa embedding câu hỏi và đoạn văn trong RAG của Tuần 13.

**Giải thích:** Đây là công thức hình học duy nhất mà cả attention và retrieval đều đứng trên. Hiểu nó một lần ở đây thì hai tuần kia chỉ còn là lắp ráp.

## Câu 4 (Trắc nghiệm)

Ba vector v1 = [1, 0, 1], v2 = [0, 1, 1] và v3 = v1 + v2 được xếp thành cột của một ma trận 3×3. Hạng của ma trận đó là bao nhiêu và vì sao?

- **A.** Không xác định được nếu chưa tính định thức
- **B.** Hạng bằng 1 vì cả ba vector đều có phần tử cuối bằng 1 hoặc 2
- **C.** Hạng bằng 2 vì v3 là tổ hợp tuyến tính của v1 và v2, nên ba vector chỉ trải ra một mặt phẳng (đáp án đúng)
- **D.** Hạng bằng 3 vì ma trận có 3 cột

**Đáp án: C**

**Giải thích:** Hạng là số cột độc lập tuyến tính tối đa (MML mục 2.6, trang 47). Vì v3 phụ thuộc vào hai vector đầu, chỉ còn hai cột độc lập. Định thức của ma trận này bằng 0 nên nó không khả nghịch.

## Câu 5 (Trắc nghiệm)

Khi giải hệ A x = b vô nghiệm bằng least squares, công thức x̂ = (AᵀA)⁻¹Aᵀb cho ra điều gì, và ta kiểm tra kết quả bằng cách nào?

- **A.** Cho ra vector riêng của AᵀA; kiểm bằng định thức
- **B.** Cho ra nghịch đảo của A; kiểm bằng cách nhân A với kết quả
- **C.** Cho ra hệ số của phép chiếu trực giao b lên không gian cột của A; kiểm bằng cách xem phần dư b − A x̂ có trực giao với mọi cột của A không (đáp án đúng)
- **D.** Cho ra nghiệm chính xác của hệ; kiểm bằng cách thay vào thấy A x̂ = b

**Đáp án: C**

**Giải thích:** Phép chiếu trực giao (MML mục 3.8, trang 81) cho điểm gần b nhất trong không gian cột của A. Trong lab, Aᵀ(b − A x̂) bằng 0 chính là phép kiểm này. Linear regression ở Tuần 3 là đúng phép chiếu này.

## Câu 6 (Tự luận)

Một ma trận 6×5 có giá trị kỳ dị xấp xỉ [4.98, 2.17, 0.02, 0.02, 0.005]. Bạn kết luận gì về hạng hiệu dụng của nó, và điều này liên quan thế nào đến LoRA ở Tuần 9 và Tuần 11?

**Trả lời mẫu:** Hai giá trị kỳ dị đầu lớn, ba giá trị sau gần bằng 0, nên ma trận có hạng hiệu dụng 2: giữ hai thành phần đầu là được xấp xỉ hạng 2 gần như không mất thông tin, theo định lý Eckart-Young (MML Theorem 4.25, trang 131). LoRA đặt giả thuyết rằng ma trận hiệu chỉnh ΔW khi fine-tune cũng có hạng hiệu dụng thấp, nên chỉ cần học tích B·A với hạng r nhỏ.

**Giải thích:** SVD cho biết một ma trận thực sự có bao nhiêu chiều đáng kể. Đó là câu trả lời cho câu hỏi 'rank r = 8 có đủ không' mà bạn sẽ gặp khi cấu hình QLoRA.

## Câu 7 (Trắc nghiệm)

Một ma trận A kích thước 2×4 có hạng rk(A) = 2, xem như ánh xạ tuyến tính Φ: R⁴ → R². Không gian nghiệm của Ax = 0 (kernel) có số chiều bằng bao nhiêu, và vì sao?

- **A.** 1, vì hạng 2 trừ đi số chiều của không gian đích là 2 và cộng thêm một chiều cho vector 0.
- **B.** 0, vì A có hạng đầy đủ theo hàng nên hệ Ax = 0 chỉ có nghiệm tầm thường x = 0.
- **C.** 4, vì kernel luôn là toàn bộ không gian nguồn khi số cột lớn hơn số hàng của ma trận.
- **D.** 2, vì theo định lý rank-nullity dim(ker Φ) + dim(Im Φ) = dim(V) = 4 và dim(Im Φ) = rk(A) = 2. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Định lý rank-nullity phát biểu dim(ker(Φ)) + dim(Im(Φ)) = dim(V) (công thức 2.129). Ảnh của Φ là span các cột của A nên dim(Im Φ) = rk(A) = 2, suy ra dim(ker Φ) = 4 − 2 = 2; Example 2.25 tính đúng kernel hai chiều cho một ma trận 2×4 như vậy. Hệ quả trong sách: nếu dim(Im Φ) < dim(V) thì Ax = 0 có vô số nghiệm. Ý này nối sang Tuần 1 lab về hạng hiệu dụng: một ma trận trọng số có kernel lớn nghĩa là nhiều hướng đầu vào bị ánh xạ về 0 (MML mục 2.7.3, Định lý 2.24, Ví dụ 2.25, tr. 59-60)

## Câu 8 (Trắc nghiệm)

MML nói rằng mọi inner product đều sinh ra một norm qua ‖x‖ = √⟨x, x⟩, nhưng điều ngược lại không đúng. Phát biểu nào sau đây đúng với nội dung sách?

- **A.** Norm Euclid ‖x‖₂ là ví dụ về một norm không được sinh ra từ bất kỳ inner product nào.
- **B.** Mọi norm trên Rⁿ đều được sinh ra từ đúng một inner product duy nhất, nên hai khái niệm tương đương.
- **C.** Norm Manhattan ‖x‖₁ là ví dụ về một norm không được sinh ra từ bất kỳ inner product nào. (đáp án đúng)
- **D.** Norm chỉ được định nghĩa khi có inner product, nên không tồn tại norm nào ngoài norm sinh từ inner product.

**Đáp án: C**

**Giải thích:** Sách viết: "not every norm is induced by an inner product. The Manhattan norm (3.3) is an example of a norm without a corresponding inner product" ngay sau công thức (3.16). Norm Euclid thì ngược lại, chính là norm sinh từ dot product (3.4). Điểm này giải thích vì sao cosine similarity (cần inner product để có góc) được xây trên dot product và norm ℓ2, không xây trên ℓ1 (MML mục 3.3, công thức 3.16, tr. 75)

## Câu 9 (Trắc nghiệm)

Trong Ví dụ 3.7 của MML, hai vector x = [1, 1]ᵀ và y = [−1, 1]ᵀ trực giao theo dot product. Nếu đổi sang inner product ⟨x, y⟩ = xᵀ diag(2, 1) y thì điều gì xảy ra?

- **A.** Chúng vẫn trực giao, vì trực giao là tính chất hình học của hai vector, không phụ thuộc inner product.
- **B.** Inner product này không hợp lệ vì ma trận diag(2, 1) không đối xứng xác định dương, nên không thể tính góc.
- **C.** Chúng trở thành cùng phương, vì ma trận diag(2, 1) kéo giãn trục thứ nhất gấp đôi làm hai vector trùng hướng.
- **D.** Chúng không còn trực giao nữa: cos ω = −1/3 và góc xấp xỉ 109,5°, cho thấy trực giao phụ thuộc inner product đã chọn. (đáp án đúng)

**Đáp án: D**

**Giải thích:** Sách tính cos ω = ⟨x, y⟩/(‖x‖‖y‖) = −1/3 nên ω ≈ 1.91 rad ≈ 109.5°, và kết luận "vectors that are orthogonal with respect to one inner product do not have to be orthogonal with respect to a different inner product". diag(2, 1) là ma trận đối xứng xác định dương nên vẫn là inner product hợp lệ theo Định lý 3.5. Liên hệ: attention score qᵀk cũng là một dạng song tuyến tính; các ma trận W_Q, W_K học được quyết định cặp token nào được coi là "vuông góc" (MML mục 3.4, Ví dụ 3.7, công thức 3.27-3.28, tr. 77-78)

## Câu 10 (Trắc nghiệm)

Cho A là ma trận trực giao (AAᵀ = AᵀA = I). Khi biến đổi hai vector x, y bằng A, độ dài ‖Ax‖ và góc giữa Ax và Ay thay đổi thế nào so với x, y ban đầu?

- **A.** Cả độ dài và góc đều giữ nguyên, vì xᵀAᵀAy = xᵀy; A biểu diễn phép xoay (có thể kèm lật). (đáp án đúng)
- **B.** Độ dài giữ nguyên nhưng góc có thể thay đổi tùy theo hướng của x và y so với các cột của A.
- **C.** Độ dài được nhân với định thức của A còn góc được giữ nguyên, nên A chỉ là phép co giãn đều.
- **D.** Góc giữ nguyên nhưng độ dài bị nhân với căn bậc hai của số chiều n do chuẩn hóa cột.

**Đáp án: A**

**Giải thích:** Với dot product, ‖Ax‖² = xᵀAᵀAx = xᵀx = ‖x‖² (công thức 3.31) và cos ω của Ax, Ay bằng xᵀy/(‖x‖‖y‖) (công thức 3.32), nên "orthogonal matrices A with Aᵀ = A⁻¹ preserve both angles and distances" và chúng là các phép xoay có thể kèm lật. Đây là nền toán của việc xoay query và key theo vị trí (RoPE, Tuần 6-7) mà không làm đổi độ dài của chúng (MML mục 3.4, Định nghĩa 3.8, công thức 3.29-3.32, tr. 78)

## Câu 11 (Trắc nghiệm)

Chiếu vector x = [1, 1, 1]ᵀ lên đường thẳng qua gốc có vector chỉ phương b = [1, 2, 2]ᵀ (dùng dot product). Điểm chiếu π_U(x) là gì?

- **A.** [1, 1, 1]ᵀ, vì x đã có tọa độ dương như b nên nó nằm sẵn trong không gian con U.
- **B.** (5/9)·[1, 2, 2]ᵀ, vì hệ số chiếu λ = bᵀx/‖b‖² = 5/9 và π_U(x) = λb. (đáp án đúng)
- **C.** (5/3)·[1, 2, 2]ᵀ, vì hệ số chiếu chính là bᵀx = 5 rồi chia cho ‖b‖ = 3.
- **D.** (1/3)·[1, 2, 2]ᵀ, vì hệ số chiếu là bᵀx chia cho ‖b‖ = 3.

**Đáp án: B**

**Giải thích:** Ma trận chiếu là P_π = bbᵀ/‖b‖² (công thức 3.46); với b = [1, 2, 2]ᵀ ta có bᵀb = 9 và P_π = (1/9)[[1,2,2],[2,4,4],[2,4,4]] (công thức 3.47). Sách tính P_π x = (1/9)[5, 10, 10]ᵀ ∈ span[[1, 2, 2]ᵀ] (công thức 3.48), tức (5/9)b. Hệ số λ = bᵀx/‖b‖² (công thức 3.41) là tọa độ của điểm chiếu theo b; nếu ‖b‖ = 1 thì λ = bᵀx, đúng dạng attention score chiếu query lên key đơn vị (MML mục 3.8.1, Ví dụ 3.10, công thức 3.46-3.48, tr. 84-85)

## Câu 12 (Trắc nghiệm)

Ma trận A = [[4, 2], [1, 3]] có trace bằng 7 và định thức bằng 10. Dựa vào tính chất tổng và tích các trị riêng, cặp trị riêng của A là gì?

- **A.** λ₁ = 4 và λ₂ = 3, vì trị riêng của ma trận vuông luôn là các phần tử nằm trên đường chéo chính.
- **B.** λ₁ = 1 và λ₂ = 6, vì tổng bằng 7 và đây là hai số nguyên dương duy nhất thỏa điều kiện tổng.
- **C.** λ₁ = 2 và λ₂ = 5, vì chúng có tổng 7 bằng trace và tích 10 bằng định thức của A. (đáp án đúng)
- **D.** λ₁ = −2 và λ₂ = −5, vì đa thức đặc trưng λ² + 7λ + 10 có hai nghiệm âm.

**Đáp án: C**

**Giải thích:** Vũ Hữu Tiệp nêu tính chất: "Tích của tất cả các trị riêng của một ma trận bằng định thức của ma trận đó. Tổng tất cả các trị riêng của một ma trận bằng tổng các phần tử trên đường chéo" (Vũ Hữu Tiệp mục 1.11.2, tr. 23). MML tính trực tiếp cùng ma trận này: p(λ) = (4 − λ)(3 − λ) − 2 = λ² − 7λ + 10 = (2 − λ)(5 − λ), cho λ₁ = 2, λ₂ = 5 với E₅ = span[[2, 1]ᵀ] và E₂ = span[[1, −1]ᵀ] (MML mục 4.2, Ví dụ 4.5, công thức 4.29-4.35, tr. 107-108)

## Câu 13 (Trắc nghiệm)

Xét A₁ = [[9, 6], [6, 5]] và A₂ = [[9, 6], [6, 3]]. Cả hai đều đối xứng. Phát biểu nào đúng về tính xác định dương của chúng?

- **A.** A₂ xác định dương còn A₁ không, vì định thức của A₂ nhỏ hơn nên dạng toàn phương của nó bị chặn tốt hơn.
- **B.** Cả hai đều xác định dương vì mọi phần tử đều dương và ma trận đối xứng thì trị riêng luôn dương.
- **C.** A₁ xác định dương vì xᵀA₁x = (3x₁ + 2x₂)² + x₂² > 0 với x ≠ 0; A₂ thì không, vì xᵀA₂x = (3x₁ + 2x₂)² − x₂² âm tại x = [2, −3]ᵀ. (đáp án đúng)
- **D.** Không ma trận nào xác định dương, vì phần tử ngoài đường chéo 6 lớn hơn phần tử đường chéo 5 và 3.

**Đáp án: C**

**Giải thích:** MML khai triển xᵀA₁x = 9x₁² + 12x₁x₂ + 5x₂² = (3x₁ + 2x₂)² + x₂² > 0 với mọi x ≠ 0, nên A₁ xác định dương; còn xᵀA₂x = (3x₁ + 2x₂)² − x₂² "can be less than 0, e.g., for x = [2, −3]ᵀ". Đây là tính chất mà Hessian của hàm lồi (Tuần 2) và ma trận Gram trong least squares đều dựa vào. Vũ Hữu Tiệp bổ sung: mọi trị riêng của ma trận xác định dương là số thực dương và ma trận đó khả nghịch (Vũ Hữu Tiệp mục 1.13.2, tr. 25); khai triển của A₁, A₂ ở (MML mục 3.2.3, Ví dụ 3.4, công thức 3.12-3.13, tr. 74)

## Câu 14 (Trắc nghiệm)

Cho x = [3, −4, 1]ᵀ. Bộ giá trị (‖x‖₁, ‖x‖₂, ‖x‖∞) theo định nghĩa các chuẩn ℓp là gì?

- **A.** (0, √26, 4), vì chuẩn ℓ1 là tổng đại số các phần tử nên với vector này 3 − 4 + 1 = 0.
- **B.** (8, 26, 4), vì chuẩn ℓ2 được định nghĩa là tổng bình phương các phần tử và không lấy căn bậc hai.
- **C.** (8, √26, 4), vì ℓ1 là tổng trị tuyệt đối, ℓ2 là căn của tổng bình phương, ℓ∞ là trị tuyệt đối lớn nhất. (đáp án đúng)
- **D.** (8, √26, 3), vì chuẩn vô cùng lấy phần tử đầu tiên của vector, không lấy trị tuyệt đối lớn nhất.

**Đáp án: C**

**Giải thích:** Theo định nghĩa: ‖x‖₁ = |3| + |−4| + |1| = 8; ‖x‖₂ = √(9 + 16 + 1) = √26; và khi p → ∞ thì ‖x‖p → max_j |x_j| = 4 (công thức 1.41). Vũ Hữu Tiệp giải thích ℓ1 như quãng đường đi trong thành phố bàn cờ, ℓ2 là đường chim bay (Vũ Hữu Tiệp mục 1.14.1, công thức 1.37-1.41, tr. 27-28). MML nêu Manhattan norm ‖x‖₁ = Σ|xᵢ| (công thức 3.3) và Euclid norm ‖x‖₂ = √(xᵀx) (công thức 3.4) (MML mục 3.1, Ví dụ 3.1-3.2, tr. 71-72)

## Câu 15 (Tự luận)

MML dùng ảnh Stonehenge 1432×1910 để minh họa xấp xỉ hạng thấp. Hãy nêu cách viết A thành tổng các ma trận hạng 1, cho biết xấp xỉ hạng 5 cần lưu bao nhiêu số so với ảnh gốc, rồi áp dụng cùng phép tính cho ma trận hiệu chỉnh LoRA kích thước d×k với hạng r.

**Trả lời mẫu:** Theo SVD, A = Σᵢ σᵢ uᵢ vᵢᵀ (tổng r ma trận hạng 1, mỗi ma trận là tích ngoài của một cột U và một cột V). Cắt tổng ở k < r ta được xấp xỉ hạng k. Với ảnh Stonehenge, ảnh gốc cần 1432·1910 = 2.735.120 số, còn xấp xỉ hạng 5 chỉ cần 5·(1432 + 1910 + 1) = 16.715 số, khoảng 0,6% ảnh gốc. Với LoRA, ma trận hiệu chỉnh d×k hạng r được lưu bằng hai ma trận d×r và r×k, tức r(d + k) số thay cho d·k; ví dụ d = k = 4096 và r = 8 thì 8·8192 = 65.536 so với 16.777.216 tham số (con số LoRA tính theo cùng công thức lưu trữ, không in trong MML).

**Giải thích:** Công thức A = Σᵢ σᵢ uᵢ vᵢᵀ là (4.91) và xấp xỉ hạng k là Â(k) = Σᵢ₌₁ᵏ σᵢ uᵢ vᵢᵀ (4.92). Sách viết: "the original image requires 1,432 · 1,910 = 2,735,120 numbers, the rank-5 approximation requires us only to store the five singular values and the five left- and right-singular vectors (1,432 and 1,910-dimensional each) for a total of 5 · (1,432 + 1,910 + 1) = 16,715 numbers", tức chỉ hơn 0,6% ảnh gốc. Phần tính cho LoRA là suy luận từ cùng công thức lưu trữ (MML mục 4.6, công thức 4.90-4.92, tr. 129-130)

## Câu 16 (Tự luận)

MML lưu ý rằng số chiều của một không gian vector không nhất thiết bằng số phần tử trong mỗi vector. Hãy giải thích nhận xét này qua ví dụ trong sách, nêu ba cách phát biểu tương đương của một cơ sở, và cho biết vì sao ý này quan trọng khi bạn nhìn một ma trận embedding có 768 cột.

**Trả lời mẫu:** Ví dụ trong sách: V = span[[0, 1]ᵀ] là không gian một chiều dù vector cơ sở có hai phần tử. Số chiều là số vector trong một cơ sở, và mọi cơ sở của cùng một không gian đều có số phần tử bằng nhau. Một tập B là cơ sở khi và chỉ khi nó là tập sinh nhỏ nhất (minimal generating set), hoặc là tập độc lập tuyến tính lớn nhất (thêm bất kỳ vector nào cũng làm phụ thuộc), hoặc mọi vector đều viết được duy nhất thành tổ hợp tuyến tính của B. Với ma trận embedding 768 cột, 768 chỉ là số phần tử của mỗi vector; số chiều thực sự mà các embedding trải ra bằng hạng của ma trận, có thể nhỏ hơn nhiều, và đó là điều SVD ở lab Tuần 1 đo được.

**Giải thích:** Sách viết: "The dimension of a vector space is not necessarily the number of elements in a vector. For instance, the vector space V = span[[0, 1]ᵀ] is one-dimensional, although the basis vector possesses two elements" (MML mục 2.6.1, tr. 46). Ba phát biểu tương đương của cơ sở và nhận xét "all bases possess the same number of elements" nằm ở trang trước; số chiều dim(V) là số vector cơ sở. Hạng của ma trận là số cột độc lập tuyến tính và bằng số chiều của không gian cột (MML mục 2.6.1-2.6.2, tr. 45-47)

## Câu 17 (Tự luận)

Tính cosine của góc giữa x = [1, 1]ᵀ và y = [1, 2]ᵀ theo Ví dụ 3.6 của MML, nêu giá trị góc xấp xỉ, rồi giải thích vì sao trong RAG người ta dùng cosine similarity (chia dot product cho tích hai norm) thay vì dùng dot product thô.

**Trả lời mẫu:** cos ω = xᵀy/(√(xᵀx)·√(yᵀy)) = 3/√10 ≈ 0,949, nên ω = arccos(3/√10) ≈ 0,32 rad, khoảng 18°. Việc chia cho ‖x‖‖y‖ đưa giá trị vào đoạn [−1, 1] theo bất đẳng thức Cauchy-Schwarz, nên cosine chỉ đo mức cùng hướng của hai vector mà không phụ thuộc độ dài của chúng. Trong RAG, hai đoạn văn dài ngắn khác nhau có embedding với norm khác nhau; dot product thô sẽ ưu tiên vector dài, còn cosine so sánh hướng, tức nội dung ngữ nghĩa (phần áp dụng cho RAG suy thẳng từ định nghĩa góc trong sách).

**Giải thích:** Sách tính cos ω = xᵀy/√(xᵀx yᵀy) = 3/√10 và "the angle between the two vectors is arccos(3/√10) ≈ 0.32 rad, which corresponds to about 18°" (MML mục 3.4, Ví dụ 3.6, công thức 3.26, tr. 77). Bất đẳng thức Cauchy-Schwarz |⟨x, y⟩| ≤ ‖x‖‖y‖ (công thức 3.17) là lý do −1 ≤ ⟨x, y⟩/(‖x‖‖y‖) ≤ 1 (công thức 3.24) và tồn tại duy nhất ω ∈ [0, π] (MML mục 3.3-3.4, công thức 3.17, 3.24-3.25, tr. 75-76)

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Định lý Eckart-Young (MML Theorem 4.25) nói gì về xấp xỉ hạng k của một ma trận, và điều đó được LoRA khai thác thế nào?

- **A.** Xấp xỉ hạng thấp chỉ đúng với ma trận đối xứng
- **B.** Mọi ma trận đều có hạng bằng số cột, nên không thể xấp xỉ hạng thấp
- **C.** Eckart-Young chỉ áp dụng cho ma trận vuông
- **D.** Giữ k giá trị kỳ dị lớn nhất của SVD cho xấp xỉ hạng k tốt nhất theo chuẩn Frobenius và chuẩn phổ; LoRA đặt cược rằng ma trận hiệu chỉnh khi fine-tune có hạng hiệu dụng thấp nên chỉ cần học tích B·A hạng r (đáp án đúng)

**Đáp án: D**

**Giải thích:** MML mục 4.6 (Theorem 4.25, trang 131) phát biểu Eckart-Young. DeepSeek-V2 dùng cùng ý cho KV cache (MLA, arXiv 2405.04434), nên đây là ý toán học xuất hiện ba lần trong lộ trình.

## Nâng cao 2 (Tự luận)

Vì sao ma trận Gram AᵀA luôn nửa xác định dương, và tính chất này xuất hiện ở đâu trong công thức phép chiếu least squares?

**Trả lời mẫu:** Với mọi x, xᵀAᵀAx = (Ax)ᵀ(Ax) = ‖Ax‖² ≥ 0, đó là định nghĩa nửa xác định dương (Vũ Hữu Tiệp mục 1.13, trang 24). Trong phép chiếu x̂ = (AᵀA)⁻¹Aᵀb, ta cần AᵀA khả nghịch, tức xác định dương chặt; điều đó xảy ra khi các cột của A độc lập tuyến tính (MML mục 3.8, trang 81).

**Giải thích:** Khi các cột phụ thuộc tuyến tính, AᵀA suy biến và phải dùng pseudo-inverse hoặc regularization; đây là gốc của ridge regression.
