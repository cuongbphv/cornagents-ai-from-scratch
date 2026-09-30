# Tuần 25: Từ câu hỏi rộng thành phạm vi nghiên cứu — ghi chú lý thuyết

## 1. Câu hỏi của bài

Nguồn chưa trả được toàn văn thì có được nói đã tích hợp từng chi tiết không?

## 2. Cơ chế cần hiểu

Tách câu hỏi, scope, thời gian nguồn, công cụ, ngân sách và điều kiện hoàn thành. Gắn claim_kind: source_fact, computed, inference hoặc hypothesis.

## 3. Phản ví dụ và lỗi cần chủ động thử

Không tự mở rộng sang một đề tài khác để dễ báo hoàn thành; bản đăng lại phải có origin cluster.

## 4. Từ nguyên lý sang bài thực hành

Làm R01: viết contract và ledger cho câu hỏi parser tiếng Việt; fixture có hai bản sao cùng xuất xứ. Phân loại phát biểu và ghi giới hạn từng claim.

Đây là bài tập biên tập cho repo dựa trên [Nghiên cứu và CornLoop](../modules/research-contracts.md) · [Bằng chứng và bộ nhớ có quản trị](../modules/evidence-and-memory.md) · [Đặc tả R01–R12](../labs/specifications.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 3.1 của tài liệu chương trình

```text
Research contract
  -> tách câu hỏi và điều chưa biết
  -> tìm nguồn / quan sát môi trường
  -> lập bảng claim–evidence–counterevidence
  -> đề xuất giả thuyết hoặc lời giải
  -> chạy phép kiểm / thí nghiệm được phép
  -> cập nhật kết luận theo kết quả
  -> báo cáo, hỏi người hoặc dừng theo budget
```

Contract phải xác định câu hỏi, miền, thời gian của dữ liệu, công cụ được phép, nguồn bị loại, ngân sách và tiêu chí hoàn thành. Không cho agent tự mở rộng thành một nhiệm vụ khác chỉ vì tìm được điều thú vị.

**Stop rule khởi đầu:** hết budget; không có quyền; không còn phép kiểm hợp lệ; đã có bằng chứng đủ theo contract; hoặc hai vòng phát triển liên tiếp không tạo thêm bằng chứng liên quan. “Hai vòng” là tham số thí nghiệm, không phải định luật tối ưu. Nếu dừng do thiếu bằng chứng, report phải ghi incomplete/uncertain chứ không chuyển thành successful.

### Theo mục 5.1 của tài liệu chương trình

Một claim quan trọng cần biết **được hỗ trợ bởi đoạn nào**, thuộc phiên bản nào, có mâu thuẫn nào và đã qua phép kiểm nào. Không yêu cầu mọi suy luận thiết kế phải có một nguồn nói y hệt; phải ghi rõ đâu là fact từ nguồn, đâu là suy luận và đâu là giả thuyết mới.

| Trường | Ý nghĩa |
|---|---|
| `claim_id`, `claim_text` | Phát biểu hẹp, có thể kiểm tra |
| `claim_kind` | `source_fact`, `computed`, `inference`, `hypothesis` |
| `source_id`, `span`, `snapshot_digest` | Đúng bản nội dung đã dùng, không chỉ URL có thể đổi |
| `published_at`, `observed_at`, `valid_from/to` | Ngày công bố, ngày đọc và thời gian áp dụng khác nhau |
| `origin_cluster` | Nhóm nguồn cùng xuất xứ để tránh đếm bản đăng lại là bằng chứng độc lập |
| `support_status` | `supported`, `contradicted`, `insufficient`, `not_applicable` |
| `verification_method` | Quy tắc/code, đối chiếu nguồn, reviewer hoặc rubric |
| `access_scope`, `license_status` | Chủ thể được dùng; quyền lưu, trích dẫn và huấn luyện |
| `limitations` | Điều phép kiểm không xác nhận được |

**Phân biệt sáu kiểm tra:** nguồn tồn tại; đoạn nguồn hỗ trợ claim; nguồn có thẩm quyền/phù hợp; thời điểm và phiên bản đúng; số liệu/đơn vị đúng; người dùng có quyền đọc. Không dùng một nhãn “grounded” để che hết sáu khía cạnh.

Hai trang cùng chép một thông cáo không phải hai phép xác nhận độc lập. Citation trỏ đúng một tài liệu sai vẫn không làm phát biểu đúng. Nguồn sơ cấp cũng có thể chỉ nêu kết quả trong điều kiện hẹp.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R01](../labs/r01-research-contract/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
