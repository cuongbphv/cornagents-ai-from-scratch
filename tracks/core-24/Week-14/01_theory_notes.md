# Tuần 14: Preference learning và DPO — ghi chú lý thuyết

## 1. Câu hỏi của bài

DPO, GRPO và RLVR có phải ba bước bắt buộc liên tiếp không?

## 2. Cơ chế cần hiểu

DPO tối ưu theo cặp chosen/rejected mà không bắt buộc học reward model riêng. Ý nghĩa preference phụ thuộc tiêu chí gán nhãn.

## 3. Phản ví dụ và lỗi cần chủ động thử

Preference về văn phong không tự chứng minh factuality. RLVR mô tả nguồn reward kiểm được; GRPO mô tả cách tối ưu policy.

## 4. Từ nguyên lý sang bài thực hành

Tự viết DPO loss toy, giải thích reference policy và tiêu chí chọn cặp. Dùng fixture để phân biệt câu trôi chảy với câu có outcome đúng.

Đây là bài tập biên tập cho repo dựa trên [Thuật toán và học có kiểm chứng](../../../modules/controlled-learning.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 6.3 của tài liệu chương trình

**1. Self-reflection không phải self-verification.** Agent nói “tôi đã kiểm tra” chỉ là một output. Feedback để cải tiến cần liên kết với kết quả từ test, nguồn hoặc reviewer.

**2. Self-consistency không loại bỏ lỗi tương quan.** Nhiều lời giải có thể cùng dùng một giả định sai. Tăng số lần lấy mẫu còn có thể chỉ làm tăng chi phí nếu evaluator không phân biệt được đúng/sai.

**3. Tối ưu prompt không tương đương training weights.** Khi GEPA tạo prompt candidate mới, cần version prompt và dữ liệu search, không báo đó là một base model vừa được tự huấn luyện. Bài GEPA báo kết quả theo các thí nghiệm của tác giả, không chứng minh luôn hơn reinforcement learning. [S07] [S26]

**4. DPO không đồng nghĩa tối ưu sự thật.** Mục tiêu học phụ thuộc cặp preference; dữ liệu thích câu trả lời tự tin có thể không trùng với dữ liệu trả lời đúng. [S16]

**5. RLVR khác GRPO.** RLVR nói đến reward kiểm chứng được; GRPO là cách tối ưu policy. Một unit test có lỗ hổng vẫn có thể cấp reward cho code sai mục tiêu. [S17]

**6. JSON đúng không đồng nghĩa quyết định đúng.** Schema kiểm được hình dạng; semantics, quyền và trạng thái sau hành động phải kiểm riêng.

**7. Agent chấm agent không mặc định là evaluator độc lập.** Nên sử dụng LLM judge cho phần cần đánh giá ngôn ngữ, hiệu chỉnh theo nhãn người và dùng code/outcome grader cho điều xác định được. [S03]

### Theo mục 11.4 của tài liệu chương trình

Ví dụ thích hợp cho lab: một hàm xử lý số có tests/properties; bài toán toán học có đáp án xác minh được; truy vấn trên database giả lập có outcome rõ. Reward cho báo cáo nghiên cứu tổng quát thường khó xác định hơn, nên không bắt đầu bằng RL.

Khi dùng reward kiểm được, phải chống tối ưu sai mục tiêu: agent không được sửa expected answer, xóa test khó hoặc tạo shortcut đọc nhãn. Training verifier và final evaluator cần tách; coverage test không đủ có thể bị khai thác dù verifier là code. Đây là thiết kế đối phó reward hacking, không phải chứng minh mọi lỗ hổng đã được loại bỏ.

## 6. Tài liệu tái sử dụng

- [Week-10/README.md](../../../Week-10/README.md)
- [Week-10/03_dpo_skeleton.py](../../../Week-10/03_dpo_skeleton.py)

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
