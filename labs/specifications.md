# Đặc tả R01–R12

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s9"></a>

## 9. Mười hai lab nâng cao có tiêu chí qua môn

Mỗi lab dưới đây là **đặc tả cần triển khai**, chưa phải module đã tồn tại trong repo. Một lab tối thiểu có `lab.yaml`, starter, fixtures, tests, report template và bài AI-off biến thể.

### R01 — Từ câu hỏi rộng thành research contract

**Đầu vào:** một câu hỏi kỹ thuật tiếng Việt có khái niệm mơ hồ và thông tin theo phiên bản. **Làm:** tách câu hỏi, scope, từ khóa, nguồn được phép và tiêu chí hoàn thành; xây claim ledger.

**Gây lỗi:** nguồn thứ cấp mô tả khác tài liệu chính thức; thông tin không có ngày; hai URL cùng một nguồn gốc. **Qua môn:** không coi các bản sao là xác nhận độc lập; claim có giới hạn; phần chưa xác minh không tự điền. **AI-off:** phân loại 10 phát biểu mới thành fact/inference/hypothesis và giải thích.

### R02 — Nghiên cứu lặp có phản chứng và stop rule

**Đầu vào:** tập tài liệu nhỏ có bản cũ/bản mới và một claim sai có vẻ thuyết phục. **Làm:** bounded search/retrieve/verify; ghi query nào tạo thêm bằng chứng.

**Gây lỗi:** query drift sang chủ đề khác, nguồn đứng đầu nhưng lỗi thời, không tìm được đáp án. **Qua môn:** dừng theo contract; không đổi câu hỏi để dễ báo thành công; report nêu nguồn mâu thuẫn và trạng thái chưa biết. **AI-off:** chọn phép kiểm tiếp theo từ ba lựa chọn và nêu chi phí/cái chưa biết.

### R03 — Memory có nguồn, thời hạn và thu hồi

**Đầu vào:** fact, episode và lesson với hai tenant giả lập. **Làm:** lifecycle, retrieval lọc quyền, valid time/observed time, lineage của summary.

**Gây lỗi:** đưa chỉ thị vào tài liệu, đổi ACL sau khi index, thu hồi nguồn sau khi đã summary. **Qua môn:** không rò dữ liệu/citation qua tenant; dữ liệu stale không được dùng như hiện hành; cache dẫn xuất bị đánh dấu. **AI-off:** giải thích vì sao xóa vector không đồng nghĩa xóa ảnh hưởng khỏi trained model.

### R04 — Học từ lỗi, không học lại câu trả lời test

**Đầu vào:** task phát triển có phản hồi từ unit test và một nhóm task chuyển giao. **Làm:** baseline frozen, episodic Reflexion và lesson có điều kiện.

**Gây lỗi:** lesson quá tổng quát; lời giải cũ đúng chỉ nhờ một giá trị đặc biệt. **Qua môn:** so cùng budget; báo task mới và retention; thất bại phải giữ trong log. **AI-off:** sửa một lesson để có phạm vi và phản ví dụ. Không có gain vẫn có thể đạt môn nếu phương pháp đúng.

### R05 — Tối ưu prompt/skill trong vùng được phép

**Đầu vào:** pipeline extraction/retrieval nhỏ, tập development. **Làm:** random candidate baseline rồi thử GEPA/DSPy hoặc implementation tìm kiếm nhỏ; ghi candidate lineage.

**Gây lỗi:** prompt candidate đòi đọc test answer; thêm quyền tool; sửa grader. **Qua môn:** thay đổi vượt vùng bị chặn; finalist được đóng băng; không chọn bằng kết quả hidden test. **AI-off:** tìm leakage trong một experiment log cho sẵn.

### R06 — Chọn thí nghiệm có giá trị thông tin

**Đầu vào:** không gian cấu hình nhỏ, evaluator có chi phí đo được. **Làm:** pre-register metric, ablation, random search; BO trên objective toy ở nhánh nâng cao.

**Gây lỗi:** đổi cùng lúc model, corpus và budget; dừng khi nhìn thấy một kết quả đẹp. **Qua môn:** so dưới cùng tổng chi phí; báo tất cả lượt chạy; chỉ ra biến gây khác biệt. **AI-off:** thiết kế thí nghiệm bác bỏ giả thuyết “graph luôn tốt hơn retrieval lặp”.

### R07 — Risk–coverage và bằng chứng thống kê

**Đầu vào:** score, quyết định và nhãn đã kiểm tra của các task độc lập. **Làm:** calibration, chọn ngưỡng trên tập riêng, CP bound trên candidate frozen.

**Gây lỗi:** không có mẫu; 100 mẫu đều đúng; nhiều retry của cùng task; confidence tự khai. **Qua môn:** không tuyên bố sai về 99% reliability; báo accepted risk lẫn coverage; trường hợp thiếu bằng chứng không pass. **AI-off:** giải thích bảng 100/299 mẫu và giả định bị phá khi task trùng.

### R08 — Bảo vệ evaluator

**Đầu vào:** một candidate repo và một evaluation service chỉ nhận digest. **Làm:** immutable bundle, hidden test không mount vào agent, ghi số lần query.

**Gây lỗi:** candidate sửa public tests, đọc biến môi trường grader, thay artifact sau khi được duyệt. **Qua môn:** protected grader không đổi; nội dung deploy mismatch bị chặn; không để evaluation secret trong workspace. **AI-off:** vẽ biên quyền và chỉ ra một đường rò rỉ chưa được bảo vệ.

### R09 — Offline learning có retention

**Đầu vào:** dữ liệu có lineage, một nhiệm vụ hẹp và khả năng cũ cần giữ. **Làm:** SFT/LoRA nhỏ; DPO toy khi có preference rõ; giữ base để so sánh.

**Gây lỗi:** synthetic data thiếu provenance, adapter làm đẹp format nhưng sai số, data split chứa bản gần trùng. **Qua môn:** report base/candidate/new/old, dùng data card; không promote chỉ vì training loss giảm. **AI-off:** phân biệt SFT, DPO, GRPO và RLVR bằng một ví dụ.

### R10 — Chạy dài nhưng không vô hạn

**Đầu vào:** research task sinh tối đa một số worker hữu hạn và có side effect giả lập. **Làm:** quota tổng, timeout, cancellation, resume và reconciliation.

**Gây lỗi:** crash sau write trước ack; event gửi lại; quyền bị thu hồi giữa hai bước; worker tạo thêm worker. **Qua môn:** không vượt quota bằng phân nhánh; dừng toàn cây worker; unknown outcome chuyển người. **AI-off:** debug một thứ tự sự kiện chưa thấy.

### R11 — Đúng candidate mới được promote

**Đầu vào:** một candidate qua development eval và evidence package. **Làm:** independent confirmation, approval bound digest, shadow, release pointer atomic, rollback.

**Gây lỗi:** source version đổi; evidence hết hạn; regression tăng; build mới khác bản được test. **Qua môn:** từng trường hợp đều có quyết định rõ; không lặng lẽ giữ quyền khi evidence không còn áp dụng. **AI-off:** chỉ ra vì sao rollback weights không tự hoàn tác một hành động bên ngoài.

### R12 — Capstone học qua nhiều vòng

**Đầu vào:** CornBench-VI Research & Learning development corpus và evaluator riêng. **Làm:** tối thiểu một baseline frozen, một learning mechanism và nhiều cohort chuyển giao.

**Gây lỗi:** memory poisoning, contradiction, metric gaming, drift, dữ liệu hết quyền, hết budget. **Qua môn:** có report cả kết quả âm, gain/retention/coverage/cost và giới hạn; bảo vệ độc lập một kết luận. Candidate không đủ bằng chứng phải ở quarantine, không hạ ngưỡng để “đủ tốt nghiệp”.

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
