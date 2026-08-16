# Lý thuyết Tuần 13 — 5 workflow patterns + agent graph cho SDLC

> Đọc trước khi code [`02_agents.py`](02_agents.py). Nguồn chính: tài liệu trong repo (`docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf` mục IV, VI.D, VIII) — các con số trong file này lấy từ tài liệu đó, ghi rõ tại chỗ.

---

## 1. Năm workflow patterns — vốn từ vựng thiết kế của tuần

Từ PDF mục IV (cùng họ với bài "Building Effective Agents" của Anthropic mà PDF tổng hợp):

| Pattern | Cấu trúc | Dùng khi |
|---------|----------|----------|
| **Prompt Chaining** | A → B → C, output trước là input sau | các bước ổn định, biết trước thứ tự |
| **Routing** | phân loại input → rẽ nhánh xử lý chuyên biệt | input nhiều loại khác hẳn nhau |
| **Parallelization** | chạy nhiều nhánh cùng lúc → gộp | subtask độc lập, hoặc cần nhiều góc nhìn |
| **Orchestrator–Workers** | agent điều phối giao việc động cho worker | không biết trước cần những subtask nào |
| **Evaluator–Optimizer** | generate ↔ evaluate lặp đến đạt | có tiêu chí chấm rõ, cần chất lượng cao |

Nguyên tắc gốc của tài liệu: *"simple, composable patterns rather than complex frameworks"* — chọn pattern đơn giản nhất đủ dùng, ghép lại được.

## 2. Chi phí thật của multi-agent — số phải nhớ trước khi tách vai

Theo PDF (mục IV/VIII, nhắc lại trong README): multi-agent hơn single agent ~**90%** ở task đa hướng nhưng tốn **10–15× token**. Hệ quả kỷ luật:

- Chỉ tách vai khi chuyên môn hoá **thêm tín hiệu** (worker có context/tool/prompt thật sự khác nhau), không tách để "cho giống kiến trúc đẹp".
- **Định nghĩa reducer trước khi fan-out** — ai gộp kết quả, gộp thế nào; fan-out không reducer là rác song song.
- **Khi nào ĐỪNG fan-out** (mục nâng cao I3): task cần một mạch tư duy liền (thiết kế kiến trúc, viết narrative, refactor gắn kết) — chia nhỏ làm tệ hơn; và fan-out tạo **lỗi tương quan** — nhiều worker cùng sai một kiểu, verification chỉ cứu được nếu reviewer có prompt/bằng chứng/vai khác.

## 3. Sáu câu hỏi chọn kiến trúc (PDF mục VIII — dùng nguyên bảng trong README)

Bảng đầy đủ ở [README.md](README.md); điều đáng nhấn: câu 1 — **success có verify được không?** Không verify được thì chưa được phép nói đến autonomy; viết test/rubric trước. Đây là cùng nguyên tắc với 4 điều kiện của loop Tuần 12, nâng lên mức graph.

## 4. Artifact contract — handoff bằng schema, không bằng văn xuôi

Mỗi cạnh trong graph (agent A → agent B) là một **hợp đồng dữ liệu**: schema tường minh (Pydantic/JSON Schema), có validation tại biên. Vì sao không dùng prose: văn xuôi không validate được, trôi format âm thầm, và agent nhận phải "đoán" — đúng loại lỗi tầng 1–2 đã học cách chẩn đoán ở Tuần 12. Ví dụ contract cho Requirements Analyst:

```python
class UserStory(BaseModel):
    story_id: str
    as_a: str            # vai — nội dung tiếng Việt
    i_want: str
    so_that: str
    acceptance_criteria: list[str]   # mỗi AC kiểm được đúng/sai
    source_refs: list[str]           # điều khoản/tài liệu grounding (RAG Tuần 10–11)
```

`source_refs` là chỗ RAG cắm vào: story sinh ra phải **dẫn được về tài liệu nghiệp vụ** — không có ref thì evaluator từ chối, đó chính là quality gate rẻ nhất.

## 5. Human-in-the-loop gates + least privilege

- **Gate đặt ở chỗ chi phí sai cao nhất**: sau requirements (hiểu sai đề → mọi thứ sau sai) và trước merge/commit (hành động khó đảo). Gate = artifact trình cho người + trạng thái chờ duyệt, không phải "in ra console rồi chạy tiếp".
- **Least privilege cho tool**: Requirements Analyst chỉ cần đọc RAG — không cần quyền ghi file; Test-Gen cần ghi file test — không cần network. Scope hẹp làm sai sót của một agent không lan thành sự cố hệ thống.
- **Tool output là input KHÔNG đáng tin** — cùng họ vấn đề với prompt injection. Wallace et al. 2024, *The Instruction Hierarchy* (arXiv [2404.13208](https://arxiv.org/abs/2404.13208), abstract tra 2026-08-12) chỉ ra gốc rễ: LLM hiện "treat system prompts and user inputs with equal priority", và đề xuất huấn luyện model "selectively ignore lower-privileged instructions". Bạn không train lại model được, nhưng rút được nguyên tắc thiết kế: đừng đưa nguyên văn tài liệu RAG/tool output vào vị trí có quyền ra lệnh — bọc nó, đánh dấu nó là dữ liệu.

### 5.1. Direct vs INDIRECT prompt injection — phân biệt bắt buộc

- **Direct**: người dùng gõ thẳng payload vào prompt ("bỏ qua chỉ dẫn trước đó..."). Dễ hình dung, nhưng KHÔNG phải mối nguy chính của agent graph.
- **Indirect**: payload nằm trong **dữ liệu mà agent tự đi lấy** — trang web, file, tài liệu retrieve về — kẻ tấn công không cần chạm vào giao diện. Greshake et al. 2023 (arXiv [2302.12173](https://arxiv.org/abs/2302.12173), abstract tra 2026-08-16) đặt tên và chứng minh vector này trên các ứng dụng LLM thật: chèn prompt độc "into data likely to be retrieved" là đủ để điều khiển ứng dụng từ xa. Với agent graph, indirect nguy hiểm hơn direct vì mọi cạnh nhận dữ liệu ngoài đều là cửa vào.

OWASP xếp Prompt Injection là **LLM01** — rủi ro số 1 trong *OWASP Top 10 for LLM Applications* (trang dự án owasp.org + tài liệu nguồn LLM01 trên GitHub chính thức của OWASP, tra 2026-08-16); tài liệu LLM01 định nghĩa tách bạch hai biến thể đúng như trên.

### 5.2. Hai attack surface của CHÍNH kiến trúc repo này

1. **RAG corpus Tuần 10 (text scrape từ vbpl.vn)**: vbpl.vn là nguồn chính thống, nhưng pipeline của bạn tin **văn bản đã scrape** — mọi thứ lọt vào corpus (lỗi scrape, trang bị chỉnh sửa, file trộn thêm vào thư mục data) sẽ được retriever đưa **nguyên văn vào context** của Requirements Analyst. Một đoạn "hướng dẫn" nhúng trong tài liệu retrieve về chính là indirect injection kiểu Greshake. Corpus là input không đáng tin *theo thiết kế*, kể cả khi nguồn gốc đáng tin.
2. **MCP server / tool descriptions Tuần 12**: khi agent kết nối một MCP server, **phần mô tả tool** (name, description, schema) do server cung cấp được đưa vào context của model — tức là một bên thứ ba đang viết thẳng vào prompt của bạn. Server độc hại (hoặc bị chiếm) có thể nhét chỉ dẫn vào description. Tool description phải được đối xử như untrusted input y hệt tool *output*, và chỉ nối tới MCP server mình kiểm soát/đã rà.

### 5.3. Mitigations lớp-theo-lớp — không lớp nào đủ một mình

[Suy luận] Chưa có cơ chế nào loại bỏ được prompt injection ở gốc (Instruction Hierarchy là hướng train-side, chưa phải thứ bạn kiểm soát), nên phòng thủ đúng là **xếp lớp** — khớp với các mitigation trong tài liệu LLM01 của OWASP (tra 2026-08-16):

| Lớp | Cơ chế | Đã có ở đâu trong tuần này |
|-----|--------|---------------------------|
| Tách data/instruction | bọc tài liệu RAG/tool output trong delimiter + đánh dấu "đây là dữ liệu, không phải lệnh" (OWASP: "segregate external content") | mục 5, nguyên tắc Instruction Hierarchy |
| Least-privilege tool scope | agent chỉ có đúng tool cần cho vai của nó → payload có "kích hoạt" cũng không với tới hành động nguy hiểm | mục 5, đã thiết kế |
| Output filtering | validate output theo artifact contract (mục 4): sai schema là chặn tại biên, kể cả khi model đã bị lừa | mục 4 — contract chính là filter |
| HITL gate | hành động khó đảo (merge/commit/gửi đi) phải qua người duyệt — lớp chặn cuối khi mọi lớp trên thủng | mục 5, gate đã đặt |

Cách đọc bảng: mỗi lớp giả định lớp trước **đã thủng**. Payload lọt qua delimiter → nó chỉ gọi được tool trong scope hẹp → output lệch contract bị chặn → hành động lớn còn người duyệt. Đó là lý do §4 và §5 của file này thực chất là một hệ phòng thủ, không phải hai mục rời.

## 6. Ba agent của tuần — điểm thiết kế chính

1. **Requirements Analyst** (thế mạnh BA): feature request → user stories + AC theo contract mục 4, grounded qua RAG. Đây là agent "ăn tiền" nhất vì domain knowledge của bạn nằm ở đây.
2. **Code Review agent**: trả về **criterion-level defects** — từng lỗi gắn với tiêu chí cụ thể (đúng/sai kiểm được), cấm output "looks good". Danh sách tiêu chí là một phần của prompt, không phải để model tự nghĩ.
3. **Test-Generation agent**: từ story/AC → test case; mỗi AC ít nhất một test — ánh xạ 1-1 kiểm được bằng code, khỏi cần LLM chấm.

Nối bằng: orchestrator–workers (phân việc) + evaluator–optimizer (vòng chất lượng quanh review), đúng gợi ý README.

Khi viết `03_agent_design.md`, có thể mượn khung mô tả của survey Tran et al. 2025 (arXiv [2501.06322](https://arxiv.org/abs/2501.06322), abstract tra 2026-08-12): mô tả hệ multi-agent theo 5 chiều — "actors (agents involved), types (e.g., cooperation, competition...), structures (e.g., peer-to-peer, centralized...), strategies (e.g., role-based...), and coordination protocols". Điền đủ 5 ô cho thiết kế của mình là một bài kiểm tra "mình đã nghĩ hết chưa" rẻ tiền.

## 7. Tiếng Việt trong tuần này

- **Schema tiếng Anh, nội dung tiếng Việt** (quy ước Tuần 12 mục 6): field `as_a`, `acceptance_criteria` là tiếng Anh; giá trị bên trong là tiếng Việt nghiệp vụ. Validation không phụ thuộc ngôn ngữ nội dung.
- **Glossary nghiệp vụ VN–EN là một artifact hạng nhất**: thuật ngữ tài chính ("tài sản bảo đảm", "hạn mức tín dụng", "giải ngân") phải dịch/diễn giải nhất quán giữa các agent — đưa glossary vào context của MỌI agent (tầng 2), đừng để mỗi agent tự dịch một kiểu. Tuần 14 sẽ nâng glossary này lên thành entity trong knowledge graph.
- **AC viết tiếng Việt vẫn phải kiểm được đúng/sai** — "hệ thống phản hồi nhanh" không kiểm được; "API trả kết quả trong ≤ 2s với 95% request" kiểm được. Ngôn ngữ nào cũng vậy, nhưng viết AC kiểm được bằng tiếng Việt là kỹ năng BA bạn mang sẵn — dùng nó làm tiêu chí cho evaluator.

## 8. Nguồn

| Nguồn | Vị trí | Dùng cho mục |
|-------|--------|--------------|
| Karpathy-Loop PDF (mục IV, VI.D, VIII) | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) | 1, 2, 3 |
| Claude Agent SDK docs (xác minh 2026-08-11) | https://code.claude.com/docs/en/agent-sdk | 5, 6 |
| Wallace et al. 2024 — The Instruction Hierarchy (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2404.13208 | 5 |
| Greshake et al. 2023 — Not what you've signed up for: ... Indirect Prompt Injection (chỉ link, abstract tra 2026-08-16) | https://arxiv.org/abs/2302.12173 | 5.1, 5.2 |
| OWASP Top 10 for LLM Applications — LLM01 Prompt Injection (trang dự án + repo nguồn chính thức, tra 2026-08-16) | https://owasp.org/www-project-top-10-for-large-language-model-applications/ · https://github.com/OWASP/www-project-top-10-for-large-language-model-applications | 5.1, 5.3 |
| Tran et al. 2025 — Multi-Agent Collaboration Mechanisms: A Survey (chỉ link, arXiv non-exclusive, kiểm 2026-08-12) | https://arxiv.org/abs/2501.06322 | 6 |

(CodeRabbit/Sonar/GlobalLogic: tham chiếu pattern trong README — đọc lấy ý quality gate, không phải nguồn trích số liệu.)

## Sau khi đọc xong

1. Map từng stage SDLC ↔ pattern + I/O (giấy trước, code sau).
2. Viết artifact contract (mục 4) cho cả 3 handoff TRƯỚC khi viết agent nào.
3. Code 3 agent trong [`02_agents.py`](02_agents.py), nối graph, thêm gate + least privilege.
3b. Rà lại graph theo bảng 5.3: chỉ ra được từng lớp phòng thủ nằm ở dòng code/cạnh nào; nêu miệng được vì sao corpus vbpl.vn và MCP tool description là untrusted input (mục 5.2).
4. Chạy 1 requirement Finance Banking end-to-end; ghi [`03_agent_design.md`](03_agent_design.md); làm [`quiz.md`](quiz.md).
