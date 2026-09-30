# Tuần 33: Học tham số offline và giữ năng lực cũ — ghi chú lý thuyết

## 1. Câu hỏi của bài

DPO preference chọn văn phong tự tin có đảm bảo factuality không?

## 2. Cơ chế cần hiểu

SFT/LoRA/DPO cần dữ liệu được phép dùng, nhãn có tiêu chí và lineage. So base/candidate trên nhóm mới, nhóm cũ và ngoài phạm vi.

## 3. Phản ví dụ và lỗi cần chủ động thử

CPU low-rank toy minh họa W+A×B, không phải adapter LLM được fine-tune. Replay không chứng minh live-model gain.

## 4. Từ nguyên lý sang bài thực hành

Làm R09: kiểm low-rank update nhỏ và rollback weights; lập data card/preference rubric. Nhánh live-model chỉ chạy khi có runtime, license, dataset và budget rõ.

Đây là bài tập biên tập cho repo dựa trên [Nghiên cứu và CornLoop](../modules/research-contracts.md) · [Đặc tả R01–R12](../labs/specifications.md) · [Thuật toán và học có kiểm chứng](../modules/controlled-learning.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 11.3 của tài liệu chương trình

Pipeline đề xuất:

```text
Permitted experiences
  -> review nguồn, privacy, license và nhãn
  -> dedup / contamination checks
  -> versioned training dataset
  -> offline training dưới budget
  -> base-vs-adapter comparison
  -> old/new/OOD evaluation
  -> candidate registry, không tự serving
```

Không đưa ảnh chụp tài liệu ngân hàng, dữ liệu khách hàng hoặc credentials thật vào bộ thực hành. Model license và dataset license được kiểm riêng tại thời điểm chọn; không suy ra có quyền train chỉ từ việc đọc được một trang web.

Với DPO, ghi tiêu chí vì sao `chosen` tốt hơn `rejected`; preference về văn phong khác preference về factuality. Với SFT, bài làm được chọn làm target cần xác minh kết quả và phạm vi, không chỉ được model tự chấm cao.

### Theo mục 11.6 của tài liệu chương trình

Phải có ít nhất ba góc nhìn: improvement trên họ task mới tương ứng kỹ năng; retention trên họ task cũ; behavior ngoài scope. Đổi tên biến hoặc đảo thứ tự câu không luôn tạo task độc lập, nên cần thiết kế biến thể thay đổi cấu trúc có ý nghĩa.

Chạy ablation tắt lesson, dùng lesson nhiễu và dùng summary cùng độ dài khi phù hợp. Nếu chỉ gain khi câu hỏi gần trùng, report gọi đúng là khả năng tận dụng memory cho các trường hợp gần, không khẳng định học kỹ năng tổng quát.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R09](../labs/r09-offline-learning/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
