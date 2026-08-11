# Tuần 13 — Map LLM vào các stage SDLC; build agent graph CornAgents.AI

> Phase 3 — SDLC / CornAgents.AI. Thiết kế các agent chuyên biệt cho requirements → design → code → review → test → docs, theo 5 workflow patterns của Anthropic, có human-in-the-loop gates.

## Mục tiêu

- Nắm **5 workflow patterns** của Anthropic: Prompt Chaining, Routing, Parallelization, Orchestrator–Workers, Evaluator–Optimizer — và chọn đúng pattern cho từng chỗ ("simple, composable patterns rather than complex frameworks").
- Thiết kế agent chuyên biệt cho từng stage SDLC, với cổng phê duyệt của con người.

## Nguồn học

- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` — mục IV (5 patterns + Dynamic Workflows), VI.D (Week 2: Go Multi-Agent), VIII (Decision Framework: 6 câu hỏi chọn kiến trúc).
- Tham chiếu agentic SDLC: CodeRabbit (agentic-SDLC guide), Sonar (AC/DC framework), GlobalLogic (VelocityAI case study) — lấy pattern & quality gates.
- Ví dụ code-review của Claude Agent SDK (đọc PR, flag bug/security, post comment).

## Nhiệm vụ (Task)

Implement 2–3 agent trong framework đã chọn:
- **Requirements Analyst agent** (thế mạnh BA của bạn): biến feature request Finance Banking → user story + acceptance criteria, grounded bởi RAG Tuần 10–11 trên tài liệu nghiệp vụ nội bộ.
- **Code Review agent** — mỗi lần review trả về **criterion-level defects**, không "looks good".
- **Test-Generation agent**.

Nối bằng pattern phù hợp (orchestrator–workers cho phân việc; evaluator–optimizer cho vòng chất lượng). Mỗi handoff giữa agent là một **artifact contract** (schema rõ, không phải prose). Thêm checkpoint phê duyệt của người + scope tool least-privilege.

## Deliverable

Workflow multi-agent: nhận một requirement → sinh **stories + design note + tests**, có human gate.

## Thời lượng

~12–15 giờ.

## Phần cứng

Bất kỳ; orchestration + API.

## Kiến thức lõi: chọn pattern nào? (Decision framework từ docs)

1. **Success có verify được không?** Không → đừng bắt đầu bằng autonomy; định nghĩa test/rubric trước.
2. **Các bước có ổn định không?** Có → chain. Không → planning / orchestrator.
3. **Subtask có độc lập không?** Có → parallelize. Không → khai báo dependency, giới hạn concurrent writes.
4. **Cần giữ các nhánh thay thế không?** Có → DAG thay vì ép mọi kết quả vào một nhánh.
5. **Facts phải sống qua run không?** Có → persist artifacts + graph state (Tuần 14), đừng dựa vào transcript.
6. **Chi phí/latency chịu được không?** Đặt budget trước khi thêm worker.

> Lưu ý từ docs: role split chỉ đáng khi chuyên môn hoá thêm tín hiệu; multi-agent hơn single agent ~90% ở task đa hướng nhưng tốn 10–15× token — cần reducer + budget rõ ràng.

---

## Checklist tiến độ

- [ ] Đọc mục IV + VIII của Karpathy-Loop PDF — nắm 5 patterns + 6 câu hỏi
- [ ] Map từng stage SDLC ↔ loại agent + pattern + input/output rõ ràng
- [ ] Agent 1 — Requirements Analyst: request → user stories + AC (dùng RAG)
- [ ] Agent 2 — Code Review: đọc diff/PR → criterion-level defects
- [ ] Agent 3 — Test-Gen: từ story/code → sinh test case
- [ ] Định nghĩa artifact contract (schema) cho từng handoff
- [ ] Nối thành graph (LangGraph state hoặc CrewAI crew)
- [ ] Thêm human approval gate giữa các stage
- [ ] Scope tool least-privilege cho từng agent
- [ ] Chạy thử 1 requirement Finance Banking end-to-end
- [ ] Ghi `agent_design.md`

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `agents.py` | Stub 3 agent + chỗ nối orchestration (TODO) |
| `agent_design.md` | Template thiết kế agent + I/O contract (deliverable) |

> ➡️ Tiếp theo: **Tuần 14** thêm lớp knowledge graph làm shared memory — workers ghi findings vào graph thay vì dồn qua context window của orchestrator.
