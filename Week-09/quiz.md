# Tuần 9 — Quiz: Fine-tuning Mac/MLX + local inference stack

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Trắc nghiệm)

Vì sao MacBook 24GB có thể fine-tune model lớn hơn RTX 3070 Ti 8GB?

- **A.** CPU Mac nhanh hơn GPU
- **B.** Unified memory 24GB dùng chung cho cả 'GPU', cho phép chứa model 13-14B (đổi lại chậm hơn ~2-4×)
- **C.** MLX nén model xuống 1-bit
- **D.** Mac có nhiều GPU hơn

## Câu 2 (Tự luận)

Mô tả luồng fine-tune → phục vụ bằng MLX trên Mac.

## Câu 3 (Trắc nghiệm)

Ollama và LM Studio đóng vai trò gì?

- **A.** Train model from scratch
- **B.** Lớp inference/serving local — tải, quản lý và chat với model (GGUF/MLX) qua API/GUI
- **C.** Vector database cho RAG
- **D.** Tokenizer

## Câu 4 (Tự luận)

Tóm tắt phân vai 3070 Ti vs Mac 24GB vs Cloud.

## Câu 5 (Trắc nghiệm)

Theo Ilharco et al. 2022 (task arithmetic, mục 7 theory notes), 'task vector' là gì và cộng/trừ nó dùng để làm gì?

- **A.** Vector embedding của mô tả task, dùng để retrieve adapter phù hợp
- **B.** τ = W_finetuned − W_base — 'hướng' fine-tune đã đẩy model tới trong không gian trọng số; CỘNG nhiều τ để ghép nhiều kỹ năng vào một model, PHỦ ĐỊNH (−τ) để giảm một hành vi mà ít ảnh hưởng task khác
- **C.** Gradient trung bình của batch cuối cùng khi train
- **D.** Một hàng của ma trận LoRA A

## Câu 6 (Tự luận)

Mô tả quy trình kiểm tra catastrophic forgetting song ngữ bắt buộc của repo (mục 5 theory notes) và làm gì khi phát hiện suy giảm.

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
