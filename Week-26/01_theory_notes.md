# Tuần 26: Nghiên cứu lặp, phản chứng và điều kiện dừng — ghi chú lý thuyết

## 1. Câu hỏi của bài

Tại sao nguồn hỗ trợ và nguồn phản bác cần giữ cùng báo cáo?

## 2. Cơ chế cần hiểu

Mỗi query phải nhằm kiểm câu hỏi trong contract. Vòng nghiên cứu ghi support/counterevidence và dừng khi hết budget hoặc không còn phép kiểm hợp lệ.

## 3. Phản ví dụ và lỗi cần chủ động thử

Hết budget nhưng chưa đủ evidence là incomplete/uncertain, không đổi nhãn thành successful.

## 4. Từ nguyên lý sang bài thực hành

Làm R02: xử lý nguồn cũ/mới/mâu thuẫn; ghi query nào thêm evidence. Thử hết budget, query drift và nguồn không trả đáp án.

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

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R02](../labs/r02-bounded-research/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
