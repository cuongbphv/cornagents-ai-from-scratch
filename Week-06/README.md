# Tuần 6 — Instruction fine-tuning (classification + instruction-following + LoRA)

> Phase 1 — Deep Internals. Fine-tune cho classification & instruction-following. (Alignment được tách riêng sang Tuần 7 để giảm tải.)

## Mục tiêu

- Fine-tune cho **classification** và **instruction-following**.
- Hiểu và áp dụng **LoRA** (paper arXiv 2106.09685 + HF PEFT docs) — so sánh với full fine-tuning.

## Nguồn học

- Paper LoRA (arXiv 2106.09685); paper InstructGPT (arXiv 2203.02155); HF PEFT docs (huggingface.co/docs/peft); `FareedKhan-dev/train-llm-from-scratch` phần SFT.
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm nguồn đã xác minh 2026-08-11).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md) — classification FT, instruction FT + masking, LoRA.
2. [`02_instruction_finetune.py`](02_instruction_finetune.py) — TỰ code format dataset + fine-tune loop (deliverable).
3. [`quiz.md`](quiz.md) — quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

1. Fine-tune classifier (`01_theory_notes.md` mục 2): dataset spam, sửa head phân loại, đo accuracy.
2. Instruction-fine-tune model của bạn (hoặc một pretrained nhỏ) theo `01_theory_notes.md` mục 3 với Alpaca-style template.
3. Áp dụng LoRA và so sánh full FT vs LoRA (tham số train được, VRAM, chất lượng).

## Deliverable

- Một **instruction-following mini-model** chat được.
- Ghi chú so sánh **full FT vs LoRA** (thêm vào cuối `02_instruction_finetune.py` hoặc file note riêng).

## Thời lượng

~10–12 giờ.

## Phần cứng

- 3070 Ti là đủ cho các bài fine-tune tuần này (model nhỏ, LoRA).

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` — chạy lại được mọi snippet trong đó
- [ ] Classification FT (`01_theory_notes.md` mục 2): chuẩn bị dataset spam + sửa head phân loại
- [ ] Fine-tune classifier, đo accuracy train/val/test
- [ ] Instruction FT (`01_theory_notes.md` mục 3): format instruction dataset (Alpaca-style prompt template)
- [ ] Instruction fine-tune + sinh phản hồi
- [ ] Áp dụng LoRA (`01_theory_notes.md` mục 4 + HF PEFT docs) — so sánh full FT vs LoRA
- [ ] Chat thử với mini-model → ghi vài ví dụ

## 🚀 Bổ sung nâng cao (định vị trong pipeline lớn)

Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **G — chỉ phần sơ đồ pipeline** (đừng đọc hết, phần còn lại là của Tuần 7):

```
Pretrain → Midtrain → SFT → Reward Model → PPO/DPO → GRPO/RLVR
                       ↑
              instruction fine-tuning bạn làm tuần này ≈ bước SFT
```

Mục đích: biết instruction FT của mình nằm ở **đâu** trong pipeline lớn, và **Midtrain** (khái niệm nanochat, không có trong pipeline GPT-2 kinh điển) chen vào trước SFT để dạy format hội thoại + special tokens + tool use.

> ➡️ Tuần 7 sẽ đọc mục **G** đầy đủ (RM, PPO, DPO, GRPO/RLVR).

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| — | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: classification/instruction FT, LoRA |
| 2 | `02_instruction_finetune.py` | Skeleton format dataset + fine-tune loop (TODO) |
| 3 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |

> ➡️ Tiếp theo: **Tuần 7** đi sâu pipeline alignment (SFT → RM → DPO/PPO → GRPO).
