# Tuần 32: Bảo vệ evaluator và dữ liệu xác nhận — ghi chú lý thuyết

## 1. Câu hỏi của bài

Sửa candidate sau khi có report tốt rồi giữ report cũ có hợp lệ không?

## 2. Cơ chế cần hiểu

Confirmation kiểm một finalist đã cố định. Regression công khai giữ hành vi đã biết nhưng có thể overfit, không thay cohort confirmation mới.

## 3. Phản ví dụ và lỗi cần chủ động thử

Thay artifact sau khi được duyệt làm evidence mismatch. Đáp án kín nằm ngoài repo public/worker; fixture công khai của bài này không phải hidden test thật.

## 4. Từ nguyên lý sang bài thực hành

Làm R08: tính digest, sửa một tham số và kiểm từ chối. Thiết kế process/credential tách biệt và sổ query budget; diễn tập contamination bằng trace chứa nhãn.

Đây là bài tập biên tập cho repo dựa trên [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../modules/runtime-boundaries.md) · [Phép đo và giới hạn thống kê](../modules/statistical-reliability.md) · [Đặc tả R01–R12](../labs/specifications.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 7.6 của tài liệu chương trình

```text
Development/training        -> dùng để xây và tối ưu candidate
Calibration                 -> chọn threshold hoặc policy quyết định
Independent confirmation    -> kiểm candidate đã đóng băng
Retention/regression        -> kiểm năng lực cũ, bảo vệ invariant
Future/shift cohort         -> kiểm chuyển giao theo thời gian/nguồn/schema mới
```

Chia ở cấp nguồn, họ nhiệm vụ, template và thời gian khi phù hợp. Không chia chunk gần trùng của cùng tài liệu sang hai tập. Public benchmark giúp phát triển và tái lập, nhưng có thể đã có trong training data của model; không mặc định là bằng chứng hoàn toàn chưa thấy.

Tập regression công khai có thể bị overfit sau nhiều vòng. Vì vậy nó bảo vệ hành vi đã biết, không thay thế tập confirmation mới. Dataset lineage phải theo dõi cả raw examples, summaries, synthetic variants và traces rò rỉ nhãn.

### Theo mục 7.7 của tài liệu chương trình

Nếu thử 100 prompt rồi chọn prompt có test đẹp nhất, tập đó đã trở thành development data. Giữ answer file kín chưa đủ; pass/fail feedback lặp lại cũng có thể bị tối ưu ngược.

Với tập candidate hữu hạn, được định trước và không chọn thích nghi từ cùng kết quả test, có thể dùng multiple-testing correction phù hợp, chẳng hạn Bonferroni với p-value hợp lệ. **Không dùng Bonferroni như thuốc chữa việc liên tục huấn luyện theo hidden test.**

Đề xuất triển khai ban đầu: development search → một finalist đóng băng → confirmation cohort mới → lưu nguyên cả kết quả fail. Phiên phát hành sau dùng cohort mới hoặc một protocol reusable-holdout/sequential được chuyên gia thống kê xem xét. Có ngân sách số lần hỏi evaluator và sổ phân bổ mức sai số. Không cherry-pick release thắng rồi bỏ các release đã thất bại.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R08](../labs/r08-evaluator-boundary/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
