# Tuần 6 — Đáp án & Giải thích: Instruction fine-tuning (Raschka ch.6–7 + LoRA)

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Ý tưởng cốt lõi của LoRA?

- **A.** Lượng tử hoá trọng số xuống 4-bit
- **B.** Đóng băng W, học thêm hai ma trận thấp hạng B,A sao cho W' = W + BA với rank r ≪ d ✅
- **C.** Tăng learning rate cho lớp cuối
- **D.** Cắt tỉa (prune) trọng số nhỏ

**Đáp án: B**

**Giải thích:** LoRA chỉ train BA (ít tham số) thay vì toàn bộ W → tiết kiệm VRAM lớn, là nền của QLoRA (Tuần 8).

## Câu 2 (Trắc nghiệm)

Để fine-tune GPT cho classification (Raschka ch.6), thay đổi kiến trúc nào là cốt lõi?

- **A.** Thêm một transformer block mới
- **B.** Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn, thường chỉ train head + vài layer cuối ✅
- **C.** Bỏ positional embedding
- **D.** Tăng gấp đôi số attention head

**Đáp án: B**

**Giải thích:** Classification không cần dự đoán token: thay head 50257 chiều bằng Linear ra num_classes (vd. spam/ham), dùng hidden state của token cuối. Đóng băng phần lớn model giúp train nhanh, ít overfit.

## Câu 3 (Tự luận)

Trong instruction fine-tuning (ch.7), vì sao thường mask phần prompt/instruction khỏi loss (chỉ tính loss trên phần response)?

**Trả lời mẫu:** Mục tiêu là dạy model SINH phản hồi tốt, không phải học thuộc lại đề bài. Nếu tính loss trên cả instruction, gradient bị pha loãng bởi việc dự đoán lại phần text đã cho sẵn — model tối ưu cho việc lặp lại prompt thay vì chất lượng response. Mask (đặt label = -100 trong PyTorch) các token thuộc prompt để cross-entropy chỉ chấm phần model phải tự sinh.

**Giải thích:** Đây là chi tiết dễ bỏ sót khi tự viết collate function cho instruction dataset.

## Câu 4 (Trắc nghiệm)

Instruction fine-tuning khác pretraining ở điểm nào về DỮ LIỆU và MỤC TIÊU?

- **A.** Khác thuật toán tối ưu hoàn toàn (không dùng cross-entropy)
- **B.** Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu — cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác ✅
- **C.** Instruction FT không cần gradient
- **D.** Pretraining chỉ dùng cho model nhỏ

**Đáp án: B**

**Giải thích:** Cơ chế học giống nhau (next-token prediction); thứ thay đổi là dữ liệu (template Alpaca-style) và hành vi mà ta muốn model hội tụ về (làm theo instruction thay vì tiếp tục văn bản).
