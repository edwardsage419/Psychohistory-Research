#!/usr/bin/env python3
"""F009 phase20: finite artificial appeal sequences, standard library only."""
import itertools, json
T=(5,12,20,29)
OPTIONS=('NONE','REPEAT','NEW_EVIDENCE','APPROVED_HOLD')
BASE=30
HOLD_UNTIL=45

def naive(seq):
    expiry=BASE
    for t,event in zip(T,seq):
        if event!='NONE':
            expiry=max(expiry,t+30)
    return expiry

def candidate(seq):
    expiry=BASE
    reviews=[]
    for t,event in zip(T,seq):
        if event=='NEW_EVIDENCE':
            reviews.append(('REVIEW_NEW_EVIDENCE',t))
        elif event=='REPEAT':
            reviews.append(('REVIEW_REPEAT_IN_CONTEXT',t))
        elif event=='APPROVED_HOLD':
            expiry=max(expiry,HOLD_UNTIL)
            reviews.append(('HUMAN_APPROVED_BOUNDED_HOLD',t))
    return expiry,reviews

checks=0
for seq in itertools.product(OPTIONS,repeat=4):
    n=naive(seq)
    c,reviews=candidate(seq)
    assert c in (30,45);checks+=1
    assert c==45 if 'APPROVED_HOLD' in seq else c==30;checks+=1
    assert n>=30;checks+=1
    assert len(reviews)==sum(x!='NONE' for x in seq);checks+=1
    assert all(x[0]!='AUTOMATIC_REFUSAL' for x in reviews);checks+=1
all_repeat=('REPEAT',)*4
assert naive(all_repeat)==59;checks+=1
assert candidate(all_repeat)[0]==30;checks+=1
assert candidate(('NEW_EVIDENCE','NONE','NONE','NONE'))[0]==30;checks+=1
assert candidate(('APPROVED_HOLD','NONE','NONE','NONE'))[0]==45;checks+=1
assert candidate(('NONE',)*4)[0]==30;checks+=1
cases=list(itertools.product(OPTIONS,repeat=4))
print(json.dumps({'cases':len(cases),'assertions':checks,
                  'naive_extended':sum(naive(x)>BASE for x in cases),
                  'candidate_extended':sum(candidate(x)[0]>BASE for x in cases),
                  'all_repeat_naive_expiry':naive(all_repeat),
                  'all_repeat_candidate_expiry':candidate(all_repeat)[0],
                  'candidate_hold_expiry':HOLD_UNTIL,
                  'scope':'fictional policy; not legal compliance or actual attack rates'},indent=2))
