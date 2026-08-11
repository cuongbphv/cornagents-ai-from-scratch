# Tuần 5 — Đáp án & Giải thích: Pretraining: training loop + 1 lần chạy GPT-2 thật

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Trắc nghiệm)

Quan hệ giữa cross-entropy loss L và perplexity (PPL)?

- **A.** PPL = L^2
- **B.** PPL = e^L ✅
- **C.** PPL = log(L)
- **D.** PPL = 1/L

**Đáp án: B**

**Giải thích:** PPL = e^L. Trực giác: perplexity ~ số lựa chọn 'trung bình' model còn phân vân; thấp hơn = dự đoán chắc hơn.

## Câu 2 (Tự luận)

Gradient accumulation là gì và vì sao quan trọng với GPU 8GB?

**Trả lời mẫu:** Thay vì cập nhật trọng số sau mỗi micro-batch nhỏ, ta cộng dồn gradient qua N micro-batch rồi mới step một lần → mô phỏng một 'effective batch' lớn (micro_batch × N) mà không cần chứa toàn bộ batch lớn trong VRAM. Với 3070 Ti 8GB chỉ vừa batch 1-2, gradient accumulation là cách đạt effective batch ~0.5M token/update kiểu Karpathy mà vẫn không OOM.

**Giải thích:** Giles part 32k đi sâu vào việc này khi train tốt hơn ở local.

## Câu 3 (Trắc nghiệm)

Lịch learning rate điển hình khi pretrain LLM là gì?

- **A.** Giữ LR cố định suốt
- **B.** Warmup tuyến tính tăng dần → rồi cosine decay giảm dần ✅
- **C.** Tăng dần đều tới cuối
- **D.** Giảm rồi tăng (chữ V)

**Đáp án: B**

**Giải thích:** Warmup tránh sốc gradient lúc đầu (trọng số ngẫu nhiên); cosine decay giúp hội tụ mượt về cuối.

## Câu 4 (Tự luận)

[Nâng cao] Giles thấy gì khi BỎ dropout trong pretraining, và vì sao?

**Trả lời mẫu:** Bỏ dropout cho test loss TỐT HƠN (part 32c), thậm chí hơn cả gradient clipping. Lý do: dropout là regularizer chống overfit, hữu ích khi fine-tune trên data nhỏ; nhưng pretraining chạy ~1 epoch trên lượng data khổng lồ thì gần như không overfit, nên dropout chỉ làm 'nhiễu' quá trình học. Vì vậy nhiều model hiện đại bỏ dropout ở pretraining.

**Giải thích:** Bài học: kỹ thuật 'tốt' phụ thuộc bối cảnh (data lớn 1-epoch vs data nhỏ nhiều epoch).

## Câu 5 (Trắc nghiệm)

[Nâng cao] Vì sao 'bits-per-byte' (bpb) tốt hơn perplexity khi so sánh các model có tokenizer khác nhau?

- **A.** bpb chạy nhanh hơn
- **B.** bpb chuẩn hoá loss về mức byte nên không phụ thuộc vocab/tokenizer → so sánh chéo được ✅
- **C.** bpb luôn nhỏ hơn perplexity
- **D.** bpb không cần dữ liệu validation

**Đáp án: B**

**Giải thích:** Perplexity phụ thuộc cách chia token; bpb quy về byte → công bằng giữa các tokenizer. nanochat dùng val_bpb làm chỉ số chính.

## Câu 6 (Trắc nghiệm)

[Nâng cao] Optimizer Muon (nanochat) áp dụng cho loại tham số nào?

- **A.** Mọi tham số, thay hẳn AdamW
- **B.** Các ma trận trọng số 2D (orthogonalize update bằng Newton-Schulz); embedding/head vẫn dùng AdamW ✅
- **C.** Chỉ embedding
- **D.** Chỉ bias

**Đáp án: B**

**Giải thích:** Muon orthogonalize bản cập nhật cho ma trận 2D → hội tụ pretraining nhanh hơn; là một yếu tố giúp nanochat 'speedrun' GPT-2.

## Câu 7 (Trắc nghiệm)

Mixed precision (bf16) lợi gì khi train?

- **A.** Tăng độ chính xác số học tuyệt đối
- **B.** Giảm VRAM và tăng tốc tính toán với mất chất lượng không đáng kể ✅
- **C.** Loại bỏ nhu cầu gradient
- **D.** Làm loss luôn giảm

**Đáp án: B**

**Giải thích:** bf16 dùng nửa bộ nhớ, tận dụng tensor core; bf16 có dải mũ rộng nên ổn định hơn fp16 (fp16 cần GradScaler).

## Câu 8 (Tự luận)

[Nâng cao] DistributedDataParallel (DDP) hoạt động thế nào (Giles part 29)?

**Trả lời mẫu:** DDP nhân bản toàn bộ model lên mỗi GPU; mỗi GPU xử lý một phần khác nhau của batch (data parallel), tính gradient cục bộ, rồi all-reduce (cộng và chia trung bình) gradient qua tất cả GPU trước khi mỗi bản sao cùng step. Kết quả tương đương train với batch lớn hơn N lần. Giles dùng DDP train base model trên 8×A100 trong cloud, nhanh hơn nhiều so với ~48h trên 1 card 3090.

**Giải thích:** DDP là mức song song đầu tiên cần biết; TP/PP/FSDP cho model không vừa 1 GPU.
