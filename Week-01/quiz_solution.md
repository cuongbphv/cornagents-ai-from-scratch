# Tuần 1, Đáp án & Giải thích: Đại số tuyến tính và hình học giải tích

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Khi nhân hai ma trận A có chiều (m, k) và B có chiều (k, n), kết quả A @ B có chiều nào, và điều kiện nào phải thỏa để phép nhân hợp lệ?

- **A.** Kết quả có chiều (k, k); chỉ cần A và B cùng số phần tử
- **B.** Kết quả có chiều (m, n); chiều trong k của A phải khớp với chiều đầu của B ✅
- **C.** Kết quả có chiều (n, m); hai ma trận phải vuông
- **D.** Kết quả có chiều (m, k); B phải khả nghịch

**Đáp án: B**

**Giải thích:** Phần tử (i, j) của tích là dot product của hàng i trong A với cột j trong B, nên hai chiều trong phải bằng nhau và hai chiều ngoài quyết định chiều kết quả (MML công thức 2.13, trang 22).

## Câu 2 (Trắc nghiệm)

Vì sao phép nhân ma trận nói chung không giao hoán, tức là A @ B thường khác B @ A?

- **A.** Vì máy tính làm tròn số theo thứ tự khác nhau
- **B.** Vì mỗi ma trận là một ánh xạ tuyến tính, và hợp hai ánh xạ phụ thuộc thứ tự thực hiện, ví dụ xoay rồi kéo dãn khác kéo dãn rồi xoay ✅
- **C.** Vì chỉ ma trận vuông mới nhân được theo cả hai chiều
- **D.** Vì định thức của tích thay đổi theo thứ tự

**Đáp án: B**

**Giải thích:** MML mục 2.7 (trang 48) nhìn ma trận như ánh xạ tuyến tính. Thí nghiệm matmul trong lab: xoay 90 độ rồi kéo dãn trục x đưa [1, 0] thành [0, 1], còn kéo dãn trước rồi xoay đưa nó thành [0, 2].

## Câu 3 (Tự luận)

Hãy giải thích bằng lời của bạn vì sao dot product giữa hai vector đo được mức độ cùng hướng của chúng, và nêu hai chỗ trong lộ trình sẽ dùng lại ý này.

**Trả lời mẫu:** Với inner product là dot product, cos của góc giữa x và y bằng x·y chia cho tích hai độ dài (MML Example 3.6, trang 77). Khi hai vector cùng hướng, cos gần 1 và dot product lớn; khi vuông góc, dot product bằng 0 (MML Definition 3.7). Lộ trình dùng lại ở điểm attention q·k của Tuần 6 và ở cosine similarity giữa embedding câu hỏi và đoạn văn trong RAG của Tuần 13.

**Giải thích:** Đây là công thức hình học duy nhất mà cả attention và retrieval đều đứng trên. Hiểu nó một lần ở đây thì hai tuần kia chỉ còn là lắp ráp.

## Câu 4 (Trắc nghiệm)

Ba vector v1 = [1, 0, 1], v2 = [0, 1, 1] và v3 = v1 + v2 được xếp thành cột của một ma trận 3×3. Hạng của ma trận đó là bao nhiêu và vì sao?

- **A.** Hạng bằng 3 vì ma trận có 3 cột
- **B.** Hạng bằng 2 vì v3 là tổ hợp tuyến tính của v1 và v2, nên ba vector chỉ trải ra một mặt phẳng ✅
- **C.** Hạng bằng 1 vì cả ba vector đều có phần tử cuối bằng 1 hoặc 2
- **D.** Không xác định được nếu chưa tính định thức

**Đáp án: B**

**Giải thích:** Hạng là số cột độc lập tuyến tính tối đa (MML mục 2.6, trang 47). Vì v3 phụ thuộc vào hai vector đầu, chỉ còn hai cột độc lập. Định thức của ma trận này bằng 0 nên nó không khả nghịch.

## Câu 5 (Trắc nghiệm)

Khi giải hệ A x = b vô nghiệm bằng least squares, công thức x̂ = (AᵀA)⁻¹Aᵀb cho ra điều gì, và ta kiểm tra kết quả bằng cách nào?

- **A.** Cho ra nghiệm chính xác của hệ; kiểm bằng cách thay vào thấy A x̂ = b
- **B.** Cho ra hệ số của phép chiếu trực giao b lên không gian cột của A; kiểm bằng cách xem phần dư b − A x̂ có trực giao với mọi cột của A không ✅
- **C.** Cho ra nghịch đảo của A; kiểm bằng cách nhân A với kết quả
- **D.** Cho ra vector riêng của AᵀA; kiểm bằng định thức

**Đáp án: B**

**Giải thích:** Phép chiếu trực giao (MML mục 3.8, trang 81) cho điểm gần b nhất trong không gian cột của A. Trong lab, Aᵀ(b − A x̂) bằng 0 chính là phép kiểm này. Linear regression ở Tuần 3 là đúng phép chiếu này.

## Câu 6 (Tự luận)

Một ma trận 6×5 có giá trị kỳ dị xấp xỉ [4.98, 2.17, 0.02, 0.02, 0.005]. Bạn kết luận gì về hạng hiệu dụng của nó, và điều này liên quan thế nào đến LoRA ở Tuần 9 và Tuần 11?

**Trả lời mẫu:** Hai giá trị kỳ dị đầu lớn, ba giá trị sau gần bằng 0, nên ma trận có hạng hiệu dụng 2: giữ hai thành phần đầu là được xấp xỉ hạng 2 gần như không mất thông tin, theo định lý Eckart-Young (MML Theorem 4.25, trang 131). LoRA đặt giả thuyết rằng ma trận hiệu chỉnh ΔW khi fine-tune cũng có hạng hiệu dụng thấp, nên chỉ cần học tích B·A với hạng r nhỏ.

**Giải thích:** SVD cho biết một ma trận thực sự có bao nhiêu chiều đáng kể. Đó là câu trả lời cho câu hỏi 'rank r = 8 có đủ không' mà bạn sẽ gặp khi cấu hình QLoRA.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Định lý Eckart–Young (MML Theorem 4.25) nói gì về xấp xỉ hạng k của một ma trận, và điều đó được LoRA khai thác thế nào?

- **A.** Mọi ma trận đều có hạng bằng số cột, nên không thể xấp xỉ hạng thấp
- **B.** Giữ k giá trị kỳ dị lớn nhất của SVD cho xấp xỉ hạng k tốt nhất theo chuẩn Frobenius và chuẩn phổ; LoRA đặt cược rằng ma trận hiệu chỉnh khi fine-tune có hạng hiệu dụng thấp nên chỉ cần học tích B·A hạng r ✅
- **C.** Xấp xỉ hạng thấp chỉ đúng với ma trận đối xứng
- **D.** Eckart–Young chỉ áp dụng cho ma trận vuông

**Đáp án: B**

**Giải thích:** MML mục 4.6 (Theorem 4.25, trang 131) phát biểu Eckart–Young. DeepSeek-V2 dùng cùng ý cho KV cache (MLA, arXiv 2405.04434), nên đây là ý toán học xuất hiện ba lần trong lộ trình.

## Nâng cao 2 (Tự luận)

Vì sao ma trận Gram AᵀA luôn nửa xác định dương, và tính chất này xuất hiện ở đâu trong công thức phép chiếu least squares?

**Trả lời mẫu:** Với mọi x, xᵀAᵀAx = (Ax)ᵀ(Ax) = ‖Ax‖² ≥ 0, đó là định nghĩa nửa xác định dương (Vũ Hữu Tiệp mục 1.13, trang 24). Trong phép chiếu x̂ = (AᵀA)⁻¹Aᵀb, ta cần AᵀA khả nghịch, tức xác định dương chặt; điều đó xảy ra khi các cột của A độc lập tuyến tính (MML mục 3.8, trang 81).

**Giải thích:** Khi các cột phụ thuộc tuyến tính, AᵀA suy biến và phải dùng pseudo-inverse hoặc regularization; đây là gốc của ridge regression.
