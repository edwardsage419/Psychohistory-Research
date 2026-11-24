"""专项研究第一轮：确认硬约束投影覆盖不变量（2026-11-24）。

RESEARCH_CANDIDATE; synthetic development cases; no independent holdout.
Base main: e3dd603b0784c2e2b9edbef7056e82f727bddbad
PR #61 fixed head: 96b4293aa6b4d3c4cf16ece126e4dff07f25874f (Draft, not merged).
Source files under platform/future_model/src/psychohistory/:
decision_language.py blob fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4
decision_conversation_math.py blob aca1b4aa5cf4b4fd5b476e078b6e2aa9af197d30
decision_conversation.py blob 5ea705d597cf3e1f8e9e9b5080878f32c45719f7
decision_feasibility.py blob 6181d6c578c7ef251e9708d0ffcf65e95d35f88f
decision_local_ai.py blob 726b7a2e0da64af7037d892ac8bf508412deb5d6

Source inspection: language _numeric_claims emits yuan/month for recurring
costs; evidence_number expects yuan for cost/cost_max; build_state skips
unrepresentable caps; _project does not block already confirmed caps solely
because they cannot be projected; C028 evaluate treats all([]) as true.
Single-cap witness after successful extraction and confirmation: monthly
limit 3000; monthly costs 2500/3500. Narrow composition accepts both.
This is a source-fragment reproduction, not execution of the full application.
USD units are artificial confirmed-ledger stress cases, not claims that
the current Chinese parser supports USD. Other constraints, overrides and
coupled conditions are excluded. No claim about full user-text accuracy.

Candidate: preserve a stable ID for every active confirmed hard obligation;
map to calculation predicates with matching dimension, currency, period,
horizon and source; unresolved/missing mapping stays UNKNOWN; known fail
dominates; ACCEPT requires all obligations to pass, with an explicit trusted
empty declaration in the zero-obligation case. Do not silently coerce units.
Monthly cost is a distinct quantity from one-off cost. Numerical candidate
below covers only inclusive nonnegative same-currency point values.
Generalization: strict inequalities, ranges, multiple currencies, joint
constraints, conditional exceptions and user corrections need new tests.
Never substitute an inferred goal or value preference.

Local Python fragment reproduction executed: 27 unit/boundary cases,
current 11 correct/16 false accepts, candidate 27 correct/0 false accepts.
Two-obligation coverage enumeration: 25 cases, baseline 3 false accepts,
candidate 0; two explicit-empty controls. Counts are finite designed cases,
not generalization estimates. This archive embeds the exact upstream
BOUNDS, MEASURES and evidence_number fetched by fixed commit; local executed
copy was transcribed from that fragment. Archive itself has not run in CI.

Integration research direction:
(1) Compare JSON-only current Ollama transport with explicit schema
constraints and quote-offset grounding, retaining semantic validation;
schema does not prove the user's meaning. Ollama official docs:
https://github.com/ollama/ollama/blob/main/docs/capabilities/structured-outputs.mdx
(2) Separate retrieval ranking from executable registry authorization.
Use source path + version/hash + applicability + admission status, never
C-number alone (C035/C036 collisions recorded in V06_RESEARCH_INTEGRATION).
Source reading: Lewis et al., NeurIPS 2020 abstract, RAG, arXiv:2005.11401;
Manning et al., 2008, Introduction to Information Retrieval book index.
These are design references, not a demonstrated personal decision benefit.
(3) Each route returns missing preconditions and a receipt binding input
revision, source/version, all obligations, admitted method and output digest.
No candidate promotion or automatic external verification.

Next owner: independent acceptance workflow with unseen inputs and actual
PR execution; later Codex only with owner-approved complete version scope.
Mac/Qwen, iPhone, RAG quality, actual decision outcomes, and CI NOT_RUN.
No private data, training, new fees, merges, deployment or frozen changes.
Run: python research/decision_hub/2026-11-24-confirmed-constraint-projection-coverage.py
"""
from decimal import Decimal, InvalidOperation
from itertools import product
import json

# Verbatim upstream fragment (fixed blob above).
BOUNDS = {
    "cost_max": ("cost", "费用", "元", "<="),
    "income_min": ("income", "收入", "元/月", ">="),
    "hours_max": ("hours", "每周工时", "小时/周", "<="),
    "onsite_max": ("onsite", "每周到岗", "天/周", "<="),
    "move_allowed": ("move_required", "搬家要求", "逻辑值", "<="),
}
MEASURES = {
    "cost": ("费用", "元", "min", "yuan"),
    "income": ("收入", "元/月", "max", "yuan/month"),
    "hours": ("每周工时", "小时/周", "min", "hours/week"),
    "onsite": ("每周到岗", "天/周", "min", "days/week"),
    "move_required": ("搬家要求", "逻辑值", "min", ""),
}


def evidence_number(item):
    if item["field"] in {"move_allowed", "move_required"}:
        return {"yes": Decimal(1), "no": Decimal(0)}.get(item["value"])
    field = BOUNDS.get(item["field"], (item["field"],))[0]
    if item["field"] == "move_if_onsite_max":
        field = "onsite"
    expected = MEASURES.get(field)
    if not expected or item["unit"] != expected[-1]:
        return None
    try:
        number = Decimal(item["value"])
        if number.is_finite() and 0 <= number <= Decimal("100000000000") and number.as_tuple().exponent >= -8:
            return number
    except InvalidOperation:
        pass
    return None

def current_projection(cap, value):
    threshold = evidence_number(cap)
    if threshold is None:
        checks = []
    else:
        x = evidence_number(value)
        checks = ['UNKNOWN' if x is None else 'CERTAIN_PASS' if x <= threshold else 'CERTAIN_FAIL']
    return 'REJECT' if 'CERTAIN_FAIL' in checks else 'ACCEPT' if all(c == 'CERTAIN_PASS' for c in checks) else 'UNRESOLVED'

def candidate(cap, value):
    if cap['unit'] not in {'yuan', 'yuan/month'} or value['unit'] != cap['unit']:
        return 'UNRESOLVED'
    try:
        t, x = Decimal(cap['value']), Decimal(value['value'])
        if any(not z.is_finite() or z < 0 or z > Decimal('100000000000') or z.as_tuple().exponent < -8 for z in (t,x)):
            return 'UNRESOLVED'
    except InvalidOperation:
        return 'UNRESOLVED'
    return 'ACCEPT' if x <= t else 'REJECT'

def gate(obligations, projected, explicit_empty=False):
    if any(projected.get(k) == 'CERTAIN_FAIL' for k in obligations):
        return 'REJECT'
    if not obligations:
        return 'ACCEPT' if explicit_empty else 'UNRESOLVED'
    return 'ACCEPT' if all(projected.get(k) == 'CERTAIN_PASS' for k in obligations) else 'UNRESOLVED'

def run():
    rows = []
    for cu, vu, amount in product(('yuan','yuan/month','USD/month'), ('yuan','yuan/month','USD/month'), ('2500','3000','3500')):
        cap = {'field':'cost_max','unit':cu,'value':'3000'}
        val = {'field':'cost','unit':vu,'value':amount}
        expected = ('REJECT' if Decimal(amount)>3000 else 'ACCEPT') if cu==vu and cu in {'yuan','yuan/month'} else 'UNRESOLVED'
        rows.append(dict(cap_unit=cu,value_unit=vu,amount=amount,expected=expected,current=current_projection(cap,val),candidate=candidate(cap,val)))
    counts = dict(cases=len(rows),current_correct=sum(r['current']==r['expected'] for r in rows),candidate_correct=sum(r['candidate']==r['expected'] for r in rows),current_false_accepts=sum(r['current']=='ACCEPT' and r['expected']!='ACCEPT' for r in rows),candidate_false_accepts=sum(r['candidate']=='ACCEPT' and r['expected']!='ACCEPT' for r in rows))
    if tuple(counts.values()) != (27,11,27,16,0):
        raise RuntimeError(counts)
    pairs = []
    for a,b in product(('CERTAIN_PASS','CERTAIN_FAIL','UNKNOWN','POSSIBLE',None), repeat=2):
        known = {k:v for k,v in (('A',a),('B',b)) if v is not None}
        old = 'REJECT' if 'CERTAIN_FAIL' in known.values() else 'ACCEPT' if all(x=='CERTAIN_PASS' for x in known.values()) else 'UNRESOLVED'
        new = gate(('A','B'),known)
        expected = 'REJECT' if 'CERTAIN_FAIL' in (a,b) else 'ACCEPT' if (a,b)==('CERTAIN_PASS','CERTAIN_PASS') else 'UNRESOLVED'
        if new != expected:
            raise RuntimeError((a,b,new,expected))
        pairs.append(dict(a=a,b=b,current=old,candidate=new,expected=expected))
    false_accepts = sum(r['current']=='ACCEPT' and r['expected']!='ACCEPT' for r in pairs)
    if false_accepts!=3 or gate((),{},True)!='ACCEPT' or gate((),{},False)!='UNRESOLVED':
        raise RuntimeError('coverage boundary')
    print(json.dumps(dict(unit_counts=counts,coverage_cases=len(pairs),coverage_baseline_false_accepts=false_accepts,coverage_candidate_false_accepts=0,empty_controls=2,unit_rows=rows,coverage_rows=pairs),ensure_ascii=False,indent=2))

if __name__ == '__main__':
    run()
