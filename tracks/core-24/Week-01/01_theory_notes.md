# Tuần 1: Môi trường học và phạm vi nhiệm vụ — ghi chú lý thuyết

## 1. Câu hỏi của bài

Agent tìm thấy nguồn hữu ích ngoài allowlist. Có được tự đọc để hoàn thành nhanh hơn không?

## 2. Cơ chế cần hiểu

Bắt đầu bằng một nhiệm vụ nhỏ có đầu vào, đầu ra và điều kiện hoàn thành rõ. Task contract ghi công cụ được phép, nguồn bị loại và ngân sách; agent không tự đổi nhiệm vụ.

## 3. Phản ví dụ và lỗi cần chủ động thử

Một notebook chạy được chưa cho biết ai có quyền dùng dữ liệu hoặc cách chạy lại trên máy khác.

## 4. Từ nguyên lý sang bài thực hành

Tạo môi trường Python, ghi phiên bản thực tế, thiết kế task đọc một fixture JSON; lưu manifest có nguồn, cấu hình và lệnh chạy. Dùng dữ liệu giả lập, không chép secrets.

Đây là bài tập biên tập cho repo dựa trên [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md) · [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../../../modules/runtime-boundaries.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

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

### Theo mục 10.1 của tài liệu chương trình

| Lớp | Đề xuất | Giới hạn và nguyên tắc |
|---|---|---|
| Code và model | Python, NumPy, PyTorch | Tách notebook minh họa khỏi runtime |
| Chất lượng code | pytest/unittest, Ruff, type checking, dependency lock | Không xem lint xanh là đủ đúng nghiệp vụ |
| Hợp đồng | Pydantic hoặc JSON Schema | Check semantics/quyền ngoài schema |
| Orchestration | Python state machine trước; LangGraph khi cần persistence | Pin version; tránh học nhiều framework cùng lúc [S22] |
| Storage | SQLite cho local lab; PostgreSQL khi có nhiều worker/tenant | Giao dịch và credential riêng cho control/eval |
| Retrieval | BM25 + dense + fusion; vector store khi cần | Không lưu mọi context vào vector DB mặc định |
| Learning candidates | Script rõ ràng; DSPy/GEPA cho nhánh prompt optimization | Chỉ development data, bounded search [S08] [S26] |
| Model adapter | Một runtime local phù hợp máy; API cloud tùy chọn | Giao diện trung lập nhà cung cấp; live eval tách replay |
| Experiments | JSONL/Parquet + manifest trước; registry khi đủ nhu cầu | Mọi run có source/data/model/code version |
| Security | OS/container sandbox theo threat model, egress broker, scoped credentials | Docker đơn lẻ không được mô tả như chứng minh cách ly [S20] |
| Protocol | MCP cho công cụ cần tích hợp | MCP không thay authorization hoặc xác nhận nghiệp vụ [S21] |
| Release | Immutable artifact, evaluation record, scoped approval | Không cần xây platform tự triển khai khổng lồ ở giai đoạn đầu |

Các tên công nghệ là lựa chọn kiến trúc, không phải khẳng định chúng là “tốt nhất hiện nay”. Khóa phiên bản ở thời điểm viết lab; dùng API adapter để tránh toàn bộ giáo trình phụ thuộc một model hoặc preview API.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

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
