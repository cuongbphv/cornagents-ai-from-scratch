# Tuần 12 — Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Phase 3 — SDLC / CornAgents.AI. Hiểu agent loop, tools, subagents, MCP; nắm mô hình 5 tầng engineering; build loop đầu tiên kiểu Karpathy; chọn lớp orchestration.

## Mục tiêu

- Nắm **mô hình 5 tầng**: Prompt → Context → Harness → Loop → Graph engineering (xem `docs/5-layers-multi-agent.jpg`) — mỗi tầng bọc tầng trước; model là commodity, hệ thống quanh nó mới là engineering.
- Hiểu **agent loop**, tools, subagents, **MCP**.
- Build **loop có đo lường đầu tiên** (kiểu ratchet loop của Karpathy autoresearch): generate → evaluate → revise → stopping rule.
- Chọn **orchestration layer** cho CornAgents.AI.

## Nguồn học

- **Claude Agent SDK** docs (code.claude.com/docs/en/agent-sdk) + "Building agents with the Claude Agent SDK".
- **Model Context Protocol** docs (200+ servers: GitHub, Postgres, Slack, Jira).
- `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` — mục II (Karpathy's Loop: autoresearch) và VI.A–B (Day 1: build loop, Day 2: add tools).
- `docs/5-layers-multi-agent.jpg` — bản đồ 5 tầng engineering.
- **LangGraph** + **CrewAI** docs (bạn đang cân nhắc cả hai); AutoGen là lựa chọn thay thế.

## Nhiệm vụ (Task)

1. Build một agent tối thiểu bằng Claude Agent SDK: đọc repo, chạy một tool, trả output có cấu trúc; kết nối **một MCP server** (vd. GitHub hoặc filesystem).
2. Build **reflective loop** (Day 1 của build path): lấy một LLM call có output đánh giá được → thêm evaluator với tiêu chí tường minh, bước revise, stopping rule (max rounds + budget), lưu mọi artifact. Vì sao loop của Karpathy chạy được: *output verifiable, action reversible, horizon ngắn, environment bounded*.
3. Quyết định stack CornAgents.AI.

## Deliverable

- Một single agent + kết nối MCP hoạt động.
- Một reflective loop chạy được (generate → evaluate → revise, có stopping rule).
- Sơ đồ kiến trúc CornAgents.AI 1 trang → `cornagents_architecture.md`.

## Thời lượng

~12 giờ.

## Phần cứng

Bất kỳ; đây là việc API/orchestration. Dùng subscription Claude.

> **Lưu ý metering:** từ 15/06/2026, headless Agent SDK trên Pro/Max rút từ pool token tuần riêng — automation nặng có thể cần API credits.

## CornAgents.AI là gì (định vị)

"CornAgents.AI" là **khái niệm riêng của bạn**, không phải một sản phẩm có sẵn phải mua. Hãy coi CornAgents.AI là framework agentic-SDLC cá nhân, build trên **Claude Agent SDK + MCP + LangGraph/CrewAI**, gắn với domain Finance Banking / BA của bạn.

## Kiến thức lõi: 5 tầng engineering

| Tầng | Là gì | Unit of work |
|---|---|---|
| 1. Prompt engineering | The message — role, instructions, examples, format | một input |
| 2. Context engineering | The memory — curate cái gì ở trong window | cái ở trong window |
| 3. Harness engineering | The machine — gather → act (tools/subagents) → verify | một pass của máy |
| 4. Loop engineering | The system — run → check (budget, max iters, no-progress) → decide | một run |
| 5. Graph engineering | The organization — nhiều agent + shared memory (Tuần 14) | cả tổ chức agent |

---

## Checklist tiến độ

- [ ] Xem `docs/5-layers-multi-agent.jpg` — tự vẽ lại 5 tầng bằng lời mình
- [ ] Đọc Claude Agent SDK docs — hiểu agent loop + tool use
- [ ] Đọc MCP docs — hiểu server/client, transport
- [ ] Build single agent: đọc repo → chạy 1 tool → output có cấu trúc
- [ ] Kết nối 1 MCP server (filesystem hoặc GitHub)
- [ ] Build reflective loop: gen → eval (tiêu chí tường minh) → revise → stop rule
- [ ] Hiểu 4 điều kiện làm loop của Karpathy chạy được (verifiable/reversible/short/bounded)
- [ ] So sánh LangGraph vs CrewAI cho nhu cầu của bạn
- [ ] Chọn stack + lý do (regulated finance → ưu tiên LangGraph: stateful, auditable)
- [ ] Vẽ `cornagents_architecture.md` (sơ đồ + tool boundaries + HITL gates)

## File trong folder

| File | Mô tả |
|------|-------|
| `README.md` | File này |
| `minimal_agent.py` | Starter single agent + MCP (pseudocode/cấu trúc) |
| `cornagents_architecture.md` | Template sơ đồ kiến trúc CornAgents.AI (deliverable) |
