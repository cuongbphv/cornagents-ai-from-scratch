# Tuần 20: Deny tests, sandbox và thu hồi quyền — ghi chú lý thuyết

## 1. Câu hỏi của bài

Tại sao thư mục evaluator riêng vẫn chưa đủ bảo vệ đáp án?

## 2. Cơ chế cần hiểu

Biên quyền cần nằm ngoài worker. Sau resume phải kiểm lại quyền hiện tại và expiry, không sống lại capability cũ từ checkpoint.

## 3. Phản ví dụ và lỗi cần chủ động thử

Thư mục control_plane riêng hoặc một reviewer agent chưa chứng minh cách ly OS. Lab offline chỉ mô phỏng quyết định policy.

## 4. Từ nguyên lý sang bài thực hành

Dùng fixtures hai tenant, quyền hết hạn và thu hồi giữa hai bước; viết deny tests cho read/write. Vẽ biên process/credential cần có khi triển khai thật.

Đây là bài tập biên tập cho repo dựa trên [Nghiên cứu và CornLoop](../modules/research-contracts.md) · [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../modules/runtime-boundaries.md) · [Phân bổ chương trình 36 tuần](../docs/curriculum/schedule.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 4.2 của tài liệu chương trình

| Tài nguyên | Research worker | Learning worker | Evaluator | Release controller |
|---|---|---|---|---|
| Raw source snapshot | Đọc qua gateway; đề nghị ingest | Đọc phần được phép | Đọc theo scope | Không cần sửa |
| Candidate workspace | Ghi | Ghi trong vùng cho phép | Chạy snapshot chỉ đọc | Đọc digest |
| Active memory/skill | Đọc theo ACL | Chỉ đề nghị version mới | Đọc bản đánh giá | Promote theo policy |
| Protected test/answer | Không đọc | Không đọc | Đọc trong môi trường riêng | Chỉ đọc kết quả tổng hợp |
| Policy, quota, secrets | Không sửa | Không sửa | Không tự cấp quyền | Quản lý theo phân quyền riêng |
| Kết quả eval đã ký | Không sửa | Không sửa | Tạo kết quả gắn digest | Kiểm chữ ký/digest |

Ở lab local, có thể dùng tiến trình và credential khác nhau. Đó là mô phỏng học tập; nếu một tài khoản quản trị có thể sửa cả hai vùng thì chưa có cách ly mạnh cho production. `CODEOWNERS` hoặc branch protection hữu ích cho review nhưng không thay thế runtime isolation.

### Theo mục 4.4 của tài liệu chương trình

Quota bao gồm tổng token, tool calls, wall time, CPU/GPU, dung lượng file, network egress và số worker con. Worker con phải tiêu từ cùng budget của nhiệm vụ mẹ, không được tạo budget mới. Bộ đếm dùng thao tác atomic/transaction phù hợp khi chạy đồng thời.

Hủy nhiệm vụ phải lan tới toàn bộ worker, subprocess, scheduled retry và capability liên quan. Kill switch không nằm trong process mà agent có thể sửa. Không xem model từ chối gọi tool là bằng chứng duy nhất rằng side effect đã dừng.

## 6. Tài liệu tái sử dụng

- [Week-15/README.md](../Week-15/README.md)
- [r03-governed-memory/README.md](../labs/r03-governed-memory/README.md)

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
