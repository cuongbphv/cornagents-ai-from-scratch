# Lý thuyết Tuần 15: Agent loop, MCP, 5 tầng engineering, reflective loop

> Đọc trước khi build agent trong [`02_minimal_agent.py`](02_minimal_agent.py). Nguồn chính của tuần là tài liệu trong repo (`docs/`) + docs chính thức đã xác minh 2026-08-11.

---

## 1. Agent là gì: định nghĩa làm việc được

Theo docs Claude Agent SDK (xác minh 2026-08-11): *agent là ứng dụng hoàn thành một task bằng cách tự hoạch định các bước và gọi tool* (đọc file, chạy lệnh, sửa code). Khác chatbot ở một chữ: **loop**.

```
while chưa xong:
    gather context → gọi model → model chọn tool → chạy tool → đưa kết quả về model
```

- **Tool** = hàm có schema (tên, mô tả, tham số): model không "chạy" gì cả, nó chỉ **sinh yêu cầu gọi tool**; harness của bạn chạy thật rồi trả kết quả vào context. Hiểu điểm này là hiểu một nửa agent engineering: chất lượng agent = chất lượng tool + mô tả tool.
- **Subagent** = agent con được giao task hẹp, có context riêng, cách chống phình context window của agent chính.

Loop này không phải phát minh của SDK nào, nó là hậu duệ trực tiếp của hai paper (cả hai có PDF trong repo): CoT (Wei et al. 2022, [`../docs/papers/2201.11903_chain-of-thought-prompting.pdf`](../docs/papers/2201.11903_chain-of-thought-prompting.pdf)) cho model "nghĩ thành lời" trước khi trả lời, rồi ReAct (Yao et al. 2022, [`../docs/papers/2210.03629_react-reasoning-acting.pdf`](../docs/papers/2210.03629_react-reasoning-acting.pdf)) đan xen reasoning với **hành động gọi tool** và quan sát kết quả. Đọc ReAct xong sẽ thấy agent loop ở trên chỉ là ReAct được đóng gói tử tế.

## 2. Năm tầng engineering: bản đồ định vị mọi vấn đề

Từ `docs/5-layers-multi-agent.jpg` (bảng đầy đủ trong [README.md](README.md)): Prompt → Context → Harness → Loop → Graph. Giá trị thực dụng nhất là **chẩn đoán theo tầng** (mục nâng cao I1):

| Triệu chứng | Tầng lỗi |
|-------------|----------|
| Output sai format | 1, Prompt |
| Model không biết thứ cần biết | 2, Context |
| Không ai kiểm kết quả | 3, Harness |
| Chạy mãi không dừng / dừng quá sớm | 4, Loop |
| Nhiều agent lặp việc nhau | 5, Graph |

Nguyên tắc gốc: **model là commodity, hệ thống quanh nó mới là engineering.** Tuần này bạn làm tầng 3-4; Tuần 16-17 lên tầng 5.

## 3. MCP: chuẩn nối agent với thế giới ngoài

Model Context Protocol (modelcontextprotocol.io, xác minh 2026-08-11): chuẩn mở nối AI app với hệ thống ngoài, ví von chính thức của docs là "cổng USB-C cho AI". Kiến trúc: **MCP server** (bọc một nguồn dữ liệu/tool: filesystem, GitHub, Postgres...) ↔ **MCP client** (app AI của bạn) qua transport chuẩn. Giá trị: viết tool một lần, mọi client dùng được, thay vì mỗi framework một kiểu adapter. Task tuần này: nối đúng **một** server (filesystem hoặc GitHub) và gọi được nó từ agent.

## 4. Reflective loop: loop có đo lường, không phải while(true)

Cấu trúc từ `docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` (mục II, VI):

```
generate → evaluate (tiêu chí tường minh) → revise → check stopping rule → lặp
```

- **Evaluator có tiêu chí viết ra được**: "nhìn ổn" không phải tiêu chí; rubric/test/schema mới là.
- **Stopping rule khai báo trước**: max rounds + budget + điều kiện đạt. Thiếu nó là tầng 4 hỏng.
- **Lưu mọi artifact mỗi vòng**: để so vòng sau hơn vòng trước thật không (đây là tính "ratchet": chỉ giữ cải thiện).

Bốn điều kiện làm loop kiểu này chạy được (từ PDF, thuộc lòng): **output verifiable, action reversible, horizon ngắn, environment bounded.** Task nào thiếu điều kiện nào thì bổ sung cơ chế bù (verify bằng gì? undo bằng gì? cắt nhỏ thế nào? giới hạn phạm vi ra sao?) trước khi cho agent tự chạy.

## 5. Chọn orchestration layer: quyết định của tuần

Khung so sánh cho lựa chọn LangGraph vs CrewAI (tiêu chí từ README): domain tài chính có kiểm soát → ưu tiên **stateful + auditable** (trace lại được ai làm gì, state lưu ngoài transcript, human gate chèn được vào giữa graph). Ghi quyết định + lý do vào [`03_cornagents_architecture.md`](03_cornagents_architecture.md): quyết định sai sửa được, quyết định không ghi lý do thì không học được gì.

## 6. Tiếng Việt trong tuần này

- **Quy ước hai lớp ngôn ngữ, giữ nhất quán từ tuần này về sau:** phần "máy đọc" (tên tool, schema, field name, code) bằng tiếng Anh theo quy ước hệ sinh thái; phần "nội dung nghiệp vụ" (system prompt mô tả nghiệp vụ, dữ liệu, output cho người dùng) bằng tiếng Việt. Trộn lẫn hai lớp làm cả người lẫn model khó bảo trì.
- **Test agent với input tiếng Việt ngay từ tuần này**, đừng đợi capstone: dữ liệu tiếng Việt đi xuyên tool boundary (đọc file → JSON → context) là chỗ lộ lỗi encoding/NFC (Tuần 13 mục 6) sớm nhất. Một test "đọc file .md tiếng Việt có dấu → tóm tắt đúng tên riêng" là đủ làm canary.
- [Suy luận] Mô tả tool bằng tiếng Anh nhưng ví dụ trong mô tả nên chứa cả mẫu tiếng Việt nếu tool sẽ nhận dữ liệu Việt, model chọn tool theo mô tả, ví dụ sát thực tế giúp chọn đúng; dựa trên cơ chế tool-choice đọc mô tả, chưa có đo lường riêng cho tiếng Việt.

## 7. Nguồn (đã xác minh truy cập được ngày 2026-08-11)

| Nguồn | URL | Dùng cho mục |
|-------|-----|--------------|
| Claude Agent SDK docs | https://code.claude.com/docs/en/agent-sdk | 1 |
| Model Context Protocol docs | https://modelcontextprotocol.io/ | 3 |
| Wei et al. 2022, Chain-of-Thought (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2201.11903, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 1 |
| Yao et al. 2022, ReAct (CC BY 4.0, kiểm 2026-08-12) | https://arxiv.org/abs/2210.03629, PDF local: [`../docs/papers/`](../docs/papers/README.md) | 1 |
| Tài liệu trong repo | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf), [`../docs/5-layers-multi-agent.jpg`](../docs/5-layers-multi-agent.jpg) | 2, 4 |

(LangGraph/CrewAI docs: link trong README, đọc đúng version lúc cài.)

## Sau khi đọc xong

1. Tự vẽ lại 5 tầng + bảng chẩn đoán bằng lời mình (checklist đầu tiên của README).
2. Build single agent + nối 1 MCP server trong [`02_minimal_agent.py`](02_minimal_agent.py); chạy canary tiếng Việt (mục 6).
3. Build reflective loop đủ 4 thành phần: generate/evaluate/revise/stop, lưu artifact từng vòng.
4. Chọn stack, viết [`03_cornagents_architecture.md`](03_cornagents_architecture.md); làm [`quiz.md`](quiz.md).

## 8. Agent theo định nghĩa giáo trình, và prompt engineering có hệ thống

Năm tầng engineering ở mục 1 là khung của repo. Mục này đối chiếu hai tầng đầu với cách giáo trình định nghĩa, để bạn có ngôn ngữ chung khi đọc paper agent và khi giải thích cho người khác.

**Agent chỉ là token prediction cộng tập action.** Jurafsky và Martin định nghĩa: "An agent is an LLM that has the power to autonomously act in the world, by calling other programs" (SLP3 mục 1.8, trang 24). Ví dụ họ đưa: gọi search engine để lấy thông tin mới, calendar để tính giờ trống, calculator, database, hay API của nhà cung cấp. Model làm được điều đó nhờ có một tập action như SEARCH() hay CALENDAR() mà nó có thể sinh ra trong output. Câu quan trọng nhất của mục: bước nhảy từ trợ lý hội thoại sang agent tự hành là lớn về hệ quả và rủi ro an toàn, nhưng "The intuition, however, is exactly the same as regular language models: token prediction. The technical difference is only that the set of actions in the world are added to the set of possible tokens to generate." Đây là cầu nối thẳng về Tuần 7: tool call chỉ là token đặc biệt trong vocab; loop agent ở mục 2 là vòng sinh token có chỗ dừng để chạy chương trình ngoài rồi nạp kết quả trở lại context. SLP3 minh họa bằng một prompt ReAct với ba action đơn giản, trong đó model xen kẽ Thought, Act và Obs; paper ReAct nằm trong kệ paper.

**Prompt engineering theo nguyên tắc, không theo danh sách.** Xiao và Zhu (*Foundations of LLMs* mục 3.1, trang 97) nói rõ vì sao họ không đưa danh sách prompt: hiệu quả của prompting phụ thuộc rất nhiều vào LLM đang dùng, prompt thay đổi theo model, nên mục tiêu là đưa nguyên tắc dẫn đường thay vì công thức. Mục 3.2 (trang 115) xếp các phương pháp nâng cao thành năm nhóm: chain of thought, problem decomposition, self-refinement, ensembling, và RAG cùng tool use. Với chain of thought (mục 3.2.1), họ dùng bài tính trung bình các số để minh họa: hỏi thẳng thì model trả lời sai; thêm demonstration của bài tương tự thì tốt hơn; và yêu cầu model viết ra các bước suy luận thay vì kết luận ngay thì tốt hơn nữa. Với RAG và tool use (mục 3.2.5, trang 134), họ đặt RAG là cách bù khi LLM chỉ dựa trên kiến thức pretrain "lack accuracy and depth". Bốn nhóm còn lại sẽ quay lại ở Tuần 16 dưới dạng pattern multi-agent.

**Cách dùng trong tuần.** Khi viết prompt cho single agent trong `02_minimal_agent.py`, thử theo đúng thứ tự FoLLM: hỏi thẳng, thêm ví dụ, rồi yêu cầu lập luận từng bước; ghi lại output của ba lần để thấy khác biệt bằng mắt. Khi nối MCP server, hãy nhìn tool call trong log như một token đặc biệt được sinh ra, đúng định nghĩa SLP3, và kiểm rằng kết quả tool được coi là input không đáng tin theo paper Instruction Hierarchy trong kệ paper.

## Đọc thêm từ kệ sách

> Catalog và điều khoản ở [`../docs/books/README.md`](../docs/books/README.md). Số trang là trang in của bản PDF đã tải ngày 2026-09-04; câu trong ngoặc kép là trích nguyên văn.

- **Prompt engineering có hệ thống.** Xiao và Zhu, *Foundations of LLMs* mục 3.1 General Prompt Design (trang 97) nói rõ prompt phụ thuộc model nên sách không đưa danh sách prompt, chỉ đưa nguyên tắc; mục 3.2 Advanced Prompting Methods là chain-of-thought và các biến thể, cùng paper CoT trong kệ paper. Đây là tầng 1 trong 5 tầng của tuần.
- **Agents theo giáo trình NLP.** SLP3 mục 1.8 Agents (trang 24) đặt agent trong bức tranh chung của LLM ngay ở chương mở đầu; chương 12 Agents của sách chưa viết xong tại bản nháp 19/08/2026.
- **Code tham chiếu mở.** Notebook `chapter06/Chapter 6 - Prompt Engineering.ipynb` trong repo Hands-On LLM (Apache-2.0).
