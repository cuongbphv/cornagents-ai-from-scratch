# Kiến trúc runtime, quyền và hợp đồng dữ liệu

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../docs/papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s4"></a>

## 4. Kiến trúc: agent có thể đổi gì và không được đổi gì?

### 4.1. Bốn vùng triển khai

```text
Người dùng / sự kiện được cho phép
                 |
                 v
+---------------------------------------------------------------+
| CONTROL PLANE — worker không có quyền sửa                      |
| Identity | authorization | task contract | quota | cancel      |
| Artifact registry | promotion policy | release approval        |
+-------------------------------+-------------------------------+
                                |
                     capability có scope + expiry
                                |
          +---------------------v-----------------------+
          | RESEARCH PLANE                              |
          | Planner -> retriever -> bounded tool runner |
          | Evidence ledger -> experiment workspace     |
          +---------------------+-----------------------+
                                |
                         candidate, chưa active
                                |
          +---------------------v-----------------------+
          | LEARNING PLANE                              |
          | Quarantine -> lessons -> skill/config/LoRA  |
          | Development data + candidate search         |
          +---------------------+-----------------------+
                                |
                       artifact digest bất biến
                                |
          +---------------------v-----------------------+
          | INDEPENDENT EVALUATION                      |
          | Protected tests | verifier | retention eval |
          | Risk report | scope | limitations           |
          +---------------------+-----------------------+
                                |
                    approval -> shadow -> bounded use
                                |
                       monitor / revoke / rollback
```

“Độc lập” trước hết là độc lập về **quyền sửa, dữ liệu và quy trình**. Dùng model thứ hai cùng nguồn và cùng lỗi không tự tạo độc lập thống kê hoặc bảo đảm sự thật.

### 4.2. Ma trận ghi/sửa

| Tài nguyên | Research worker | Learning worker | Evaluator | Release controller |
|---|---|---|---|---|
| Raw source snapshot | Đọc qua gateway; đề nghị ingest | Đọc phần được phép | Đọc theo scope | Không cần sửa |
| Candidate workspace | Ghi | Ghi trong vùng cho phép | Chạy snapshot chỉ đọc | Đọc digest |
| Active memory/skill | Đọc theo ACL | Chỉ đề nghị version mới | Đọc bản đánh giá | Promote theo policy |
| Protected test/answer | Không đọc | Không đọc | Đọc trong môi trường riêng | Chỉ đọc kết quả tổng hợp |
| Policy, quota, secrets | Không sửa | Không sửa | Không tự cấp quyền | Quản lý theo phân quyền riêng |
| Kết quả eval đã ký | Không sửa | Không sửa | Tạo kết quả gắn digest | Kiểm chữ ký/digest |

Ở lab local, có thể dùng tiến trình và credential khác nhau. Đó là mô phỏng học tập; nếu một tài khoản quản trị có thể sửa cả hai vùng thì chưa có cách ly mạnh cho production. `CODEOWNERS` hoặc branch protection hữu ích cho review nhưng không thay thế runtime isolation.

### 4.3. Quyền gắn với hành động, không gắn với lời hứa của model

Mỗi đề nghị hành động chứa `task_id`, `actor`, loại thao tác, tài nguyên, tham số chuẩn hóa, phiên bản input, `idempotency_key` và hạn sử dụng. Approval phải gắn với digest nội dung đó. Đổi một tham số quan trọng hoặc source version làm thay đổi ý nghĩa tác vụ thì phải kiểm lại.

Không dùng một phê duyệt chung “đồng ý agent tự làm” cho mọi hành động về sau. Sau restart/resume vẫn kiểm quyền hiện hành; quyền đã thu hồi không sống lại chỉ vì checkpoint cũ còn token.

### 4.4. Giới hạn tài nguyên ở cấp toàn nhiệm vụ

Quota bao gồm tổng token, tool calls, wall time, CPU/GPU, dung lượng file, network egress và số worker con. Worker con phải tiêu từ cùng budget của nhiệm vụ mẹ, không được tạo budget mới. Bộ đếm dùng thao tác atomic/transaction phù hợp khi chạy đồng thời.

Hủy nhiệm vụ phải lan tới toàn bộ worker, subprocess, scheduled retry và capability liên quan. Kill switch không nằm trong process mà agent có thể sửa. Không xem model từ chối gọi tool là bằng chứng duy nhất rằng side effect đã dừng.

### 4.5. Durable execution không đồng nghĩa exactly-once

Checkpoint giúp ghi lại trạng thái agent; thao tác ghi bên ngoài cần thiết kế idempotency và reconciliation riêng. [S22]

Ví dụ: tool đã tạo artifact nhưng acknowledgment bị mất. Retry phải tra operation ID và trạng thái thật, không tạo artifact thứ hai. Với thao tác không hỗ trợ idempotency hoặc không thể xác định đã thành công chưa, trạng thái phải là `UNKNOWN_OUTCOME`; chuyển người xác minh thay vì retry mù.

**Lab invariant:** tối đa một business effect cho cùng khóa nghiệp vụ trong môi trường thử; không ghi nếu quyền hiện tại không cho phép; mọi trạng thái thành công phải có outcome evidence. Bộ test hữu hạn không chứng minh invariant ngoài mọi điều kiện thực tế.

---

<a id="s10"></a>

## 10. Stack triển khai và hợp đồng dữ liệu

### 10.1. Stack khởi đầu: càng ít lớp càng dễ kiểm tra

| Lớp | Đề xuất | Giới hạn và nguyên tắc |
|---|---|---|
| Code và model | Python, NumPy, PyTorch | Tách notebook minh họa khỏi runtime |
| Chất lượng code | pytest/unittest, Ruff, type checking, dependency lock | Không xem lint xanh là đủ đúng nghiệp vụ |
| Hợp đồng | Pydantic hoặc JSON Schema | Check semantics/quyền ngoài schema |
| Orchestration | Python state machine trước; LangGraph khi cần persistence | Pin version; tránh học nhiều framework cùng lúc [S22] |
| Storage | SQLite cho local lab; PostgreSQL khi có nhiều worker/tenant | Giao dịch và credential riêng cho control/eval |
| Retrieval | BM25 + dense + fusion; vector store khi cần | Không lưu mọi context vào vector DB mặc định |
| Learning candidates | Script rõ ràng; DSPy/GEPA cho nhánh prompt optimization | Chỉ development data, bounded search [S08] [S26] |
| Model adapter | Một runtime local phù hợp máy; API cloud tùy chọn | Giao diện trung lập nhà cung cấp; live eval tách replay |
| Experiments | JSONL/Parquet + manifest trước; registry khi đủ nhu cầu | Mọi run có source/data/model/code version |
| Security | OS/container sandbox theo threat model, egress broker, scoped credentials | Docker đơn lẻ không được mô tả như chứng minh cách ly [S20] |
| Protocol | MCP cho công cụ cần tích hợp | MCP không thay authorization hoặc xác nhận nghiệp vụ [S21] |
| Release | Immutable artifact, evaluation record, scoped approval | Không cần xây platform tự triển khai khổng lồ ở giai đoạn đầu |

Các tên công nghệ là lựa chọn kiến trúc, không phải khẳng định chúng là “tốt nhất hiện nay”. Khóa phiên bản ở thời điểm viết lab; dùng API adapter để tránh toàn bộ giáo trình phụ thuộc một model hoặc preview API.

### 10.2. Task contract YAML minh họa

Cấu hình dưới đây là **schema đề xuất cho runner cần xây**, không phải file đã có thể đưa cho một framework bất kỳ để chạy.

```yaml
schema_version: "cornagents.task.chương trình"
task_id: "research-demo-001"
objective: "Đánh giá parser số và đơn vị tiếng Việt trên dữ liệu giả lập"
mode: "sandbox_research"
data_policy:
  allowed_collections: ["synthetic_vi_units_v1"]
  production_data: false
  training_reuse: "requires_dataset_review"
  persist_evaluation_inputs: false
authority:
  principal: "research-worker-demo"
  tools: ["search_fixture", "read_fixture", "run_sandbox_tests"]
  external_writes: false
  can_promote_candidate: false
  can_modify_evaluator: false
  capability_ttl_seconds: 1800
budget:
  total_model_tokens: 40000
  total_tool_calls: 60
  total_wall_seconds: 1800
  max_concurrent_workers: 2
  max_total_workers: 4
  max_candidate_variants: 6
  share_budget_with_descendants: true
network:
  mode: "deny_by_default"
  allowed_destinations: []
learning:
  allowed_targets: ["candidate_lesson", "candidate_parser"]
  persistent_fact_requires_evidence: true
  default_state: "QUARANTINED"
completion:
  require_evidence_ledger: true
  require_baseline_comparison: true
  allow_negative_result: true
  require_unresolved_questions: true
```

Những budget này chỉ để cấu hình một bài thực hành, chưa phải mức tối ưu đo được. `capability_ttl_seconds` hết hạn phải thực sự bị executor từ chối; không chỉ xuất hiện trong prompt. Một job chưa xong khi hết hạn có thể được người có thẩm quyền cấp phiên mới, nhưng không tự gia hạn.

### 10.3. Một lesson candidate phải mang theo bằng chứng

```yaml
schema_version: "cornagents.lesson.chương trình"
lesson_id: "vi-number-parser-lesson-001"
state: "QUARANTINED"
kind: "procedural"
claim: "Dùng parser xác định khi field thuộc grammar số và đơn vị đã hỗ trợ"
scope:
  task_family: "synthetic_vi_numeric_extraction"
  supported_units: ["đồng", "nghìn đồng", "triệu đồng", "tỷ đồng"]
  excludes: ["ambiguous_ocr", "missing_unit_header"]
evidence:
  experiment_ids: ["development-exp-001"]
  source_ids: ["synthetic-schema-v1"]
  status: "requires_independent_confirmation"
counterexamples:
  - "Thiếu header đơn vị nên không được tự suy ra hệ số"
  - "Chuỗi số mơ hồ giữa dấu thập phân và dấu phân cách"
verification:
  deterministic_property_tests_required: true
  transfer_cohort_required: true
  reviewer_approval_required: true
revocation:
  invalidate_on_schema_change: true
  invalidate_on_source_revocation: true
```

Các ID trong ví dụ là tên minh họa, không phải experiment đã chạy. Production implementation phải kiểm referential integrity: experiment/source được trỏ đến phải tồn tại và có quyền đọc.

### 10.4. Interface nên tách rõ trách nhiệm

| Interface đề xuất | Hợp đồng quan trọng |
|---|---|
| `ResearchPlanner` | Sinh plan trong task contract; không tự cấp capability |
| `EvidenceRetriever` | Trả source spans đã lọc quyền, version và provenance |
| `ToolExecutor` | Validate schema + quyền hiện tại + budget + side effect policy |
| `ExperimentRunner` | Chạy immutable code/data snapshot trong sandbox |
| `OutcomeVerifier` | Đọc trạng thái thực; phân biệt pass/fail/unknown |
| `LearningProposer` | Tạo candidate có lineage; không ghi active registry |
| `IndependentEvaluator` | Chỉ nhận snapshot; không cho candidate sửa protected criteria |
| `PromotionController` | Kiểm evidence, digest, approval, scope và rollback trước khi dùng |

Không cần mỗi interface thành một microservice ngay. Tách module và credentials đủ cho học; tách process/service khi cần biên an toàn thật. Một `LLMJudge` chỉ là thành phần trong evaluation, không được đồng nhất với toàn bộ `IndependentEvaluator`.

### 10.5. Pseudocode của hai vòng chạy

Đây là pseudocode kiến trúc, chưa phải chương trình đã thực thi:

```text
RESEARCH(task):
    capability := control_plane.authorize(task)
    state := load_or_create_checkpoint(task)
    while not state.terminal:
        control_plane.check_current_authority_and_budget(task, capability)
        proposal := planner.propose_next_step(state, task.contract)
        validated := external_policy.validate(proposal, task)
        observation := sandbox_executor.execute(validated)
        evidence_ledger.append_observation(observation)
        state := reducer.update(state, observation)
        checkpoint.save(state)
        if outcome_is_ambiguous:
            state := NEEDS_RECONCILIATION_OR_HUMAN
    return report_with_evidence_and_limitations(state)

LEARN(batch_of_permitted_experiences):
    candidate := learner.propose_scoped_change(batch)
    quarantine.store(candidate)
    if not development_checks_pass(candidate):
        return REJECTED_WITH_REASONS
    snapshot := build_and_freeze(candidate)
    report := isolated_evaluator.evaluate_once_under_protocol(snapshot)
    proposal := release_review.package(snapshot, report)
    return proposal  # Không tự promote; chưa đồng nghĩa được triển khai
```

Nếu task bị hủy, exception và subprocess phải được supervisor xử lý; pseudocode không thể hiện đầy đủ transaction, locking hay failure handling. Phần đó thuộc lab R10/R11.

### 10.6. Log cái cần kiểm, không thu thập vô hạn

Trace cần task/run ID, input/output đã redact, tool calls, source references, quyền, timing, cost, outcome và lý do quyết định ngắn gọn. Không phụ thuộc vào việc nhà cung cấp cho truy cập toàn bộ suy luận nội bộ của model. Không cần lưu chain-of-thought riêng tư để biết một tool đã ghi sai tài nguyên.

Traces cũng là dữ liệu có thể nhạy cảm. Quy định retention, ACL, redaction, deletion và training eligibility riêng; không tự động đưa mọi log vào “bộ nhớ tự học”.

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
