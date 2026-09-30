# Phép đo và giới hạn thống kê

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s7"></a>

## 7. Độ chính xác cao phải được phát biểu như thế nào?

### 7.1. Không viết “agent chính xác 99%” mà thiếu định nghĩa

Một phát biểu chất lượng phải có dạng:

> Trên nhóm tác vụ T, nguồn dữ liệu D và khoảng thời gian V, với policy/model/memory snapshot C, hệ thống có tỷ lệ hoàn thành được xác minh là X; tỷ lệ tự xử lý là Y; cận thống kê cho loại lỗi E là U theo protocol P. Những trường hợp ngoài scope chuyển người hoặc không kết luận.

`X`, `Y`, `U` chỉ điền sau khi đo. Không lấy benchmark của paper, model vendor hay ví dụ giả lập để điền vào báo cáo CornAgents.

### 7.2. Metric phải đi theo mục tiêu và loại rủi ro

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

### 7.3. Ví dụ định lượng: không lỗi chưa đủ để tuyên bố chắc chắn

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

### 7.4. Calibration, selective prediction và abstention

Một classifier/verifier có thể được hiệu chỉnh xác suất trên dữ liệu riêng; temperature scaling là phương pháp nền để học calibration. Nó khác với thay sampling temperature của LLM. Model tự nói “chắc 95%” không tự tạo một xác suất đã hiệu chỉnh. [S12]

Trong chương trình, decision policy có thể dùng tín hiệu như: đủ evidence không, nguồn mâu thuẫn không, tool outcome rõ không, câu hỏi có nằm trong grammar/schema đã hỗ trợ không. Threshold chọn trên tập calibration, sau đó đóng băng trước đánh giá độc lập.

Không lấy một scalar “confidence” để bỏ qua permission gate. Với tác vụ ngoài scope, không được tự nâng quyền chỉ vì confidence cao.

### 7.5. Learn then Test và conformal: học cả giới hạn của bảo đảm

Learn then Test đặt bài toán lựa chọn cấu hình đáp ứng kiểm soát rủi ro dưới góc nhìn multiple hypothesis testing. Dùng nó làm nền học thuật cho chọn threshold/candidate với dữ liệu calibration phù hợp. [S13]

Conformal Risk Control xem xét kiểm soát kỳ vọng của loss bị chặn, đơn điệu theo các điều kiện của phương pháp. Không đồng nhất bảo đảm kỳ vọng đó với bảo đảm xác suất cao cho mọi task, mọi subgroup hoặc mọi distribution shift. [S14]

**Yêu cầu bài học:** trước khi viết “guarantee”, học viên phải ghi random variable nào, loss nào, mẫu được lấy thế nào, giả định exchangeability/i.i.d. nào dùng, và thay đổi nào khiến kết quả không còn áp dụng. Các kiểm tra drift không thể bảo đảm phát hiện mọi dạng dịch chuyển.

### 7.6. Tách dữ liệu theo vai trò, không chỉ chia ba file ngẫu nhiên

```text
Development/training        -> dùng để xây và tối ưu candidate
Calibration                 -> chọn threshold hoặc policy quyết định
Independent confirmation    -> kiểm candidate đã đóng băng
Retention/regression        -> kiểm năng lực cũ, bảo vệ invariant
Future/shift cohort         -> kiểm chuyển giao theo thời gian/nguồn/schema mới
```

Chia ở cấp nguồn, họ nhiệm vụ, template và thời gian khi phù hợp. Không chia chunk gần trùng của cùng tài liệu sang hai tập. Public benchmark giúp phát triển và tái lập, nhưng có thể đã có trong training data của model; không mặc định là bằng chứng hoàn toàn chưa thấy.

Tập regression công khai có thể bị overfit sau nhiều vòng. Vì vậy nó bảo vệ hành vi đã biết, không thay thế tập confirmation mới. Dataset lineage phải theo dõi cả raw examples, summaries, synthetic variants và traces rò rỉ nhãn.

### 7.7. Thử nhiều candidate và đánh giá nhiều lần

Nếu thử 100 prompt rồi chọn prompt có test đẹp nhất, tập đó đã trở thành development data. Giữ answer file kín chưa đủ; pass/fail feedback lặp lại cũng có thể bị tối ưu ngược.

Với tập candidate hữu hạn, được định trước và không chọn thích nghi từ cùng kết quả test, có thể dùng multiple-testing correction phù hợp, chẳng hạn Bonferroni với p-value hợp lệ. **Không dùng Bonferroni như thuốc chữa việc liên tục huấn luyện theo hidden test.**

Đề xuất triển khai ban đầu: development search → một finalist đóng băng → confirmation cohort mới → lưu nguyên cả kết quả fail. Phiên phát hành sau dùng cohort mới hoặc một protocol reusable-holdout/sequential được chuyên gia thống kê xem xét. Có ngân sách số lần hỏi evaluator và sổ phân bổ mức sai số. Không cherry-pick release thắng rồi bỏ các release đã thất bại.

### 7.8. Điều kiện promote không chỉ là accuracy tăng

Cần đồng thời: không vi phạm invariant quan trọng trong suite; rủi ro dưới ngưỡng theo protocol; coverage không bị tụt để né task khó; năng lực cũ không suy giảm vượt margin; chi phí và latency trong budget; dữ liệu/giấy phép phù hợp; người có thẩm quyền duyệt thay đổi.

So candidate với baseline trên cùng nhiệm vụ, dùng paired analysis khi phù hợp. Bootstrap theo task family nếu các trial phụ thuộc; không bootstrap từng token hoặc từng lần chạy như mẫu độc lập. Báo confidence interval, số trial, lỗi nhãn đã phát hiện và trường hợp không thống nhất giữa reviewer.

**Không có kiểm định nào thay thế việc biết evaluator đang chấm đúng mục tiêu.** Nếu oracle sai, tối ưu thuật toán chỉ làm hệ thống học cách hợp với oracle sai nhanh hơn.

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
