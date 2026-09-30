# Ví dụ thống kê tham khảo

Nội dung tham khảo được hợp nhất ngày 30/09/2026. Những kết quả thực thi được ghi trong ví dụ gốc là thông tin kế thừa, chưa được chạy lại ở đây; không phải kết quả CornBench hoặc phép kiểm agent. Kết quả kiểm code hiện tại nằm riêng ở `evaluation/offline_check_report.json`.

## Phụ lục A — mã thống kê đã chạy thử

### A.1. Phạm vi

Đoạn code dưới đây tính cận trên lỗi nhị thức một phía và đánh giá **riêng một cổng thống kê**. Nó không kiểm tra privacy, permissions, dataset độc lập, quality of labels hoặc đủ điều kiện deploy. Những giả định đó không thể xác nhận chỉ từ hai con số `errors` và `trials`.

Môi trường đã chạy: **Python 3.13.5 / SciPy 1.17.0**. Thư viện SciPy cần có trong môi trường; đây là phiên bản đã thử, không phải khẳng định là phiên bản mới nhất.

Lưu đoạn đầu thành `risk_gate.py`, đoạn test thành `test_risk_gate.py` cùng thư mục, rồi chạy:

```bash
python risk_gate.py
python -m unittest -v test_risk_gate
```

### A.2. Implementation

```python
"""A statistical evidence check, NOT a deployment or safety authorization."""
from dataclasses import dataclass
import math
from numbers import Real
from scipy.stats import beta


def _probability(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, not a boolean")
    value = float(value)
    if not math.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError(f"{name} must be finite and strictly between 0 and 1")
    return value


def _counts(errors: int, trials: int) -> None:
    if type(errors) is not int or type(trials) is not int:
        raise TypeError("errors and trials must be Python integers, not booleans")
    if not 0 <= errors <= trials:
        raise ValueError("require 0 <= errors <= trials")


def cp_upper(errors: int, trials: int, alpha: float = 0.05) -> float:
    """One-sided (1-alpha) Clopper-Pearson upper binomial error bound.

    Requires a fixed policy and a suitable independent Bernoulli sample.
    Input validation cannot establish these scientific assumptions.
    No observations return the conservative upper bound 1.0.
    """
    _counts(errors, trials)
    alpha = _probability(alpha, "alpha")
    if trials == 0 or errors == trials:
        return 1.0
    if errors == 0:
        return -math.expm1(math.log(alpha) / trials)
    # isf avoids computing 1-alpha, which can round to 1 for tiny alpha.
    result = float(beta.isf(alpha, errors + 1, trials - errors))
    if not math.isfinite(result):
        raise ArithmeticError("non-finite quantile; do not approve")
    return result


@dataclass(frozen=True)
class RiskAssessment:
    status: str
    error_upper_bound: float
    allowed_error: float
    confidence_level: float
    errors: int
    trials: int


def assess_error_risk(
    errors: int, trials: int, allowed_error: float, alpha: float = 0.05
) -> RiskAssessment:
    allowed_error = _probability(allowed_error, "allowed_error")
    upper = cp_upper(errors, trials, alpha)
    if trials == 0:
        status = "INSUFFICIENT_EVIDENCE"
    else:
        status = "PASS_STATISTICAL_GATE" if upper <= allowed_error else "NOT_PASSED"
    return RiskAssessment(status, upper, allowed_error, 1.0 - alpha, errors, trials)


if __name__ == "__main__":
    for n in (0, 100, 299, 2995):
        result = assess_error_risk(0, n, allowed_error=0.01)
        print(f"n={n:4d}  upper={result.error_upper_bound:.8f}  {result.status}")
```

### A.3. Unit tests

```python
import math
import unittest
from scipy.stats import binomtest
from risk_gate import cp_upper, assess_error_risk


class RiskGateTests(unittest.TestCase):
    def test_no_data_is_not_pass(self):
        self.assertEqual(assess_error_risk(0, 0, .01).status, 'INSUFFICIENT_EVIDENCE')
        self.assertEqual(cp_upper(0, 0), 1.0)

    def test_zero_errors_closed_form(self):
        self.assertAlmostEqual(cp_upper(0, 100), 1 - .05 ** (1/100), places=14)

    def test_one_percent_threshold(self):
        self.assertGreater(cp_upper(0, 298), .01)
        self.assertLessEqual(cp_upper(0, 299), .01)

    def test_point_one_percent_threshold(self):
        self.assertGreater(cp_upper(0, 2994), .001)
        self.assertLessEqual(cp_upper(0, 2995), .001)

    def test_agrees_with_scipy_exact_one_sided(self):
        for k, n in ((0, 10), (1, 100), (7, 100), (20, 20)):
            with self.subTest(k=k, n=n):
                ci = binomtest(k, n, alternative='less').proportion_ci(
                    confidence_level=.95, method='exact')
                self.assertAlmostEqual(cp_upper(k, n), ci.high, places=10)

    def test_all_errors(self):
        self.assertEqual(cp_upper(10, 10), 1.0)

    def test_monotonic_in_errors(self):
        values = [cp_upper(k, 50) for k in range(51)]
        self.assertTrue(all(a <= b for a, b in zip(values, values[1:])))

    def test_more_clean_observations_lower_bound(self):
        self.assertGreater(cp_upper(0, 100), cp_upper(0, 1000))

    def test_invalid_counts(self):
        for k, n in ((-1, 10), (2, 1), (0, -1)):
            with self.subTest(k=k, n=n), self.assertRaises(ValueError):
                cp_upper(k, n)

    def test_bool_or_float_counts_rejected(self):
        for k, n in ((True, 10), (0, False), (0., 10), (0, 10.)):
            with self.subTest(k=k, n=n), self.assertRaises(TypeError):
                cp_upper(k, n)

    def test_invalid_alpha(self):
        for alpha in (0, 1, -1, float('nan'), float('inf')):
            with self.subTest(alpha=alpha), self.assertRaises(ValueError):
                cp_upper(0, 100, alpha)
        with self.assertRaises(TypeError):
            cp_upper(0, 100, True)

    def test_invalid_target(self):
        for target in (0, 1, float('nan')):
            with self.subTest(target=target), self.assertRaises(ValueError):
                assess_error_risk(0, 100, target)

    def test_higher_confidence_more_conservative(self):
        self.assertGreater(cp_upper(1, 100, .01), cp_upper(1, 100, .05))

    def test_pass_does_not_mean_safety_authorization(self):
        result = assess_error_risk(0, 299, .01)
        self.assertEqual(result.status, 'PASS_STATISTICAL_GATE')
        self.assertFalse(hasattr(result, 'deploy_authorized'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

### A.4. Kết quả thực thi trong phiên soạn

```text
n=   0  upper=1.00000000  INSUFFICIENT_EVIDENCE
n= 100  upper=0.02951305  NOT_PASSED
n= 299  upper=0.00996915  PASS_STATISTICAL_GATE
n=2995  upper=0.00099974  PASS_STATISTICAL_GATE

Unit tests: 14 tests, OK.
```

Các kiểm tra gồm edge cases, no data, tham số không hợp lệ, tính đơn điệu, ngưỡng 1%/0,1% và đối chiếu với `scipy.stats.binomtest(..., alternative="less")` dùng CI exact một phía. Giá trị alpha và target trong example không tự áp dụng cho nhiều candidate hoặc nhiều subgroup.

Không chuyển `PASS_STATISTICAL_GATE` thành `DEPLOY_AUTHORIZED`. Release controller còn phải kiểm provenance, coverage, regression, quyền, impact, approval và scope. Đây là phân biệt bắt buộc của bài R07/R11.

---

<a id="appendix-b"></a>
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
