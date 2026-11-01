#!/usr/bin/env python3
"""R328 S124 independent closed-form exact Fraction audit (no R generator import).
Use --selftest to recompute fixed Git blob identities from independent oracle.
Use --check DIR to validate the actual archived CSV/JSON if locally available.
"""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

FIELDS = ['alpha','prior','target','prior_precision','sensory_precision','step','estimate','sensory_error','prior_error','energy','analytic_optimum','lambda','energy_gap']
CSV = 'R328_S124_ALL_480_STEP_SIZE_STATES.csv'
JSON = 'R328_S124_EXACT_96_STABILITY_WORLDS.json'

def E(x, m, y, r, p):
    return (r*(x-m)**2+p*(y-x)**2)/2

def oracle():
    rows, worlds = [], []
    for alpha in (F(1,4), F(1,2), F(3,4), F(1)):
        for m in (F(0),F(1)):
            for y in (F(0),F(1),F(2)):
                for r in (F(1),F(2)):
                    for p in (F(1),F(2)):
                        opt = (r*m+p*y)/(r+p)
                        lam = 1-alpha*(r+p)
                        energies=[]
                        for t in range(5):
                            x=opt+(m-opt)*lam**t
                            en=E(x,m,y,r,p)
                            gap=(r+p)*(m-opt)**2*lam**(2*t)/2
                            assert en-E(opt,m,y,r,p)==gap
                            energies.append(en)
                            rows.append([str(alpha),str(m),str(y),str(r),str(p),str(t),str(x),str(y-x),str(m-x),str(en),str(opt),str(lam),str(gap)])
                        category=('FLAT_ZERO_RESIDUAL' if y==m else 'CONTRACTIVE' if abs(lam)<1 else 'NEUTRAL' if abs(lam)==1 else 'EXPANSIVE')
                        worlds.append(dict(alpha=str(alpha),prior=str(m),target=str(y),prior_precision=str(r),sensory_precision=str(p),lambda_=str(lam),analytic_optimum=str(opt),estimate_step4=str(opt+(m-opt)*lam**4),energy_step4=str(energies[-1]),category=category,energy_nonincreasing=all(energies[i+1]<=energies[i] for i in range(4)),strict_increase_steps=sum(energies[i+1]>energies[i] for i in range(4))))
    # The primary JS schema uses 'lambda', a Python keyword. Rename without reordering.
    worlds=[{('lambda' if k=='lambda_' else k):v for k,v in w.items()} for w in worlds]
    assert len(rows)==480 and len(worlds)==96
    assert len({tuple(r[:6]) for r in rows})==480
    assert Counter(w['category'] for w in worlds)=={'FLAT_ZERO_RESIDUAL':32,'CONTRACTIVE':32,'NEUTRAL':8,'EXPANSIVE':24}
    b=io.StringIO(newline='')
    wr=csv.writer(b,lineterminator='\n')
    wr.writerow(FIELDS);wr.writerows(rows)
    data={'model':'R328_S124_FINITE_STEP_SIZE_STABILITY_E1','source_row_count':480,'world_count':96,'worlds':worlds}
    return rows,worlds,b.getvalue().encode(),(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()

def gitsha(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def check_mutations(rows,worlds):
    # Fixed source-level structural/semantic oracle, rather than a shallow digest-only gate.
    def check(rs,ws):
        if len(rs)!=480 or len(ws)!=96: raise ValueError('coverage')
        if len({tuple(r[:6]) for r in rs})!=480: raise ValueError('duplicate')
        expected,ew,_,_=oracle()
        if rs!=expected or ws!=ew: raise ValueError('exact closed-form mismatch')
    check(rows,worlds)
    mutants=[]
    mutants.append(('omit_row',rows[:-1],worlds))
    mutants.append(('duplicate_row',rows[:1]+rows[:1]+rows[2:],worlds))
    mutated=[r[:] for r in rows];mutated[10][9]='999';mutants.append(('energy_change',mutated,worlds))
    mutated=[r[:] for r in rows];mutated[10][0]='1';mutants.append(('alpha_change',mutated,worlds))
    mutated=[w.copy() for w in worlds];mutated[0]['evidence_grade']='E2';mutants.append(('evidence_promotion',rows,mutated))
    rejected=[]
    for label,rs,ws in mutants:
        try:check(rs,ws)
        except ValueError:rejected.append(label)
        else:raise AssertionError('mutation accepted: '+label)
    return rejected

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--check',type=Path)
    p.add_argument('--selftest',action='store_true')
    a=p.parse_args()
    rows,worlds,expected_csv,expected_json=oracle()
    rejected=check_mutations(rows,worlds)
    if a.check:
        assert (a.check/CSV).read_bytes()==expected_csv, 'persisted CSV mismatch'
        assert (a.check/JSON).read_bytes()==expected_json, 'persisted JSON mismatch'
    print(json.dumps({'status':'PASS_NONBLIND_E1_CLOSED_FORM','rows':len(rows),'worlds':len(worlds),'mutants_rejected':rejected,'csv_git_blob':gitsha(expected_csv),'json_git_blob':gitsha(expected_json),'csv_bytes':len(expected_csv),'json_bytes':len(expected_json)},sort_keys=True))

if __name__=='__main__':main()
