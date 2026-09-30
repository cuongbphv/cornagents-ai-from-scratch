"""Offline educational reference. No live model or production isolation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from cornagents.education import (research_contract, evidence_status, MemoryStore,
    parse_amount, validate_candidate, search_under_budget, risk_report, evaluate_frozen,
    digest, low_rank_update, DurableToy, ResearchBudget, ReleaseToy, cohort_report)

def run(data):
    job = DurableToy(ResearchBudget(data['limit']))
    states = []
    for action in data['actions']:
        if action.get('cancel'):
            job.budget.cancelled = True
            states.append('CANCELLED')
        elif action.get('revoke'):
            job.authorized = False
            states.append('REVOKED')
        else:
            try:
                states.append(job.execute(**action))
            except (ValueError, PermissionError, RuntimeError) as error:
                states.append(type(error).__name__)
    return {'states': states, 'effects': len(job.effects), 'spent': job.budget.used}
