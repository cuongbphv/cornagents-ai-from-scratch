# Tuần 7 — Đáp án & Giải thích: Nhập môn alignment: SFT → Reward Model → DPO/PPO → GRPO

> ⚠️ Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Phân biệt SFT, DPO và GRPO.

**Trả lời mẫu:** SFT (Supervised Fine-Tuning): học bắt chước các phản hồi tốt bằng cross-entropy trên cặp (prompt, response chuẩn). DPO (Direct Preference Optimization): tối ưu trực tiếp từ cặp (chosen, rejected) bằng một loss dạng logistic, BỎ QUA reward model và PPO → đơn giản, ổn định. GRPO (Group Relative Policy Optimization): RL bỏ critic, lấy nhiều sample cho cùng prompt và chuẩn hoá reward theo nhóm; hợp với reward kiểm chứng được (RLVR) → nền của reasoning models.

**Giải thích:** Thứ tự thường gặp: SFT → (RM) → DPO hoặc PPO → GRPO. Xem mục G advanced_topics_vi.md.

## Câu 2 (Trắc nghiệm)

Reward Model (RM) trong RLHF học để làm gì?

- **A.** Sinh phản hồi cuối cùng cho người dùng
- **B.** Chấm điểm/so sánh mức ưu tiên giữa các output để hướng dẫn RL ✅
- **C.** Tokenize dữ liệu
- **D.** Lưu KV cache

**Đáp án: B**

**Giải thích:** RM học từ nhãn ưu tiên của con người, xuất ra điểm scalar; PPO dùng điểm này làm reward. FareedKhan implement RM from scratch.

## Câu 3 (Trắc nghiệm)

So với PPO/RLHF kinh điển, DPO bỏ được thành phần nào?

- **A.** Bỏ dữ liệu ưu tiên (preference)
- **B.** Bỏ việc train reward model riêng và vòng lặp PPO — tối ưu thẳng từ cặp ưu tiên ✅
- **C.** Bỏ model tham chiếu (reference)
- **D.** Bỏ tokenizer

**Đáp án: B**

**Giải thích:** DPO biến bài toán RLHF thành một loss phân loại trực tiếp trên cặp (chosen, rejected), vẫn dùng policy tham chiếu nhưng không cần RM/PPO.

## Câu 4 (Tự luận)

[Nâng cao] RLVR (Reinforcement Learning from Verifiable Rewards) là gì, vì sao hợp với reasoning?

**Trả lời mẫu:** RLVR dùng reward KIỂM CHỨNG ĐƯỢC một cách khách quan: đáp án toán đúng/sai, unit test code pass/fail, thay vì điểm chủ quan từ reward model. Vì tín hiệu thưởng chính xác và không bị 'hack', model có thể tự khám phá chuỗi suy luận (chain-of-thought) dẫn tới đáp án đúng. Đây là cơ chế đứng sau các reasoning model kiểu o1/R1; thường kết hợp với GRPO.

**Giải thích:** Xem nanochat chat_rl.py (tasks gsm8k, spellingbee) và paper DeepSeekMath/GRPO (arXiv 2402.03300).

## Câu 5 (Trắc nghiệm)

[Nâng cao] Bước 'midtrain' (nanochat) nằm ở đâu trong pipeline?

- **A.** Trước pretrain
- **B.** Giữa pretrain và SFT — dạy format hội thoại, special tokens, tool use ✅
- **C.** Sau GRPO
- **D.** Thay thế SFT

**Đáp án: B**

**Giải thích:** Midtrain là khái niệm KHÔNG có trong pipeline GPT-2 kinh điển; nó chuẩn bị base model cho giai đoạn chat/SFT.

## Câu 6 (Tự luận)

Trong RLHF/DPO, thành phần KL divergence (hoặc reference policy) đóng vai trò gì?

**Trả lời mẫu:** Nó giữ policy mới không trôi quá xa khỏi model tham chiếu (thường là bản SFT). Không có ràng buộc này, RL có thể 'hack' reward: sinh văn bản kỳ dị đạt điểm cao từ reward model nhưng mất khả năng ngôn ngữ chung (reward hacking / catastrophic drift). Trong PPO nó là phạt KL trong reward; trong DPO nó nằm ngay trong loss qua tỉ số log-prob với pi_ref và hệ số beta.

**Giải thích:** Đây là lý do mọi công thức DPO đều chứa pi_theta/pi_ref — không phải chi tiết trang trí.
