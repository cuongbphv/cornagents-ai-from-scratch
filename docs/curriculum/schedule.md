# Phân bổ chương trình 36 tuần

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s8"></a>

## 8. Lộ trình 36 tuần và cách vào học

### 8.1. Điểm vào và nhịp học

| Người học | Lộ trình đề xuất |
|---|---|
| Chưa lập trình | Chuẩn bị 4–6 tuần: Python, Git, terminal, JSON/HTTP, SQL và test; sau đó vào core |
| Đã lập trình, mới AI | Core 24 tuần + extension nghiên cứu/học có kiểm soát 12 tuần |
| Có nền ML và systems | Dùng bài đánh giá đầu vào để rút gọn; giữ fast-track 18 tuần của repo và thêm module còn thiếu |
| Muốn đi sâu nghiên cứu | Sau core/extension, chọn một nhánh chuyên sâu thay vì học đồng thời mọi thuật toán |

Dự kiến 10–12 giờ/tuần là giả định thiết kế để phân bổ việc học, không bảo đảm ai cũng hoàn thành trong thời lượng đó. 36 tuần không đồng nghĩa làm chủ toàn bộ machine learning, formal methods và AI research.

Một nhịp học gợi ý: đọc nguyên lý; tự viết phần nhỏ; chạy thí nghiệm; chủ động gây lỗi; giải thích kết quả; làm bài biến thể. Giữ **Dự đoán → Tự triển khai → Gây lỗi → Đo → Sửa → Chuyển giao** từ lịch rút gọn.

### 8.2. Core 24 tuần: làm nền đủ chắc để tự học không thành tự làm sai

| Tuần | Nội dung | Artifact / cửa qua môn | Kết nối với chương trình |
|---|---|---|---|
| 1–2 | Môi trường, dữ liệu, baseline, eval đầu tiên | Task contract nhỏ, manifest, baseline không LLM | Tập thói quen định nghĩa đúng trước khi tối ưu |
| 3–4 | Đại số tuyến tính, đạo hàm, xác suất qua code | Logistic regression NumPy, gradient check | Biết phân biệt lỗi model và lỗi phép đo |
| 5–6 | Autograd, MLP, PyTorch, training loop | So gradient reference, học overfit có chủ ý | Không coi loss đẹp là chứng minh generalization |
| 7–8 | Tokenizer, BPE, causal attention | Unicode, round-trip, mask/label-shift tests | Tự chẩn đoán input và leakage |
| 9–10 | Tiny Transformer, RoPE, normalization, KV cache | Cache parity, profiler, resource report | Biết hạn chế tài nguyên và tính đúng |
| 11–12 | Data curation, dedup, training dynamics | Split theo nguồn, ablation, data card | Chuẩn bị chống contamination khi tự học |
| 13–14 | SFT/LoRA, preference learning | Adapter/tiny experiment; DPO loss toy | Phân biệt L2 với L3 |
| 15–16 | Hybrid retrieval, reranking, context | Retrieval report và evidence span | Không học fact thiếu provenance |
| 17–18 | Document AI, số/đơn vị, serving | Trích dữ liệu có vùng nguồn; latency/cost profile | Tách extraction đúng khỏi báo cáo trôi chảy |
| 19–20 | Bounded agent, typed tools, MCP | Tool contract, deny tests, sandbox | Cơ sở quyền và policy ngoài model |
| 21–22 | Durable workflow, events, SDLC | Crash/retry/revoke tests, protected evaluator | Không nhân đôi side effect khi chạy dài |
| 23–24 | Capstone lịch rút gọn và mini research | Baselines, held-out results, AI-off defense | Đủ điều kiện bắt đầu learning loop |

Các module này tái sử dụng nội dung tương ứng của lịch rút gọn và repo; không yêu cầu dời toàn bộ thư mục cũ. Graph, multi-agent và GPU optimization chuyên sâu vẫn là lựa chọn theo bài toán.

### 8.3. Extension 12 tuần: nghiên cứu và cải tiến có kiểm soát

| Tuần | Module | Sản phẩm chính | Cổng năng lực |
|---|---|---|---|
| 25 | Research contracts & evidence | Báo cáo phân rã câu hỏi, source/claim ledger | Phân biệt fact, inference và hypothesis |
| 26 | Iterative research & falsification | Research loop có stop rule và nguồn mâu thuẫn | Không kết luận vượt bằng chứng |
| 27 | Governed memory | Memory lifecycle, temporal/ACL/revoke tests | Không học dữ liệu không được phép |
| 28 | Learning from experience | Reflexion baseline và lesson có phản ví dụ | Có transfer test, không chỉ retry task cũ |
| 29 | Prompt/skill optimization | Một candidate search dùng dữ liệu development | Không đụng protected test |
| 30 | Experiment selection | Ablation + random search + BO toy tùy chọn | So lợi ích dưới cùng budget |
| 31 | Calibration & risk–coverage | Selective policy và cận thống kê | Giải thích đúng giả định và mẫu |
| 32 | Evaluator integrity | Eval service cách ly, contamination drill | Agent không sửa tiêu chuẩn để thắng |
| 33 | Offline parameter learning | Tiny/adapter experiment hoặc CPU toy tương đương cơ chế | Dataset lineage, retention, rollback |
| 34 | Long-running bounded research | Checkpoint, quota chung, cancellation, permissions | Lỗi runtime không vượt biên |
| 35 | Controlled promotion | Evidence package, shadow và rollback drill | Đúng artifact được đánh giá mới được dùng |
| 36 | CornBench-VI R&L | Nhiều chu kỳ học, benchmark + báo cáo tái lập | G1/G2/G3 được chấm riêng |

Tuần 33 không bắt mọi máy chạy QLoRA 7B/8B. Người không có GPU có thể chứng minh cơ chế low-rank trên model nhỏ, dùng replay để test lifecycle; phải ghi rõ chưa đo chất lượng adapter LLM thực. Không dùng kết quả giả lập thay kết quả live-model.

### 8.4. Cách chấm để không khuyến khích “AI làm hộ hết”

AI-off yêu cầu tự viết/sửa một lõi nhỏ và giải thích một phản ví dụ chưa gặp. AI-on cho phép công cụ coding nhưng yêu cầu traces, tests, cấu hình và giải trình nguồn dữ liệu. Bài nghiên cứu được chấm theo sự đúng đắn của phương pháp và minh bạch kết quả, không chấm cao chỉ vì claim tăng accuracy.

Bản build chạy được chưa đủ. Người học phải trả lời: “Kết quả nào sẽ khiến tôi không phát hành candidate này?” và “Điều gì tôi vẫn chưa biết sau thí nghiệm?”.

---

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
