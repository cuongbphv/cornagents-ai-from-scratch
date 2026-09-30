# Thuật toán và học có kiểm chứng

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s6"></a>

## 6. Thuật toán: chọn theo điều kiện, không theo độ nổi tiếng

### 6.1. Thứ tự ưu tiên giải bài toán

Đề xuất thứ tự: **phép tính/quy tắc có thể xác định → retrieval có bằng chứng → workflow cố định → agent đơn → tìm kiếm nhiều candidate → multi-agent khi có lý do đo được**.

Đây không phải bảng xếp hạng chất lượng phổ quát. Nó là cách bắt đầu với baseline dễ kiểm tra. Một câu hỏi mở không thể ép thành regex; một phép cộng tiền theo schema không cần một hội đồng agent bỏ phiếu.

### 6.2. Ma trận thuật toán và mức độ cần học

| Nhóm | Cần nắm | Tự làm đến đâu? | Phép kiểm quan trọng |
|---|---|---|---|
| Nền model | Autograd, stable softmax, cross-entropy, AdamW, BPE, causal attention, RoPE, KV cache | Implementation nhỏ, so reference | Gradient check, mask, cache parity |
| Retrieval | BM25, dense similarity, RRF, reranker, retrieval lặp | Tự viết baseline/fusion; dùng embedding/reranker có sẵn | Recall@k, nDCG, coverage, đúng ACL/phiên bản |
| Agent loop | ReAct, state machine, graph/DAG, stop conditions | Tự viết bounded loop trước framework | Tool semantics, outcome, budget, trường hợp không đủ thông tin |
| Học qua trải nghiệm | Reflexion, lesson retrieval, counterexample memory | Buffer nhỏ và lifecycle có kiểm soát | Task chuyển giao, bài cũ, bài ngoài scope |
| Tối ưu prompt/skill | Random search baseline, GEPA/DSPy theo phiên bản đã pin | Candidate search trong development data | Same-budget comparison; không dùng test để tối ưu |
| Độ bất định | Calibration, Brier, reliability diagram, selective prediction | Tự tính metric, thử ngưỡng | Risk–coverage và calibration ngoài training |
| Kiểm soát rủi ro | Binomial bound, Learn then Test, conformal risk control | CP trước; LTT/CRC ở nhánh học thuật | Giả định, multiple testing, drift, kích thước mẫu |
| Chọn thí nghiệm | Ablation, random search, Bayesian optimization, value of information | Objective toy đo được, budget cố định | Sample efficiency và chi phí evaluator |
| Học model | SFT, LoRA, DPO; RLVR/GRPO tùy chọn | Toy/adapter nhỏ, không train model lớn bắt buộc | Verifier độc lập, dữ liệu có lineage, retention |
| Hệ thống | Idempotency, reconciliation, versioning, atomic promotion | Chạy fault injection | Crash sau write, token hết hạn, event duplicate |

ReAct kết hợp suy luận và tương tác; Self-RAG có cơ chế học reflection token và retrieval; self-consistency tổng hợp nhiều lời giải. Chúng là những phương pháp cụ thể với các điều kiện thí nghiệm, không phải nhãn để gắn vào mọi prompt dài. [S05] [S06] [S24]

### 6.3. Bảy phân biệt tránh học sai

**1. Self-reflection không phải self-verification.** Agent nói “tôi đã kiểm tra” chỉ là một output. Feedback để cải tiến cần liên kết với kết quả từ test, nguồn hoặc reviewer.

**2. Self-consistency không loại bỏ lỗi tương quan.** Nhiều lời giải có thể cùng dùng một giả định sai. Tăng số lần lấy mẫu còn có thể chỉ làm tăng chi phí nếu evaluator không phân biệt được đúng/sai.

**3. Tối ưu prompt không tương đương training weights.** Khi GEPA tạo prompt candidate mới, cần version prompt và dữ liệu search, không báo đó là một base model vừa được tự huấn luyện. Bài GEPA báo kết quả theo các thí nghiệm của tác giả, không chứng minh luôn hơn reinforcement learning. [S07] [S26]

**4. DPO không đồng nghĩa tối ưu sự thật.** Mục tiêu học phụ thuộc cặp preference; dữ liệu thích câu trả lời tự tin có thể không trùng với dữ liệu trả lời đúng. [S16]

**5. RLVR khác GRPO.** RLVR nói đến reward kiểm chứng được; GRPO là cách tối ưu policy. Một unit test có lỗ hổng vẫn có thể cấp reward cho code sai mục tiêu. [S17]

**6. JSON đúng không đồng nghĩa quyết định đúng.** Schema kiểm được hình dạng; semantics, quyền và trạng thái sau hành động phải kiểm riêng.

**7. Agent chấm agent không mặc định là evaluator độc lập.** Nên sử dụng LLM judge cho phần cần đánh giá ngôn ngữ, hiệu chỉnh theo nhãn người và dùng code/outcome grader cho điều xác định được. [S03]

### 6.4. Tìm kiếm và tối ưu thí nghiệm có kiểm soát

Với câu hỏi “thử cấu hình retrieval nào tiếp theo?”, bắt đầu random/grid search nhỏ. Khi mỗi phép đo đắt và không gian thích hợp, học Bayesian optimization qua surrogate và acquisition function như expected improvement. Phải kiểm nghiệm rằng chi phí xây surrogate có đáng so với baseline. [S19]

Với value of information, ý tưởng là chọn phép đo dự kiến làm quyết định tốt hơn sau khi trừ chi phí, **trong tập hành động được phép**. Không lấy câu “tôi kỳ vọng tăng độ chính xác 20%” của LLM làm số liệu acquisition mà chưa kiểm định. Những ước lượng lợi ích phải được backtest hoặc được ghi rõ là heuristic.

Tree search/MCTS chỉ nên thành lab nâng cao khi state, action và phép đánh giá có nghĩa rõ. Không mặc định mở cây suy luận thật rộng cho mọi câu hỏi tài liệu. Multi-agent chỉ vào thí nghiệm khi có phân chia công việc hữu ích; shared context, thông tin sai lan truyền và chi phí phối hợp đều cần đo. [S23]

### 6.5. Baseline “không tự học” là bắt buộc

Nếu memory-enabled agent thắng, cần biết nó thắng vì học lesson, vì thêm tài liệu, vì dùng nhiều token hay vì test đã lọt vào memory. Mỗi thí nghiệm học cần một bản **frozen** cùng model, data access và budget; khác biệt chủ yếu là cơ chế học đang nghiên cứu.

---

<a id="s11"></a>

## 11. Học không cập nhật trọng số và học có cập nhật trọng số

### 11.1. Đường mặc định: thay thứ nhỏ nhất có thể kiểm chứng

Khi agent thất bại, chẩn đoán trước theo tầng:

| Nguyên nhân chính | Hướng sửa đầu tiên |
|---|---|
| Thiếu tài liệu hoặc sai phiên bản | Curation, retrieval, temporal metadata |
| Output sai cấu trúc | Schema, constrained output, validator |
| Sai phép tính/đơn vị | Code xác định và unit tests |
| Gọi tool sai quyền/trạng thái | Tool contract và executor |
| Quy trình nhiều bước rối | State machine/workflow đơn giản hơn |
| Thiếu kỹ năng lặp lại có dữ liệu rõ | Prompt/skill optimization hoặc adapter có eval |
| Oracle/reward chấm sai | Sửa phép đo dưới review, không tiếp tục tối ưu candidate |

Đây là heuristic kỹ thuật cần kiểm chứng, không phải khẳng định fine-tuning không có ích. Mục tiêu là tránh sửa weights cho một lỗi thực ra nằm ở schema hoặc retrieval.

### 11.2. Learning không gradient

Dùng trải nghiệm đã được phép lưu để đề xuất lesson/prompt/skill. Học viên phải giữ được provenance và lưu version. Bản học xong được so với bản frozen trên task chưa dùng để tối ưu. Không đánh đồng “context dài hơn” với “năng lực tốt hơn”; báo chi phí token và lỗi do context nhiễu.

Một candidate prompt thay đổi nghĩa của action, chẳng hạn tự nhận có quyền xuất dữ liệu, không phải improvement hợp lệ dù score ngôn ngữ tăng. Phạm vi chỉnh sửa được định trước trong manifest.

### 11.3. Offline SFT/LoRA/DPO

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

### 11.4. RLVR/GRPO chỉ khi reward đủ xác định

Ví dụ thích hợp cho lab: một hàm xử lý số có tests/properties; bài toán toán học có đáp án xác minh được; truy vấn trên database giả lập có outcome rõ. Reward cho báo cáo nghiên cứu tổng quát thường khó xác định hơn, nên không bắt đầu bằng RL.

Khi dùng reward kiểm được, phải chống tối ưu sai mục tiêu: agent không được sửa expected answer, xóa test khó hoặc tạo shortcut đọc nhãn. Training verifier và final evaluator cần tách; coverage test không đủ có thể bị khai thác dù verifier là code. Đây là thiết kế đối phó reward hacking, không phải chứng minh mọi lỗ hổng đã được loại bỏ.

### 11.5. L4 — sửa harness như một thí nghiệm giới hạn

Chỉ cho sửa thư mục/strategy được allowlist, chẳng hạn query selection hoặc parser. Không cho sửa phần kiểm quyền, secrets, quota, evaluator, release approval và log bất biến. Build candidate không có credential của evaluator hay release service.

Darwin Gödel Machine là nguồn gợi mở cho self-modification trong coding agents; CornAgents không suy ra từ đó rằng hệ thống tự sửa có thể tự chứng minh mọi thay đổi an toàn. [S11]

### 11.6. Chứng minh đã học, không chỉ đã ghi nhớ

Phải có ít nhất ba góc nhìn: improvement trên họ task mới tương ứng kỹ năng; retention trên họ task cũ; behavior ngoài scope. Đổi tên biến hoặc đảo thứ tự câu không luôn tạo task độc lập, nên cần thiết kế biến thể thay đổi cấu trúc có ý nghĩa.

Chạy ablation tắt lesson, dùng lesson nhiễu và dùng summary cùng độ dài khi phù hợp. Nếu chỉ gain khi câu hỏi gần trùng, report gọi đúng là khả năng tận dụng memory cho các trường hợp gần, không khẳng định học kỹ năng tổng quát.

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
