# Lý thuyết Tuần 16: 5 workflow patterns + agent graph cho SDLC

> Đọc trước khi code [`02_agents.py`](02_agents.py). Nguồn chính: tài liệu trong repo (`docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` mục IV, VI.D, VIII): các con số trong file này lấy từ tài liệu đó, ghi rõ tại chỗ.

---

## 1. Năm workflow patterns: vốn từ vựng thiết kế của tuần

Từ PDF mục IV (cùng họ với bài "Building Effective Agents" của Anthropic mà PDF tổng hợp):

| Pattern | Cấu trúc | Dùng khi |
|---------|----------|----------|
| **Prompt Chaining** | A → B → C, output trước là input sau | các bước ổn định, biết trước thứ tự |
| **Routing** | phân loại input → rẽ nhánh xử lý chuyên biệt | input nhiều loại khác hẳn nhau |
| **Parallelization** | chạy nhiều nhánh cùng lúc → gộp | subtask độc lập, hoặc cần nhiều góc nhìn |
| **Orchestrator-Workers** | agent điều phối giao việc động cho worker | không biết trước cần những subtask nào |
| **Evaluator-Optimizer** | generate ↔ evaluate lặp đến đạt | có tiêu chí chấm rõ, cần chất lượng cao |

Nguyên tắc gốc của tài liệu: *"simple, composable patterns rather than complex frameworks"*, chọn pattern đơn giản nhất đủ dùng, ghép lại được.

## 2. Chi phí thật của multi-agent: số phải nhớ trước khi tách vai

Theo PDF (mục IV/VIII, nhắc lại trong README): multi-agent hơn single agent ~**90%** ở task đa hướng nhưng tốn **10-15× token**. Hệ quả kỷ luật:

- Chỉ tách vai khi chuyên môn hoá **thêm tín hiệu** (worker có context/tool/prompt thật sự khác nhau), không tách để "cho giống kiến trúc đẹp".
- **Định nghĩa reducer trước khi fan-out**: ai gộp kết quả, gộp thế nào; fan-out không reducer là rác song song.
- **Khi nào ĐỪNG fan-out** (mục nâng cao I3): task cần một mạch tư duy liền (thiết kế kiến trúc, viết narrative, refactor gắn kết): chia nhỏ làm tệ hơn; và fan-out tạo **lỗi tương quan**: nhiều worker cùng sai một kiểu, verification chỉ cứu được nếu reviewer có prompt/bằng chứng/vai khác.

## 3. Sáu câu hỏi chọn kiến trúc (PDF mục VIII: dùng nguyên bảng trong README)

Bảng đầy đủ ở [README.md](README.md); điều đáng nhấn: câu 1, **success có verify được không?** Không verify được thì chưa được phép nói đến autonomy; viết test/rubric trước. Đây là cùng nguyên tắc với 4 điều kiện của loop Tuần 15, nâng lên mức graph.

## 4. Artifact contract: handoff bằng schema, không bằng văn xuôi

Mỗi cạnh trong graph (agent A → agent B) là một **hợp đồng dữ liệu**: schema tường minh (Pydantic/JSON Schema), có validation tại biên. Vì sao không dùng prose: văn xuôi không validate được, trôi format âm thầm, và agent nhận phải "đoán", đúng loại lỗi tầng 1-2 đã học cách chẩn đoán ở Tuần 15. Ví dụ contract cho Requirements Analyst:

```python
class UserStory(BaseModel):
    story_id: str
    as_a: str            # vai, nội dung tiếng Việt
    i_want: str
    so_that: str
    acceptance_criteria: list[str]   # mỗi AC kiểm được đúng/sai
    source_refs: list[str]           # điều khoản/tài liệu grounding (RAG Tuần 13-14)
```

`source_refs` là chỗ RAG cắm vào: story sinh ra phải **dẫn được về tài liệu nghiệp vụ**: không có ref thì evaluator từ chối, đó chính là quality gate rẻ nhất.

## 5. Human-in-the-loop gates + least privilege

- **Gate đặt ở chỗ chi phí sai cao nhất**: sau requirements (hiểu sai đề → mọi thứ sau sai) và trước merge/commit (hành động khó đảo). Gate = artifact trình cho người + trạng thái chờ duyệt, không phải "in ra console rồi chạy tiếp".
- **Least privilege cho tool**: Requirements Analyst chỉ cần đọc RAG, không cần quyền ghi file; Test-Gen cần ghi file test, không cần network. Scope hẹp làm sai sót của một agent không lan thành sự cố hệ thống.
- **Tool output là input KHÔNG đáng tin**: cùng họ vấn đề với prompt injection. Wallace et al. 2024, *The Instruction Hierarchy* (arXiv [2404.13208](https://arxiv.org/abs/2404.13208), abstract tra 2026-08-12) chỉ ra gốc rễ: LLM hiện "treat system prompts and user inputs with equal priority", và đề xuất huấn luyện model "selectively ignore lower-privileged instructions". Bạn không train lại model được, nhưng rút được nguyên tắc thiết kế: đừng đưa nguyên văn tài liệu RAG/tool output vào vị trí có quyền ra lệnh, bọc nó, đánh dấu nó là dữ liệu.

## 6. Ba agent của tuần: điểm thiết kế chính

1. **Requirements Analyst** (thế mạnh BA): feature request → user stories + AC theo contract mục 4, grounded qua RAG. Đây là agent "ăn tiền" nhất vì domain knowledge của bạn nằm ở đây.
2. **Code Review agent**: trả về **criterion-level defects**: từng lỗi gắn với tiêu chí cụ thể (đúng/sai kiểm được), cấm output "looks good". Danh sách tiêu chí là một phần của prompt, không phải để model tự nghĩ.
3. **Test-Generation agent**: từ story/AC → test case; mỗi AC ít nhất một test, ánh xạ 1-1 kiểm được bằng code, khỏi cần LLM chấm.

Nối bằng: orchestrator-workers (phân việc) + evaluator-optimizer (vòng chất lượng quanh review), đúng gợi ý README.

Khi viết `03_agent_design.md`, có thể mượn khung mô tả của survey Tran et al. 2025 (arXiv [2501.06322](https://arxiv.org/abs/2501.06322), abstract tra 2026-08-12): mô tả hệ multi-agent theo 5 chiều, "actors (agents involved), types (e.g., cooperation, competition...), structures (e.g., peer-to-peer, centralized...), strategies (e.g., role-based...), and coordination protocols". Điền đủ 5 ô cho thiết kế của mình là một bài kiểm tra "mình đã nghĩ hết chưa" rẻ tiền.

## 7. Tiếng Việt trong tuần này

- **Schema tiếng Anh, nội dung tiếng Việt** (quy ước Tuần 15 mục 6): field `as_a`, `acceptance_criteria` là tiếng Anh; giá trị bên trong là tiếng Việt nghiệp vụ. Validation không phụ thuộc ngôn ngữ nội dung.
- **Glossary nghiệp vụ VN-EN là một artifact hạng nhất**: thuật ngữ tài chính ("tài sản bảo đảm", "hạn mức tín dụng", "giải ngân") phải dịch/diễn giải nhất quán giữa các agent, đưa glossary vào context của MỌI agent (tầng 2), đừng để mỗi agent tự dịch một kiểu. Tuần 17 sẽ nâng glossary này lên thành entity trong knowledge graph.
- **AC viết tiếng Việt vẫn phải kiểm được đúng/sai**: "hệ thống phản hồi nhanh" không kiểm được; "API trả kết quả trong ≤ 2s với 95% request" kiểm được. Ngôn ngữ nào cũng vậy, nhưng viết AC kiểm được bằng tiếng Việt là kỹ năng BA bạn mang sẵn, dùng nó làm tiêu chí cho evaluator.

## 8. Nguồn

| Nguồn | Vị trí | Dùng cho mục |
|-------|--------|--------------|
| Karpathy-Loop PDF (mục IV, VI.D, VIII) | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) | 1, 2, 3 |
| Claude Agent SDK docs (xác minh 2026-08-11) | https://code.claude.com/docs/en/agent-sdk | 5, 6 |
| Wallace et al. 2024, The Instruction Hierarchy (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2404.13208 | 5 |
| Tran et al. 2025, Multi-Agent Collaboration Mechanisms: A Survey (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2501.06322 | 6 |

(CodeRabbit/Sonar/GlobalLogic: tham chiếu pattern trong README, đọc lấy ý quality gate, không phải nguồn trích số liệu.)

## Sau khi đọc xong

1. Map từng stage SDLC ↔ pattern + I/O (giấy trước, code sau).
2. Viết artifact contract (mục 4) cho cả 3 handoff TRƯỚC khi viết agent nào.
3. Code 3 agent trong [`02_agents.py`](02_agents.py), nối graph, thêm gate + least privilege.
4. Chạy 1 requirement Finance Banking end-to-end; ghi [`03_agent_design.md`](03_agent_design.md); làm [`quiz.md`](quiz.md).

## 9. Problem decomposition và self-refinement: gốc của các workflow pattern

Năm workflow pattern ở mục trên (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) là cách đóng gói của Anthropic. Chúng đứng trên hai ý tưởng cũ hơn mà giáo trình mô tả ở mức prompt đơn: chia nhỏ bài toán và tự sửa.

**Problem decomposition.** Xiao và Zhu (*Foundations of LLMs* mục 3.2.2, trang 117) nhận xét LLM giải bài phức tạp tốt hơn khi bài được chia thành các bài con đơn giản hơn, và đặt điều đó vào một khung rộng hơn tên là problem decomposition, đã được bàn nhiều trong tâm lý học và khoa học máy tính. Họ nhắc hai chế độ tư duy của Kahneman: System 1 nhanh, tự động, trực giác; System 2 chậm, có chủ đích, phân tích, được kích hoạt khi cần tính toán phức tạp. Chain of thought và decomposition là cách kéo LLM sang chế độ thứ hai. Ở mức hệ thống, orchestrator-workers là decomposition được thể chế hóa: một model trung tâm chia việc, các worker giải từng phần, kết quả được gom lại. Requirements Analyst agent của bạn chia một feature request thành các user story là một decomposition; mỗi story kèm acceptance criteria là một bài con có tiêu chí kiểm được.

**Self-refinement.** Mục 3.2.3 (trang 124) xuất phát từ việc dự đoán của LLM có thể sai, và vì LLM đã làm được các tác vụ như sửa và hiệu chỉnh, nên hợp lý khi để model tự tinh chỉnh output của mình; họ nói self-refinement là hiện tượng thường thấy trong tâm lý học con người. Evaluator-optimizer là phiên bản hai vai của cùng ý tưởng: một bên sinh, một bên chấm theo tiêu chí, lặp đến khi đạt. Code Review agent của bạn là evaluator; điểm khác với self-refinement trong một prompt là evaluator được tách vai, có tiêu chí viết sẵn, và không nhìn thấy lý lẽ của bên sinh; [Suy luận] nhờ vậy ít bị thuyết phục hơn, dựa trên quan sát mẫu hành vi, chưa có nguồn đo lường trong kệ sách. Đó là lý do mục nâng cao I3 khuyên tách vai khi tiêu chí kiểm được rõ ràng, và giữ một agent khi không.

**Ensembling và routing.** Hai nhóm còn lại của FoLLM mục 3.2 (trang 130) ứng với hai pattern còn lại: ensembling, sinh nhiều lời giải rồi gộp hoặc bỏ phiếu, là parallelization; còn routing là chọn prompt hoặc model chuyên biệt theo loại input, thứ bạn đã thấy ở dataset BANKING77 trong guide dataset. Khi điền `03_agent_design.md`, với mỗi agent hãy ghi nó là hiện thân của ý tưởng nào trong bốn ý tưởng này; nếu không ghi được, có thể agent đó không cần tồn tại, và một prompt tốt hơn là đủ. Đây cũng là tinh thần của decision framework sáu câu hỏi trong PDF Karpathy-Loop: thêm agent chỉ khi có tiêu chí kiểm được và chi phí token 10 đến 15 lần đáng trả.
