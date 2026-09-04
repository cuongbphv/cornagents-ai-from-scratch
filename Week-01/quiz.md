# Tuần 1, Quiz: Đại số tuyến tính và hình học giải tích

> Tự kiểm tra **trước** khi xem solution. Tổng **8** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
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
