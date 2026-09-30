# Tốt nghiệp và bảo trì chương trình

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s18"></a>

## 18. Tiêu chí nghiệm thu chương trình và cách cập nhật công nghệ

### 18.1. Tốt nghiệp chương trình không đồng nghĩa chứng nhận production

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

### 18.2. Giữ lõi bền vững, cập nhật bề mặt công nghệ

Công bố DevDay chính thức ngày **29/09/2026** cho thấy hướng agent làm công việc kéo dài và thêm bề mặt tích hợp. Một số phần như Decisions API được công bố ở limited preview, MCP Events theo proposed specification; không nên biến khả năng preview thành điều kiện tốt nghiệp. [S25]

chương trình chuyển các thay đổi sản phẩm thành năng lực nền: state bền vững, events, quyền, chi phí và verification. Không đóng curriculum vào một model thương mại cụ thể hay giả định giá/availability không đổi.

Mỗi impact note mới nên có nguồn/ngày, trạng thái release, capability liên quan, lab hiện tại đã bao phủ chưa, risk mới, chi phí chuyển đổi và quyết định `adopt/watch/skip`. Người duyệt thay đổi core dựa trên bằng chứng, không chỉ vì một công bố gây chú ý.

### 18.3. Definition of Done cho bản phát hành tài liệu

Bản Markdown này cung cấp kiến trúc, lộ trình và đặc tả lab; nó **không hoàn thành** backlog triển khai nêu trên. Khi repo chính thức phát hành chương trình, cần bổ sung commit SHA, dependency lock, lab implementation status, kết quả chạy thực, data cards và known limitations.

Chỉ có ví dụ thống kê ở Phụ lục A đã được thực thi trong phiên soạn tài liệu này. Các schema/pseudocode/trees còn lại được đánh dấu là đề xuất và không được hiểu thành tính năng có sẵn.

### 18.4. Nguyên tắc chốt

**Agent được tự nghiên cứu một phương án tốt hơn. Agent không được tự quyết rằng bằng chứng của mình đã đủ, tự hạ chuẩn khi thất bại hoặc tự nới phạm vi quyền để hoàn thành mục tiêu.**

Một hệ thống thật sự đáng tin không chỉ tạo được câu trả lời và cải tiến. Nó biết giới hạn của bằng chứng, giữ được khả năng dừng, chấp nhận kết quả âm và để người chịu trách nhiệm kiểm tra điều đã xảy ra.

---

<a id="appendix-a"></a>

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
