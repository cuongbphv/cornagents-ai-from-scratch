# Tuần 8, Đáp án & Giải thích: Pretraining: training loop + 1 lần chạy GPT-2 thật

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

**Giải thích:** Xem cách nanoGPT/train.py implement gradient_accumulation_steps.

## Câu 3 (Trắc nghiệm)

Lịch learning rate điển hình khi pretrain LLM là gì?

- **A.** Giữ LR cố định suốt
- **B.** Warmup tuyến tính tăng dần → rồi cosine decay giảm dần ✅
- **C.** Tăng dần đều tới cuối
- **D.** Giảm rồi tăng (chữ V)

**Đáp án: B**

**Giải thích:** Warmup tránh sốc gradient lúc đầu (trọng số ngẫu nhiên); cosine decay giúp hội tụ mượt về cuối.

## Câu 4 (Tự luận)

[Nâng cao] Vì sao các repo pretraining hiện đại (vd. nanoGPT config mặc định) đặt dropout = 0?

**Trả lời mẫu:** Dropout là regularizer chống overfit, hữu ích khi fine-tune trên data nhỏ; nhưng pretraining chạy ~1 epoch trên lượng data khổng lồ thì gần như không overfit, nên dropout chỉ làm 'nhiễu' quá trình học. Vì vậy pretraining hiện đại thường bỏ dropout (nanoGPT để dropout=0.0 cho pretrain, gợi ý 0.1+ khi fine-tune).

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

[Nâng cao] DistributedDataParallel (DDP) hoạt động thế nào?

**Trả lời mẫu:** DDP nhân bản toàn bộ model lên mỗi GPU; mỗi GPU xử lý một phần khác nhau của batch (data parallel), tính gradient cục bộ, rồi all-reduce (cộng và chia trung bình) gradient qua tất cả GPU trước khi mỗi bản sao cùng step. Kết quả tương đương train với batch lớn hơn N lần. Đây là cách nanoGPT/llm.c train trên node 8×A100 qua torchrun.

**Giải thích:** DDP là mức song song đầu tiên cần biết; TP/PP/FSDP cho model không vừa 1 GPU.

## Câu 9 (Trắc nghiệm)

Vì sao Jurafsky và Martin (SLP3 mục 3.3) không dùng xác suất thô của tập test để đánh giá language model mà dùng perplexity?

- **A.** Vì xác suất thô luôn bằng 1 với model đủ lớn
- **B.** Vì xác suất của tập test giảm khi văn bản dài hơn, nên cần một số đo tính trên mỗi token, chuẩn hóa theo độ dài, để so được giữa các văn bản khác độ dài ✅
- **C.** Vì perplexity tính nhanh hơn xác suất
- **D.** Vì xác suất thô chỉ định nghĩa được cho n-gram, không cho LLM

**Đáp án: B**

**Giải thích:** SLP3 trang 76: 'the probability of a test set gets smaller the longer the text. It's useful to have a metric that is per-word, normalized by length'. Perplexity là exp của cross-entropy trung bình trên token, đúng công thức ở mục lý thuyết của tuần.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Vì sao nanochat báo val_bpb (bits per byte) trên leaderboard thay cho loss thô, theo lập luận của SLP3 về perplexity?

- **A.** Vì bpb luôn nhỏ hơn loss
- **B.** Vì perplexity và loss tính trên token nên phụ thuộc tokenizer; chia lượng thông tin cho số byte thay cho số token cho phép so sánh chéo các model có vocab khác nhau ✅
- **C.** Vì GPU tính byte nhanh hơn token
- **D.** Vì bpb là metric của MMLU

**Đáp án: B**

**Giải thích:** SLP3 mục 3.3 và 3.7 nối perplexity với cross-entropy và entropy tính bằng bit; leaderboard nanochat đọc ngày 2026-09-04 có cột val_bpb và CORE, GPT-2 gốc CORE 0.2565.

## Nâng cao 2 (Tự luận)

Xiao và Zhu mô tả đường cong scaling law có ba pha theo lượng dữ liệu (Hestness et al. 2017). Ba pha đó là gì và lần pretrain 124M của bạn nằm ở đâu?

**Trả lời mẫu:** Khi dữ liệu còn ít, hiệu năng cải thiện chậm; sau đó vào pha cải thiện nhanh theo dạng power-law; cuối cùng chậm lại khi thêm dữ liệu không còn tăng nhiều (FoLLM mục 2.2.4, trang 63). Lần chạy 124M trên một mẫu FineWeb-Edu nằm ở quy mô rất nhỏ so với các model trong paper; mục tiêu của nó là hiểu cơ chế và đọc loss curve, không phải đuổi số.

**Giải thích:** Fleuret mục 3.7 (trang 51) nói cùng ý và dẫn Kaplan et al. 2020; hai paper Scaling Laws và Chinchilla trong kệ paper là nguồn gốc con số.
