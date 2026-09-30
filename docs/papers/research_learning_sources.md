# Nguồn nghiên cứu và học có kiểm chứng

**Cách đọc:** `[Sxx]` trong nội dung liên kết tới nguồn sơ cấp tương ứng. Nguồn dùng để xác định cơ chế, kết quả trong phạm vi tác giả hoặc trạng thái công bố; các khuyến nghị kiến trúc/curriculum trong tài liệu là tổng hợp đề xuất, không phải phát biểu rằng nguồn đã xác nhận toàn bộ thiết kế CornAgents.

| ID | Nguồn | Dùng cho / giới hạn |
|---|---|---|
| S01 | [OpenAI — Introducing deep research][S01] | Cơ chế nghiên cứu nhiều bước và công cụ theo công bố; không suy ra nội bộ đầy đủ hoặc tự cập nhật weights mỗi phiên |
| S02 | [Anthropic — How we built our multi-agent research system][S02] | Mô hình điều phối/worker và bài học kỹ thuật; không mặc định topology tối ưu cho mọi task |
| S03 | [Anthropic — Demystifying evals for AI agents][S03] | Task/trial, transcript/outcome, nhiều loại grader; không lấy model judge làm oracle tuyệt đối |
| S04 | [Shinn et al. — Reflexion][S04] | Linguistic feedback và episodic memory không đổi weights |
| S05 | [Yao et al. — ReAct][S05] | Kết hợp reasoning/action; không có bảo đảm correctness phổ quát |
| S06 | [Asai et al. — Self-RAG][S06] | Retrieval/reflection được học; phân biệt với prompt tự nhận xét đơn giản |
| S07 | [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning][S07] | Candidate prompt search theo công trình; không universalize kết quả so sánh |
| S08 | [DSPy — repository chính thức][S08] | Công cụ xây/tối ưu pipeline; API cần pin khi triển khai |
| S09 | [The AI Scientist][S09] | Tham khảo tự động hóa các bước nghiên cứu; không là bằng chứng mọi nghiên cứu sinh ra đều đúng/mới |
| S10 | [Google DeepMind — AlphaEvolve][S10] | Kết hợp proposal và automated evaluator trong miền thuật toán xác định |
| S11 | [Darwin Gödel Machine][S11] | Hướng tự sửa coding agent; không coi empirical eval là chứng minh an toàn tổng quát |
| S12 | [Guo et al. — On Calibration of Modern Neural Networks][S12] | Nền calibration; không dùng verbal confidence thay xác suất đã hiệu chỉnh |
| S13 | [Angelopoulos et al. — Learn then Test][S13] | Risk control qua multiple testing; cần đúng sampling/protocol |
| S14 | [Angelopoulos et al. — Conformal Risk Control][S14] | Kiểm soát loss trong điều kiện phương pháp; không đồng nhất expected risk với mọi bảo đảm xác suất cao |
| S15 | [SciPy — BinomTestResult.proportion_ci][S15] | Exact/Clopper–Pearson; example phân biệt một phía/hai phía |
| S16 | [Rafailov et al. — Direct Preference Optimization][S16] | Preference optimization, không bắt buộc reward model riêng |
| S17 | [DeepSeekMath][S17] | GRPO; phân biệt optimizer và nguồn reward |
| S18 | [Shumailov et al. — The Curse of Recursion][S18] | Rủi ro recursive generated-data training; không kết luận mọi synthetic data gây hại |
| S19 | [Frazier — A Tutorial on Bayesian Optimization][S19] | Surrogate/acquisition cho phép đo đắt; áp dụng cần so baseline |
| S20 | [Anthropic — How we contain Claude][S20] | Containment và biên hệ thống bên ngoài model |
| S21 | [MCP — Security Best Practices][S21] | Biên authorization/security khi tích hợp công cụ; docs có thể thay phiên bản |
| S22 | [LangGraph — Persistence][S22] | Checkpoint/persistence; không tự tạo exactly-once cho mọi side effect |
| S23 | [Anthropic — nghiên cứu multi-agent systems][S23] | Vấn đề phối hợp và phân chia công việc; nhiều agent không tự tạo độc lập |
| S24 | [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning in Language Models][S24] | Tổng hợp các reasoning paths; không coi đồng thuận là sự thật |
| S25 | [OpenAI — DevDay 2026 recap][S25] | Mốc 29/09/2026 được ghi trong catalog kế thừa, chưa xác minh lại ở đây; không yêu cầu preview cho core |
| S26 | [GEPA — repository chính thức][S26] | Implementation tham khảo; chưa chạy trong bản thiết kế này |
| S27 | [OpenAI Help — Deep research in ChatGPT][S27] | Hành vi/scope sản phẩm theo tài liệu công khai, không coi sản phẩm là autonomous R&D hoàn chỉnh |
| S28 | [cornagents-ai-from-scratch — repository][S28] | Repo của chương trình; không phải bằng chứng hiệu năng hoặc audit toàn bộ code |

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

---

**Đích của CornAgents.AI:** một người học hiểu được vì sao AI hoạt động, một agent làm việc có bằng chứng, và một vòng cải tiến mà cả chất lượng lẫn quyền kiểm soát đều không được tự tuyên bố là đã đạt.


Các mục trên là catalog kế thừa từ tài liệu thiết kế được cung cấp, không phải xác nhận đã truy cập hoặc đọc toàn văn từng nguồn trong phiên biên tập này. Giữ ngày/version trong URL để tra cứu; kiểm lại nguồn khi triển khai.
