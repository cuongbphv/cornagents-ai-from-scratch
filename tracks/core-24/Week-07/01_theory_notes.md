# Tuần 7: Tokenizer, BPE và Unicode tiếng Việt — ghi chú lý thuyết

## 1. Câu hỏi của bài

Round-trip pass có chứng minh tokenizer phù hợp mọi tài liệu không?

## 2. Cơ chế cần hiểu

Tokenizer là một hợp đồng chuyển đổi input. Round-trip, normalization và cách xử lý bytes/Unicode cần được kiểm riêng trên văn bản tiếng Việt.

## 3. Phản ví dụ và lỗi cần chủ động thử

Hai chuỗi nhìn giống nhau có thể khác biểu diễn Unicode; chuẩn hóa tùy tiện có thể mất thông tin nguồn cần đối chiếu.

## 4. Từ nguyên lý sang bài thực hành

Viết bộ fixture gồm tiếng Việt có dấu, dấu kết hợp, ký tự lạ và khoảng trắng. Kiểm encode/decode; ghi chính sách normalization và giữ raw input.

Đây là bài tập biên tập cho repo dựa trên [Thuật toán và học có kiểm chứng](../../../modules/controlled-learning.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 6.2 của tài liệu chương trình

| Nhóm | Cần nắm | Tự làm đến đâu? | Phép kiểm quan trọng |
|---|---|---|---|
| Nền model | Autograd, stable softmax, cross-entropy, AdamW, BPE, causal attention, RoPE, KV cache | Implementation nhỏ, so reference | Gradient check, mask, cache parity |
| Retrieval | BM25, dense similarity, RRF, reranker, retrieval lặp | Tự viết baseline/fusion; dùng embedding/reranker có sẵn | Recall@k, nDCG, coverage, đúng ACL/phiên bản |
| Agent loop | ReAct, state machine, graph/DAG, stop conditions | Tự viết bounded loop trước framework | Tool semantics, outcome, budget, trường hợp không đủ thông tin |
| Học qua trải nghiệm | Reflexion, lesson retrieval, counterexample memory | Buffer nhỏ và lifecycle có kiểm soát | Task chuyển giao, bài cũ, bài ngoài scope |
| Tối ưu prompt/skill | Random search baseline, GEPA/DSPy theo phiên bản đã pin | Candidate search trong development data | Same-budget comparison; không dùng test để tối ưu |
| Độ bất định | Calibration, Brier, reliability diagram, selective prediction | Tự tính metric, thử ngưỡng | Risk–coverage và calibration ngoài training |
| Kiểm soát rủi ro | Binomial bound, Learn then Test, conformal risk control | CP trước; LTT/CRC ở nhánh học thuật | Giả định, multiple testing, drift, kích thước mẫu |
| Chọn thí nghiệm | Ablation, random search, Bayesian optimization, value of information | Objective toy đo được, budget cố định | Sample efficiency và chi phí evaluator |
| Học model | SFT, LoRA, DPO; RLVR/GRPO tùy chọn | Toy/adapter nhỏ, không train model lớn bắt buộc | Verifier độc lập, dữ liệu có lineage, retention |
| Hệ thống | Idempotency, reconciliation, versioning, atomic promotion | Chạy fault injection | Crash sau write, token hết hạn, event duplicate |

ReAct kết hợp suy luận và tương tác; Self-RAG có cơ chế học reflection token và retrieval; self-consistency tổng hợp nhiều lời giải. Chúng là những phương pháp cụ thể với các điều kiện thí nghiệm, không phải nhãn để gắn vào mọi prompt dài. [S05] [S06] [S24]

## 6. Tài liệu tái sử dụng

- [Week-06/README.md](../../../Week-06/README.md)

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
