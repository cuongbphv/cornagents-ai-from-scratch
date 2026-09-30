# Tuần 4: Đạo hàm, xác suất và gradient check — ghi chú lý thuyết

## 1. Câu hỏi của bài

Có nên chọn learning rate bằng điểm test rồi báo điểm test là đánh giá độc lập?

## 2. Cơ chế cần hiểu

Gradient check so đạo hàm tự tính với sai phân số trên một hàm nhỏ. Sampling unit và giả định độc lập phải được nêu khi chuyển từ ví dụ tính toán sang kết luận thống kê.

## 3. Phản ví dụ và lỗi cần chủ động thử

Tăng số retry của cùng câu hỏi không tự tạo thêm task độc lập; sai phân số cũng cần chọn bước và tolerance phù hợp.

## 4. Từ nguyên lý sang bài thực hành

Tự tính gradient logistic regression, kiểm bằng sai phân trung tâm; chia dữ liệu train/validation/test theo vai trò. Giải thích nguồn sai số số học.

Đây là bài tập biên tập cho repo dựa trên [Phép đo và giới hạn thống kê](../../../modules/statistical-reliability.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

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

## 6. Tài liệu tái sử dụng

- [Week-02/README.md](../../../Week-02/README.md)
- [Week-02/02_calculus_probability_lab.py](../../../Week-02/02_calculus_probability_lab.py)
- [Week-03/README.md](../../../Week-03/README.md)

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
