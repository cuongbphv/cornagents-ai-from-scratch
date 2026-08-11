# Tuần 2 — Backprop từ đầu + mô hình tư duy về Transformer

> Phase 1 — Deep Internals. Đây là một trong **những tuần giá trị nhất** (cùng Tuần 3–5). Mục tiêu: thực sự hiểu backpropagation bằng cách tự xây, và dựng mô hình tư duy (mental model) về transformer/attention **trước khi** code chúng ở Tuần 3.

## Mục tiêu

- Hiểu **backprop** ở mức bản chất: tự build một autograd engine nhỏ (micrograd).
- Nắm **mental model** của transformer & attention trước khi đụng code.
- Hiểu vì sao attention là **permutation-equivariant** và cần **positional info**.

## Nguồn học

- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm link nguồn đã xác minh 2026-08-11).
- Repo mở `karpathy/micrograd` — đọc code + README rồi **tự build lại** autograd + backprop.
- Repo mở `karpathy/makemore` — bigram → MLP (theo paper Bengio 2003, "A Neural Probabilistic Language Model").
- *The Annotated Transformer* (Harvard NLP, nlp.seas.harvard.edu) — mental model về transformer.
- Paper gốc — **"Attention Is All You Need"** (arXiv 1706.03762).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md) — đọc lý thuyết backprop + mental model transformer trước.
2. [`02_micrograd.py`](02_micrograd.py) — TỰ build autograd engine (deliverable chính).
3. [`03_check_grad.py`](03_check_grad.py) — đối chiếu gradient với PyTorch, khớp mới đạt.
4. [`04_makemore_notes.md`](04_makemore_notes.md) — làm bigram → MLP, ghi NLL đo được.
5. [`05_attention_writeup.md`](05_attention_writeup.md) — viết giải thích permutation-equivariance (deliverable 2).
6. [`quiz.md`](quiz.md) — làm quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Hai file này do `scripts/generate_quiz.py` sinh ra nên giữ nguyên tên, không đánh số.)*

## Nhiệm vụ (Task)

- Đọc code repo micrograd rồi **tự build lại** (giá trị scalar + autograd + backward).
- Bắt đầu **makemore**: bigram model → MLP.

## Deliverables

1. Repo **micrograd** của riêng bạn → `02_micrograd.py` (+ test gradient khớp với PyTorch).
2. Bài viết (Claude review) giải thích **vì sao attention permutation-equivariant và cần positional encoding** → `05_attention_writeup.md`.

## Thời lượng

~12–15 giờ.

## Phần cứng

3070 Ti / Mac — CPU hay GPU đều ổn (workload nhẹ).

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` — chạy lại được mọi snippet trong đó
- [ ] Đọc code repo `karpathy/micrograd` + tự code lại
- [ ] Tự viết `02_micrograd.py`: class `Value` với `+`, `*`, `tanh/relu`, `backward()`
- [ ] Kiểm tra gradient khớp PyTorch (chạy `03_check_grad.py`)
- [ ] Đọc repo `karpathy/makemore`: bigram → MLP
- [ ] Tự code bigram model (đếm + neural net 1 layer)
- [ ] Mở rộng makemore lên MLP (theo Bengio 2003)
- [ ] Đọc The Annotated Transformer (phần encoder/attention) để dựng mental model
- [ ] Viết `05_attention_writeup.md` bằng lời mình → nhờ Claude review
- [ ] Tự kiểm tra: vẽ được computation graph + giải thích backward bằng chain rule

## 🚀 Bổ sung nâng cao

**Tuần này cũng KHÔNG có mục nâng cao** (xem bảng neo trong [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md)). Tự tay viết micrograd và dựng mental model transformer đã đủ nặng — chia trí lúc này là phản tác dụng.

Ngay tuần sau (Tuần 3) bạn sẽ mở một loạt mục **A1–A6, C, E** để so sánh attention GPT-2 với Llama 3/Qwen3.

## File trong folder này

Số ở đầu tên file = thứ tự học (xem mục "Thứ tự học trong tuần" ở trên).

| # | File | Mô tả |
|---|------|-------|
| — | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: autograd engine, makemore, mental model transformer |
| 2 | `02_micrograd.py` | Skeleton để TỰ build autograd engine (có TODO) |
| 3 | `03_check_grad.py` | So sánh gradient micrograd của bạn với PyTorch |
| 4 | `04_makemore_notes.md` | Khung ghi chú + TODO cho bigram → MLP |
| 5 | `05_attention_writeup.md` | Template để viết giải thích permutation-equivariance |
| 6 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |

> Nhắc lại tiêu chí: nếu chưa giải thích được cho Claude bằng lời của mình → chưa học xong. Tuần này đặc biệt cần đi chậm và tự tay làm.
