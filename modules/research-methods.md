# Giả thuyết và phương pháp nghiên cứu

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s15"></a>

## 15. Các hướng nghiên cứu tạo đóng góp riêng

Những mục dưới đây là **giả thuyết được đề xuất**, chưa có kết quả và chưa xác nhận tính mới qua một systematic literature review đầy đủ. Mục tiêu là tạo đóng góp đo được, không chỉ đổi tên các phương pháp đã có.

### H1 — Bộ nhớ có phản ví dụ giúp giảm áp dụng sai bài học

**Giả thuyết:** lưu lesson cùng điều kiện và trường hợp làm nó sai giúp giảm lỗi chuyển giao hơn việc chỉ lưu một câu lesson tích cực, dưới cùng budget context.

**So sánh:** episodic memory; summary cùng độ dài; lesson có điều kiện; lesson có điều kiện và phản ví dụ.

**Đo:** sai do áp dụng ngoài scope, success trên task mới, retention, abstention, token và thời gian chọn memory. Kiểm cả tình huống phản ví dụ bị gán sai để tránh tin memory một cách mù quáng.

**Bác bỏ hoặc thu hẹp:** không hơn baseline ở cùng token budget; giảm lỗi chỉ bằng từ chối gần hết; hoặc phần lợi ích biến mất khi kiểm task family mới.

### H2 — Chọn học phần còn thiếu hiệu quả hơn tự sửa toàn bộ pipeline

**Giả thuyết:** phân loại failure thành retrieval, reasoning, computation, permission và runtime rồi chỉ cho sửa tầng liên quan tạo improvement tốt hơn tìm kiếm thay đổi rộng, tính cả chi phí kiểm định.

**So sánh:** candidate search unrestricted trong vùng sandbox; search theo failure taxonomy; baseline không học. Phải giữ nguyên biên an toàn cho mọi cấu hình — “unrestricted” chỉ nói phạm vi kỹ thuật được thí nghiệm, không bỏ policy.

**Đo:** verified gain trên cohort mới, số candidate, tổng cost, regression và thời gian reviewer. Taxonomy có thể sai; thêm ablation nhãn lỗi bị nhiễu.

**Đóng góp tiềm năng:** dataset nguyên nhân lỗi, protocol chẩn đoán và reproduction package; chưa cần phát minh một model foundation mới.

### H3 — Thu hồi bài học theo phụ thuộc nguồn tốt hơn memory TTL cố định

**Giả thuyết:** khi nguồn/version/quyền thay đổi, invalidation theo lineage giảm sử dụng tri thức lỗi thời hơn chỉ xóa sau một TTL, trong corpus có cập nhật.

**So sánh:** không expiry; TTL cố định; lineage-triggered revoke; kết hợp cả hai. Đo false invalidation, chi phí update và trường hợp graph lineage bị thiếu cạnh.

**Giới hạn:** không coi lineage graph đúng hoàn toàn. Cần chấm riêng chất lượng lineage; lợi ích trên corpus nhỏ ít thay đổi có thể không đáng chi phí.

### H4 — Cải tiến được kiểm chứng tốt hơn chỉ thêm reviewer agent

**Giả thuyết:** external outcome checks + structured evidence + abstention đem lại trade-off risk–coverage/cost tốt hơn chỉ thêm một LLM reviewer cùng nhiệm vụ.

**So sánh:** frozen single-agent; thêm LLM reviewer; external checks; kết hợp cả hai. Không mặc định reviewer vô ích; đo khi nhiệm vụ cần phán đoán ngôn ngữ.

**Đo:** nguồn sai nhưng nhiều agent đồng ý, unsupported claim, final outcome, false rejection và human burden. Việc tìm thấy miền reviewer hữu ích là kết quả có giá trị, không phải thất bại của hướng nghiên cứu.

### H5 — Curriculum do agent đề nghị nhưng người/harness giới hạn

**Giả thuyết:** agent chọn task phát triển tiếp theo dựa trên failure coverage và uncertainty đã đo sẽ cải thiện sample efficiency hơn curriculum ngẫu nhiên, mà không bỏ quên nhóm kỹ năng cũ.

**Cơ chế đề xuất:** chọn từ pool được phép; ưu tiên nhóm còn thiếu bằng chứng; giữ quota tối thiểu cho retention và nhóm hiếm; không cho chọn task xác nhận cuối. Không dùng confidence tự khai làm tín hiệu duy nhất.

**Bác bỏ:** agent chỉ chọn task dễ để tăng score; nhóm hiếm giảm chất lượng; hoặc chi phí chọn task lớn hơn lợi ích. Có thể dùng active learning/BO như công cụ, nhưng claim mới phải nằm ở thiết kế và kết quả đo trên bài toán CornAgents.

### Nên bắt đầu hướng nào?

Đề xuất làm **H1 trên tác vụ số/đơn vị hoặc retrieval tiếng Việt** trước. Nó đủ hẹp để có phản ví dụ và phép kiểm rõ, không đòi train model lớn; đồng thời kết nối trực tiếp memory, self-learning và reliability. Sau khi evaluator ổn định mới mở H3 hoặc H4. Đây là ưu tiên thiết kế cho repo, chưa phải kết luận H1 chắc chắn có hiệu quả nhất.

---

<a id="s16"></a>

## 16. Nâng chiều sâu học thuật mà không làm quá tải người mới

### 16.1. Ba tầng độ sâu

| Tầng | Kỳ vọng | Ví dụ |
|---|---|---|
| Hiểu để dùng đúng | Nêu cơ chế, điều kiện và giới hạn | Vì sao reflection không tự thành verification? |
| Tự triển khai phần nhỏ | Có test đối chiếu và phản ví dụ | CP bound, RRF, low-rank update, idempotent state machine |
| Nghiên cứu và tái lập | Hypothesis, baseline, ablation, uncertainty, report | So memory có phản ví dụ với baseline cùng budget |

Không bắt tất cả học viên chứng minh mọi định lý trước khi viết agent. Nhưng người viết claim thống kê phải hiểu các giả định họ đang dùng; người xây tool ghi dữ liệu phải hiểu retry/transaction chứ không chỉ biết prompt.

### 16.2. Các mảng học thuật nên bồi dưỡng

**Xác suất và thống kê:** conditioning, sampling, confidence intervals, calibration, hypothesis testing, multiple comparisons, sequential/adaptive evaluation và paired analysis. Trọng tâm là tránh kết luận sai từ experiment, không chỉ làm bài tính.

**Tối ưu hóa và quyết định:** gradient methods ở phần model; constrained optimization cho candidate selection; Bayesian optimization cho phép thử đắt; value of information khi chọn phép đo. Cần nêu objective đo được và giới hạn surrogate.

**Phương pháp khoa học:** operational definition, falsifiability, ablation, reproducibility, negative results và distinction correlation/causation. Viết điều gì sẽ khiến mình bỏ giả thuyết trước khi chạy.

**Kỹ thuật phần mềm và distributed systems:** type contracts, invariants, idempotency, checkpoint, consistency, crash recovery, capability boundaries. Những chủ đề này trực tiếp nâng độ tin cậy của agent, không phải phần phụ sau khi “AI đã thông minh”.

**Formal methods ở nhánh tự chọn:** mô hình hóa state machine của approval/revoke/retry, kiểm invariant trên mô hình hữu hạn. Phân biệt tính chất đã chứng minh trên mô hình với correctness của implementation và sự thật ngữ nghĩa của output LLM. Một model checker không tự xác nhận nội dung nghiên cứu đúng.

**Continual learning:** positive/negative transfer, retention, replay data được cấp quyền, dataset shift và learned representation. Không ép mọi bài phải cập nhật weights; procedural memory cũng cần đánh giá chuyển giao.

### 16.3. Một paper phải tạo một vật chứng

```text
Paper và phiên bản đã đọc:
Câu hỏi paper giải quyết:
Giả định và miền thử nghiệm:
Phương pháp thực sự thay đổi gì:
Điều paper không chứng minh:
Phần sẽ tái lập ở quy mô nhỏ:
Baseline và tổng budget:
Kết quả, kể cả âm:
Sai khác so với cấu hình paper:
Quyết định áp dụng / không áp dụng / còn thiếu bằng chứng:
```

Không ghi “đã triển khai Self-RAG” nếu chỉ thêm câu “hãy tự kiểm tra” vào prompt; không ghi “đã tái lập GEPA” nếu chỉ chọn prompt tốt nhất bằng tay. Có thể gọi trung thực là baseline lấy cảm hứng và nêu phần chưa làm.

### 16.4. Đọc có chọn lọc

Một nhóm đọc nền: ReAct, Reflexion, calibration, Learn then Test. Nhóm thực nghiệm tự cải tiến: GEPA và một trong AlphaEvolve/Darwin Gödel Machine. Nhóm an toàn hệ thống: evals, containment, MCP security và persistence.

Chỉ chọn một bài advanced để tái lập sâu ở cuối extension. Không biến 12 tuần thành yêu cầu tái tạo tất cả công trình hiện đại.

---

[S01]: https://openai.com/index/introducing-deep-research/
[S02]: https://www.anthropic.com/engineering/multi-agent-research-system
[S03]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
[S04]: https://arxiv.org/abs/2303.11366v4
[S05]: https://arxiv.org/abs/2210.03629
[S06]: https://arxiv.org/abs/2310.11511
[S07]: https://arxiv.org/abs/2507.19457
[S08]: https://github.com/stanfordnlp/dspy
[S09]: https://arxiv.org/abs/2408.06292
[S10]: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
[S11]: https://arxiv.org/abs/2505.22954
[S12]: https://arxiv.org/abs/1706.04599
[S13]: https://arxiv.org/abs/2110.01052
[S14]: https://arxiv.org/abs/2208.02814
[S15]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html
[S16]: https://arxiv.org/abs/2305.18290
[S17]: https://arxiv.org/abs/2402.03300
[S18]: https://arxiv.org/abs/2305.17493
[S19]: https://arxiv.org/abs/1807.02811
[S20]: https://www.anthropic.com/engineering/how-we-contain-claude
[S21]: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
[S22]: https://docs.langchain.com/oss/python/langgraph/persistence
[S23]: https://www.anthropic.com/research/multiagent-systems
[S24]: https://arxiv.org/abs/2203.11171
[S25]: https://openai.com/index/devday-2026-recap/
[S26]: https://github.com/gepa-ai/gepa
[S27]: https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt
[S28]: https://github.com/cuongbphv/cornagents-ai-from-scratch
