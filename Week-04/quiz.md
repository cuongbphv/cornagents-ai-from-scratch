# Tuần 4 — Quiz: Lắp ráp & chạy mô hình GPT

> Tự kiểm tra **trước** khi xem solution. Tổng **7** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

LayerNorm trong transformer chuẩn hoá theo chiều nào?

- **A.** Theo chiều batch (như BatchNorm)
- **B.** Theo chiều feature/embedding của từng token (last dim)
- **C.** Theo chiều sequence
- **D.** Theo toàn bộ tensor

## Câu 2 (Tự luận)

Pre-LN + residual: x = x + Sublayer(LN(x)). Vì sao thiết kế này giúp train mạng sâu?

## Câu 3 (Trắc nghiệm)

Feed-forward network (FFN) trong block GPT-2 mở rộng chiều ẩn lên khoảng mấy lần d_model?

- **A.** 2 lần
- **B.** 4 lần
- **C.** 8 lần
- **D.** Không mở rộng

## Câu 4 (Trắc nghiệm)

GPT-2 small có khoảng bao nhiêu tham số (với emb_dim=768, n_layers=12, n_heads=12)?

- **A.** ~50M
- **B.** ~124M
- **C.** ~350M
- **D.** ~1.5B

## Câu 5 (Tự luận)

[Nâng cao] RMSNorm khác LayerNorm ở điểm nào, vì sao model hiện đại chuộng nó?

## Câu 6 (Trắc nghiệm)

[Nâng cao] SwiGLU FFN của Llama/Qwen thay thế phần nào của GPT-2?

- **A.** Thay attention
- **B.** Thay FFN GELU-4× bằng một FFN có cổng (gated) dùng SiLU, ~2/3·4d chiều ẩn
- **C.** Thay LayerNorm
- **D.** Thay positional embedding

## Câu 7 (Trắc nghiệm)

[Nâng cao] Trong một lớp Mixture-of-Experts (MoE), 'router' làm gì?

- **A.** Chọn top-k expert (FFN con) cho mỗi token, chỉ kích hoạt số ít expert
- **B.** Định tuyến gradient ngược
- **C.** Chọn GPU để chạy
- **D.** Sắp xếp token theo độ dài

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
