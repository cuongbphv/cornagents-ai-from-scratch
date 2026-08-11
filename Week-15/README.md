# Tuần 15 — Capstone + evaluation/observability

> Phase 3 — SDLC / CornAgents.AI (tuần cuối). Ship một workflow CornAgents.AI hoàn chỉnh, domain-relevant, và đánh giá nó.

## Mục tiêu

Ship **một** workflow CornAgents.AI end-to-end, polished, gắn domain, và đánh giá.

## Nguồn học

- **Langfuse/LangSmith** (tracing + eval agent).
- **promptfoo** hoặc LLM-as-judge (chất lượng output).
- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` — mục VII (Evaluation and Quality: metrics theo layer, complexity budget) + Table VI (Production Checklist).
- Hiểu biết Phase 1–2 để chọn model: Claude làm "brain"; model 7B fine-tuned cho sub-task hẹp (vd. một tác vụ phân loại nghiệp vụ hẹp).

## Nhiệm vụ (Task)

Chọn stage SDLC giá trị nhất cho bối cảnh của bạn — **khuyến nghị: spec-to-stories + automated review cho một feature Finance Banking** (chọn nghiệp vụ bạn thạo, giữ ở mức tổng quát). Kết hợp **RAG** (grounding trực tiếp) + **knowledge graph Tuần 14** (shared memory + fact-check multi-hop) + **agents** (workflow) + tùy chọn model fine-tuned. Instrument tracing; viết eval rubric; đo success rate, human-override rate, groundedness.

Khai báo **complexity budget** trước khi chạy: max model calls, max sub-agents, max tokens/chi phí, max retries — hết budget thì trả artifact tốt nhất hiện có + lý do dừng, không giấu partial failure sau một câu trả lời trôi chảy.

## Deliverable

- Capstone CornAgents.AI demo được.
- Báo cáo evaluation.
- Retrospective viết tay nối ngược về Phase 1 internals (bạn hiểu *vì sao* nó hoạt động).

## Thời lượng

~12–15 giờ.

## Phần cứng

Local cho sub-model fine-tuned; API cho agent brain.

## Thước đo "hệ thống đáng tin" (từ docs)

> *"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."*

Khi câu này đúng với capstone của bạn, loops/swarms/graphs là cơ chế engineering compose được; khi sai, thêm agent chỉ tăng độ mờ đục.

---

## Checklist tiến độ

- [ ] Chốt 1 use case Finance Banking (spec-to-stories + review)
- [ ] Ghép RAG (Tuần 10–11) + agents (Tuần 13) + knowledge graph (Tuần 14) thành 1 luồng
- [ ] (Tùy chọn) cắm model fine-tuned (Tuần 8/9) cho sub-task hẹp
- [ ] Khai báo complexity budget (calls, tokens, cost, retries) trước khi chạy
- [ ] Instrument tracing (Langfuse/LangSmith)
- [ ] Viết eval rubric → `eval_rubric.md`
- [ ] Đo: success rate, human-override rate, groundedness
- [ ] Kiểm tra câu "every important output can be traced..." với demo của bạn
- [ ] Demo end-to-end (script hoặc video ngắn)
- [ ] Viết `retrospective.md` (nối về Phase 1: vì sao nó hoạt động)

## 🚀 Bổ sung nâng cao (kỷ luật trước khi "ship")

Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **I5** (và ôn lại **H**, **I4**):

- **I5 · Complexity budget** — khai báo *trước* khi chạy: max calls, max sub-agents, max concurrent workers, max wall-clock, max tokens/chi phí, max retries, và bằng chứng tối thiểu để được finalize. Hết budget → trả artifact tốt nhất + issue chưa xử lý + **lý do dừng**; không giấu partial failure sau một câu trả lời trôi chảy.
- **I5 · Metric bị game** — ratchet chỉ cải thiện thứ nó *thấy được*: có thể giảm loss mà tăng chi phí inference hoặc overfit chính eval set. Giữ ràng buộc phụ.
- **H · Cạm bẫy LLM-as-judge** — áp trực tiếp vào `eval_rubric.md` của bạn.
- **I5 · Thước đo cuối**: *"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."* Tự kiểm câu này với capstone — đúng thì kiến trúc của bạn compose được; sai thì thêm agent chỉ tăng độ mờ đục.

> Nguồn gốc: [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) mục VII–IX + Table VI (Production Checklist).

## 📦 Dữ liệu cho tuần này

Xem [`../Week-00/datasets_finance_banking.md`](../Week-00/datasets_finance_banking.md) — mục **4** (bộ eval, chú ý license non-commercial), mục **9** (benchmark), mục **10** (dòng Tuần 15).

Metric bắt buộc có: **groundedness** — mọi câu trả lời có dẫn được về điều khoản/tài liệu nguồn hay không. Trong domain có quy định, đây là chỉ số quan trọng hơn cả success rate.

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `eval_rubric.md` | Template rubric + metrics (deliverable) |
| `retrospective.md` | Template retrospective nối về internals (deliverable) |

> 🎓 Đây là mục tiêu thật của cả roadmap. Nếu trễ tiến độ, ưu tiên bảo vệ Tuần 2–5 (core from-scratch) và Tuần 12–15 (mục tiêu agentic-SDLC).
