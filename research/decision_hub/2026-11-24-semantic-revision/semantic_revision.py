"""Research candidate; transcribed bounded source fragments, not full PR execution."""
import re
import operator
import itertools
import json

_HEDGE = r"可能|大概|大约|估计|大致|大抵|左右|上下|也许|听说|好像|不知道|不确定|未核实|尚未确认|未必|未定|暂不清楚|我猜|看起来|是否"
# Exact source fragment: decision_language.py lines 307-311.
def _qualify(clause: str, base_kind: str, context: str, strict: bool = False) -> str:
    if context:
        return context
    if re.search(_HEDGE, clause):
        return "estimate"
    return "strict_constraint" if strict and base_kind == "constraint" else base_kind

OPS = {'<':operator.lt, '<=':operator.le, '>':operator.gt, '>=':operator.ge}
def old_op(direction, kind):
    # decision_conversation_math.py BOUNDS plus strict role branch.
    op = '<=' if direction == 'upper' else '>='
    if kind == 'strict_constraint':
        op = '>' if op == '>=' else '<'
    return op

def reference_op(direction, strict):
    return ('<' if strict else '<=') if direction == 'upper' else ('>' if strict else '>=')

def decision(p):
    return 'UNRESOLVED' if p is None else 'ACCEPT' if p else 'REJECT'

def baseline_exception(scope, onsite, family):
    # decision_language.py interpret: sufficient gate, other guards held true.
    sufficient = re.search(r"只要|那么|则|就", scope) and not re.search(
        r"除非|才(?:能|可以)|同时|而且|并且|还要|还需|以及|且", scope,
    )
    # Assumes confirmed move_allowed=no and move_required=yes; measurement known iff onsite is not None.
    return decision(onsite if sufficient else False)

def all_completions(*values):
    results = {all(xs) for xs in itertools.product(*[(False,True) if x is None else (x,) for x in values])}
    return decision(next(iter(results)) if len(results)==1 else None)

def run():
    rows=[]
    for direction, strict, context, offset in itertools.product(('upper','lower'),(False,True),('','revision'),(-1,0,1)):
        threshold=3000; x=threshold+offset
        clause='预算修订' if context else '预算'
        kind=_qualify(clause,'constraint',context,strict)
        old=decision(OPS[old_op(direction,kind)](x,threshold))
        expected=decision(OPS[reference_op(direction,strict)](x,threshold))
        # Candidate records comparator independently of update operation.
        candidate=decision(OPS[reference_op(direction,strict)](x,threshold))
        rows.append(dict(direction=direction,strict=strict,context=context,offset=offset,role=kind,old=old,expected=expected,candidate=candidate))
    scope='只要每周到岗不超过2天，就可以搬家，但前提是家人同意'
    branches=[]
    for a,b in itertools.product((False,True,None),repeat=2):
        old=baseline_exception(scope,a,b)
        expected=all_completions(a,b)
        # Candidate preserves the explicit conjunction; Kleene AND on independent predicates.
        candidate=decision(False if False in (a,b) else True if (a,b)==(True,True) else None)
        branches.append(dict(onsite=a,family=b,old=old,expected=expected,candidate=candidate))
    groups=[]
    for direction,roles in itertools.product(('upper','lower'),(('strict_constraint','constraint'),('constraint','strict_constraint'))):
        # Equal scope and numeric value: _group reports CONFIRMED; active dict uses last claim.
        old=decision(OPS[old_op(direction,roles[-1])](3000,3000))
        # For two explicitly conjoined hard requirements, both must hold.
        expected=decision(all(OPS[old_op(direction,r)](3000,3000) for r in roles))
        candidate=expected
        groups.append(dict(direction=direction,roles=roles,old=old,expected=expected,candidate=candidate))
    def stats(rs):
        return dict(cases=len(rs),baseline_correct=sum(r['old']==r['expected'] for r in rs),candidate_correct=sum(r['candidate']==r['expected'] for r in rs),baseline_false_accept=sum(r['old']=='ACCEPT' and r['expected']!='ACCEPT' for r in rs),candidate_false_accept=sum(r['candidate']=='ACCEPT' and r['expected']!='ACCEPT' for r in rs))
    result=dict(revision=stats(rows),exception=stats(branches),conjunction=stats(groups),rows=rows,branches=branches,groups=groups)
    assert result['revision']==dict(cases=24,baseline_correct=22,candidate_correct=24,baseline_false_accept=2,candidate_false_accept=0)
    assert result['exception']==dict(cases=9,baseline_correct=6,candidate_correct=9,baseline_false_accept=2,candidate_false_accept=0)
    assert result['conjunction']==dict(cases=4,baseline_correct=2,candidate_correct=4,baseline_false_accept=2,candidate_false_accept=0)
    return result
if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
