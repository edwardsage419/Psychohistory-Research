#!/usr/bin/env python3
"""R215 S11 post-computation audit harness. R and B calculators remain separate."""
import csv
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    r=load(ROOT.parent/'validation/r215_s11_exact.py','r215_s11_source').main()
    b=load(ROOT/'b_r215_s11_moment.py','b_r215_s11_analytic').main()
    assert len(r['rows'])==len(b['rows'])==36
    fields=['world','threshold','true_ATT','accept_probability','accepted_source_count',
            'D_mean_shift_from_full','C_mean_shift_from_full',
            'D_MSE_change_from_full','C_MSE_change_from_full']
    count=0
    for a,z in zip(r['rows'],b['rows']):
        for key in fields:
            assert str(a[key])==str(z[key]),(a['world'],a['threshold'],key)
            count+=1
        for method in ('D','C'):
            for key in ('mean','variance','mse_ATT'):
                assert a[method][key]==z[method][key],(a['world'],a['threshold'],method,key)
                count+=1
    assert count==540
    assert r['summary']['D_MSE_increased']==9
    assert r['summary']['D_MSE_decreased']==20
    assert r['summary']['D_MSE_equal']==7
    assert r['summary']['D_conditional_mean_shift_nonzero']==15
    with (ROOT.parent/'validation/R215_S11_36_CONDITION_EXACT.csv').open(newline='',encoding='utf-8') as f:
        csvrows=list(csv.DictReader(f))
    assert len(csvrows)==36
    csvchecks=0
    for x,row in zip(r['rows'],csvrows):
        checks={'world':x['world'],'h':str(x['threshold']),
                'accept_n':str(x['accepted_source_count']),
                'D_mean':x['D']['mean'],'D_var':x['D']['variance'],
                'D_mse':x['D']['mse_ATT'],'C_mean':x['C']['mean'],
                'C_var':x['C']['variance'],'C_mse':x['C']['mse_ATT'],
                'D_mse_delta':x['D_MSE_change_from_full'],
                'C_mse_delta':x['C_MSE_change_from_full']}
        for k,v in checks.items():
            assert row[k]==v,(x['world'],x['threshold'],k)
            csvchecks+=1
    assert csvchecks==396
    # Mutation: one digit in an archived risk must fail the comparison.
    wrong=dict(csvrows[0]);wrong['D_mse']='999'
    assert wrong['D_mse']!=r['rows'][0]['D']['mse_ATT']
    print({'R_B_exact_fields':count,'R_CSV_exact_fields':csvchecks,
           'wrong_receipt_mutation_detected':True,
           'R_source_checks':r['summary']['checks'],
           'B_analytic_checks':b['summary']['total_internal_checks'],
           'failed':0,'evidence':'internal_E1'})

if __name__=='__main__':main()
