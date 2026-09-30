# Tuần 19: Hợp đồng công cụ và agent có giới hạn — ghi chú lý thuyết

## 1. Câu hỏi của bài

JSON đúng schema nhưng action ngoài scope có được chạy không?

## 2. Cơ chế cần hiểu

Tool schema kiểm hình dạng; executor phải kiểm thêm semantics, quyền hiện tại và ngân sách. Model đề nghị hành động nhưng không tự cấp capability.

## 3. Phản ví dụ và lỗi cần chủ động thử

Prompt dặn không ghi file không phải biên thực thi. Dữ liệu ngoài có thể chứa chỉ thị trái nhiệm vụ.

## 4. Từ nguyên lý sang bài thực hành

Dùng R01/R10 reference offline; tạo schema cho read_fixture, từ chối tool không có trong contract. Viết starter executor chỉ hỗ trợ công cụ giả lập.

Đây là bài tập biên tập cho repo dựa trên [Nghiên cứu và CornLoop](../modules/research-contracts.md) · [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../modules/runtime-boundaries.md) · [Phân bổ chương trình 36 tuần](../docs/curriculum/schedule.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 4.3 của tài liệu chương trình

Mỗi đề nghị hành động chứa `task_id`, `actor`, loại thao tác, tài nguyên, tham số chuẩn hóa, phiên bản input, `idempotency_key` và hạn sử dụng. Approval phải gắn với digest nội dung đó. Đổi một tham số quan trọng hoặc source version làm thay đổi ý nghĩa tác vụ thì phải kiểm lại.

Không dùng một phê duyệt chung “đồng ý agent tự làm” cho mọi hành động về sau. Sau restart/resume vẫn kiểm quyền hiện hành; quyền đã thu hồi không sống lại chỉ vì checkpoint cũ còn token.

### Theo mục 10.4 của tài liệu chương trình

| Interface đề xuất | Hợp đồng quan trọng |
|---|---|
| `ResearchPlanner` | Sinh plan trong task contract; không tự cấp capability |
| `EvidenceRetriever` | Trả source spans đã lọc quyền, version và provenance |
| `ToolExecutor` | Validate schema + quyền hiện tại + budget + side effect policy |
| `ExperimentRunner` | Chạy immutable code/data snapshot trong sandbox |
| `OutcomeVerifier` | Đọc trạng thái thực; phân biệt pass/fail/unknown |
| `LearningProposer` | Tạo candidate có lineage; không ghi active registry |
| `IndependentEvaluator` | Chỉ nhận snapshot; không cho candidate sửa protected criteria |
| `PromotionController` | Kiểm evidence, digest, approval, scope và rollback trước khi dùng |

Không cần mỗi interface thành một microservice ngay. Tách module và credentials đủ cho học; tách process/service khi cần biên an toàn thật. Một `LLMJudge` chỉ là thành phần trong evaluation, không được đồng nhất với toàn bộ `IndependentEvaluator`.

## 6. Tài liệu tái sử dụng

- [Week-15/README.md](../Week-15/README.md)
- [r01-research-contract/README.md](../labs/r01-research-contract/README.md)

## 7. Phạm vi kết luận

Test offline xác nhận trường hợp đã thử, không xác nhận chất lượng model thật, runtime isolation, tính đại diện của dataset hoặc đủ điều kiện production. Không dùng số liệu của paper hay ví dụ trong nguồn để điền score của CornAgents.AI.

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
