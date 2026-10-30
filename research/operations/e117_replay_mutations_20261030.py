#!/usr/bin/env python3
"""Synthetic-fixture dynamic regression against the exact archived B checker.
No persisted original CSV/JSON bytes are claimed to be replayed here.
"""
import copy
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).parent
src=ROOT.parent/'evidence_audit'/'b_r286_s82_covariance_and_receipt_audit_20261030.py'
spec=importlib.util.spec_from_file_location('archived_b',src)
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

rows=[]
results=[]
for s in b.STAYS:
    for p in b.POLICIES:
        for n in range(64):
            seq=format(n,'06b')
            bits=[int(x) for x in seq]
            same=sum(x==y for x,y in zip(bits,bits[1:]))
            w=F(1,2)*s**same*(1-s)**(5-same)
            value=sum((b.COEFF[p][i]*bits[i] for i in range(5)),F(0))
            loss=(bits[5]-value)**2
            rows.append(dict(zip(b.COLS,[str(s),str(2*s-1),p,seq,seq[:5],str(bits[5]),str(w),str(value),str(loss)])))
        risk=b.risk_by_moments(s,p)
        results.append(dict(stay_probability=str(s),rho=str(2*s-1),policy=p,complete_sources=64,
            source_mass='1',exact_heldout_Brier=str(risk),independent_covariance_Brier=str(risk),
            constant_half_baseline_Brier='1/4',delta_vs_constant_half=str(risk-F(1,4)),
            frozen_original_coefficients=[str(x) for x in b.COEFF[p]]))
obj=dict(research_id='R286_S82',freeze_protocol='research/validation/R286_S82_MARKOV_REWARD_DEPENDENCE_PRESCORE_FREEZE_2026-10-30.md',
         original_R286_status='UNCHANGED_CLOSED_BOUNDED_E1',scope='INTERNAL_NONBLIND_ARTIFICIAL_E1_MARKOV_REWARD_DEPENDENCE',
         stay_probabilities=['1/4','1/2','3/4'],model_labeled_complete_source_types=576,
         independent_analytic_agreement=True,original_R286_iid_baseline_agreement=True,
         R073='FROZEN',PESEN_v0_1='FROZEN',new_E2_predictions=0,new_E3_predictions=0,
         external_independent_replication='NOT_RUN',results=results)
assert b.audit(rows,obj)==(576,9)
assert b.mutations(rows,obj)==8

top=['research_id','freeze_protocol','original_R286_status','stay_probabilities',
     'model_labeled_complete_source_types','independent_analytic_agreement',
     'original_R286_iid_baseline_agreement','external_independent_replication']
item=['rho','source_mass','frozen_original_coefficients']
accept=[]
for kind in ['change','delete']:
    for k in top+item:
        o=copy.deepcopy(obj)
        target=o if k in top else o['results'][0]
        if kind=='delete': target.pop(k)
        else:
            target[k]=('VERIFIED_EXTERNALLY' if k=='external_independent_replication' else 'WRONG_VALUE')
        try:
            got=b.audit(rows,o)
            accept.append(dict(kind=kind,field=k,accepted=got==(576,9)))
        except Exception as exc:
            accept.append(dict(kind=kind,field=k,accepted=False,error=type(exc).__name__))
assert len(accept)==22
assert all(x['accepted'] for x in accept),accept
report=dict(checker_git_blob='894c97e7d250afe6fdcf8a8c593fe9b4b599c511',fixture='INDEPENDENTLY_REBUILT_SYNTHETIC_576_ROWS_9_RESULTS',
            baseline_pass=True,existing_mutations_rejected=8,new_metadata_mutations_accepted=len(accept),
            cases=accept,original_persisted_CSV_replayed=False,original_persisted_JSON_replayed=False,
            science_scope='INTERNAL_NONBLIND_E1_ENGINEERING_ONLY')
(ROOT/'e117_mutation_results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},ensure_ascii=False))
