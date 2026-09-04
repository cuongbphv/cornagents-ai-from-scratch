# Tuần 9, Đáp án & Giải thích: Instruction fine-tuning (classification + instruction-following + LoRA)

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Ý tưởng cốt lõi của LoRA?

- **A.** Lượng tử hoá trọng số xuống 4-bit
- **B.** Đóng băng W, học thêm hai ma trận thấp hạng B,A sao cho W' = W + BA với rank r ≪ d ✅
- **C.** Tăng learning rate cho lớp cuối
- **D.** Cắt tỉa (prune) trọng số nhỏ

**Đáp án: B**

**Giải thích:** LoRA chỉ train BA (ít tham số) thay vì toàn bộ W → tiết kiệm VRAM lớn, là nền của QLoRA (Tuần 11).

## Câu 2 (Trắc nghiệm)

Để fine-tune GPT cho classification, thay đổi kiến trúc nào là cốt lõi?

- **A.** Thêm một transformer block mới
- **B.** Thay output head (vocab_size) bằng một head nhỏ số lớp = số nhãn, thường chỉ train head + vài layer cuối ✅
- **C.** Bỏ positional embedding
- **D.** Tăng gấp đôi số attention head

**Đáp án: B**

**Giải thích:** Classification không cần dự đoán token: thay head 50257 chiều bằng Linear ra num_classes (vd. spam/ham), dùng hidden state của token cuối. Đóng băng phần lớn model giúp train nhanh, ít overfit.

## Câu 3 (Tự luận)

Trong instruction fine-tuning, vì sao thường mask phần prompt/instruction khỏi loss (chỉ tính loss trên phần response)?

**Trả lời mẫu:** Mục tiêu là dạy model SINH phản hồi tốt, không phải học thuộc lại đề bài. Nếu tính loss trên cả instruction, gradient bị pha loãng bởi việc dự đoán lại phần text đã cho sẵn, model tối ưu cho việc lặp lại prompt thay vì chất lượng response. Mask (đặt label = -100 trong PyTorch) các token thuộc prompt để cross-entropy chỉ chấm phần model phải tự sinh.

**Giải thích:** Đây là chi tiết dễ bỏ sót khi tự viết collate function cho instruction dataset.

## Câu 4 (Trắc nghiệm)

Instruction fine-tuning khác pretraining ở điểm nào về DỮ LIỆU và MỤC TIÊU?

- **A.** Khác thuật toán tối ưu hoàn toàn (không dùng cross-entropy)
- **B.** Pretraining: text thô, học dự đoán token kế; instruction FT: cặp (instruction, response) có cấu trúc, học làm theo yêu cầu, cùng loss cross-entropy nhưng phân phối dữ liệu và hành vi đích khác ✅
- **C.** Instruction FT không cần gradient
- **D.** Pretraining chỉ dùng cho model nhỏ

**Đáp án: B**

**Giải thích:** Cơ chế học giống nhau (next-token prediction); thứ thay đổi là dữ liệu (template Alpaca-style) và hành vi mà ta muốn model hội tụ về (làm theo instruction thay vì tiếp tục văn bản).

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Shazeer (arXiv 2002.05202) thay FFN 'Linear rồi GELU' bằng SwiGLU có ba ma trận. Ông giữ số tham số không đổi bằng cách nào, và điều này giải thích con số nào trong config Mistral 7B?

- **A.** Bỏ ma trận output
- **B.** Giảm số đơn vị ẩn d_ff; Mistral 7B có hidden_dim 14336 với d = 4096, tức 3,5d thay cho 4d ✅
- **C.** Dùng bias để bù
- **D.** Chia sẻ trọng số giữa hai ma trận gate và up

**Đáp án: B**

**Giải thích:** Shazeer mục 3: 'we reduce the number of hidden units d_ff'. Mistral 7B Table 1 (arXiv 2310.06825).

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói instruction tuning là supervised learning với cùng objective language modeling. Vậy khác biệt kỹ thuật duy nhất so với pretraining ở Tuần 8 nằm ở đâu, và hệ quả lên cách tính loss là gì?

**Trả lời mẫu:** Khác ở dữ liệu (cặp instruction và response) và ở việc mask loss: chỉ tính cross-entropy trên phần response để model học sinh phản hồi, không học lặp lại đề bài; trong PyTorch đặt label -100 cho token prompt. Hàm loss, optimizer và cấu trúc training loop giữ nguyên (SLP3 mục 8.1, trang 210).

**Giải thích:** Paper 'Instruction Tuning With Loss Over Instructions' trong kệ paper thử ngược điều này và tìm thấy hai ngoại lệ đáng nhớ.
