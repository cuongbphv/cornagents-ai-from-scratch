# Tuần 9 — Quiz: Fine-tuning Mac/MLX + local inference stack

> Tự kiểm tra **trước** khi xem solution. Tổng **4** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
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

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
