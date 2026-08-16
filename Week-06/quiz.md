# Tuần 6 — Quiz: Instruction fine-tuning (classification + instruction-following + LoRA)

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

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
- **B.** Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu — cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác
- **C.** Instruction FT không cần gradient
- **D.** Pretraining chỉ dùng cho model nhỏ

## Câu 5 (Trắc nghiệm)

Mask response-only (label -100 cho phần prompt) là mặc định tốt, nhưng theo paper Instruction Modelling (arXiv 2405.14394, dẫn ở mục 3 theory notes), tính loss CẢ trên phần instruction lại có lợi trong điều kiện nào?

- **A.** Luôn luôn có lợi, nên bỏ hẳn masking
- **B.** Khi dataset có instruction dài kèm output ngắn, hoặc khi có ít mẫu train — nhóm tác giả quy lợi ích cho việc giảm overfitting
- **C.** Khi model có trên 7B tham số
- **D.** Khi dùng optimizer khác AdamW

## Câu 6 (Trắc nghiệm)

LoRA r=16 trên ma trận 4096×4096 chỉ train ~0.78% tham số, nhưng vì sao VRAM khi train giảm còn MẠNH hơn cả tỷ lệ đó?

- **A.** Vì LoRA tự động quantize base model xuống 4-bit
- **B.** Vì AdamW giữ 2 giá trị moment cho MỖI tham số được train — LoRA cắt số tham số train ~50–100× nên cắt luôn optimizer state tương ứng, thường là phần ăn VRAM lớn nhất khi full FT
- **C.** Vì LoRA bỏ không lưu activation
- **D.** Vì ma trận A, B được lưu ở CPU

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
