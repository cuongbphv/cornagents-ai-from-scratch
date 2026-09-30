# Tuần 15: Hybrid retrieval và reranking — ghi chú lý thuyết

## 1. Câu hỏi của bài

Candidate retrieval tốt hơn nhưng corpus cũng lớn hơn: đã xác nhận lợi ích riêng của fusion chưa?

## 2. Cơ chế cần hiểu

BM25 và dense retrieval cung cấp các tín hiệu khác nhau; fusion/reranking cần được so với baseline trên cùng nguồn và task.

## 3. Phản ví dụ và lỗi cần chủ động thử

Không mặc định hybrid hoặc graph thắng. Nếu thêm tài liệu hoặc token budget thì phải khai báo phần thay đổi đó.

## 4. Từ nguyên lý sang bài thực hành

Chọn corpus công khai được phép dùng hoặc giả lập; so retrieval baseline với fusion dưới budget rõ. Kiểm recall và lỗi nguồn ở từng query.

Đây là bài tập biên tập cho repo dựa trên [Thuật toán và học có kiểm chứng](../../../modules/controlled-learning.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 6.1 của tài liệu chương trình

Đề xuất thứ tự: **phép tính/quy tắc có thể xác định → retrieval có bằng chứng → workflow cố định → agent đơn → tìm kiếm nhiều candidate → multi-agent khi có lý do đo được**.

Đây không phải bảng xếp hạng chất lượng phổ quát. Nó là cách bắt đầu với baseline dễ kiểm tra. Một câu hỏi mở không thể ép thành regex; một phép cộng tiền theo schema không cần một hội đồng agent bỏ phiếu.

### Theo mục 6.5 của tài liệu chương trình

Nếu memory-enabled agent thắng, cần biết nó thắng vì học lesson, vì thêm tài liệu, vì dùng nhiều token hay vì test đã lọt vào memory. Mỗi thí nghiệm học cần một bản **frozen** cùng model, data access và budget; khác biệt chủ yếu là cơ chế học đang nghiên cứu.

## 6. Tài liệu tái sử dụng

- [Week-13/README.md](../../../Week-13/README.md)
- [Week-14/README.md](../../../Week-14/README.md)

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
