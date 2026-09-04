# Tuần 15: Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Phase 3: SDLC / CornAgents.AI. Hiểu agent loop, tools, subagents, MCP; nắm mô hình 5 tầng engineering; build loop đầu tiên kiểu Karpathy; chọn lớp orchestration.

## Mục tiêu

- Nắm **mô hình 5 tầng** gồm Prompt, Context, Harness, Loop rồi Graph engineering (xem `docs/5-layers-multi-agent.jpg`): mỗi tầng bọc tầng trước; model là commodity, hệ thống quanh nó mới là engineering.
- Hiểu **agent loop**, tools, subagents, **MCP**.
- Build **loop có đo lường đầu tiên** (kiểu ratchet loop của Karpathy autoresearch): generate, rồi evaluate, rồi revise, kết thúc bằng stopping rule.
- Chọn **orchestration layer** cho CornAgents.AI.

## Nguồn học

- **Claude Agent SDK** docs (code.claude.com/docs/en/agent-sdk) + "Building agents with the Claude Agent SDK".
- **Model Context Protocol** docs (200+ servers: GitHub, Postgres, Slack, Jira).
- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`: mục II (Karpathy's Loop: autoresearch) và VI.A-B (Day 1: build loop, Day 2: add tools).
- `docs/5-layers-multi-agent.jpg`: bản đồ 5 tầng engineering.
- **LangGraph** + **CrewAI** docs (bạn đang cân nhắc cả hai); AutoGen là lựa chọn thay thế.
- Lý thuyết tự chứa của tuần: [`01_theory_notes.md`](01_theory_notes.md) (kèm nguồn đã xác minh 2026-08-11).

## Thứ tự học trong tuần (mở file theo số)

1. [`01_theory_notes.md`](01_theory_notes.md): agent loop, MCP, 5 tầng + bảng chẩn đoán, reflective loop.
2. [`02_minimal_agent.py`](02_minimal_agent.py): skeleton agent loop (TODO 1-7): tự điền tool schema, dispatch, vòng lặp; sau đó nối 1 MCP server (deliverable).
3. [`03_cornagents_architecture.md`](03_cornagents_architecture.md): sơ đồ kiến trúc + quyết định stack (deliverable).
4. [`quiz.md`](quiz.md): quiz cuối tuần, đối chiếu [`quiz_solution.md`](quiz_solution.md). *(Giữ nguyên tên vì do `scripts/generate_quiz.py` sinh ra.)*

## Nhiệm vụ (Task)

1. Build một agent tối thiểu bằng Claude Agent SDK: đọc repo, chạy một tool, trả output có cấu trúc; kết nối **một MCP server** (vd. GitHub hoặc filesystem).
2. Build **reflective loop** (Day 1 của build path): lấy một LLM call có output đánh giá được, rồi thêm evaluator với tiêu chí tường minh, bước revise, stopping rule (max rounds + budget), lưu mọi artifact. Vì sao loop của Karpathy chạy được: *output verifiable, action reversible, horizon ngắn, environment bounded*.
3. Quyết định stack CornAgents.AI.

## Deliverable

- Một single agent + kết nối MCP hoạt động.
- Một reflective loop chạy được (generate, rồi evaluate, rồi revise, có stopping rule).
- Sơ đồ kiến trúc CornAgents.AI 1 trang, ghi vào `03_cornagents_architecture.md`.

## Thời lượng

~12 giờ.

## Phần cứng

Bất kỳ; đây là việc API/orchestration. Dùng subscription Claude.

> Về metering, từ 15/06/2026, headless Agent SDK trên Pro/Max rút từ pool token tuần riêng, nên automation nặng có thể cần API credits.

## CornAgents.AI là gì (định vị)

"CornAgents.AI" là **khái niệm riêng của bạn**, không phải một sản phẩm có sẵn phải mua. Hãy coi CornAgents.AI là framework agentic-SDLC cá nhân, build trên **Claude Agent SDK + MCP + LangGraph/CrewAI**, gắn với domain Finance Banking / BA của bạn.

## Kiến thức lõi: 5 tầng engineering

| Tầng | Là gì | Unit of work |
|---|---|---|
| 1. Prompt engineering | The message, role, instructions, examples, format | một input |
| 2. Context engineering | The memory, curate cái gì ở trong window | cái ở trong window |
| 3. Harness engineering | The machine, gather → act (tools/subagents) → verify | một pass của máy |
| 4. Loop engineering | The system, run → check (budget, max iters, no-progress) → decide | một run |
| 5. Graph engineering | The organization, nhiều agent + shared memory (Tuần 17) | cả tổ chức agent |

---

## Checklist tiến độ

- [ ] Đọc `01_theory_notes.md` và vẽ lại được bảng chẩn đoán theo tầng.
- [ ] Xem `docs/5-layers-multi-agent.jpg` và tự vẽ lại 5 tầng bằng lời mình.
- [ ] Đọc Claude Agent SDK docs, hiểu agent loop và tool use.
- [ ] Đọc MCP docs, hiểu server/client và transport.
- [ ] Build single agent: đọc repo, chạy 1 tool, trả output có cấu trúc.
- [ ] Kết nối 1 MCP server (filesystem hoặc GitHub).
- [ ] Build reflective loop: generate, rồi evaluate theo tiêu chí tường minh, rồi revise, có stop rule.
- [ ] Hiểu 4 điều kiện làm loop của Karpathy chạy được (verifiable/reversible/short/bounded).
- [ ] So sánh LangGraph với CrewAI cho nhu cầu của bạn.
- [ ] Chọn stack kèm lý do (regulated finance thì ưu tiên LangGraph vì stateful, auditable).
- [ ] Vẽ `03_cornagents_architecture.md` (sơ đồ, tool boundaries, HITL gates).

## Bổ sung nâng cao (5 tầng + ratchet loop)

Tuần này phần "nâng cao" **chính là nội dung tuần**, nên đọc [`../Week-00/advanced_topics_vi.md`](../Week-00/advanced_topics_vi.md) mục **I1-I2** song song:

- Mục I1 trình bày năm tầng engineering, Prompt, Context, Harness, Loop rồi Graph, kèm cách **chẩn đoán theo tầng**: output sai format là lỗi tầng 1; model không biết thứ cần biết là tầng 2; không ai kiểm kết quả là tầng 3; chạy mãi không dừng là tầng 4; agent lặp việc nhau là tầng 5.
- Mục I2 bàn ratchet loop và `program.md`: 4 điều kiện làm loop chạy được (verifiable / reversible / horizon ngắn / environment bounded) và ý tưởng "programming the program" bằng ngôn ngữ tự nhiên.
- Cũng ở I2, commit DAG ≠ knowledge graph: đừng gộp hai thứ này (work lineage vs domain knowledge).

> Nguồn gốc: [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) mục II & VI, [`../docs/5-layers-multi-agent.jpg`](../docs/5-layers-multi-agent.jpg).

## File trong folder

Số ở đầu tên file = thứ tự học.

| # | File | Mô tả |
|---|------|-------|
| · | `README.md` | File này |
| 1 | `01_theory_notes.md` | Lý thuyết tự chứa: agent loop, MCP, 5 tầng, reflective loop |
| 2 | `02_minimal_agent.py` | Skeleton agent loop: tool schema, dispatch, stop condition, budget (TODO) |
| 3 | `03_cornagents_architecture.md` | Template sơ đồ kiến trúc CornAgents.AI (deliverable) |
| 4 | `quiz.md` / `quiz_solution.md` | Quiz cuối tuần (sinh từ `scripts/quiz_bank.json`, không đánh số) |
