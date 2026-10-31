#!/usr/bin/env python3
"""Independent, nonblind microstate audit of R309 S105 artificial two-step SIR.

Uses no import from the R309 model or S105 producer. Validation uses explicit exceptions,
including under Python -O. No clinical or social observations.
"""
import argparse, copy, csv, hashlib, json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

PARAMS=(F(0),F(1,2),F(1))
STATES=tuple((s,i,5-s-i) for s in range(6) for i in range(6-s))
WORLDS=tuple((s,i,r,p,q) for s,i,r in STATES for p in PARAMS for q in PARAMS)
ORIGINAL_SHA='9470c1e1c880f51da5c11377b6cc8be7f799542d0cebd1f82d4fc3539cabd134'

def name(w):
    s,i,r,p,q=w
    return f'S={s}|I={i}|R={r}|contact_p={p}|recovery_q={q}'

def micro_kernel(w):
    """Directly enumerate independent binary contact and old-recovery assignments."""
    s,i,r,p,q=w
    edges=s*i
    out=defaultdict(F)
    for cmask in range(1<<edges):
        n=cmask.bit_count()
        cw=p**n*(1-p)**(edges-n)
        x=sum(bool((cmask>>(a*i))&((1<<i)-1)) for a in range(s)) if i else 0
        for rmask in range(1<<i):
            y=rmask.bit_count()
            rw=q**y*(1-q)**(i-y)
            out[(s-x,i+x-y,r+y)]+=cw*rw
    if sum(out.values(),F())!=1:raise ValueError('microkernel does not normalize')
    return out

def independent_oracle():
    kernel={w:micro_kernel(w) for w in WORLDS}
    rows={};worlds={}
    for w in WORLDS:
        s,i,r,p,q=w
        one=kernel[w]
        two=defaultdict(F)
        second_new=F()
        for mid,m1 in one.items():
            if not m1:continue
            for end,m2 in kernel[(*mid,p,q)].items():
                two[end]+=m1*m2
                if end[0]<mid[0]:second_new+=m1*m2
        extinction1=sum((v for u,v in one.items() if u[1]==0),F())
        extinction2=sum((v for u,v in two.items() if u[1]==0),F())
        worlds[name(w)]={
            'world':name(w),'S':s,'I':i,'R':r,'p':str(p),'q':str(q),
            'one_step_extinction':str(extinction1),
            'two_step_extinction':str(extinction2),
            'second_step_extinction_increment':str(extinction2-extinction1),
            'second_step_any_new_infection':str(second_new),
            'expected_S2':str(sum((m*u[0] for u,m in two.items()),F())),
            'expected_I2':str(sum((m*u[1] for u,m in two.items()),F())),
            'expected_R2':str(sum((m*u[2] for u,m in two.items()),F()))}
        for u in STATES:rows[(name(w),u)]=str(two[u])
    return rows,worlds

def validate(rows,summary,source_sha,oracle_rows,oracle_worlds):
    if source_sha!=ORIGINAL_SHA:raise ValueError('original source SHA mismatch')
    if summary.get('source_original_sha256')!=ORIGINAL_SHA:raise ValueError('receipt source SHA mismatch')
    if summary.get('study')!='R309_S105' or summary.get('evidence')!='E1_ARTIFICIAL_INTERNAL_NONBLIND':
        raise ValueError('scientific scope altered')
    if summary.get('new_E2')!=0 or summary.get('new_E3')!=0:raise ValueError('evidence promotion')
    if summary.get('frozen_R073')!='FROZEN' or summary.get('frozen_PESEN_v0_1')!='FROZEN':
        raise ValueError('frozen controls altered')
    if summary.get('scientific_status')!='PARTIAL_E1_ARTIFICIAL_TWO_STEP':raise ValueError('acceptance overclaim')
    if summary.get('original_worlds')!=189 or summary.get('two_step_state_cells')!=3969:
        raise ValueError('world or cell universe metadata')
    if len(rows)!=3969:raise ValueError('missing or extra state cell')
    seen=set()
    for row in rows:
        key=(row['world'],(int(row['final_S']),int(row['final_I']),int(row['final_R'])))
        if key in seen:raise ValueError('duplicate state cell')
        seen.add(key)
        if key not in oracle_rows:raise ValueError('unknown state cell')
        w=oracle_worlds.get(row['world'])
        if w is None:raise ValueError('unknown world')
        for k in ('S','I','R'):
            if int(row[k])!=w[k]:raise ValueError('world state metadata mismatch')
        for k in ('p','q'):
            if row[k]!=w[k]:raise ValueError('world parameter mismatch')
        if row['two_step_probability']!=oracle_rows[key]:raise ValueError('two-step probability differs')
    if seen!=set(oracle_rows):raise ValueError('incomplete cell coverage')
    items=summary.get('worlds')
    if not isinstance(items,list) or len(items)!=189:raise ValueError('missing or extra summary worlds')
    worldseen=set()
    for item in items:
        key=item['world']
        if key in worldseen:raise ValueError('duplicate summary world')
        worldseen.add(key)
        expected=oracle_worlds.get(key)
        if expected is None:raise ValueError('unknown summary world')
        if item!=expected:raise ValueError('summary field mismatch')
    if worldseen!=set(oracle_worlds):raise ValueError('incomplete summary coverage')
    if summary.get('two_step_positive_cells')!=sum(F(x)>0 for x in oracle_rows.values()):
        raise ValueError('positive cell count mismatch')
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--artifacts',type=Path,default=Path(__file__).resolve().parent.parent/'validation')
    ap.add_argument('--original',type=Path,default=Path(__file__).resolve().parent.parent/'R309'/'R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv')
    a=ap.parse_args()
    digest=hashlib.sha256(a.original.read_bytes()).hexdigest()
    with (a.artifacts/'R309_S105_ALL_3969_TWO_STEP_STATES.csv').open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    summary=json.loads((a.artifacts/'R309_S105_TWO_STEP_SUMMARY.json').read_text(encoding='utf-8'))
    oracle_rows,oracle_worlds=independent_oracle()
    validate(rows,summary,digest,oracle_rows,oracle_worlds)
    mutations={}
    def test(key,fn):
        rr=copy.deepcopy(rows);ss=copy.deepcopy(summary);dd=digest
        if key=='corrupted_source_digest':dd='0'*64
        else:fn(rr,ss)
        try:validate(rr,ss,dd,oracle_rows,oracle_worlds)
        except (ValueError,KeyError,TypeError,IndexError):mutations[key]='REJECTED'
        else:raise RuntimeError('FAILED_TO_REJECT_'+key)
    test('duplicate_state_cell',lambda r,s:r.__setitem__(1,copy.deepcopy(r[0])))
    test('missing_state_cell',lambda r,s:r.pop())
    test('altered_state_probability',lambda r,s:r[0].__setitem__('two_step_probability','1/3'))
    test('altered_extinction',lambda r,s:s['worlds'][0].__setitem__('two_step_extinction','1/3'))
    test('altered_one_step_baseline',lambda r,s:s['worlds'][0].__setitem__('one_step_extinction','1/3'))
    test('altered_expected_I2',lambda r,s:s['worlds'][0].__setitem__('expected_I2','1/3'))
    test('false_E2_promotion',lambda r,s:s.__setitem__('new_E2',1))
    test('corrupted_source_digest',lambda r,s:None)
    print(json.dumps({'status':'PASS','audit':'INTERNAL_NONBLIND_E1','oracle_method':'microstate contact and recovery masks',
        'worlds':len(oracle_worlds),'two_step_state_cells':len(oracle_rows),
        'mutations':mutations,'original_source_sha256':digest,
        'sample_half':oracle_worlds['S=3|I=2|R=0|contact_p=1/2|recovery_q=1/2']},indent=2))
if __name__=='__main__':main()
