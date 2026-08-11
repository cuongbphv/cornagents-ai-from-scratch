# Tuần 7 — Quiz: Nhập môn alignment: SFT → Reward Model → DPO/PPO → GRPO

> Tự kiểm tra **trước** khi xem solution. Tổng **6** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Phân biệt SFT, DPO và GRPO.

## Câu 2 (Trắc nghiệm)

Reward Model (RM) trong RLHF học để làm gì?

- **A.** Sinh phản hồi cuối cùng cho người dùng
- **B.** Chấm điểm/so sánh mức ưu tiên giữa các output để hướng dẫn RL
- **C.** Tokenize dữ liệu
- **D.** Lưu KV cache

## Câu 3 (Trắc nghiệm)

So với PPO/RLHF kinh điển, DPO bỏ được thành phần nào?

- **A.** Bỏ dữ liệu ưu tiên (preference)
- **B.** Bỏ việc train reward model riêng và vòng lặp PPO — tối ưu thẳng từ cặp ưu tiên
- **C.** Bỏ model tham chiếu (reference)
- **D.** Bỏ tokenizer

## Câu 4 (Tự luận)

[Nâng cao] RLVR (Reinforcement Learning from Verifiable Rewards) là gì, vì sao hợp với reasoning?

## Câu 5 (Trắc nghiệm)

[Nâng cao] Bước 'midtrain' (nanochat) nằm ở đâu trong pipeline?

- **A.** Trước pretrain
- **B.** Giữa pretrain và SFT — dạy format hội thoại, special tokens, tool use
- **C.** Sau GRPO
- **D.** Thay thế SFT

## Câu 6 (Tự luận)

Trong RLHF/DPO, thành phần KL divergence (hoặc reference policy) đóng vai trò gì?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
