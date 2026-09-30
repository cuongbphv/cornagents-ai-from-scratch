"""Finite, offline examples for CornAgents.AI learning labs.

No model calls, network, secrets, real business effects or production isolation.
These functions check selected contracts; they do not establish agent reliability.
"""
from dataclasses import dataclass, field
import hashlib
import json
import math
import re


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def research_contract(question, scope, tools, budget):
    if not question.strip() or not scope or not tools:
        raise ValueError("Question, scope and allowed tools are required")
    if type(budget) is not int or budget <= 0:
        raise ValueError("Budget must be a positive integer")
    return dict(question=question, scope=list(scope), tools=list(tools), budget=budget)


def evidence_status(claim, sources):
    """Uses fixture labels, not a claim-entailment model or an authority oracle."""
    related = [s for s in sources if s.get("claim") == claim]
    support = {s["origin"] for s in related if s["relation"] == "support"}
    contradict = {s["origin"] for s in related if s["relation"] == "contradict"}
    status = "CONFLICT" if support and contradict else "SUPPORTED" if support else "CONTRADICTED" if contradict else "INSUFFICIENT"
    return {"status": status, "independent_origins": len(support)}


@dataclass
class ResearchBudget:
    limit: int
    used: int = 0
    cancelled: bool = False

    def __post_init__(self):
        if type(self.limit) is not int or self.limit <= 0 or self.used != 0:
            raise ValueError("Positive integer limit and fresh counter required")

    def spend(self, cost=1):
        if type(cost) is not int or cost <= 0:
            raise ValueError("Positive integer cost required")
        if self.cancelled or self.used + cost > self.limit:
            raise PermissionError("Cancelled or quota exhausted")
        self.used += cost


@dataclass
class MemoryStore:
    records: dict = field(default_factory=dict)

    def propose(self, key, tenant, text, sources, valid_until):
        if key in self.records:
            raise ValueError("Use a new immutable record ID")
        self.records[key] = dict(tenant=tenant, text=text, sources=list(sources),
                                 valid_until=valid_until, state="QUARANTINED")

    def activate(self, key, reviewed):
        record = self.records[key]
        if not reviewed or not record["sources"] or record["state"] != "QUARANTINED":
            raise PermissionError("Evidence and external review required")
        record["state"] = "ACTIVE_SCOPED"

    def read(self, key, tenant, now):
        record = self.records[key]
        if (record["tenant"] != tenant or record["state"] != "ACTIVE_SCOPED"
                or now >= record["valid_until"]):
            raise PermissionError("Not active, expired or outside tenant")
        return record["text"]

    def revoke_source(self, source):
        affected = {source}
        if source in self.records:
            self.records[source]["state"] = "REVOKED"
        changed = True
        while changed:
            changed = False
            for key, record in self.records.items():
                if key not in affected and any(s in affected for s in record["sources"]):
                    affected.add(key)
                    record["state"] = "REVOKED"
                    changed = True
        return sorted(affected - {source})


UNITS = {"đồng": 1, "nghìn đồng": 1000, "triệu đồng": 1000000, "tỷ đồng": 1000000000}


def parse_amount(text):
    """Only nonnegative integer strings and exact, explicit units in this grammar."""
    match = re.fullmatch(r"(0|[1-9][0-9]*) (đồng|nghìn đồng|triệu đồng|tỷ đồng)", text)
    if not match:
        return {"status": "AMBIGUOUS", "raw": text}
    return {"status": "OK", "value": int(match[1]) * UNITS[match[2]], "unit": "đồng"}


def validate_candidate(candidate, allowed_paths):
    if not candidate.get("edits") or not set(candidate["edits"]).issubset(set(allowed_paths)):
        raise PermissionError("Edits outside the experiment allowlist")
    if candidate.get("reads_hidden_answers") or candidate.get("adds_tools"):
        raise PermissionError("Cannot read hidden answers or expand authority")
    return digest(candidate)


def search_under_budget(trials, total_budget):
    budget = ResearchBudget(total_budget)
    history = []
    for trial in trials:
        try:
            budget.spend(trial["cost"])
        except PermissionError:
            break
        history.append(dict(trial))
    eligible = [t for t in history if t["status"] == "OK"]
    best = max(eligible, key=lambda t: t["score"]) if eligible else None
    return {"best": best, "history": history, "spent": budget.used}


def _probability(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(name)
    if not math.isfinite(value) or not 0 < value < 1:
        raise ValueError(name)
    return value


def cp_upper(errors, trials, alpha=0.05):
    """One-sided exact binomial bound; finite-sample numerical teaching implementation.

    Caller must establish fixed policy, independent representative observations and
    valid sampling/stopping protocol. This function cannot establish those assumptions.
    """
    if type(errors) is not int or type(trials) is not int:
        raise TypeError("Counts must be integers, not booleans")
    if not 0 <= errors <= trials:
        raise ValueError("Require 0 <= errors <= trials")
    _probability(alpha, "alpha")
    if trials == 0 or errors == trials:
        return 1.0
    if errors == 0:
        return -math.expm1(math.log(alpha) / trials)
    def log_cdf(p):
        terms = [math.lgamma(trials + 1) - math.lgamma(i + 1) - math.lgamma(trials - i + 1)
                 + i * math.log(p) + (trials - i) * math.log1p(-p)
                 for i in range(errors + 1)]
        top = max(terms)
        return top + math.log(sum(math.exp(t - top) for t in terms))
    lo, hi = 0.0, 1.0
    target = math.log(alpha)
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid == lo or mid == hi:
            break
        if log_cdf(mid) > target:
            lo = mid
        else:
            hi = mid
    return hi


def risk_report(total, accepted, errors, allowed_error, alpha=0.05):
    if any(type(x) is not int for x in (total, accepted, errors)):
        raise TypeError("Integer counts required")
    if not 0 <= errors <= accepted <= total:
        raise ValueError("Invalid counts")
    _probability(allowed_error, "allowed_error")
    upper = cp_upper(errors, accepted, alpha)
    return {"total": total, "accepted": accepted, "errors": errors,
            "coverage": accepted / total if total else None,
            "accepted_risk": errors / accepted if accepted else None,
            "upper": upper,
            "status": "INSUFFICIENT_EVIDENCE" if not accepted else
                      "PASS_STATISTICAL_GATE" if upper <= allowed_error else "NOT_PASSED"}


def evaluate_frozen(artifact, expected_digest, cases):
    """Fixture evaluator. No process isolation or protection from an OS administrator."""
    if digest(artifact) != expected_digest:
        raise PermissionError("Artifact differs from the evaluated snapshot")
    return [parse_amount(case["input"]) == case["expected"] for case in cases]


def low_rank_update(weights, left, right):
    if len(weights) != len(left) or not weights:
        raise ValueError("Incompatible row dimensions")
    cols = len(weights[0]); rank = len(right)
    if not rank or any(len(row) != cols for row in weights + right):
        raise ValueError("Incompatible column dimensions")
    if any(len(row) != rank for row in left):
        raise ValueError("Incompatible rank dimensions")
    return [[weights[i][j] + sum(left[i][r] * right[r][j] for r in range(rank))
             for j in range(cols)] for i in range(len(weights))]


@dataclass
class DurableToy:
    budget: ResearchBudget
    effects: dict = field(default_factory=dict)
    authorized: bool = True
    unresolved: set = field(default_factory=set)

    def execute(self, key, payload, lose_ack=False, outcome_unknown=False):
        if not self.authorized or self.budget.cancelled:
            raise PermissionError("Authority must be checked after resume")
        if key in self.unresolved:
            raise RuntimeError("UNKNOWN_OUTCOME: reconcile before retry")
        if key in self.effects:
            if self.effects[key] != payload:
                raise ValueError("Idempotency key reused for a different action")
            return "RECONCILED"
        self.budget.spend()
        if outcome_unknown:
            self.unresolved.add(key)
            return "UNKNOWN_OUTCOME"
        self.effects[key] = payload
        return "ACK_LOST" if lose_ack else "SUCCESS"


@dataclass
class ReleaseToy:
    active: str = "baseline"
    previous: str | None = None

    def promote(self, artifact, evaluated_digest, approved_digest, scope, has_violation=False):
        current = digest(artifact)
        if (has_violation or not scope or current != evaluated_digest
                or current != approved_digest):
            raise PermissionError("Require matching evaluation, approval and valid scope")
        self.previous, self.active = self.active, current
        return self.active

    def rollback(self):
        if self.previous is None:
            raise ValueError("No previous release")
        self.active, self.previous = self.previous, self.active
        return self.active


def cohort_report(cases):
    """Only deterministic parser outcomes on explicitly supplied synthetic fixtures."""
    results = [parse_amount(c["input"]) for c in cases]
    correct = [result == case["expected"] for result, case in zip(results, cases)]
    return {"label": "SYNTHETIC_FIXTURE_REPLAY", "tasks": len(cases),
            "matched": sum(correct), "results": results,
            "success_rate": sum(correct) / len(cases) if cases else None}
