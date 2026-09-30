# Tuần 36: CornBench-VI: học qua nhiều vòng và báo cáo tái lập — ghi chú lý thuyết

## 1. Câu hỏi của bài

Candidate không cải thiện nhưng thí nghiệm đúng có được hạ ngưỡng để tốt nghiệp không?

## 2. Cơ chế cần hiểu

Capstone gồm frozen baseline, một cơ chế học và nhiều cohort mới. Chấm G1/G2/G3 riêng; báo gain, retention, risk–coverage và tổng chi phí kể cả kết quả âm.

## 3. Phản ví dụ và lỗi cần chủ động thử

Fixture vài task dùng tìm lỗi kỹ thuật, không phải benchmark đã xuất bản hay bằng chứng accuracy của agent. H1 chưa được xác nhận tốt hơn.

## 4. Từ nguyên lý sang bài thực hành

Làm R12 và H1: đăng ký protocol, chia development/confirmation/retention theo family; chạy baseline/lesson ablation. Reference parser replay chỉ kiểm fixture; nộp report giới hạn và lệnh tái lập.

Đây là bài tập biên tập cho repo dựa trên [Đặc tả R01–R12](../labs/specifications.md) · [Thiết kế CornBench-VI Research & Learning](../benchmarks/cornbench_vi_rl/DESIGN.md) · [Giả thuyết và phương pháp nghiên cứu](../modules/research-methods.md) · [Tốt nghiệp và bảo trì chương trình](../modules/graduation-and-maintenance.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 12.3 của tài liệu chương trình

**Pilot:** khoảng 30–50 task phát triển để tìm lỗi evaluator và taxonomy. Đây là kích thước khởi đầu cho kỹ thuật, không đủ mặc định để tuyên bố độ chính xác rất cao.

**Đánh giá độc lập:** cỡ mẫu chọn theo metric, confidence và mức lỗi cần phân biệt; giữ riêng nguồn/template/task family. Nhãn quan trọng được hai người hoặc quy trình xác minh độc lập đối chiếu khi khả thi; ghi bất đồng và cách phân xử.

**Theo thời gian:** chia cohort trước khi chạy vòng học. Agent học trên cohort đã được cho phép; đánh giá bằng cohort chưa dùng để tối ưu. Evaluation run không ghi input/nhãn vào active memory. Mẫu test vẫn phải được đưa vào agent để nó giải, nhưng không cung cấp hidden answer, không cho lưu bền hoặc dùng lại trace làm training data.

Công khai development set, data card và protocol. Với final benchmark, cơ chế giữ kín/rotating test do maintainer quản lý ngoài repo public. Không hứa public repo có “test hoàn toàn kín” nếu toàn bộ file đã commit.

### Theo mục 12.4 của tài liệu chương trình

| Mã | Cấu hình | Câu hỏi giúp trả lời |
|---|---|---|
| B0 | Rules/search/code không LLM khi bài toán cho phép | Có cần agent không? |
| B1 | Single-model + fixed retrieval/workflow | Model và nguồn đã đủ chưa? |
| B2 | Bounded single-agent, frozen | Giá trị của agent loop là gì? |
| B3 | B2 + verified memory | Memory giúp gì khi giữ các phần khác tương đương? |
| B4 | B3 + controlled skill/prompt candidates | Cải tiến qua phiên có generalize không? |
| B5 | Multi-agent hoặc offline adapter, tùy chọn | Có lợi thêm sau khi tính chi phí không? |

Giữ cùng phiên bản model/corpus và so cả chất lượng dưới cùng ngân sách lẫn frontier chất lượng–chi phí. Nếu cơ chế cần thêm token, báo đúng phần thêm; không giả vờ mọi cấu hình có cùng tài nguyên. Những cấu hình không thể so trực tiếp phải nêu rõ.

### Theo mục 12.5 của tài liệu chương trình

Báo task success, accepted error/coverage, evidence errors, permission violations, recovery, retention, new-family gain, canary incidents, human minutes và toàn bộ chi phí search/training/inference/eval.

\[
\text{CostPerVerifiedSuccess}=
\frac{\text{chi phí toàn bộ trial, kể cả fail/retry}}{\text{số task success đã xác minh}}.
\]

Không có success thì để undefined/infinite theo quy ước rõ, không bỏ task khỏi mẫu. Với tự học, cần báo thêm **amortized cost**: tổng chi phí tạo/kiểm candidate phân bổ trên số nhiệm vụ thực sự dùng được sau đó. Giảm 5% token mỗi request có thể không hoàn vốn nếu candidate search quá đắt; bài học phải tính cả hai vế.

### Theo mục 18.1 của tài liệu chương trình

Một hệ thống học tập hoàn thành chương trình khi có thể chứng minh các nhóm năng lực sau trong phạm vi benchmark/lab đã công bố:

| Năng lực | Bằng chứng nghiệm thu |
|---|---|
| Hiểu cơ chế | AI-off: mô hình nhỏ, thuật toán, thống kê, runtime |
| Nghiên cứu có nguồn | Claim ledger, phản chứng, báo cáo giới hạn |
| Học có phạm vi | Candidate lineage; task chuyển giao; retention |
| Không tự cấp quyền | Negative tests cho policy/quota/evaluator/release |
| Không tự chấm để thắng | Evaluator boundary, test isolation, digest binding |
| Không giấu thất bại | Log toàn bộ trial/candidate, negative-result report |
| Biết thiếu bằng chứng | Abstention, insufficient-evidence state, risk–coverage |
| Khôi phục được | Crash/retry/revoke/rollback drill trong sandbox |
| Tái lập được | Manifest dữ liệu/model/code/config và instructions |

Đạt các bài trên không phải giấy chứng nhận hệ thống an toàn cho ngân hàng. Production cần threat model, review, kiểm thử và quy trình tổ chức riêng theo trường hợp sử dụng.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R12](../labs/r12-cornbench-learning/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
