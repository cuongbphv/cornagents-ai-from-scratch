# Lý thuyết Tuần 18: Capstone: lắp ghép, complexity budget, evaluation

> Đọc trước khi chốt use case và viết [`02_eval_rubric.md`](02_eval_rubric.md). Tuần này không có khái niệm mới, nó là bài kiểm tra xem 17 tuần trước có ghép lại được thành một hệ thống **đo được** không. Nguồn: PDF trong `docs/` + paper LLM-judge đã xác minh 2026-08-11.

---

## 1. Bản đồ lắp ghép: mỗi mảnh về đúng vai

```
Feature request (Finance Banking)
   │
   ▼
Requirements Analyst agent (T16) ──đọc──> RAG (T13-14): grounding trực tiếp vào tài liệu
   │  ghi entities/relations                 │
   ▼                                         ▼
Knowledge Graph (T17): shared memory ──fact-check──> Review agent (T16)
   │                                         │
   ▼                                         ▼
Test-Gen agent (T16)              (tùy chọn) model fine-tuned (T11/T12) cho sub-task hẹp
   │
   ▼
Human gate → artifacts: stories + design note + tests + eval report
```

Nguyên tắc phân vai model (từ README): Claude làm "brain" orchestration; model 7B fine-tuned chỉ nhận sub-task hẹp đã chứng minh được ở Tuần 11-12 (ví dụ một tác vụ phân loại nghiệp vụ): **không** giao 7B làm brain để "tiết kiệm".

## 2. Complexity budget: khai báo TRƯỚC khi chạy

Từ PDF mục VII + I5 (bảng trong README): max model calls, max sub-agents, max concurrent workers, max wall-clock, max tokens/chi phí, max retries, và **bằng chứng tối thiểu để được finalize**.

- Hết budget → trả **artifact tốt nhất hiện có + danh sách issue chưa xử lý + lý do dừng**. Không giấu partial failure sau một câu trả lời trôi chảy, che partial failure là dạng "bịa" ở mức hệ thống.
- Budget là số cụ thể viết vào config trước khi chạy, không phải cảm giác "chạy lâu quá thì dừng".

## 3. Ba metric bắt buộc: định nghĩa vận hành được

| Metric | Định nghĩa đo được | Cách đo |
|--------|---------------------|---------|
| **Success rate** | % run cho ra artifact đạt rubric | chấm theo [`02_eval_rubric.md`](02_eval_rubric.md), tiêu chí đúng/sai |
| **Human-override rate** | % artifact người duyệt phải sửa/bác tại gate | đếm tại human gate, rẻ và trung thực nhất |
| **Groundedness** | % claim dẫn được về nguồn (điều khoản/tài liệu/edge) | kiểm `source_refs` từng claim; với KG: cite edge có provenance |

Trong domain có quy định, **groundedness quan trọng hơn success rate** (đã chốt trong README): một câu trả lời "thành công" mà không dẫn nguồn là rủi ro, không phải thành tích.

## 4. Eval rubric: viết sao cho chấm được

- Mỗi tiêu chí là câu **đúng/sai kiểm được**, kèm cách kiểm (test, so schema, đối chiếu nguồn): kỹ năng viết AC của Tuần 16 mục 7 áp lại cho chính hệ thống.
- Chấm bằng LLM-judge thì các bẫy đã xác minh ở Tuần 14 (Zheng et al., arXiv 2306.05685: thiên vị độ dài, vị trí, cùng họ model) áp **trực tiếp** vào rubric của bạn, giữ judge cố định, kiểm tay mẫu nhỏ, đừng tin một chỉ số duy nhất.
- **Metric bị game** (mục nâng cao I5): ratchet chỉ cải thiện thứ nó thấy, success rate tăng có thể đi kèm chi phí tăng hoặc overfit eval set; luôn giữ ràng buộc phụ (budget, groundedness) bên cạnh metric chính.

## 5. Tracing + thước đo cuối

Instrument Langfuse/LangSmith cho MỌI bước (bài Tuần 14 mục 6, giờ áp cho cả graph). Thước đo "hệ thống đáng tin" từ PDF, tự kiểm từng vế với demo của bạn:

> *"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."*

Vế nào không chỉ ra được bằng trace/artifact thật → đó là việc phải làm nốt, không phải câu chữ để trích. Câu này đúng thì loops/swarms/graphs compose được; sai thì thêm agent chỉ tăng độ mờ đục.

## 6. Retrospective: nối ngược về Phase 1 (deliverable thật của roadmap)

[`03_retrospective.md`](03_retrospective.md) trả lời: hệ thống hoạt động **vì sao**: nối từng hành vi quan sát được về internals đã tự tay build. Gợi ý các sợi chỉ: temperature thấp giữ groundedness (sampling, T8/T13) ← bạn hiểu softmax T4; RAG thắng fine-tune cho kiến thức quy định (T11) ← bạn hiểu trọng số học phân phối, không lưu facts (T8-9); KG bắt multi-hop mà embedding trượt (T17) ← bạn hiểu cosine đo ngữ nghĩa, không đo cấu trúc (T13); chi phí multi-agent 10-15× (T16) ← bạn hiểu mỗi token đi qua từng layer (T7). Viết bằng lời mình, tiêu chí tự đánh giá của cả repo.

## 7. Tiếng Việt trong capstone

- **Groundedness tiếng Việt = dẫn về đúng số Điều/Khoản/văn bản**: tận dụng provenance đã ép từ Tuần 13 (metadata) và Tuần 17 (edge). Claim nghiệp vụ không có ref là fail rubric, bất kể văn có mượt.
- **Rubric viết bằng tiếng Việt**: người duyệt tại gate là người đọc nghiệp vụ tiếng Việt; rubric họ không đọc được thì human gate chỉ là hình thức. (Tên metric/field giữ tiếng Anh theo quy ước hai lớp, Tuần 15 mục 6.)
- **Eval set = câu hỏi nghiệp vụ tiếng Việt thật** (50-100 câu đã xây từ Tuần 14) + bộ 10 prompt song ngữ (Tuần 12) nếu có model fine-tuned trong luồng, kiểm cả chất lượng lẫn "sức khỏe song ngữ" trong một lần đo.
- [Suy luận] Judge chấm groundedness trên văn bản pháp lý tiếng Việt nên được kiểm tay tỷ lệ cao hơn bình thường (ví dụ 20% mẫu thay vì 10%): thiên vị judge trên tiếng Việt chưa được đo riêng trong nguồn đã dẫn, thận trọng là rẻ.

## 8. Nguồn

| Nguồn | Vị trí | Dùng cho mục |
|-------|--------|--------------|
| Karpathy-Loop PDF (mục VII-IX, Table VI) | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) | 2, 5 |
| Zheng et al. 2023, LLM-as-a-Judge (xác minh 2026-08-11) | https://arxiv.org/abs/2306.05685 | 4 |

(Langfuse/LangSmith/promptfoo: link trong README nguồn học.)

## Sau khi đọc xong

1. Chốt use case + vẽ bản đồ lắp ghép của riêng bạn (mục 1) trên giấy.
2. Khai báo complexity budget bằng số, viết vào config.
3. Viết [`02_eval_rubric.md`](02_eval_rubric.md) (tiếng Việt, tiêu chí đúng/sai) trước khi chạy demo.
4. Chạy end-to-end, đo 3 metric, tự kiểm câu "traced to..." từng vế; viết [`03_retrospective.md`](03_retrospective.md); làm [`quiz.md`](quiz.md).

## 9. Đánh giá hệ thống: từ accuracy trên test set tới rubric của capstone

Ba metric bắt buộc ở mục 3 (success rate, human-override rate, groundedness) là thiết kế riêng của repo. Mục này nối chúng về cách giáo trình đánh giá hệ thống NLP, để rubric của bạn không tự phát minh lại thuật ngữ và để biết mình đang đo cái gì. Catalog sách ở [`../docs/books/README.md`](../docs/books/README.md).

**Accuracy trên tập test chưa thấy.** Jurafsky và Martin mở đầu mục 1.9 (SLP3, trang 25) bằng câu hỏi làm sao biết một ý tưởng NLP mới có hiệu quả, hay so hai hệ thống, và trả lời: cần một cách đánh giá, "But we first have to decide what 'how well it works' means!" Thứ hay đo nhất là accuracy: tạo một test set gồm câu hỏi hoặc câu cần gán nhãn, người gán đáp án đúng, chạy hệ thống, đếm tỉ lệ đúng. Điều kiện họ nhấn: test set phải **unseen**, người phát triển chưa từng train trên đó. Đây là kỷ luật validation của Tuần 3 mục 5, giờ áp cho một hệ thống nhiều agent thay cho một model: các feature request bạn dùng để chỉnh prompt và schema không được nằm trong bộ chấm cuối. Với LLM, SLP3 nhắc có nhiều benchmark lớn dưới dạng câu hỏi kiến thức trắc nghiệm hoặc tự luận; success rate của capstone là accuracy trên một benchmark tự dựng cho đúng domain, và giá trị của nó nằm ở việc bạn tự viết đáp án đúng có dẫn điều khoản.

**Exact match và token F1.** Mục 11.6 (trang 271) cho hai kỹ thuật chấm QA: với câu hỏi trắc nghiệm như MMLU, báo exact match, tỉ lệ câu trả lời trùng khít đáp án; với câu trả lời tự do như Natural Questions, dùng token F1, coi dự đoán và đáp án là hai túi token, tính F1 cho từng câu rồi lấy trung bình. Áp vào rubric: các tiêu chí đúng sai kiểm được (có trường bắt buộc trong story, có test case cho mỗi acceptance criterion) là exact match; các tiêu chí về nội dung (story có nêu đúng điều khoản áp dụng) gần với F1 hơn, và đó là chỗ LLM-judge xuất hiện cùng các cạm bẫy đã học ở Tuần 14.

**Precision và recall cho phần retrieval của capstone.** Vì workflow ghép RAG và KG, phần grounding nên đo bằng metric của IR: precision và recall trên tập tài liệu được lấy về, và với kết quả xếp hạng thì tính trên top-k rồi vẽ precision-recall curve (IR-book mục 8.3 và 8.4, trang 155 đến 158). Groundedness ở mục 3 là một dạng precision ở mức claim: trong các claim hệ thống đưa ra, bao nhiêu claim dẫn được về một điều khoản hay một cạnh có provenance. Human-override rate không có tương ứng trực tiếp trong các sách đã đọc; nó là số đo vận hành, rẻ và trung thực, và là thứ bạn nên báo trước tiên với người dùng nghiệp vụ.

**Nhóm metric ngoài accuracy.** Xiao và Zhu (*Foundations of LLMs* mục 5.1.4, trang 221) liệt kê các nhóm đánh giá LLM khi inference: độ chính xác (perplexity, F1), độ bền trước input mơ hồ, đối kháng hay lệch phân phối, tính dùng được (trôi chảy, mạch lạc, đúng trọng tâm, đa dạng) thường cần người chấm, và các metric về đạo đức và công bằng. Rubric capstone nên có ít nhất một tiêu chí thuộc nhóm độ bền: đưa một feature request mơ hồ hoặc thiếu thông tin và kiểm xem workflow có dừng hỏi lại hay bịa. Trong domain có quy định, hành vi dừng hỏi lại đáng điểm cao hơn một câu trả lời trôi chảy nhưng không dẫn nguồn.
