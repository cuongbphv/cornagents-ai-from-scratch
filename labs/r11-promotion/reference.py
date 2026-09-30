"""Offline educational reference. No live model or production isolation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from cornagents.education import (research_contract, evidence_status, MemoryStore,
    parse_amount, validate_candidate, search_under_budget, risk_report, evaluate_frozen,
    digest, low_rank_update, DurableToy, ResearchBudget, ReleaseToy, cohort_report)

def run(data):
    release = ReleaseToy()
    release.promote(data['artifact'], digest(data['evaluated']), digest(data['approved']),
                    data['scope'], data.get('violation', False))
    if data.get('rollback'):
        release.rollback()
    return {'active': release.active}
