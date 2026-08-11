# Thiết kế Agent SDLC — (deliverable Tuần 13)

> Điền các chỗ ______. Map từng stage SDLC sang agent với I/O contract rõ ràng.

## 1. Map SDLC → Agent

| Stage SDLC | Agent | Input | Output | Tool được phép |
|-----------|-------|-------|--------|----------------|
| Requirements | Requirements Analyst | feature request + RAG domain | user stories + AC | RAG retrieve (read-only) |
| Design | (tùy chọn) | stories | design note | ______ |
| Code review | Code Review | diff/PR | issues + approve | git read, ______ |
| Test | Test-Gen | stories/code | test suite | ______ |
| Docs | (tùy chọn) | code/stories | docs | ______ |

## 2. Human-in-the-loop gates

- Gate sau Requirements: ai duyệt? tiêu chí pass? ______
- Gate sau Tests / trước merge: ______

## 3. I/O contract (ví dụ JSON)

```json
{
  "requirement": {"feature_request": "...", "domain_context": "..."},
  "stories": {"user_stories": ["..."], "acceptance_criteria": ["..."]},
  "review": {"issues": [{"severity": "high", "note": "..."}], "approved": false},
  "tests": {"tests": ["def test_...():"]}
}
```

## 4. Least-privilege & an toàn

- Mỗi agent chỉ giữ tool tối thiểu (bảng ở mục 1).
- Không agent nào tự merge/commit khi chưa qua human gate.
- Log mọi tool call để audit.

## 5. Thử nghiệm end-to-end

- Requirement dùng để test: ______
- Kết quả mỗi stage: ______
- Chỗ agent làm tốt / cần cải thiện: ______
