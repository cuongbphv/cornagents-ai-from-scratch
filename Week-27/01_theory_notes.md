# Tuần 27: Bộ nhớ có nguồn, thời hạn và quyền đọc — ghi chú lý thuyết

## 1. Câu hỏi của bài

Xóa entry khỏi memory có đồng nghĩa đã unlearn dữ liệu khỏi model train trước đó không?

## 2. Cơ chế cần hiểu

Tách fact, episode và procedural lesson. Worker đề nghị; review mới chuyển từ quarantine sang active có phạm vi. Đọc phải kiểm trạng thái, tenant và thời hạn.

## 3. Phản ví dụ và lỗi cần chủ động thử

Thu hồi nguồn phải lần theo summary/cache/lesson dẫn xuất. Xóa vector không tự xóa ảnh hưởng đã học vào weights.

## 4. Từ nguyên lý sang bài thực hành

Làm R03: hai tenant giả lập, nguồn bị revoke và summary hai tầng; kiểm không trả text/citation ngoài quyền. Vẽ lineage và ghi phần code toy chưa mô phỏng.

Đây là bài tập biên tập cho repo dựa trên [Kiến trúc runtime, quyền và hợp đồng dữ liệu](../modules/runtime-boundaries.md) · [Bằng chứng và bộ nhớ có quản trị](../modules/evidence-and-memory.md) · [Đặc tả R01–R12](../labs/specifications.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 5.2 của tài liệu chương trình

**Semantic memory:** fact hoặc quy tắc đã có nguồn, scope và thời hạn.

**Episodic memory:** điều đã xảy ra trong một lần chạy. Episode mô tả trải nghiệm, không tự khẳng định quy luật chung.

**Procedural memory:** skill/lesson về cách giải, gồm điều kiện áp dụng, cách kiểm tra và chống chỉ định.

Một ghi chép “thử A, fail; thử B, pass” chỉ là episode. Muốn thành lesson “B tốt hơn A khi X” phải có thí nghiệm phù hợp và phản ví dụ, đồng thời ghi rõ chưa đủ bằng chứng cho các trường hợp khác.

### Theo mục 5.3 của tài liệu chương trình

```text
PROPOSED -> QUARANTINED -> ELIGIBLE_FOR_REVIEW -> ACTIVE_SCOPED
                   |               |                  |
                   v               v                  v
                REJECTED        REJECTED     STALE / REVOKED / SUPERSEDED
```

Worker chỉ tạo `PROPOSED`. Quarantine kiểm source/ACL, nội dung chỉ thị lạ, phạm vi, duplicate, mâu thuẫn và provenance. Không có nguồn cho fact thì không tự promote thành semantic fact. Một lesson có thể bắt đầu là “giả thuyết hữu ích chưa xác nhận”, nhưng retrieval phải hiển thị nhãn đó.

`ACTIVE_SCOPED` không có nghĩa đúng mãi. Retrieval recheck quyền, hiệu lực và trạng thái hiện tại tại thời điểm dùng. Khi một nguồn bị thu hồi hoặc sửa, dependency graph đánh dấu các summary, vector entry, lesson và cache dẫn xuất cần xử lý. Quyền truy cập cần được lọc trước khi trả nội dung cho model, không chỉ che citation sau khi sinh câu trả lời.

Xóa khỏi memory không đồng nghĩa đã loại ảnh hưởng khỏi weights của model từng được train bằng dữ liệu đó. Với training, cần lineage và quyết định xử lý riêng theo dataset/model version; không hứa “xóa một hàng là unlearn hoàn toàn”.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R03](../labs/r03-governed-memory/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
