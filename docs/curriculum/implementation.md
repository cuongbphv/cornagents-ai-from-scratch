# Cấu trúc chương trình và thứ tự triển khai

Thuộc CornAgents.AI. Tài liệu chương trình được hợp nhất ngày 30/09/2026. Phân bổ bài học và kiến trúc là đề xuất; ví dụ không phải kết quả đánh giá agent. [Nguồn sơ cấp và phạm vi sử dụng](../papers/research_learning_sources.md) giữ mã S01–S28 để đối chiếu. Các nguồn kế thừa chưa được xác minh lại toàn văn trong lần biên tập này.

<a id="s17"></a>

## 17. Cấu trúc repo và backlog triển khai

### 17.1. Nâng cấp cộng thêm, tránh phá liên kết cũ

```text
README.md
ENTRYPOINTS.md
CHANGELOG.md
curriculum.yaml
tracks/
  beginner-core-24.md
  research-learning-12.md
  fast-track-mapping.md
  specialization-research.md
modules/
  research-contracts.md
  evidence-and-memory.md
  controlled-learning.md
  statistical-reliability.md
  promotion-and-revocation.md
labs/
  r01-research-contract/
  r02-bounded-research/
  r03-governed-memory/
  r04-conditional-lessons/
  r05-candidate-search/
  r06-experiment-design/
  r07-risk-coverage/
  r08-evaluator-boundary/
  r09-offline-learning/
  r10-durable-research/
  r11-promotion/
  r12-cornbench-learning/
src/cornagents/
  contracts/
  research/
  evidence/
  memory/
  learning/
  runtime/
  adapters/
control_plane/
  policies/
  quotas/
  approvals/
  releases/
evaluation/
  public_contracts/
  development/
  regression/
  protocols/
  statistics/
benchmarks/cornbench_vi_rl/
  DATA_CARD.md
  TASK_SCHEMA.json
  development/
  baseline_configs/
research/
  hypotheses/
  replications/
  negative_results/
  evidence_packages/
profiles/
  cpu-replay.yaml
  local-live-model.example.yaml
  isolated-evaluator.example.yaml
Week-00/ ... Week-18/           # giữ cấu trúc đang có
```

Đây là cây **đề xuất**, không phải danh sách thư mục đã tạo hoặc đã tồn tại. `control_plane/` tách folder chỉ thể hiện kiến trúc code; deployment phải áp quyền thật. Hidden answers và signing secrets nằm ngoài repo public và ngoài workspace agent.

### 17.2. Curriculum metadata làm nguồn cấu trúc duy nhất

Một module khai báo prerequisite, learning outcome, lab, test, source và trạng thái `designed/implemented/validated`. Roadmap/portal sinh từ metadata đó khi có generator; không ghi `validated` chỉ vì bài viết xong.

Ví dụ manifest:

```yaml
module_id: "R07"
title: "Risk–coverage và kiểm định cổng thống kê"
status: "designed"
prerequisites: ["probability-basics", "agent-evaluation", "dataset-splits"]
learning_outcomes:
  - "Phân biệt tỷ lệ lỗi quan sát với cận rủi ro"
  - "Giải thích vì sao retry cùng task không tạo mẫu độc lập"
  - "Chọn threshold không dùng confirmation set"
learner_gate:
  mode: "ai_off"
  task: "Giải thích trường hợp 100 mẫu không lỗi nhưng chưa đạt ngưỡng 1%"
system_gate:
  requires: ["input-validation-tests", "risk-coverage-report", "split-manifest"]
change_gate:
  requires: ["frozen-candidate", "independent-evaluation"]
sources: ["S12", "S13", "S14", "S15"]
```

### 17.3. Backlog theo dependency, không theo độ hào nhoáng

| Đợt / PR | Phạm vi | Điều kiện hoàn thành |
|---|---|---|
| P0.1 | Sửa claim sai đã nêu trong lịch rút gọn; thêm scope của chương trình | Không còn wording tạo hiểu nhầm validation/test, alignment hoặc tuyệt đối hóa |
| P0.2 | ENTRYPOINTS và curriculum mapping | Người học biết mình thuộc đường nào; giữ link cũ |
| P1.1 | Task contract, bounded runner, fake tools | Quota, deny và cancellation có tests |
| P1.2 | Evidence ledger và source snapshot | Claim có source span/version; thiếu nguồn có trạng thái rõ |
| P1.3 | Risk example + evaluation protocol | Code kiểm edge cases; tài liệu nêu giả định và giới hạn |
| P2.1 | Memory quarantine, scope, revoke | Bắt được stale/cross-tenant/poisoned-memory fixtures |
| P2.2 | R04 conditional lesson baseline | Có transfer và retention report, kể cả không gain |
| P2.3 | Protected evaluator + immutable candidate | Không sửa grader/đọc answer; digest mismatch bị chặn |
| P3.1 | Prompt/skill candidate search | Fixed budget, train/calibration/confirmation tách đúng |
| P3.2 | Shadow/promotion/rollback | Đúng version, scope, approval; replay incident thành công |
| P3.3 | CornBench-VI pilot + H1 | Dataset card, baselines, negative results, reproduction instructions |
| P4 | Offline adapter, multi-agent, advanced optimizer | Chỉ mở sau khi evidence và evaluation pipeline vững |

**PR đầu tiên nên nhỏ:** sửa học thuật + contract + evaluator skeleton. Không bắt đầu bằng một dashboard nhiều agent hoặc fine-tuning tốn GPU khi chưa biết “đúng” được chấm như thế nào.

### 17.4. CI chia thành hai loại

**Offline correctness CI:** schema, state transitions, quota/revoke, replay fixtures, immutable IDs, statistical code, docs/source references. Có thể chạy không API key.

**Live-model evaluation:** explicit budget, người có quyền khởi chạy, model revision, data license, nhiều trial và báo cáo. Không biến job này thành action mặc định chạy tốn phí với mọi pull request không được tin cậy.

CI với fake model chứng minh runner xử lý đúng những trace đã kiểm, không chứng minh model thật biết nghiên cứu. Hai loại kết quả có nhãn khác nhau trên portal.

### 17.5. Quản trị contribution

Người đóng góp bổ sung task phải nêu nguồn/giấy phép, scope và phương pháp xác định expected outcome. Thay đổi evaluator là PR độc lập, có reviewer; không lén thay evaluator trong cùng PR để candidate của mình thắng. Những thay đổi tiêu chuẩn hợp lý vẫn được phép, nhưng phải version và đánh giá lại baseline.

Agent được tạo đề xuất và mở artifact trong vùng được cấp quyền. Không tự merge nhánh bảo vệ, tự đổi permissions hay ký release. Khi làm việc trên repository nội bộ, quyền đọc mã nguồn cũng phải theo task, không suy ra từ việc đã đăng nhập một connector.

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
