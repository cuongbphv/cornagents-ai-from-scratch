"""Offline educational reference. No live model or production isolation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from cornagents.education import (research_contract, evidence_status, MemoryStore,
    parse_amount, validate_candidate, search_under_budget, risk_report, evaluate_frozen,
    digest, low_rank_update, DurableToy, ResearchBudget, ReleaseToy, cohort_report)

def run(data):
    store = MemoryStore()
    store.propose('fact', 'A', 'fact text', ['source'], 10)
    store.propose('summary', 'A', 'summary', ['fact'], 10)
    if data['reviewed']:
        store.activate('fact', True)
        store.activate('summary', True)
    if data['revoke']:
        store.revoke_source('source')
    try:
        text = store.read('summary', data['reader'], data['now'])
    except PermissionError:
        text = 'DENIED'
    return {'read': text, 'states': [store.records[k]['state'] for k in ['fact','summary']]}
