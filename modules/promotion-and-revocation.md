# Duyệt, thu hồi và rollback

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s14"></a>

## 14. Cổng phát hành, shadow, canary và rollback

### 14.1. Promotion phải dùng đúng vật đã được đánh giá

Evidence package gắn với model revision, prompt/skill/config digest, code commit/build digest, memory snapshot hoặc retrieval corpus version, policy version và evaluator version. Nếu những thành phần ảnh hưởng kết quả thay đổi, cần xác định lại phạm vi evidence; không chỉ giữ nguyên nhãn “chương trình.0”.

Nếu memory được phép tăng trong lúc phục vụ, đó cũng là thay đổi trạng thái. Chỉ nhận các cập nhật đi qua memory gate đã định nghĩa; đánh dấu rằng evidence cho snapshot cũ không tự chứng minh mọi bộ nhớ tương lai. Sau một mức thay đổi hoặc sự kiện rủi ro, cần re-evaluation theo policy.

### 14.2. Hợp đồng chuyển trạng thái

| Trạng thái | Điều kiện đi tiếp | Không được làm |
|---|---|---|
| Candidate | Lineage và development checks đủ | Tự quảng bá là bản đã kiểm định |
| Frozen | Artifact bất biến, protocol xác định | Thay code sau khi test mà giữ report cũ |
| Independently evaluated | Metrics, confidence, regression, scope rõ | Lược bỏ lần chạy fail |
| Approved | Chủ thể có quyền duyệt đúng digest/scope | Agent tự tạo approval cho mình |
| Shadow | So trên workload được cho phép, không side effect thực | Gọi shadow nhưng vẫn ghi dữ liệu nghiệp vụ |
| Bounded canary | Số lượng/tác động nhỏ, giám sát và người chịu trách nhiệm | Dùng production nhạy cảm chỉ vì “cần test” |
| Active scoped | Có expiry/review triggers/rollback | Dùng ngoài scope được phê duyệt |
| Revoked/rolled back | Không được thực thi bằng capability cũ | Tự khởi động lại để vượt thu hồi |

### 14.3. Ngưỡng không chỉ do agent tự quyết

Ví dụ mục tiêu cho một task hẹp: `accepted_error_target = 0.01`, `confidence = 0.95`, `min_coverage = 0.70`. Đây là **số minh họa** để học cách kiểm, chưa phải ngưỡng đủ an toàn cho tài liệu ngân hàng hay hệ thống nghiệp vụ. Người chịu trách nhiệm bài toán phải đặt ngưỡng theo hậu quả lỗi và chi phí người xử lý.

Với permission/exfiltration/critical side effects, một vi phạm xác nhận được phải chặn phát hành và điều tra; không dùng tăng accuracy để bù. Không quan sát vi phạm trong test không đồng nghĩa xác suất vi phạm bằng 0.

### 14.4. Canary không phải nơi thử liều

Trong chương trình, canary nên là workload giả lập hoặc tác vụ thật mức tác động thấp đã được chủ thể có thẩm quyền cho phép. Shadow đọc dữ liệu cũng có rủi ro privacy, nên vẫn cần ACL, retention và budget. Không xem “không ghi” là miễn mọi nghĩa vụ dữ liệu.

Theo dõi tăng abstention, giảm coverage, latency, lỗi nguồn/đơn vị, bất đồng verifier, quyền bị từ chối, cost và số phút người sửa. Một detector drift chỉ là tín hiệu điều tra; không xác nhận mọi task còn trong phân phối huấn luyện.

### 14.5. Rollback và revoke khác nhau

Rollback đổi release pointer về bản trước. Revoke cấm quyền/candidate/source cụ thể được dùng tiếp. Một bản trước có thể cũng bị ảnh hưởng bởi nguồn đã bị thu hồi, nên rollback không tự giải quyết mọi incident.

Side effect bên ngoài có thể không đảo được. Phải ghi rõ cái gì hoàn tác được, cần compensating operation nào và ai xác nhận. Với ambiguous outcome, reconcile trước; không cho agent tự thử nhiều thao tác bù thiếu kiểm soát.

### 14.6. Incident cũng là dữ liệu học, nhưng chưa phải dữ liệu train

Lưu incident đã redact, root-cause hypothesis, bằng chứng và biện pháp cô lập. Sau review mới chuyển thành regression case hoặc lesson candidate. Không đưa nguyên secret/log nhạy cảm vào bộ huấn luyện chỉ vì “học từ lỗi thực tế”.

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
