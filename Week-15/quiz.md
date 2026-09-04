# Tuần 15, Quiz: Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Tự kiểm tra **trước** khi xem solution. Tổng **9** câu, trong đó **2** câu nâng cao. Đáp án + giải thích ở [`quiz_solution.md`](quiz_solution.md).
> _Sinh tự động từ `scripts/quiz_bank.json`: đừng sửa tay; chạy lại `python scripts/generate_quiz.py`._

## Câu 1 (Tự luận)

Mô tả 'agent loop' cơ bản.

## Câu 2 (Trắc nghiệm)

MCP (Model Context Protocol) là gì?

- **A.** Một định dạng file
- **B.** Một chuẩn mở để kết nối model với tool/nguồn dữ liệu qua server/client (GitHub, Postgres, Slack, filesystem...)
- **C.** Một thuật toán RL
- **D.** Một model ngôn ngữ

## Câu 3 (Trắc nghiệm)

Khác biệt chính giữa LangGraph và CrewAI?

- **A.** LangGraph: graph có trạng thái, tường minh, auditable; CrewAI: crew theo vai (role) prototype nhanh
- **B.** LangGraph chỉ cho vision, CrewAI cho text
- **C.** CrewAI không hỗ trợ tool
- **D.** Cả hai giống hệt nhau

## Câu 4 (Tự luận)

Vì sao workflow tài chính có quy định nên ưu tiên LangGraph?

## Câu 5 (Trắc nghiệm)

Human-in-the-loop (HITL) gate nghĩa là gì?

- **A.** Cách tính token
- **B.** Agent chạy hoàn toàn tự động không cần người
- **C.** Một loại tool
- **D.** Điểm dừng yêu cầu con người phê duyệt/sửa trước khi agent đi tiếp

## Câu 6 (Trắc nghiệm)

Mô hình 5 tầng engineering (docs/5-layers-multi-agent.jpg) xếp theo thứ tự nào, từ trong ra ngoài?

- **A.** Prompt → Context → Harness → Loop → Graph
- **B.** Loop → Prompt → Context → Graph → Harness
- **C.** Prompt → Harness → Context → Graph → Loop
- **D.** Context → Prompt → Loop → Harness → Graph

## Câu 7 (Tự luận)

Bốn điều kiện nào làm loop autoresearch của Karpathy chạy được, và vì sao thiếu một cái là loop hỏng?

---

## Phần nâng cao

> Các câu dưới đây đòi đọc mục tương ứng trong `Week-00/advanced_topics_vi.md` hoặc paper gốc. Làm sau khi xong phần cơ bản.

## Nâng cao 1 (Trắc nghiệm)

Anthropic phân biệt workflow và agent thế nào, và khuyến nghị nào của họ về framework?

- **A.** Workflow là hệ trong đó LLM và tool được điều phối qua các đường code định trước; agent là hệ trong đó LLM tự điều khiển quy trình và cách dùng tool; các triển khai thành công nhất dùng các pattern đơn giản, ghép được, không dùng framework phức tạp
- **B.** Không có khác biệt
- **C.** Workflow là agent chạy nhanh hơn; nên dùng framework nặng
- **D.** Agent luôn tốt hơn workflow

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói khác biệt kỹ thuật giữa LLM thường và agent chỉ là gì? Điều đó gợi ý cách bạn nên nhìn tool call trong log của Claude Agent SDK ra sao?

---
> Mẹo dùng Claude làm bạn học: trả lời bằng lời của bạn, rồi dán câu trả lời cho Claude và nhờ chấm so với `quiz_solution.md`.
