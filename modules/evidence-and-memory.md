# Bằng chứng và bộ nhớ có quản trị

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s5"></a>

## 5. Bằng chứng, bộ nhớ và học từ thất bại

### 5.1. Evidence ledger: ghi claim thay vì chỉ lưu một đống URL

Một claim quan trọng cần biết **được hỗ trợ bởi đoạn nào**, thuộc phiên bản nào, có mâu thuẫn nào và đã qua phép kiểm nào. Không yêu cầu mọi suy luận thiết kế phải có một nguồn nói y hệt; phải ghi rõ đâu là fact từ nguồn, đâu là suy luận và đâu là giả thuyết mới.

| Trường | Ý nghĩa |
|---|---|
| `claim_id`, `claim_text` | Phát biểu hẹp, có thể kiểm tra |
| `claim_kind` | `source_fact`, `computed`, `inference`, `hypothesis` |
| `source_id`, `span`, `snapshot_digest` | Đúng bản nội dung đã dùng, không chỉ URL có thể đổi |
| `published_at`, `observed_at`, `valid_from/to` | Ngày công bố, ngày đọc và thời gian áp dụng khác nhau |
| `origin_cluster` | Nhóm nguồn cùng xuất xứ để tránh đếm bản đăng lại là bằng chứng độc lập |
| `support_status` | `supported`, `contradicted`, `insufficient`, `not_applicable` |
| `verification_method` | Quy tắc/code, đối chiếu nguồn, reviewer hoặc rubric |
| `access_scope`, `license_status` | Chủ thể được dùng; quyền lưu, trích dẫn và huấn luyện |
| `limitations` | Điều phép kiểm không xác nhận được |

**Phân biệt sáu kiểm tra:** nguồn tồn tại; đoạn nguồn hỗ trợ claim; nguồn có thẩm quyền/phù hợp; thời điểm và phiên bản đúng; số liệu/đơn vị đúng; người dùng có quyền đọc. Không dùng một nhãn “grounded” để che hết sáu khía cạnh.

Hai trang cùng chép một thông cáo không phải hai phép xác nhận độc lập. Citation trỏ đúng một tài liệu sai vẫn không làm phát biểu đúng. Nguồn sơ cấp cũng có thể chỉ nêu kết quả trong điều kiện hẹp.

### 5.2. Lưu ba loại bộ nhớ riêng

**Semantic memory:** fact hoặc quy tắc đã có nguồn, scope và thời hạn.

**Episodic memory:** điều đã xảy ra trong một lần chạy. Episode mô tả trải nghiệm, không tự khẳng định quy luật chung.

**Procedural memory:** skill/lesson về cách giải, gồm điều kiện áp dụng, cách kiểm tra và chống chỉ định.

Một ghi chép “thử A, fail; thử B, pass” chỉ là episode. Muốn thành lesson “B tốt hơn A khi X” phải có thí nghiệm phù hợp và phản ví dụ, đồng thời ghi rõ chưa đủ bằng chứng cho các trường hợp khác.

### 5.3. Vòng đời memory đề xuất

```text
PROPOSED -> QUARANTINED -> ELIGIBLE_FOR_REVIEW -> ACTIVE_SCOPED
                   |               |                  |
                   v               v                  v
                REJECTED        REJECTED     STALE / REVOKED / SUPERSEDED
```

Worker chỉ tạo `PROPOSED`. Quarantine kiểm source/ACL, nội dung chỉ thị lạ, phạm vi, duplicate, mâu thuẫn và provenance. Không có nguồn cho fact thì không tự promote thành semantic fact. Một lesson có thể bắt đầu là “giả thuyết hữu ích chưa xác nhận”, nhưng retrieval phải hiển thị nhãn đó.

`ACTIVE_SCOPED` không có nghĩa đúng mãi. Retrieval recheck quyền, hiệu lực và trạng thái hiện tại tại thời điểm dùng. Khi một nguồn bị thu hồi hoặc sửa, dependency graph đánh dấu các summary, vector entry, lesson và cache dẫn xuất cần xử lý. Quyền truy cập cần được lọc trước khi trả nội dung cho model, không chỉ che citation sau khi sinh câu trả lời.

Xóa khỏi memory không đồng nghĩa đã loại ảnh hưởng khỏi weights của model từng được train bằng dữ liệu đó. Với training, cần lineage và quyết định xử lý riêng theo dataset/model version; không hứa “xóa một hàng là unlearn hoàn toàn”.

### 5.4. Bài học có phản ví dụ — “falsification-aware memory”

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

### 5.5. Chống vòng lặp tự tin từ dữ liệu tự sinh

Không lấy output do model đánh giá “tốt” rồi coi là ground truth cho model tiếp theo. Dữ liệu tổng hợp có thể hữu ích nhưng cần nguồn gốc, kiểm định và tập neo độc lập. Công trình về recursive training cho thấy rủi ro suy giảm khi phụ thuộc vào dữ liệu sinh qua các thế hệ; không suy ra mọi dữ liệu tổng hợp đều xấu. [S18]

Tách nguồn **đề xuất**, nguồn **gán nhãn** và nguồn **đánh giá**. Nếu tất cả đều từ cùng một model, phải khai báo độ phụ thuộc đó và bổ sung kiểm chứng bên ngoài cho claim quan trọng.

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
