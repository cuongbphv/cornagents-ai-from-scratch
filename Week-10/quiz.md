# Tuần 10, Quiz: Nhập môn alignment: SFT → Reward Model → DPO/PPO → GRPO

> Tự kiểm tra **trước** khi xem solution. Tổng **11** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Phân biệt SFT, DPO và GRPO.

## Câu 2 (Trắc nghiệm)

Reward Model (RM) trong RLHF học để làm gì?

- **A.** Chấm điểm/so sánh mức ưu tiên giữa các output để hướng dẫn RL
- **B.** Tokenize dữ liệu
- **C.** Lưu KV cache
- **D.** Sinh phản hồi cuối cùng cho người dùng

## Câu 3 (Trắc nghiệm)

So với PPO/RLHF kinh điển, DPO bỏ được thành phần nào?

- **A.** Bỏ tokenizer
- **B.** Bỏ model tham chiếu (reference)
- **C.** Bỏ dữ liệu ưu tiên (preference)
- **D.** Bỏ việc train reward model riêng và vòng lặp PPO, tối ưu thẳng từ cặp ưu tiên

## Câu 4 (Tự luận)

[Nâng cao] RLVR (Reinforcement Learning from Verifiable Rewards) là gì, vì sao hợp với reasoning?

## Câu 5 (Trắc nghiệm)

[Nâng cao] Bước 'midtrain' (nanochat) nằm ở đâu trong pipeline?

- **A.** Trước pretrain
- **B.** Sau GRPO
- **C.** Thay thế SFT
- **D.** Giữa pretrain và SFT, dạy format hội thoại, special tokens, tool use

## Câu 6 (Tự luận)

Trong RLHF/DPO, thành phần KL divergence (hoặc reference policy) đóng vai trò gì?

## Câu 7 (Tự luận)

Jurafsky và Martin viết rằng các phương pháp alignment bằng dữ liệu ưu tiên hiện nay đứng trên khung reinforcement learning của Sutton và Barto. Hãy đặt tên từng thành phần của khung đó (agent, environment, action, reward, policy) vào bài toán alignment một LLM.

## Câu 8 (Trắc nghiệm)

Dataset HH-RLHF (Bai et al. 2022) bạn dùng tuần này viết tắt của gì, và điều đó nói gì về nội dung các cặp chosen/rejected?

- **A.** 'Human-Human RLHF', data do hai người chat với nhau
- **B.** 'Helpful Hints for RLHF', bộ hướng dẫn gán nhãn
- **C.** 'High-quality Human RLHF', data đã lọc chất lượng cao
- **D.** 'Helpful and Harmless', một phần các cặp chosen/rejected không so 'câu nào hay hơn' mà so 'câu nào AN TOÀN hơn'

## Câu 9 (Tự luận)

Vì sao nói 'refusal là hành vi được HUẤN LUYỆN, không phải bản năng', và vì sao RM/DPO/GRPO không tự đem lại harmlessness?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

GRPO (DeepSeekMath, arXiv 2402.03300) khác PPO ở điểm cốt lõi nào?

- **A.** GRPO chỉ dùng cho code
- **B.** GRPO không dùng KL
- **C.** GRPO bỏ critic (value network), ước lượng baseline từ điểm của một nhóm output sinh cho cùng prompt
- **D.** GRPO không cần reward

## Nâng cao 2 (Tự luận)

Hãy nối softmax policy của Sutton và Barto (eq. 13.2) với logits của LLM, và chỉ ra vì sao alignment bằng RL không cần thêm lớp nào mới vào model.

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
