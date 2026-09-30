# Tuần 17: Document AI và số/đơn vị tiếng Việt — ghi chú lý thuyết

## 1. Câu hỏi của bài

Bảng chỉ ghi 12, không còn header đơn vị: có được đoán là triệu đồng không?

## 2. Cơ chế cần hiểu

Trích xuất cần giữ raw span và vị trí/đơn vị của nguồn. Parser chỉ tính khi input nằm trong grammar và schema đã hỗ trợ.

## 3. Phản ví dụ và lỗi cần chủ động thử

Thiếu header đơn vị hoặc OCR mơ hồ thì không tự suy hệ số. Kết quả AMBIGUOUS khác với số 0.

## 4. Từ nguyên lý sang bài thực hành

Tự viết parser số nguyên có đơn vị tường minh, thử thiếu đơn vị và dấu OCR. Xuất raw span, normalized value và lý do từ chối; so với fixture.

Đây là bài tập biên tập cho repo dựa trên [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md) · [Thiết kế CornBench-VI Research & Learning](../../../benchmarks/cornbench_vi_rl/DESIGN.md) · [Document AI: đọc số và đơn vị tiếng Việt](../../../modules/document-ai.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 13 của tài liệu chương trình

### Nhiệm vụ: cải thiện đọc số và đơn vị trong tài liệu yêu cầu tiếng Việt

Đây là **tình huống giả lập để thiết kế lab**, không phải kết quả đã chạy agent.

**Bước 1 — contract.** Người giao việc định nghĩa các trường được hỗ trợ, dữ liệu giả lập, grammar số, khoảng thời gian và các thao tác bị cấm. Agent chỉ được tạo parser candidate và báo cáo.

**Bước 2 — baseline.** Chạy cách extraction hiện có trên development set. Lưu raw span, field, unit, normalized value và kết quả đúng/sai theo nhãn đã định nghĩa. Không lấy lời giải thích tự tin của model làm nhãn.

**Bước 3 — nghiên cứu.** Agent đối chiếu schema và tìm nhóm lỗi: nhầm đơn vị, thiếu header, ký hiệu OCR mơ hồ hoặc dùng version cũ. Mỗi nhận xét phải trỏ tới observation cụ thể.

**Bước 4 — giả thuyết.** “Trong nhóm trường có grammar xác định, parser số có kiểm tra đơn vị sẽ giảm lỗi so với sinh trực tiếp; ngoài grammar chuyển người.” Đây là giả thuyết có thể bác bỏ, không phải kết luận mặc định.

**Bước 5 — thí nghiệm.** Tạo parser ở candidate workspace, chạy unit/property tests và so baseline. Không thay nhãn/expected output để parser xanh. Đo cả coverage vì parser có thể từ chối nhiều trường hơn.

**Bước 6 — phản chứng.** Thử thiếu đơn vị, đổi đơn vị, text OCR hỏng, chuỗi gần khớp nhưng ngoài grammar. Nếu không đủ thông tin, parser trả `AMBIGUOUS`, kèm span chứ không tự đoán.

**Bước 7 — đề nghị học.** Agent tạo một lesson có điều kiện, patch và evidence package. Tất cả ở quarantine; active skill chưa đổi.

**Bước 8 — kiểm độc lập.** Evaluator chạy snapshot trên cohort chưa dùng để tối ưu, đo accepted risk/coverage và retention. Nếu dữ liệu không đủ cho ngưỡng thống kê, trạng thái là cần thêm bằng chứng, dù chưa thấy lỗi.

**Bước 9 — quyết định.** Candidate có thể bị reject do coverage thấp, không cải thiện hoặc lỗi nghiêm trọng. Nếu được duyệt, chạy shadow rồi phạm vi giới hạn; không tự được phép parse mọi tài liệu thực tế.

**Bước 10 — học tiếp.** Một thay đổi schema mới làm lesson hết phạm vi. System hạ trạng thái, chuyển task sang review và đề xuất một nghiên cứu mới. Không âm thầm dùng evidence cũ để giữ quyền.

### Thành phẩm của một vòng

```text
research_report.md          # vấn đề, nguồn, giả thuyết, kết luận và giới hạn
claims.jsonl                # claim–evidence–counterevidence
experiment_manifest.json    # version/config/data/code và budget
candidate_patch.diff        # phần sửa trong allowlist
candidate_lesson.yaml       # chưa active
evaluation_summary.json     # độc lập, gắn đúng digest
release_decision.md         # promote/reject/insufficient và lý do
```

Vòng nghiên cứu tốt có thể kết thúc bằng “không phát hành”. Hệ thống đã tạo tri thức về điều kiện thất bại mà không làm hỏng bản đang phục vụ.

## 6. Tài liệu tái sử dụng

- [Week-13/README.md](../../../Week-13/README.md)

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
