# Mẫu protocol và hồ sơ phát hành

Nội dung tham khảo được hợp nhất ngày 30/09/2026. Những kết quả thực thi được ghi trong ví dụ gốc là thông tin kế thừa, chưa được chạy lại ở đây; không phải kết quả CornBench hoặc phép kiểm agent. Kết quả kiểm code hiện tại nằm riêng ở `evaluation/offline_check_report.json`.

## Phụ lục B — mẫu hồ sơ nghiên cứu và phát hành

### B.1. Research protocol trước thí nghiệm

```text
Question / task family:
Domain, source time window, permitted data:
Hypothesis and falsification condition:
Baseline and candidate:
What changes, what stays fixed:
Primary metric and non-compensable constraints:
Sampling unit and dependence assumptions:
Development / calibration / confirmation split:
Trial count, random seeds and stopping rule:
Total budget including failed trials:
Who labels outcomes and how disagreements are handled:
What the agent may edit / must not edit:
Expected failure modes:
How negative results will be reported:
```

### B.2. Evidence package trước review

```text
Candidate ID and immutable digest:
Code/model/prompt/skill/config versions:
Memory/corpus snapshot and lineage:
Task contract and allowed operating scope:
Dataset card, permission and license checks:
Development search history, including rejected candidates:
Independent evaluation protocol and evaluator version:
Sample counts, errors, coverage and uncertainty:
Retention / shift results:
Critical incidents and unresolved defects:
Resource cost and expected operational cost:
Approval identity, scope, expiry and action binding:
Shadow/canary plan:
Rollback and revocation procedure:
Known limits and claims explicitly not made:
```

### B.3. Khi nào phải chọn “chưa đủ bằng chứng”?

Khi sample quá nhỏ; dataset không đại diện; metric/label chưa rõ; input ngoài scope; nguồn mâu thuẫn chưa phân xử; quyền sử dụng dữ liệu chưa xác nhận; candidate đã thay đổi sau eval; hoặc evaluator có dấu hiệu bị overfit/contaminate.

“Chưa đủ bằng chứng” không phải đồng nghĩa candidate sai. Nó là lý do chưa trao quyền sử dụng theo tiêu chuẩn đang xét. Nhờ tách hai điều đó, hệ thống vẫn nghiên cứu tiếp trong sandbox mà không phải nới chuẩn vận hành.

---

<a id="sources"></a>
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
