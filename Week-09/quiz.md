# Tuần 9, Quiz: Instruction fine-tuning (classification + instruction-following + LoRA)

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Ý tưởng cốt lõi của LoRA?

- **A.** Lượng tử hoá trọng số xuống 4-bit
- **B.** Đóng băng W, học thêm hai ma trận thấp hạng B,A sao cho W' = W + BA với rank r ≪ d
- **C.** Tăng learning rate cho lớp cuối
- **D.** Cắt tỉa (prune) trọng số nhỏ

## Câu 2 (Trắc nghiệm)

Để fine-tune GPT cho classification, thay đổi kiến trúc nào là cốt lõi?

- **A.** Thêm một transformer block mới
- **B.** Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn, thường chỉ train head + vài layer cuối
- **C.** Bỏ positional embedding
- **D.** Tăng gấp đôi số attention head

## Câu 3 (Tự luận)

Trong instruction fine-tuning, vì sao thường mask phần prompt/instruction khỏi loss (chỉ tính loss trên phần response)?

## Câu 4 (Trắc nghiệm)

Instruction fine-tuning khác pretraining ở điểm nào về DỮ LIỆU và MỤC TIÊU?

- **A.** Khác thuật toán tối ưu hoàn toàn (không dùng cross-entropy)
- **B.** Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu, cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác
- **C.** Instruction FT không cần gradient
- **D.** Pretraining chỉ dùng cho model nhỏ

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Shazeer (arXiv 2002.05202) thay FFN 'Linear rồi GELU' bằng SwiGLU có ba ma trận. Ông giữ số tham số không đổi bằng cách nào, và điều này giải thích con số nào trong config Mistral 7B?

- **A.** Bỏ ma trận output
- **B.** Giảm số đơn vị ẩn d_ff; Mistral 7B có hidden_dim 14336 với d = 4096, tức 3,5d thay cho 4d
- **C.** Dùng bias để bù
- **D.** Chia sẻ trọng số giữa hai ma trận gate và up

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói instruction tuning là supervised learning với cùng objective language modeling. Vậy khác biệt kỹ thuật duy nhất so với pretraining ở Tuần 8 nằm ở đâu, và hệ quả lên cách tính loss là gì?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
