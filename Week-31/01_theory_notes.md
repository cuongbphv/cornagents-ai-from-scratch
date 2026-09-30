# Tuần 31: Hiệu chỉnh, risk–coverage và cận thống kê — ghi chú lý thuyết

## 1. Câu hỏi của bài

Không thấy lỗi trong mẫu có chứng minh tỷ lệ lỗi thật bằng 0 không?

## 2. Cơ chế cần hiểu

Coverage=A/N; accepted risk=E/A khi A>0. Chọn threshold trên calibration rồi cố định; cận nhị thức dùng cho policy và mẫu phù hợp, không cho một câu trả lời cụ thể.

## 3. Phản ví dụ và lỗi cần chủ động thử

Model tự nói chắc 95% không phải xác suất đã hiệu chỉnh. CP pass chỉ là cổng thống kê, không cấp quyền deploy; nhiều candidate cần protocol khác.

## 4. Từ nguyên lý sang bài thực hành

Làm R07: no-data, zero-error, một lỗi và retry trùng task; giải thích giả định. So công thức zero-error với reference; ghi rõ CP toy không kiểm representativeness.

Đây là bài tập biên tập cho repo dựa trên [Phép đo và giới hạn thống kê](../modules/statistical-reliability.md) · [Đặc tả R01–R12](../labs/specifications.md), không phải thí nghiệm đã chạy. Ghi điều gì thay đổi, điều gì giữ nguyên và điều kiện khiến bạn bác bỏ kết luận trước khi đo. Kết quả âm vẫn cần lưu.

## 5. Nội dung liên quan từ tài liệu chương trình

Các đoạn dưới thuộc bộ tài liệu chương trình theo chủ đề; giữ số mục để tra cứu. Các ký hiệu nguồn Sxx giữ nguyên để truy về nguồn sơ cấp; việc trích lại không có nghĩa đã kiểm chứng toàn bộ các paper hoặc chạy lại kết quả tác giả.

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

### Theo mục 7.3 của tài liệu chương trình

Với policy đã đóng băng, phép thử Bernoulli độc lập, đại diện cho miền cần dùng và protocol không dừng tùy tiện khi kết quả đẹp, cận trên một phía Clopper–Pearson cho tỷ lệ lỗi `p` là:

\[
U(k,n,\alpha) =
\begin{cases}
1, & n=0\ \text{hoặc}\ k=n,\\
\operatorname{Beta}^{-1}(1-\alpha; k+1,n-k), & 0\leq k<n.
\end{cases}
\]

Khi chưa quan sát lỗi nào:

\[
U(0,n,\alpha)=1-\alpha^{1/n}.
\]

Đây là cận cho **tỷ lệ lỗi của policy trên phân phối giả định**, không phải xác suất một câu trả lời cụ thể đúng. SciPy cung cấp khoảng tin cậy nhị thức exact/Clopper–Pearson; ví dụ ở Phụ lục A chọn đúng dạng một phía và đối chiếu implementation. [S15]

| Mẫu độc lập, 0 lỗi quan sát | Cận trên lỗi một phía, mức tin cậy 95% | Có đủ để qua ngưỡng lỗi 1%? |
|---|---:|---|
| 0 | Không có bằng chứng; dùng cận bảo thủ 100% | Không |
| 100 | Khoảng 2,9513% | Không |
| 299 | Khoảng 0,9969% | Có, riêng cổng thống kê này và theo các giả định |
| 2.995 | Khoảng 0,09997% | Có, riêng cổng thống kê này và theo các giả định |

Các số là **phép tính**, không phải kết quả chạy CornAgents. Mốc 299 chỉ áp dụng cho một kiểm định với `alpha=0.05` trong ví dụ. Nhiều ràng buộc hoặc nhiều candidate cần phân bổ sai số khác. 299 lần retry cùng một câu hỏi không trở thành 299 nhiệm vụ độc lập.

### Theo mục 7.5 của tài liệu chương trình

Learn then Test đặt bài toán lựa chọn cấu hình đáp ứng kiểm soát rủi ro dưới góc nhìn multiple hypothesis testing. Dùng nó làm nền học thuật cho chọn threshold/candidate với dữ liệu calibration phù hợp. [S13]

Conformal Risk Control xem xét kiểm soát kỳ vọng của loss bị chặn, đơn điệu theo các điều kiện của phương pháp. Không đồng nhất bảo đảm kỳ vọng đó với bảo đảm xác suất cao cho mọi task, mọi subgroup hoặc mọi distribution shift. [S14]

**Yêu cầu bài học:** trước khi viết “guarantee”, học viên phải ghi random variable nào, loss nào, mẫu được lấy thế nào, giả định exchangeability/i.i.d. nào dùng, và thay đổi nào khiến kết quả không còn áp dụng. Các kiểm tra drift không thể bảo đảm phát hiện mọi dạng dịch chuyển.

## 6. Tài liệu tái sử dụng

Thực hành theo lab của tuần và các mục nguồn ở trên.

Mở lab [R07](../labs/r07-risk-coverage/README.md); fixture là dữ liệu giả lập công khai, không phải hidden benchmark.

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
