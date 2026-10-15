#!/usr/bin/env python3
"""R065 Phase E: retrospective day89 source-reset analytic prediction bound.

No third-party participant-level rows are retained. Pure Python 3.10+.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

SOURCE_BLOB = '01bf211468abe093618dfa5e5c39e883230c9c03'
CRITICAL_DAYS = (4, 21, 38, 55, 72, 89, 106, 123)


def parse_verified(raw):
    digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if digest != SOURCE_BLOB:
        raise ValueError('source Git blob identity mismatch')
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline='')))


def heldout_prediction(y, total_copies, n, alpha=4):
    if y not in (0,1) or n < 2 or not 0 <= total_copies <= n or not 0 < alpha:
        raise ValueError('invalid predictive counts')
    if total_copies < y or total_copies-y > n-1:
        raise ValueError('held-out label incompatible with total')
    return (total_copies-y+alpha)/(n-1+2*alpha)


def analyze(rows, draws=20000, seed=20261016, min_subjects=10):
    if draws < 3:
        raise ValueError('draws must be at least three')
    fields = ('participant_id','critical','day','accurate','copied','stakes',
              'counterbalance','comprehension_check_repetitions')
    people = {}
    for row in rows:
        if any(row.get(field) in (None, '', 'NA', 'NaN', 'nan') for field in fields):
            raise ValueError('missing required source field')
        pid = row['participant_id']
        acc, copied, flag = map(float,(row['accurate'],row['copied'],row['critical']))
        reps, day = float(row['comprehension_check_repetitions']),float(row['day'])
        if (acc not in (0,1) or copied not in (0,1) or flag not in (0,1)
                or not math.isfinite(reps) or not day.is_integer()
                or row['stakes'] not in ('high','low')):
            raise ValueError('invalid source measurement')
        p = people.setdefault(pid,{'n':0,'accuracy':0,'reps':0,'trials':[]})
        p['n'] += 1
        p['accuracy'] += acc
        p['reps'] += reps
        if flag:
            if acc+copied != 1:
                raise ValueError('critical outcome not complementary')
            p['trials'].append((int(day),row['stakes'],int(copied),row['counterbalance']))
    excluded={'accuracy':0,'comprehension':0,'union':0,'rows':0}
    diagnostic=[]
    for p in people.values():
        bad_a = p['accuracy']/p['n'] < .45
        bad_c = p['reps']/p['n'] > 2
        excluded['accuracy'] += bad_a
        excluded['comprehension'] += bad_c
        excluded['union'] += bad_a or bad_c
        if bad_a or bad_c:
            excluded['rows'] += p['n']
            continue
        trial=sorted(p['trials'])
        if tuple(x[0] for x in trial) != CRITICAL_DAYS:
            raise ValueError('critical schedule is not eight fixed days')
        if sum(x[1]=='high' for x in trial) != 4:
            raise ValueError('critical stake imbalance')
        diagnostic.append(trial[5][2])
    n=len(diagnostic)
    if n<min_subjects:
        raise ValueError('too few eligible subjects')
    copies=sum(diagnostic)
    values=[]
    for y in diagnostic:
        q=heldout_prediction(y,copies,n)
        alternative=-(y*math.log(q)+(1-y)*math.log1p(-q))
        values.append((math.log(2)-alternative,.25-(y-q)**2))
    def avg(a,k):
        return sum(x[k] for x in a)/len(a)
    state=seed & 0xffffffff
    def rand():
        nonlocal state
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        state &= 0xffffffff
        return state/4294967296.0
    bs=[[],[]]
    for _ in range(draws):
        subtotal=[0.,0.]
        for _ in values:
            x=values[int(rand()*n)]
            subtotal[0]+=x[0]
            subtotal[1]+=x[1]
        bs[0].append(subtotal[0]/n)
        bs[1].append(subtotal[1]/n)
    ci=[]
    for a in bs:
        a.sort()
        ci.append([a[math.floor(.025*(draws-1))],a[math.ceil(.975*(draws-1))]])
    return {
        'source_blob_sha1':SOURCE_BLOB,'raw_rows':len(rows),'raw_participants':len(people),
        'eligible_participants':n,'excluded':excluded,'critical_day':89,
        'copied_day89':copies,'copy_rate_day89':copies/n,
        'uniform_logloss':math.log(2),'uniform_brier':.25,
        'heldout_loo_logloss':math.log(2)-avg(values,0),
        'heldout_loo_brier':.25-avg(values,1),
        'uniform_minus_loo_mean_logloss':avg(values,0),
        'uniform_minus_loo_mean_brier':avg(values,1),
        'paired_bootstrap_95':{'logloss':ci[0],'brier':ci[1]},
        'bootstrap_seed':seed,'bootstrap_draws':draws,
        'classification':'POST_HOC_BOUND; SEVEN_AUTHOR_MODEL_FITS_NOT_REPRODUCED',
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=analyze(parse_verified(args.source.read_bytes()))
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'eligible_participants':result['eligible_participants'],'status':'PASS'}))


if __name__=='__main__':
    main()
