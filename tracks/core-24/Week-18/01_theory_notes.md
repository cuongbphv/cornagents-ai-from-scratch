# Tuần 18: Serving, phiên bản và chi phí thực — ghi chú lý thuyết

## 1. Câu hỏi của bài

Fake model replay pass có thể ghi là benchmark LLM thật không?

## 2. Cơ chế cần hiểu

Tách replay fixtures khỏi live-model evaluation. Mỗi kết quả inference cần biết model revision, config, input scope và tài nguyên đã dùng.

## 3. Phản ví dụ và lỗi cần chủ động thử

Replay thành công chỉ kiểm trace giả lập; không chứng minh model thật biết giải nhiệm vụ. Giá và availability cần kiểm lúc dùng.

## 4. Từ nguyên lý sang bài thực hành

Xây adapter interface cho fake/local model, đo latency của đúng workload, ghi toàn bộ retry. Không cần API trả phí để hoàn thành bài offline.

Đây là bài tập biên tập cho repo dựa trên [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md) · [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../../../modules/runtime-boundaries.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 17.4 của tài liệu chương trình

**Offline correctness CI:** schema, state transitions, quota/revoke, replay fixtures, immutable IDs, statistical code, docs/source references. Có thể chạy không API key.

**Live-model evaluation:** explicit budget, người có quyền khởi chạy, model revision, data license, nhiều trial và báo cáo. Không biến job này thành action mặc định chạy tốn phí với mọi pull request không được tin cậy.

CI với fake model chứng minh runner xử lý đúng những trace đã kiểm, không chứng minh model thật biết nghiên cứu. Hai loại kết quả có nhãn khác nhau trên portal.

## 6. Tài liệu tái sử dụng

- [Week-12/README.md](../../../Week-12/README.md)

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
