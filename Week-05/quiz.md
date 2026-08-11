# Tuần 5 — Quiz: Pretraining: training loop + 1 lần chạy GPT-2 thật

> Tự kiểm tra **trước** khi xem solution. Tổng **8** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Quan hệ giữa cross-entropy loss L và perplexity (PPL)?

- **A.** PPL = L^2
- **B.** PPL = e^L
- **C.** PPL = log(L)
- **D.** PPL = 1/L

## Câu 2 (Tự luận)

Gradient accumulation là gì và vì sao quan trọng với GPU 8GB?

## Câu 3 (Trắc nghiệm)

Lịch learning rate điển hình khi pretrain LLM là gì?

- **A.** Giữ LR cố định suốt
- **B.** Warmup tuyến tính tăng dần → rồi cosine decay giảm dần
- **C.** Tăng dần đều tới cuối
- **D.** Giảm rồi tăng (chữ V)

## Câu 4 (Tự luận)

[Nâng cao] Vì sao các repo pretraining hiện đại (vd. nanoGPT config mặc định) đặt dropout = 0?

## Câu 5 (Trắc nghiệm)

[Nâng cao] Vì sao 'bits-per-byte' (bpb) tốt hơn perplexity khi so sánh các model có tokenizer khác nhau?

- **A.** bpb chạy nhanh hơn
- **B.** bpb chuẩn hoá loss về mức byte nên không phụ thuộc vocab/tokenizer → so sánh chéo được
- **C.** bpb luôn nhỏ hơn perplexity
- **D.** bpb không cần dữ liệu validation

## Câu 6 (Trắc nghiệm)

[Nâng cao] Optimizer Muon (nanochat) áp dụng cho loại tham số nào?

- **A.** Mọi tham số, thay hẳn AdamW
- **B.** Các ma trận trọng số 2D (orthogonalize update bằng Newton-Schulz); embedding/head vẫn dùng AdamW
- **C.** Chỉ embedding
- **D.** Chỉ bias

## Câu 7 (Trắc nghiệm)

Mixed precision (bf16) lợi gì khi train?

- **A.** Tăng độ chính xác số học tuyệt đối
- **B.** Giảm VRAM và tăng tốc tính toán với mất chất lượng không đáng kể
- **C.** Loại bỏ nhu cầu gradient
- **D.** Làm loss luôn giảm

## Câu 8 (Tự luận)

[Nâng cao] DistributedDataParallel (DDP) hoạt động thế nào?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
