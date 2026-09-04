# Tuần 18: Capstone + evaluation/observability

> Phase 3: SDLC / CornAgents.AI (tuần cuối). Ship một workflow CornAgents.AI hoàn chỉnh, domain-relevant, và đánh giá nó.

## Mục tiêu

Ship **một** workflow CornAgents.AI end-to-end, polished, gắn domain, và đánh giá.

## Nguồn học

- **Langfuse/LangSmith** (tracing + eval agent).
- **promptfoo** hoặc LLM-as-judge (chất lượng output).
- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`: mục VII (Evaluation and Quality: metrics theo layer, complexity budget) + Table VI (Production Checklist).
- Hiểu biết Phase 1-2 để chọn model: Claude làm "brain"; model 7B fine-tuned cho sub-task hẹp (vd. một tác vụ phân loại nghiệp vụ hẹp).
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): bản đồ lắp ghép, complexity budget, 3 metric, rubric.
2. [`02_eval_rubric.md`](02_eval_rubric.md): viết rubric TRƯỚC khi chạy demo (deliverable).
3. [`03_retrospective.md`](03_retrospective.md): retrospective nối về Phase 1 (deliverable).
4. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

Chọn stage SDLC giá trị nhất cho bối cảnh của bạn, **khuyến nghị: spec-to-stories + automated review cho một feature Finance Banking** (chọn nghiệp vụ bạn thạo, giữ ở mức tổng quát). Kết hợp **RAG** (grounding trực tiếp) + **knowledge graph Tuần 17** (shared memory + fact-check multi-hop) + **agents** (workflow) + tùy chọn model fine-tuned. Instrument tracing; viết eval rubric; đo success rate, human-override rate, groundedness.

Khai báo **complexity budget** trước khi chạy: max model calls, max sub-agents, max tokens/chi phí, max retries, hết budget thì trả artifact tốt nhất hiện có + lý do dừng, không giấu partial failure sau một câu trả lời trôi chảy.

## Deliverable

- Capstone CornAgents.AI demo được.
- Báo cáo evaluation.
- Retrospective viết tay nối ngược về Phase 1 internals (bạn hiểu *vì sao* nó hoạt động).

## Thời lượng

~12-15 giờ.

## Phần cứng

Local cho sub-model fine-tuned; API cho agent brain.

## Thước đo "hệ thống đáng tin" (từ docs)

> *"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."*

Khi câu này đúng với capstone của bạn, loops/swarms/graphs là cơ chế engineering compose được; khi sai, thêm agent chỉ tăng độ mờ đục.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` và khai báo complexity budget bằng số trước khi chạy.
- [ ] Chốt 1 use case Finance Banking (spec-to-stories + review).
- [ ] Ghép RAG (Tuần 13-14), agents (Tuần 16) và knowledge graph (Tuần 17) thành 1 luồng.
- [ ] (Tùy chọn) cắm model fine-tuned (Tuần 11/12) cho sub-task hẹp.
- [ ] Khai báo complexity budget (calls, tokens, cost, retries) trước khi chạy.
- [ ] Instrument tracing (Langfuse/LangSmith).
- [ ] Viết eval rubric vào `02_eval_rubric.md`.
- [ ] Đo success rate, human-override rate và groundedness.
- [ ] Kiểm tra câu "every important output can be traced..." với demo của bạn.
- [ ] Demo end-to-end (script hoặc video ngắn).
- [ ] Viết `03_retrospective.md` (nối về Phase 1: vì sao nó hoạt động).

## Bổ sung nâng cao (kỷ luật trước khi "ship")

Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **I5** (và ôn lại **H**, **I4**):

- Mục I5 yêu cầu khai báo complexity budget *trước* khi chạy: max calls, max sub-agents, max concurrent workers, max wall-clock, max tokens/chi phí, max retries, và bằng chứng tối thiểu để được finalize. Hết budget thì trả artifact tốt nhất kèm issue chưa xử lý và **lý do dừng**; không giấu partial failure sau một câu trả lời trôi chảy.
- Cũng ở I5 là cảnh báo metric bị game: ratchet chỉ cải thiện thứ nó *thấy được*, có thể giảm loss mà tăng chi phí inference hoặc overfit chính eval set. Giữ ràng buộc phụ.
- Mục H về cạm bẫy LLM-as-judge áp trực tiếp vào `02_eval_rubric.md` của bạn.
- Thước đo cuối của I5 là câu *"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."* Tự kiểm câu này với capstone, đúng thì kiến trúc của bạn compose được; sai thì thêm agent chỉ tăng độ mờ đục.

> Nguồn gốc: [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) mục VII-IX + Table VI (Production Checklist).

## Dữ liệu cho tuần này

Xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md): mục **4** (bộ eval, chú ý license non-commercial), mục **9** (benchmark), mục **10** (dòng Tuần 18).

Metric bắt buộc phải có là **groundedness**, tức mọi câu trả lời có dẫn được về điều khoản/tài liệu nguồn hay không. Trong domain có quy định, đây là chỉ số quan trọng hơn cả success rate.

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: lắp ghép, budget, metric, rubric |
| 2 | `02_eval_rubric.md` | Template rubric + metrics (deliverable) |
| 3 | `03_retrospective.md` | Template retrospective nối về internals (deliverable) |
| 4 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |

> Đây là mục tiêu thật của cả roadmap. Nếu trễ tiến độ, ưu tiên bảo vệ Tuần 5-8 (core from-scratch) và Tuần 15-18 (mục tiêu agentic-SDLC).
