# Tuần 2: Bản đối chứng và phép đánh giá đầu tiên — ghi chú lý thuyết

## 1. Câu hỏi của bài

Không có task nào được nhận xử lý: accepted risk có bằng 0 không?

## 2. Cơ chế cần hiểu

Định nghĩa outcome trước khi tối ưu. Với bài toán có quy tắc rõ, dùng rules/search/code không LLM làm bản đối chứng B0.

## 3. Phản ví dụ và lỗi cần chủ động thử

Thêm câu trả lời dễ vào tập test hoặc bỏ các lần fail làm mẫu số thay đổi và khiến báo cáo đẹp giả tạo.

## 4. Từ nguyên lý sang bài thực hành

Lập fixture đúng/sai và rubric cho parser số nguyên có đơn vị. Chạy bản đối chứng, lưu từng input, expected và output; báo toàn bộ task kể cả từ chối.

Đây là bài tập biên tập cho repo dựa trên [Phép đo và giới hạn thống kê](../../../modules/statistical-reliability.md) · [Phân bổ chương trình 36 tuần](../../../docs/curriculum/schedule.md) · [Thiết kế CornBench-VI Research & Learning](../../../benchmarks/cornbench_vi_rl/DESIGN.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

### Theo mục 7.1 của tài liệu chương trình

Một phát biểu chất lượng phải có dạng:

> Trên nhóm tác vụ T, nguồn dữ liệu D và khoảng thời gian V, với policy/model/memory snapshot C, hệ thống có tỷ lệ hoàn thành được xác minh là X; tỷ lệ tự xử lý là Y; cận thống kê cho loại lỗi E là U theo protocol P. Những trường hợp ngoài scope chuyển người hoặc không kết luận.

`X`, `Y`, `U` chỉ điền sau khi đo. Không lấy benchmark của paper, model vendor hay ví dụ giả lập để điền vào báo cáo CornAgents.

### Theo mục 7.2 của tài liệu chương trình

Với `N` nhiệm vụ đã lên kế hoạch đánh giá, `A` nhiệm vụ hệ thống tự nhận xử lý, `E_A` nhiệm vụ xử lý sai trong số được nhận:

\[
\text{Coverage} = A/N,\qquad
\widehat{R}_{accepted} = E_A/A \quad (A>0).
\]

Nếu `A=0`, risk trên accepted set chưa đo được, không ghi thành 0% lỗi. Báo thêm số nhiệm vụ giải thành công đã xác minh trên **toàn bộ N** để không thưởng một hệ thống từ chối tất cả.

| Nhóm metric | Cách dùng |
|---|---|
| Verified task success | Đúng outcome theo contract, không chỉ đúng văn phong |
| Accepted risk và coverage | Biết khi nào tự xử lý, khi nào cần người |
| Critical field correctness | Exact match hoặc tolerance có ý nghĩa cho số, đơn vị, version |
| Evidence quality | Claim được hỗ trợ; thiếu bằng chứng; mâu thuẫn; citation sai |
| Policy violations | Đọc/ghi ngoài quyền; dùng dữ liệu hoặc công cụ trái scope |
| Recovery | Khôi phục không tạo thêm side effect; phát hiện unknown outcome |
| Learning gain và retention | Tiến bộ trên nhóm chưa dùng để học; không làm hỏng nhóm cũ |
| Human burden | Thời gian sửa, duyệt, xử lý cảnh báo; không chỉ số lần bấm approve |
| Efficiency | Token, GPU/CPU, wall time, chi phí tất cả lần fail/retry |

Khi chấm một báo cáo có nhiều claims tương quan, không coi mỗi câu trong cùng báo cáo là một thử nghiệm độc lập. Đơn vị suy luận thống kê có thể là task hoặc document family; phải chọn và giải thích trước.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

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
