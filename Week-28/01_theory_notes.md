# Tuần 28: Học từ lỗi bằng bài học có điều kiện — ghi chú lý thuyết

## 1. Câu hỏi của bài

Lesson “luôn dùng parser” sai ở trường hợp nào trong lab?

## 2. Cơ chế cần hiểu

Reflexion là phản hồi ngôn ngữ và episodic memory, không tự cập nhật weights. Lesson phải có điều kiện áp dụng, phản ví dụ và cách xử lý ngoài scope.

## 3. Phản ví dụ và lỗi cần chủ động thử

Thắng khi retry cùng task có thể chỉ tận dụng đáp án cũ. Cần frozen baseline, transfer tasks và retention dưới budget khai báo.

## 4. Từ nguyên lý sang bài thực hành

Làm R04: so parser rule/bộ nhớ lesson trên trường có grammar; kiểm đổi đơn vị và thiếu header. Thiết kế nhánh Reflexion live riêng; reference offline không gọi LLM.

Đây là bài tập biên tập cho repo dựa trên [Nghiên cứu và CornLoop](../modules/research-contracts.md) · [Bằng chứng và bộ nhớ có quản trị](../modules/evidence-and-memory.md) · [Thuật toán và học có kiểm chứng](../modules/controlled-learning.md) · [Đặc tả R01–R12](../labs/specifications.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 5.4 của tài liệu chương trình

Đây là cách tổ chức memory đề xuất riêng, chưa phải thuật toán mới đã được chứng minh tốt hơn.

```text
Lesson: ưu tiên parser số xác định thay vì để LLM tính chuỗi số tự do.
Áp dụng: trường có grammar và đơn vị nằm trong schema đã hỗ trợ.
Bằng chứng: bộ phát triển có nhãn, kết quả parser và lỗi LLM.
Phản ví dụ: ký hiệu viết tắt mơ hồ, OCR mất dấu, bảng thiếu header.
Không áp dụng: tự đoán đơn vị khi schema không xác định.
Cách xử lý ngoài scope: giữ raw span, báo ambiguous, chuyển người.
Tái kiểm khi: schema, miền dữ liệu hoặc nguồn OCR thay đổi.
```

Điểm mới về thiết kế là **lưu điều kiện khiến bài học không còn đúng**, không chỉ lưu lời khuyên tích cực. Phải ablate để xem thêm trường phản ví dụ có thực sự giúp hay chỉ làm context dài hơn.

### Theo mục 11.6 của tài liệu chương trình

Phải có ít nhất ba góc nhìn: improvement trên họ task mới tương ứng kỹ năng; retention trên họ task cũ; behavior ngoài scope. Đổi tên biến hoặc đảo thứ tự câu không luôn tạo task độc lập, nên cần thiết kế biến thể thay đổi cấu trúc có ý nghĩa.

Chạy ablation tắt lesson, dùng lesson nhiễu và dùng summary cùng độ dài khi phù hợp. Nếu chỉ gain khi câu hỏi gần trùng, report gọi đúng là khả năng tận dụng memory cho các trường hợp gần, không khẳng định học kỹ năng tổng quát.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R04](../labs/r04-conditional-lessons/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
