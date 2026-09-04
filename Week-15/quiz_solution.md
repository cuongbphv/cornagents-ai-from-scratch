# Tuần 15, Đáp án & Giải thích: Nền tảng agentic: 5 tầng engineering, Claude Agent SDK, MCP

> Chỉ mở sau khi đã tự trả lời `quiz.md`.

## Câu 1 (Tự luận)

Mô tả 'agent loop' cơ bản.

**Trả lời mẫu:** perceive (nhận input/trạng thái) → reason (LLM suy luận, quyết định bước tiếp) → chọn tool → execute tool → quan sát kết quả → lặp lại cho tới khi đạt mục tiêu, rồi trả về structured output. Khác với một lần gọi LLM, agent có vòng lặp nhiều bước có dùng công cụ và trạng thái.

**Giải thích:** Đây là khung chung của Claude Agent SDK và mọi agent framework.

## Câu 2 (Trắc nghiệm)

MCP (Model Context Protocol) là gì?

- **A.** Một định dạng file
- **B.** Một chuẩn mở để kết nối model với tool/nguồn dữ liệu qua server/client (GitHub, Postgres, Slack, filesystem...) (đáp án đúng)
- **C.** Một thuật toán RL
- **D.** Một model ngôn ngữ

**Đáp án: B**

**Giải thích:** MCP tách 'bộ não' khỏi nguồn dữ liệu/tool, cho phép tái sử dụng các server tool chuẩn hoá.

## Câu 3 (Trắc nghiệm)

Khác biệt chính giữa LangGraph và CrewAI?

- **A.** LangGraph: graph có trạng thái, tường minh, auditable; CrewAI: crew theo vai (role) prototype nhanh (đáp án đúng)
- **B.** LangGraph chỉ cho vision, CrewAI cho text
- **C.** CrewAI không hỗ trợ tool
- **D.** Cả hai giống hệt nhau

**Đáp án: A**

**Giải thích:** LangGraph hợp workflow cần kiểm soát/audit (tài chính có quy định); CrewAI nhanh để dựng nhóm agent theo vai.

## Câu 4 (Tự luận)

Vì sao workflow tài chính có quy định nên ưu tiên LangGraph?

**Trả lời mẫu:** Vì LangGraph cho phép định nghĩa trạng thái và luồng chuyển tiếp một cách tường minh, có thể kiểm tra/ghi vết (auditable) từng bước, và chèn các human-in-the-loop gate rõ ràng. Trong domain tài chính bị ràng buộc quy định, khả năng giải trình 'vì sao agent ra quyết định này' và kiểm soát chặt từng chuyển tiếp quan trọng hơn tốc độ prototype.

**Giải thích:** CrewAI tiện cho thử nghiệm nhanh nhưng kém minh bạch hơn về luồng trạng thái.

## Câu 5 (Trắc nghiệm)

Human-in-the-loop (HITL) gate nghĩa là gì?

- **A.** Cách tính token
- **B.** Agent chạy hoàn toàn tự động không cần người
- **C.** Một loại tool
- **D.** Điểm dừng yêu cầu con người phê duyệt/sửa trước khi agent đi tiếp (đáp án đúng)

**Đáp án: D**

**Giải thích:** HITL gate đặt giữa các stage rủi ro để con người kiểm soát; thiết kế least-privilege + HITL ngay từ đầu.

## Câu 6 (Trắc nghiệm)

Mô hình 5 tầng engineering (docs/5-layers-multi-agent.jpg) xếp theo thứ tự nào, từ trong ra ngoài?

- **A.** Prompt → Context → Harness → Loop → Graph (đáp án đúng)
- **B.** Loop → Prompt → Context → Graph → Harness
- **C.** Prompt → Harness → Context → Graph → Loop
- **D.** Context → Prompt → Loop → Harness → Graph

**Đáp án: A**

**Giải thích:** Prompt (the message) → Context (the memory) → Harness (the machine: gather-act-verify) → Loop (the system: run-check-decide) → Graph (the organization: nhiều agent + shared memory). Mỗi tầng bọc tầng trước; model là commodity, hệ thống quanh nó là engineering.

## Câu 7 (Tự luận)

Bốn điều kiện nào làm loop autoresearch của Karpathy chạy được, và vì sao thiếu một cái là loop hỏng?

**Trả lời mẫu:** (1) Output verifiable, có metric đo được (val_bpb), không thì agent tối ưu thứ sai; (2) Action reversible, git reset về commit giữ lại được, thất bại không phá state; (3) Horizon ngắn, run ~5 phút cho feedback dày; (4) Environment bounded, repo giới hạn không gian hành động. Thiếu verify thì không biết giữ hay bỏ thay đổi; thiếu reversible thì một lỗi phá cả quá trình; horizon dài làm tín hiệu học thưa; environment mở làm không gian tìm kiếm nổ.

**Giải thích:** Đây là checklist trước khi cho agent chạy tự động bất kỳ việc gì, kể cả trong CornAgents.AI.

---

## Phần nâng cao

## Nâng cao 1 (Trắc nghiệm)

Anthropic phân biệt workflow và agent thế nào, và khuyến nghị nào của họ về framework?

- **A.** Workflow là hệ trong đó LLM và tool được điều phối qua các đường code định trước; agent là hệ trong đó LLM tự điều khiển quy trình và cách dùng tool; các triển khai thành công nhất dùng các pattern đơn giản, ghép được, không dùng framework phức tạp (đáp án đúng)
- **B.** Không có khác biệt
- **C.** Workflow là agent chạy nhanh hơn; nên dùng framework nặng
- **D.** Agent luôn tốt hơn workflow

**Đáp án: A**

**Giải thích:** Trích 'Building Effective AI Agents': workflows là 'Systems where LLMs and tools are orchestrated through predefined code paths'; agents là 'Systems where LLMs dynamically direct their own processes and tool usage'.

## Nâng cao 2 (Tự luận)

Jurafsky và Martin nói khác biệt kỹ thuật giữa LLM thường và agent chỉ là gì? Điều đó gợi ý cách bạn nên nhìn tool call trong log của Claude Agent SDK ra sao?

**Trả lời mẫu:** SLP3 mục 1.8 (trang 24): agent là LLM có thể hành động bằng cách gọi chương trình khác, và 'The technical difference is only that the set of actions in the world are added to the set of possible tokens to generate'. Vậy tool call trong log là một token đặc biệt được sinh ra rồi được harness thực thi; kết quả tool quay lại context như input không đáng tin, theo paper Instruction Hierarchy trong kệ paper.

**Giải thích:** Cách nhìn này nối thẳng Tuần 15 về Tuần 7: vẫn là token prediction.
