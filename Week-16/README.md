# Tuần 16: Map LLM vào các stage SDLC; build agent graph CornAgents.AI

> Phase 3: SDLC / CornAgents.AI. Thiết kế các agent chuyên biệt cho chuỗi requirements, design, code, review, test rồi docs, theo 5 workflow patterns của Anthropic, có human-in-the-loop gates.

## Mục tiêu

- Nắm **5 workflow patterns** của Anthropic: Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer, và chọn đúng pattern cho từng chỗ ("simple, composable patterns rather than complex frameworks").
- Thiết kế agent chuyên biệt cho từng stage SDLC, với cổng phê duyệt của con người.

## Nguồn học

- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`: mục IV (5 patterns + Dynamic Workflows), VI.D (Week 5: Go Multi-Agent), VIII (Decision Framework: 6 câu hỏi chọn kiến trúc).
- Tham chiếu agentic SDLC: CodeRabbit (agentic-SDLC guide), Sonar (AC/DC framework), GlobalLogic (VelocityAI case study): lấy pattern & quality gates.
- Ví dụ code-review của Claude Agent SDK (đọc PR, flag bug/security, post comment).
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): 5 patterns, chi phí multi-agent, artifact contract, gates.
2. [`02_agents.py`](02_agents.py): code 3 agent + nối orchestration (deliverable).
3. [`03_agent_design.md`](03_agent_design.md): thiết kế agent + I/O contract (deliverable).
4. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

Implement 2-3 agent trong framework đã chọn:
- Requirements Analyst agent (thế mạnh BA của bạn) biến feature request Finance Banking thành user story và acceptance criteria, grounded bởi RAG Tuần 13-14 trên tài liệu nghiệp vụ nội bộ.
- Code Review agent mỗi lần review trả về **criterion-level defects**, không "looks good".
- Test-Generation agent sinh test case từ story và code.

Nối bằng pattern phù hợp (orchestrator-workers cho phân việc; evaluator-optimizer cho vòng chất lượng). Mỗi handoff giữa agent là một **artifact contract** (schema rõ, không phải prose). Thêm checkpoint phê duyệt của người + scope tool least-privilege.

## Deliverable

Workflow multi-agent nhận một requirement rồi sinh **stories + design note + tests**, có human gate.

## Thời lượng

~12-15 giờ.

## Phần cứng

Bất kỳ; orchestration + API.

## Kiến thức lõi: chọn pattern nào? (Decision framework từ docs)

1. Success có verify được không? Nếu không, đừng bắt đầu bằng autonomy; định nghĩa test/rubric trước.
2. Các bước có ổn định không? Nếu có thì dùng chain; nếu không thì dùng planning hoặc orchestrator.
3. Subtask có độc lập không? Nếu có thì parallelize; nếu không thì khai báo dependency và giới hạn concurrent writes.
4. Cần giữ các nhánh thay thế không? Nếu có thì dùng DAG thay vì ép mọi kết quả vào một nhánh.
5. Facts phải sống qua run không? Nếu có thì persist artifacts và graph state (Tuần 17), đừng dựa vào transcript.
6. Chi phí/latency chịu được không? Đặt budget trước khi thêm worker.

> Lưu ý từ docs: role split chỉ đáng khi chuyên môn hoá thêm tín hiệu; multi-agent hơn single agent ~90% ở task đa hướng nhưng tốn 10-15× token, cần reducer + budget rõ ràng.

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` và viết artifact contract trước khi viết agent.
- [ ] Đọc mục IV và VIII của Karpathy-Loop PDF, nắm 5 patterns và 6 câu hỏi.
- [ ] Map từng stage SDLC sang loại agent, pattern và input/output rõ ràng.
- [ ] Agent 1, Requirements Analyst, biến request thành user stories và AC (dùng RAG).
- [ ] Agent 2, Code Review, đọc diff/PR và trả về criterion-level defects.
- [ ] Agent 3, Test-Gen, sinh test case từ story/code.
- [ ] Định nghĩa artifact contract (schema) cho từng handoff.
- [ ] Nối thành graph (LangGraph state hoặc CrewAI crew).
- [ ] Thêm human approval gate giữa các stage.
- [ ] Scope tool least-privilege cho từng agent.
- [ ] Chạy thử 1 requirement Finance Banking end-to-end.
- [ ] Ghi `03_agent_design.md`.

## Bổ sung nâng cao (chọn pattern & chi phí thật)

Đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **I2-I3**:

- Mục I3 trình bày năm workflow patterns chi tiết cùng con số cần nhớ trước khi tách vai: multi-agent thắng single agent ~**90%** ở task đa hướng nhưng tốn **10-15× token**, nên chỉ tách vai khi chuyên môn hoá *thêm tín hiệu*, và luôn định nghĩa **reducer** trước khi fan-out.
- Cũng ở I3 là câu hỏi khi nào ĐỪNG fan-out: task cần một mạch tư duy liền (thiết kế kiến trúc, viết narrative, refactor gắn kết chặt) sẽ *tệ hơn* khi chia nhỏ; fan-out song song còn tạo **lỗi tương quan**, và verification chỉ cứu được nếu reviewer có prompt/bằng chứng/vai khác.
- Mục I2 nói mỗi kiến trúc externalize một bottleneck: loop externalize iteration, chain externalize thứ tự, swarm externalize parallel search, DAG externalize lineage, graph externalize shared facts. Bạn đang ở bước swarm/chain; tuần sau mới lên graph.

> Nguồn gốc: [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) mục IV & VIII.

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: 5 patterns, contract, gates |
| 2 | `02_agents.py` | Stub 3 agent + chỗ nối orchestration (TODO) |
| 3 | `03_agent_design.md` | Template thiết kế agent + I/O contract (deliverable) |
| 4 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |

> Tiếp theo: **Tuần 17** thêm lớp knowledge graph làm shared memory, workers ghi findings vào graph thay vì dồn qua context window của orchestrator.
