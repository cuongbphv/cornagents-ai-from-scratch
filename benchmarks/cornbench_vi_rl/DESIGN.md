# Thiết kế CornBench-VI Research & Learning

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s12"></a>

## 12. CornBench-VI Research & Learning

### 12.1. Benchmark đo cả điều đã học và điều không được phép quên

Tên đề xuất: **CornBench-VI R&L**. Đây là phiên bản mở rộng của capstone lịch rút gọn, chưa phải dataset được xuất bản.

Miền khởi đầu: tài liệu kỹ thuật tiếng Việt, yêu cầu phần mềm giả lập, hướng dẫn có nhiều phiên bản, bảng số/đơn vị và repo toy. Agent cần nghiên cứu một vấn đề rồi đề xuất cải tiến parser/retrieval/skill có phạm vi. Không dùng benchmark để giao dịch tài chính hoặc ra quyết định pháp lý thật.

**Ba phân hệ:** research-only để chấm nguồn và kết luận; executable tasks để có outcome xác định; learning-over-time để kiểm candidate qua các cohort mới.

### 12.2. Bộ tình huống cốt lõi

| Nhóm | Điều thay đổi có ý nghĩa | Hành vi mong đợi |
|---|---|---|
| Phiên bản | Bản mới không áp dụng hồi tố | Chọn bản theo thời điểm cần trả lời |
| Số và đơn vị | Triệu thành tỷ; dấu bị OCR sai | Tính theo schema hoặc báo mơ hồ, không đoán |
| Nguồn | Nhiều bản đăng lại cùng nguồn | Không đếm thành bằng chứng độc lập |
| Mâu thuẫn | Hai nguồn nói khác trong scope khác | Nêu điều kiện, không bỏ phiếu đơn giản |
| Quyền | User/tenant mất quyền sau khi index | Chặn cả truy cập mới lẫn cache/summary dẫn xuất |
| Bộ nhớ | Một lesson giả được đề nghị | Quarantine, không tự thành fact |
| Tool | Timeout sau khi write thành công | Reconcile/idempotency, không nhân đôi tác động |
| Budget | Worker phân nhánh để chạy tiếp | Dừng ở quota chung |
| Học kỹ năng | Tối ưu prompt khớp template cũ | Kiểm task family mới và retention |
| Evaluator | Candidate sửa tests để xanh | Protected tests và artifact binding phát hiện |
| Nghiên cứu | Thí nghiệm bác bỏ giả thuyết | Báo kết quả âm, không sửa câu chuyện hậu nghiệm |
| Phát hành | Candidate thay đổi sau khi test | Không dùng evidence của bản cũ cho bản mới |

### 12.3. Thiết kế dữ liệu theo giai đoạn

**Pilot:** khoảng 30–50 task phát triển để tìm lỗi evaluator và taxonomy. Đây là kích thước khởi đầu cho kỹ thuật, không đủ mặc định để tuyên bố độ chính xác rất cao.

**Đánh giá độc lập:** cỡ mẫu chọn theo metric, confidence và mức lỗi cần phân biệt; giữ riêng nguồn/template/task family. Nhãn quan trọng được hai người hoặc quy trình xác minh độc lập đối chiếu khi khả thi; ghi bất đồng và cách phân xử.

**Theo thời gian:** chia cohort trước khi chạy vòng học. Agent học trên cohort đã được cho phép; đánh giá bằng cohort chưa dùng để tối ưu. Evaluation run không ghi input/nhãn vào active memory. Mẫu test vẫn phải được đưa vào agent để nó giải, nhưng không cung cấp hidden answer, không cho lưu bền hoặc dùng lại trace làm training data.

Công khai development set, data card và protocol. Với final benchmark, cơ chế giữ kín/rotating test do maintainer quản lý ngoài repo public. Không hứa public repo có “test hoàn toàn kín” nếu toàn bộ file đã commit.

### 12.4. Baseline và ablation

| Mã | Cấu hình | Câu hỏi giúp trả lời |
|---|---|---|
| B0 | Rules/search/code không LLM khi bài toán cho phép | Có cần agent không? |
| B1 | Single-model + fixed retrieval/workflow | Model và nguồn đã đủ chưa? |
| B2 | Bounded single-agent, frozen | Giá trị của agent loop là gì? |
| B3 | B2 + verified memory | Memory giúp gì khi giữ các phần khác tương đương? |
| B4 | B3 + controlled skill/prompt candidates | Cải tiến qua phiên có generalize không? |
| B5 | Multi-agent hoặc offline adapter, tùy chọn | Có lợi thêm sau khi tính chi phí không? |

Giữ cùng phiên bản model/corpus và so cả chất lượng dưới cùng ngân sách lẫn frontier chất lượng–chi phí. Nếu cơ chế cần thêm token, báo đúng phần thêm; không giả vờ mọi cấu hình có cùng tài nguyên. Những cấu hình không thể so trực tiếp phải nêu rõ.

### 12.5. Scorecard công khai, không giấu sau một điểm tổng

Báo task success, accepted error/coverage, evidence errors, permission violations, recovery, retention, new-family gain, canary incidents, human minutes và toàn bộ chi phí search/training/inference/eval.

\[
\text{CostPerVerifiedSuccess}=
\frac{\text{chi phí toàn bộ trial, kể cả fail/retry}}{\text{số task success đã xác minh}}.
\]

Không có success thì để undefined/infinite theo quy ước rõ, không bỏ task khỏi mẫu. Với tự học, cần báo thêm **amortized cost**: tổng chi phí tạo/kiểm candidate phân bổ trên số nhiệm vụ thực sự dùng được sau đó. Giảm 5% token mỗi request có thể không hoàn vốn nếu candidate search quá đắt; bài học phải tính cả hai vế.

### 12.6. Đánh giá con người và hệ thống song song

G1 đo năng lực người học ở một nhiệm vụ biến thể. G2 đo hệ thống. G3 quyết định candidate có được sử dụng. Không dùng score G2 để suy ra học viên hiểu thuật toán, cũng không dùng việc học viên giải thích hay để bỏ qua lỗi runtime.

Với nghiên cứu giáo dục, cần sự đồng ý và quy trình xử lý dữ liệu người học. Pilot ít người chỉ là bằng chứng ban đầu; không khẳng định nhân quả rộng từ một lớp nhỏ không có thiết kế thích hợp.

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
