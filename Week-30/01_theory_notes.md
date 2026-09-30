# Tuần 30: Thiết kế và chọn thí nghiệm — ghi chú lý thuyết

## 1. Câu hỏi của bài

Có được dừng ngay khi thấy một kết quả đẹp rồi bỏ run thất bại không?

## 2. Cơ chế cần hiểu

Đặt objective, metric, tổng budget và stopping rule trước. Random search/ablation là baseline; BO chỉ thử khi evaluator đắt và objective thích hợp.

## 3. Phản ví dụ và lỗi cần chủ động thử

Gain ước đoán bằng lời của LLM chưa phải acquisition score đã hiệu chỉnh. Tính cả run fail và chi phí chọn thí nghiệm.

## 4. Từ nguyên lý sang bài thực hành

Làm R06: giữ model/corpus, thay một cấu hình; runner dừng trước khi vượt budget. Lưu run fail, tiêu chí chọn và tổng chi phí.

Đây là bài tập biên tập cho repo dựa trên [Thuật toán và học có kiểm chứng](../modules/controlled-learning.md) · [Đặc tả R01–R12](../labs/specifications.md) · [Giả thuyết và phương pháp nghiên cứu](../modules/research-methods.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 6.4 của tài liệu chương trình

Với câu hỏi “thử cấu hình retrieval nào tiếp theo?”, bắt đầu random/grid search nhỏ. Khi mỗi phép đo đắt và không gian thích hợp, học Bayesian optimization qua surrogate và acquisition function như expected improvement. Phải kiểm nghiệm rằng chi phí xây surrogate có đáng so với baseline. [S19]

Với value of information, ý tưởng là chọn phép đo dự kiến làm quyết định tốt hơn sau khi trừ chi phí, **trong tập hành động được phép**. Không lấy câu “tôi kỳ vọng tăng độ chính xác 20%” của LLM làm số liệu acquisition mà chưa kiểm định. Những ước lượng lợi ích phải được backtest hoặc được ghi rõ là heuristic.

Tree search/MCTS chỉ nên thành lab nâng cao khi state, action và phép đánh giá có nghĩa rõ. Không mặc định mở cây suy luận thật rộng cho mọi câu hỏi tài liệu. Multi-agent chỉ vào thí nghiệm khi có phân chia công việc hữu ích; shared context, thông tin sai lan truyền và chi phí phối hợp đều cần đo. [S23]

### Theo mục 16.3 của tài liệu chương trình

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

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R06](../labs/r06-experiment-design/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
