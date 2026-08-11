# Tuần 12 — Quiz: Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Tự kiểm tra **trước** khi xem solution. Tổng **7** câu. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json` — đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Mô tả 'agent loop' cơ bản.

## Câu 2 (Trắc nghiệm)

MCP (Model Context Protocol) là gì?

- **A.** Một model ngôn ngữ
- **B.** Một chuẩn mở để kết nối model với tool/nguồn dữ liệu qua server/client (GitHub, Postgres, Slack, filesystem...)
- **C.** Một thuật toán RL
- **D.** Một định dạng file

## Câu 3 (Trắc nghiệm)

Khác biệt chính giữa LangGraph và CrewAI?

- **A.** LangGraph chỉ cho vision, CrewAI cho text
- **B.** LangGraph: graph có trạng thái, tường minh, auditable; CrewAI: crew theo vai (role) prototype nhanh
- **C.** Cả hai giống hệt nhau
- **D.** CrewAI không hỗ trợ tool

## Câu 4 (Tự luận)

Vì sao workflow tài chính có quy định nên ưu tiên LangGraph?

## Câu 5 (Trắc nghiệm)

Human-in-the-loop (HITL) gate nghĩa là gì?

- **A.** Agent chạy hoàn toàn tự động không cần người
- **B.** Điểm dừng yêu cầu con người phê duyệt/sửa trước khi agent đi tiếp
- **C.** Một loại tool
- **D.** Cách tính token

## Câu 6 (Trắc nghiệm)

Mô hình 5 tầng engineering (docs/5-layers-multi-agent.jpg) xếp theo thứ tự nào, từ trong ra ngoài?

- **A.** Prompt → Harness → Context → Graph → Loop
- **B.** Prompt → Context → Harness → Loop → Graph
- **C.** Context → Prompt → Loop → Harness → Graph
- **D.** Loop → Prompt → Context → Graph → Harness

## Câu 7 (Tự luận)

Bốn điều kiện nào làm loop autoresearch của Karpathy chạy được, và vì sao thiếu một cái là loop hỏng?

---
> 💡 Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
