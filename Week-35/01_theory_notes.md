# Tuần 35: Duyệt đúng bản cải tiến, shadow và rollback — ghi chú lý thuyết

## 1. Câu hỏi của bài

Tại sao rollback và revoke cần hai quyết định riêng?

## 2. Cơ chế cần hiểu

Evidence và approval gắn đúng digest, policy/model/corpus/memory snapshot, scope và expiry. Shadow không tác động quyết định thực; canary cần phạm vi/tác động đã duyệt.

## 3. Phản ví dụ và lỗi cần chủ động thử

Rollback đổi bản đang dùng; revoke cấm dùng quyền/nguồn/candidate. Rollback không tự đảo một side effect bên ngoài.

## 4. Từ nguyên lý sang bài thực hành

Làm R11: promote đúng digest, sửa artifact sau eval, scope thiếu, violation và rollback. Viết release package; thử trong mô phỏng, không deploy production.

Đây là bài tập biên tập cho repo dựa trên [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../modules/runtime-boundaries.md) · [Đặc tả R01–R12](../labs/specifications.md) · [Duyệt, thu hồi và rollback](../modules/promotion-and-revocation.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 14.1 của tài liệu chương trình

Evidence package gắn với model revision, prompt/skill/config digest, code commit/build digest, memory snapshot hoặc retrieval corpus version, policy version và evaluator version. Nếu những thành phần ảnh hưởng kết quả thay đổi, cần xác định lại phạm vi evidence; không chỉ giữ nguyên nhãn “chương trình.0”.

Nếu memory được phép tăng trong lúc phục vụ, đó cũng là thay đổi trạng thái. Chỉ nhận các cập nhật đi qua memory gate đã định nghĩa; đánh dấu rằng evidence cho snapshot cũ không tự chứng minh mọi bộ nhớ tương lai. Sau một mức thay đổi hoặc sự kiện rủi ro, cần re-evaluation theo policy.

### Theo mục 14.2 của tài liệu chương trình

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

### Theo mục 14.5 của tài liệu chương trình

Rollback đổi release pointer về bản trước. Revoke cấm quyền/candidate/source cụ thể được dùng tiếp. Một bản trước có thể cũng bị ảnh hưởng bởi nguồn đã bị thu hồi, nên rollback không tự giải quyết mọi incident.

Side effect bên ngoài có thể không đảo được. Phải ghi rõ cái gì hoàn tác được, cần compensating operation nào và ai xác nhận. Với ambiguous outcome, reconcile trước; không cho agent tự thử nhiều thao tác bù thiếu kiểm soát.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R11](../labs/r11-promotion/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
