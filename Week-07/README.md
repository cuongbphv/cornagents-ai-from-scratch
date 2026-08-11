# Tuần 7 — Nhập môn alignment: SFT → Reward Model → DPO/PPO → GRPO

> Phase 1 — Deep Internals (tuần cuối phase). Hiểu pipeline alignment ở mức khái niệm và chạy ít nhất **một stage** from scratch. (Tách từ Tuần 6 cũ để lộ trình bớt dồn.)

## Mục tiêu

- Hiểu pipeline alignment: **SFT → reward model → PPO/DPO → GRPO** (khái niệm).
- Chạy **một alignment stage** từ đầu (khuyến nghị bắt đầu với **SFT hoặc DPO**).
- Phân biệt được SFT vs DPO vs GRPO và biết khi nào dùng cái nào.

## Nguồn học

- **FareedKhan-dev/train-llm-from-scratch** `src/post_training/` — SFT/RM/PPO/DPO/GRPO bằng PyTorch thuần trên dataset thật (Alpaca, Dolly, Anthropic HH-RLHF, UltraFeedback, GSM8K).
- Paper DPO (arXiv 2305.18290), InstructGPT/RLHF (arXiv 2203.02155), DeepSeekMath/GRPO (arXiv 2402.03300).
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm nguồn đã xác minh 2026-08-11).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md) — pipeline alignment, loss RM/DPO/GRPO với ví dụ số.
2. [`02_alignment_notes.md`](02_alignment_notes.md) — viết so sánh SFT vs DPO vs GRPO bằng lời mình (deliverable).
3. [`quiz.md`](quiz.md) — quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

1. Đọc FareedKhan `src/post_training/` — hiểu cấu trúc SFT/RM/DPO.
2. Chạy **một alignment stage** scaled-down (SFT hoặc DPO) trên dataset nhỏ.
3. Viết ghi chú phân biệt SFT vs DPO vs GRPO bằng lời mình.

## Deliverable

- Log/checkpoint của **một stage alignment** đã chạy.
- Ghi chú phân biệt **SFT vs DPO vs GRPO** → `02_alignment_notes.md`.

## Thời lượng

~10–12 giờ.

## Phần cứng

- 3070 Ti cho stage scaled-down (model nhỏ).
- Cloud nếu đẩy lên base lớn hơn hoặc full PPO/GRPO (box dev FareedKhan dùng 2×H100 DDP + bf16 — chạy scaled-down hoặc thuê).

> **Nếu thiếu thời gian (Phase 1):** nén Tuần 7 còn *hiểu khái niệm* + một lần chạy DPO; hoãn chiều sâu reasoning/GRPO sang sau roadmap.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` — tự tính lại được các ví dụ loss trong đó
- [ ] Vẽ lại pipeline alignment: Pretrain → (Midtrain) → SFT → RM → PPO/DPO → GRPO/RLVR
- [ ] Đọc FareedKhan `src/post_training/` — hiểu cấu trúc SFT/RM/DPO
- [ ] Hiểu loss của Reward Model (log-sigmoid của hiệu score)
- [ ] Hiểu vì sao DPO bỏ được RM riêng + dạng loss DPO
- [ ] Hiểu GRPO: group-relative advantage, vì sao hợp RLVR (toán/code)
- [ ] Chạy MỘT stage alignment (SFT hoặc DPO) scaled-down
- [ ] Viết `02_alignment_notes.md`: SFT vs DPO vs GRPO
- [ ] So phản hồi model trước/sau stage đã chạy → ghi ví dụ

## 🚀 Bổ sung nâng cao (pipeline alignment đầy đủ)

Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **G**:

- Pipeline đầy đủ: `Pretrain → Midtrain → SFT → Reward Model → PPO/DPO → GRPO/RLVR`.
- **Midtrain** (nanochat) — bước *không có* trong pipeline GPT-2 kinh điển: dạy format hội thoại, special tokens, tool use.
- **GRPO/RLVR** — bỏ critic, chuẩn hoá reward theo nhóm sample; **RLVR** = reward kiểm chứng được (toán đúng/sai, test pass) → nền reasoning model.
- **Tool-use RL** (nanochat) — model học gọi Python để tính/đếm, reward khi kết quả đúng.

> Nguồn: FareedKhan `src/post_training/` (SFT→RM→PPO→DPO→GRPO pure PyTorch); paper DPO/GRPO; nanochat `chat_sft.py`, `chat_rl.py`.

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| — | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: pipeline alignment, RM/DPO/GRPO |
| 2 | `02_alignment_notes.md` | Template so sánh SFT/DPO/GRPO (deliverable) |
| 3 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
