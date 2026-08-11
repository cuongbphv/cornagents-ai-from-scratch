# CornAgents.AI — Kiến trúc (deliverable Tuần 12)

> Sơ đồ + quyết định stack. Điền các chỗ ______. Đây là framework agentic-SDLC riêng của bạn.

## 1. Stack đã chọn

| Lớp | Lựa chọn | Lý do |
|-----|----------|-------|
| Harness/agent brain | Claude Agent SDK | ______ |
| Tool/data access | MCP (GitHub, Postgres, filesystem...) | ______ |
| Orchestration | LangGraph **hoặc** CrewAI → chọn: ______ | ______ |

> Gợi ý: regulated finance → **LangGraph** (stateful, auditable, kiểm soát rõ ràng). CrewAI nếu ưu tiên prototype nhanh theo vai trò.

## 2. Sơ đồ kiến trúc (vẽ/ASCII)

```
            ┌──────────────────────────────┐
  Người ───►│  Orchestrator (LangGraph)    │
            │  - state, routing, HITL gate │
            └──────┬───────────────┬───────┘
                   │               │
          ┌────────▼─────┐   ┌─────▼────────┐
          │ Agent A      │   │ Agent B      │   ...
          │ (vai trò)    │   │ (vai trò)    │
          └──────┬───────┘   └─────┬────────┘
                 │  MCP tools       │
        ┌────────▼──────────────────▼────────┐
        │  MCP servers: GitHub / FS / Postgres │
        │  + RAG (Tuần 10–11) cho domain        │
        └──────────────────────────────────────┘
```

## 3. Nguyên tắc thiết kế (day one)

- [ ] **Human-in-the-loop gates** ở các bước rủi ro (commit, merge, gửi ra ngoài).
- [ ] **Tool least-privilege**: mỗi agent chỉ có tool tối thiểu cần thiết.
- [ ] **Auditable state**: log mọi quyết định + tool call.
- [ ] **Domain grounding**: nối RAG Finance Banking làm nguồn sự thật.

## 4. Tool boundaries (điền)

| Agent | Tools được phép | KHÔNG được phép |
|-------|-----------------|-----------------|
| ______ | ______ | ______ |

## 5. Failure modes cần lường trước

- ______
- ______
