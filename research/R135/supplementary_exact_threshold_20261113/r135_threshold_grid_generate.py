#!/usr/bin/env python3
from fractions import Fraction
from pathlib import Path
import json
from r135_threshold_scan import scan_one

rate_strs=['0.02','0.08','0.12','0.20','0.21','0.22','0.23','0.24','0.245','0.25','0.26','0.27','0.28','0.282','0.2824','0.283','0.29','0.30','0.40','0.50']
rates=[]
for raw in rate_strs:
    r=scan_one(float(raw),b=2)
    rates.append({'assignment_error':raw,'cooperative_mirror_ESS':r['cooperative_mirror_orbits'],'raw_cooperative':r['raw_cooperative'],'allD_raw_ESS':r['raw_alld']})
bs=[]
for b,expected in [('4',73),('3',59),('2',25),('1.2',15),('1.1',13)]:
    r=scan_one(0.02,b=float(b))
    if r['cooperative_mirror_orbits']!=expected: raise ValueError('original paper check mismatch')
    bs.append({'benefit':b,'published_2004_nontrivial_ESS':expected,'recomputed':r['cooperative_mirror_orbits']})
payload={
'run_date':'2026-11-13','study':'R135 postfreeze, supplementary floating-point exploratory grid',
'original_eq':'Ohtsuki and Iwasa 2004 JTB 231 107-120 equations (3)-(10)',
'source':'https://doi.org/10.1016/j.jtbi.2004.06.005',
'grade':'internal E1 mathematical modelling only',
'execution_error':'1/50','benefit_for_noise_grid':'2','cost':'1',
'strategy_space':'256 binary norms by 16 binary strategies with all 15 distinct strategy mutants',
'strict_tolerance':'1e-12 (exploratory float grid only; exact threshold uses separate Fraction and symbolic certificates)',
'original_source_benefit_count_crosscheck':bs,'rates':rates,
'proof_statement':'The exact threshold is supported by the separate interval and symbolic certificates; this floating point grid is not itself a global proof.',
'human_E2':0,'historical_E3':0}
Path(__file__).with_name('R135_THRESHOLD_GRID_20261113.json').write_text(json.dumps(payload,indent=2)+'\n')
print('grid rates',len(rates),'last',rates[-5:])
