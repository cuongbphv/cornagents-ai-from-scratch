# Lý thuyết Tuần 15 — Capstone: lắp ghép, complexity budget, evaluation

> Đọc trước khi chốt use case và viết [`02_eval_rubric.md`](02_eval_rubric.md). Tuần này không có khái niệm mới — nó là bài kiểm tra xem 14 tuần trước có ghép lại được thành một hệ thống **đo được** không. Nguồn: PDF trong `docs/` + paper LLM-judge đã xác minh 2026-08-11.

---

## 1. Bản đồ lắp ghép — mỗi mảnh về đúng vai

```
Feature request (Finance Banking)
   │
   ▼
Requirements Analyst agent (T13) ──đọc──> RAG (T10–11): grounding trực tiếp vào tài liệu
   │  ghi entities/relations                 │
   ▼                                         ▼
Knowledge Graph (T14): shared memory ──fact-check──> Review agent (T13)
   │                                         │
   ▼                                         ▼
Test-Gen agent (T13)              (tùy chọn) model fine-tuned (T8/T9) cho sub-task hẹp
   │
   ▼
Human gate → artifacts: stories + design note + tests + eval report
```

Nguyên tắc phân vai model (từ README): Claude làm "brain" orchestration; model 7B fine-tuned chỉ nhận sub-task hẹp đã chứng minh được ở Tuần 8–9 (ví dụ một tác vụ phân loại nghiệp vụ) — **không** giao 7B làm brain để "tiết kiệm".

## 2. Complexity budget — khai báo TRƯỚC khi chạy

Từ PDF mục VII + I5 (bảng trong README): max model calls, max sub-agents, max concurrent workers, max wall-clock, max tokens/chi phí, max retries, và **bằng chứng tối thiểu để được finalize**.

- Hết budget → trả **artifact tốt nhất hiện có + danh sách issue chưa xử lý + lý do dừng**. Không giấu partial failure sau một câu trả lời trôi chảy — che partial failure là dạng "bịa" ở mức hệ thống.
- Budget là số cụ thể viết vào config trước khi chạy, không phải cảm giác "chạy lâu quá thì dừng".

## 3. Ba metric bắt buộc — định nghĩa vận hành được

| Metric | Định nghĩa đo được | Cách đo |
|--------|---------------------|---------|
| **Success rate** | % run cho ra artifact đạt rubric | chấm theo [`02_eval_rubric.md`](02_eval_rubric.md), tiêu chí đúng/sai |
| **Human-override rate** | % artifact người duyệt phải sửa/bác tại gate | đếm tại human gate — rẻ và trung thực nhất |
| **Groundedness** | % claim dẫn được về nguồn (điều khoản/tài liệu/edge) | kiểm `source_refs` từng claim; với KG: cite edge có provenance |

Trong domain có quy định, **groundedness quan trọng hơn success rate** (đã chốt trong README): một câu trả lời "thành công" mà không dẫn nguồn là rủi ro, không phải thành tích.

## 4. Eval rubric — viết sao cho chấm được

- Mỗi tiêu chí là câu **đúng/sai kiểm được**, kèm cách kiểm (test, so schema, đối chiếu nguồn) — kỹ năng viết AC của Tuần 13 mục 7 áp lại cho chính hệ thống.
- Chấm bằng LLM-judge thì các bẫy đã xác minh ở Tuần 11 (Zheng et al., arXiv 2306.05685: thiên vị độ dài, vị trí, cùng họ model) áp **trực tiếp** vào rubric của bạn — giữ judge cố định, kiểm tay mẫu nhỏ, đừng tin một chỉ số duy nhất.
- **Metric bị game** (mục nâng cao I5): ratchet chỉ cải thiện thứ nó thấy — success rate tăng có thể đi kèm chi phí tăng hoặc overfit eval set; luôn giữ ràng buộc phụ (budget, groundedness) bên cạnh metric chính.

## 5. Tracing + thước đo cuối

Instrument Langfuse/LangSmith cho MỌI bước (bài Tuần 11 mục 6, giờ áp cho cả graph). Thước đo "hệ thống đáng tin" từ PDF — tự kiểm từng vế với demo của bạn:

> *"Every important output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a bounded execution record."*

Vế nào không chỉ ra được bằng trace/artifact thật → đó là việc phải làm nốt, không phải câu chữ để trích. Câu này đúng thì loops/swarms/graphs compose được; sai thì thêm agent chỉ tăng độ mờ đục.

## 6. Retrospective — nối ngược về Phase 1 (deliverable thật của roadmap)

[`03_retrospective.md`](03_retrospective.md) trả lời: hệ thống hoạt động **vì sao** — nối từng hành vi quan sát được về internals đã tự tay build. Gợi ý các sợi chỉ: temperature thấp giữ groundedness (sampling — T5/T10) ← bạn hiểu softmax T1; RAG thắng fine-tune cho kiến thức quy định (T8) ← bạn hiểu trọng số học phân phối, không lưu facts (T5–6); KG bắt multi-hop mà embedding trượt (T14) ← bạn hiểu cosine đo ngữ nghĩa, không đo cấu trúc (T10); chi phí multi-agent 10–15× (T13) ← bạn hiểu mỗi token đi qua từng layer (T4). Viết bằng lời mình — tiêu chí tự đánh giá của cả repo.

## 7. Tiếng Việt trong capstone

- **Groundedness tiếng Việt = dẫn về đúng số Điều/Khoản/văn bản** — tận dụng provenance đã ép từ Tuần 10 (metadata) và Tuần 14 (edge). Claim nghiệp vụ không có ref là fail rubric, bất kể văn có mượt.
- **Rubric viết bằng tiếng Việt** — người duyệt tại gate là người đọc nghiệp vụ tiếng Việt; rubric họ không đọc được thì human gate chỉ là hình thức. (Tên metric/field giữ tiếng Anh theo quy ước hai lớp — Tuần 12 mục 6.)
- **Eval set = câu hỏi nghiệp vụ tiếng Việt thật** (50–100 câu đã xây từ Tuần 11) + bộ 10 prompt song ngữ (Tuần 9) nếu có model fine-tuned trong luồng — kiểm cả chất lượng lẫn "sức khỏe song ngữ" trong một lần đo.
- [Suy luận] Judge chấm groundedness trên văn bản pháp lý tiếng Việt nên được kiểm tay tỷ lệ cao hơn bình thường (ví dụ 20% mẫu thay vì 10%) — thiên vị judge trên tiếng Việt chưa được đo riêng trong nguồn đã dẫn, thận trọng là rẻ.

## 8. Benchmark & trajectory-level eval cho agent — định vị, không thay thế

Ba metric mục 3 đo hệ thống của bạn trên bài toán của bạn. Hai benchmark công khai dưới đây (abstract kiểm trên arXiv 2026-08-16) hữu ích để **định vị** cách cộng đồng đo agent, không phải để thay eval của repo:

- **SWE-bench (Jimenez et al., arXiv 2310.06770):** 2,294 bài từ GitHub issue + pull request thật của 12 repo Python — cho codebase + issue, agent phải sửa code cho pass test. Đáng nhớ vì cách chấm: **outcome-level thuần túy** (test pass hay không), và vì con số khiêm tốn thời điểm công bố — abstract ghi model tốt nhất lúc đó (Claude 2) giải được "1.96% of the issues". Số này là ảnh chụp 2023; bảng xếp hạng hiện tại phải tra lại, đừng trích số cũ làm số mới.
- **τ-bench (Yao et al., arXiv 2406.12045):** agent + tool + **user mô phỏng** hội thoại nhiều lượt, phải tuân thủ policy nghiệp vụ; chấm bằng cách so **trạng thái database cuối hội thoại** với goal state đã gán nhãn. Điểm đáng học nhất là metric **pass^k**: chạy cùng task k lần, tính xác suất *tất cả* k lần đều thành công — đo **độ ổn định**, thứ mà success rate một lần chạy che mất. Abstract: agent tốt nhất lúc đó thành công <50% task, và pass^8 ở domain retail rơi xuống <25% — cùng một agent, "thi một lần đậu" khác hẳn "thi tám lần đậu cả tám".

**Outcome-level vs trajectory-level:** cả 3 metric mục 3 đều là outcome-level — chấm artifact cuối, không nhìn đường đi. Trajectory/step-wise eval chấm từng bước trong trace: gọi đúng tool không, đúng thứ tự phụ thuộc không, có lặp vô ích đốt budget không, fail ở bước nào. Hai tầng bắt lỗi khác nhau: outcome tốt vẫn có thể che một trajectory lãng phí (ăn vào complexity budget mục 2), outcome hỏng mà không có trajectory thì không biết sửa đâu. Nguyên liệu đã có sẵn — trace Langfuse/LangSmith của mục 5 chính là trajectory; τ-bench cho thấy thêm một lớp nữa: chạy lặp để đo độ ổn định kiểu pass^k.

**Khuyến nghị cho capstone:** giữ 3 metric mục 3 làm chính — chúng đo đúng bài toán Finance Banking tiếng Việt của bạn, điều không benchmark ngoài nào làm được. Benchmark ngoài chỉ dùng để đối chiếu *phương pháp* đo (outcome theo rubric như SWE-bench, so goal-state và pass^k như τ-bench), không nhập task của họ vào eval set của bạn. [Suy luận] Nếu thêm được một phép đo từ mục này thì đáng nhất là chạy lặp 3–5 lần vài task chủ chốt theo tinh thần pass^k — chi phí thấp mà lộ ngay độ ổn định; mức lợi ích cụ thể với hệ của bạn chỉ biết sau khi đo.

## 9. Nguồn

| Nguồn | Vị trí | Dùng cho mục |
|-------|--------|--------------|
| Karpathy-Loop PDF (mục VII–IX, Table VI) | [`../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf`](../docs/Graph-Engineering-Athropic-Karpathy-Loop.pdf) | 2, 5 |
| Zheng et al. 2023 — LLM-as-a-Judge (xác minh 2026-08-11) | https://arxiv.org/abs/2306.05685 | 4 |
| Jimenez et al. 2023 — SWE-bench (abstract kiểm 2026-08-16) | https://arxiv.org/abs/2310.06770 | 8 |
| Yao et al. 2024 — τ-bench (abstract kiểm 2026-08-16) | https://arxiv.org/abs/2406.12045 | 8 |

(Langfuse/LangSmith/promptfoo: link trong README nguồn học.)

## Sau khi đọc xong

1. Chốt use case + vẽ bản đồ lắp ghép của riêng bạn (mục 1) trên giấy.
2. Khai báo complexity budget bằng số, viết vào config.
3. Viết [`02_eval_rubric.md`](02_eval_rubric.md) (tiếng Việt, tiêu chí đúng/sai) trước khi chạy demo.
4. Chạy end-to-end, đo 3 metric, tự kiểm câu "traced to..." từng vế; chạy lặp vài task chủ chốt theo tinh thần pass^k (mục 8) nếu còn budget; viết [`03_retrospective.md`](03_retrospective.md); làm [`quiz.md`](quiz.md).
