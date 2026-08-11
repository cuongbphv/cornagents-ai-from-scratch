# Tuần 6 — Instruction fine-tuning (Raschka ch.6–7 + LoRA)

> Phase 1 — Deep Internals. Fine-tune cho classification & instruction-following. (Alignment được tách riêng sang Tuần 7 để giảm tải.)

## Mục tiêu

- Fine-tune cho **classification** (ch.6) và **instruction-following** (ch.7).
- Hiểu và áp dụng **LoRA** (Appendix E) — so sánh với full fine-tuning.

## Nguồn học

- Raschka — **ch.6–7** + **Appendix E** (LoRA).

## Nhiệm vụ (Task)

1. Fine-tune classifier (ch.6): dataset spam, sửa head phân loại, đo accuracy.
2. Instruction-fine-tune model của bạn (hoặc một pretrained nhỏ) theo ch.7 với Alpaca-style template.
3. Áp dụng LoRA và so sánh full FT vs LoRA (tham số train được, VRAM, chất lượng).

## Deliverable

- Một **instruction-following mini-model** chat được.
- Ghi chú so sánh **full FT vs LoRA** (thêm vào cuối `instruction_finetune.py` hoặc file note riêng).

## Thời lượng

~10–12 giờ.

## Phần cứng

- 3070 Ti là đủ cho ch.6–7 (model nhỏ, LoRA).

---

## Checklist tiến độ

- [ ] ch.6: chuẩn bị dataset classification (spam) + sửa head phân loại
- [ ] ch.6: fine-tune classifier, đo accuracy train/val/test
- [ ] ch.7: format instruction dataset (Alpaca-style prompt template)
- [ ] ch.7: instruction fine-tune + sinh phản hồi
- [ ] Áp dụng LoRA (Appendix E) — so sánh full FT vs LoRA
- [ ] Chat thử với mini-model → ghi vài ví dụ

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `instruction_finetune.py` | Skeleton format dataset + fine-tune loop (TODO) |

> ➡️ Tiếp theo: **Tuần 7** đi sâu pipeline alignment (SFT → RM → DPO/PPO → GRPO).
