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

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `eval_rubric.md` | Template rubric + metrics (deliverable) |
| `retrospective.md` | Template retrospective nối về internals (deliverable) |

> 🎓 Đây là mục tiêu thật của cả roadmap. Nếu trễ tiến độ, ưu tiên bảo vệ Tuần 2–5 (core from-scratch) và Tuần 12–15 (mục tiêu agentic-SDLC).
