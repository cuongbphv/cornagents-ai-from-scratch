# Tuần 24: Bảo vệ năng lực và điều kiện vào nghiên cứu — ghi chú lý thuyết

## 1. Câu hỏi của bài

Thí nghiệm không có gain có thể đạt môn nghiên cứu không?

## 2. Cơ chế cần hiểu

G1 kiểm người học tự giải thích/sửa phần lõi; G2 kiểm hệ thống; G3 xét candidate. Ba cửa tách nhau, không lấy artifact AI sinh để suy ra học viên hiểu.

## 3. Phản ví dụ và lỗi cần chủ động thử

Tốt nghiệp bài lab không phải chứng nhận production. Đề xuất phải ghi điều chưa biết và điều kiện khiến mình không phát hành.

## 4. Từ nguyên lý sang bài thực hành

Tự sửa một lỗi biến thể không dùng AI; trình bày report của tuần 23; đóng băng candidate và lập quyết định reject/insufficient/promote với scope giả lập.

Đây là bài tập biên tập cho repo dựa trên [Nghiên cứu và CornLoop](../modules/research-contracts.md) · [Phân bổ chương trình 36 tuần](../docs/curriculum/schedule.md) · [Tốt nghiệp và bảo trì chương trình](../modules/graduation-and-maintenance.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 3.4 của tài liệu chương trình

| Cửa | Chủ thể được đánh giá | Câu hỏi |
|---|---|---|
| G1 — AI-off | Người học | Có tự giải thích, triển khai phần lõi và sửa lỗi mới không? |
| G2 — AI-on | Hệ thống | Có hoàn thành tác vụ đúng, có bằng chứng và đúng phạm vi không? |
| G3 — change gate | Bản cải tiến | Có đủ bằng chứng để thay bản đang dùng, không phá khả năng cũ và không nới quyền không? |

Ví dụ, model mới viết báo cáo hay hơn nhưng gọi thêm nguồn ngoài allowlist: G2/G3 không đạt. Sinh artifact tốt nhờ AI nhưng không giải thích được leakage: G1 không đạt. Candidate không thắng baseline nhưng thí nghiệm được thiết kế và báo cáo đúng vẫn có thể đạt môn nghiên cứu; nó chỉ không được promote.

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

- [Week-18/README.md](../Week-18/README.md)
- [r11-promotion/README.md](../labs/r11-promotion/README.md)

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
