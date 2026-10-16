#!/usr/bin/env python3
"""R065 J: deterministic author-eligible sample and source-pinned Model3 replay.

Locally requires unmodified author processed CSV and data/<participant_id>.csv.
Outputs no individual results or pseudonyms. Requires companion R065 A/H/I modules.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

DAYS = (4, 21, 38, 55, 72, 89, 106, 123)
ASCII = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')


def select_eligible(rows: list[dict], each: int = 12, strict: bool = True) -> dict[str, list[str]]:
    if not isinstance(each, int) or isinstance(each, bool) or each <= 0:
        raise ValueError('invalid sample size')
    required = ('participant_id','accurate','comprehension_check_repetitions',
                'critical','day','stakes','counterbalance')
    people: dict[str, dict] = {}
    for row in rows:
        if any(row.get(k) in (None,'','NA','NaN','nan') for k in required):
            raise ValueError('missing required source field')
        pid = row['participant_id']
        if any(ch not in ASCII for ch in pid):
            raise ValueError('non-ASCII pseudonym')
        a,c,flag = float(row['accurate']), float(row['comprehension_check_repetitions']), float(row['critical'])
        day = float(row['day'])
        if a not in (0,1) or flag not in (0,1) or not math.isfinite(c) or not day.is_integer():
            raise ValueError('invalid source trial measurement')
        p = people.setdefault(pid, {'n':0,'accurate':0.,'checks':0.,'critical':[]})
        p['n'] += 1
        p['accurate'] += a
        p['checks'] += c
        if flag:
            p['critical'].append((int(day),row['stakes'],row['counterbalance']))
    groups: dict[str,list[str]] = {'first_high':[],'first_low':[]}
    for pid,p in people.items():
        if p['accurate']/p['n'] < .45 or p['checks']/p['n'] > 2:
            continue
        schedule = sorted(p['critical'])
        if tuple(x[0] for x in schedule) != DAYS:
            raise ValueError('eligible person has incorrect diagnostic schedule')
        seq = ''.join('H' if x[1]=='high' else 'L' if x[1]=='low' else '?' for x in schedule)
        if seq not in ('HLHLHLHL','LHLHLHLH'):
            raise ValueError('unexpected stakes ordering')
        expected_counter = '1' if seq[0] == 'H' else '0'
        if any(x[2] != expected_counter for x in schedule):
            raise ValueError('counterbalance alias mismatch')
        groups['first_high' if seq[0]=='H' else 'first_low'].append(pid)
    if strict and (len(people)!=295 or len(groups['first_high'])!=121 or
                   len(groups['first_low'])!=105 or len(rows)!=16103):
        raise ValueError('full source cohort identity mismatch')
    out = {}
    for label,ids in groups.items():
        ids.sort()
        if len(ids) < each:
            raise ValueError('too few eligible persons in '+label)
        picked=[ids[int((j+0.5)*len(ids)/each)] for j in range(each)]
        if len(set(picked)) != each:
            raise ValueError('repeated participant selected')
        out[label] = picked
    if len(set(out['first_high'] + out['first_low'])) != 2*each:
        raise ValueError('duplicate participant between groups')
    return out


def verify_manifest(manifest: dict, count: int = 24) -> list[str]:
    if (manifest.get('stage')!='R065_PHASE_J' or manifest.get('selected_subjects')!=count or
        manifest.get('selected_first_high')!=count//2 or manifest.get('selected_first_low')!=count//2):
        raise ValueError('unexpected Phase J selection manifest')
    shas = manifest.get('pinned_raw_git_blobs_in_group_order')
    if (not isinstance(shas,list) or len(shas)!=count or
        any(not isinstance(s,str) or len(s)!=40 or any(c not in '0123456789abcdef' for c in s) for s in shas)):
        raise ValueError('invalid pinned source blob list')
    return shas


def replay(processed: bytes, raw_dir: Path, manifest: dict) -> dict:
    from r065_critical_replay import parse_verified
    from r065_phase_h_model3_reset import source_trials
    from r065_phase_i_beta_profile import (AUTHOR,BLOCK,counts_for,combine,fit_beta,lopo,nll)
    selected=select_eligible(parse_verified(processed), strict=True)
    ids=selected['first_high']+selected['first_low']
    pins=verify_manifest(manifest)
    if len(ids)!=len(pins):
        raise ValueError('selection size mismatch')
    all_trials=[source_trials((raw_dir/(pid+'.csv')).read_bytes(),sha)
                for pid,sha in zip(ids,pins)]
    out={'status':'EXACT_SOURCE_BYTES_REPLAY','subjects':len(ids),
         'first_high':len(selected['first_high']),'first_low':len(selected['first_low']),
         'models':{}}
    for name,reset in (('author',AUTHOR),('boundary',BLOCK)):
        per=[counts_for(t,reset) for t in all_trials]
        whole=combine(per)
        fit=fit_beta(whole)
        heldout=lopo(per)
        out['models'][name]={'counts':whole,'beta_optimal':fit['beta'],
            'in_sample_mean_nll':fit['total_nll']/whole['play'],
            'fixed_beta5_mean_nll':nll(whole,5)/whole['play'],
            'looo_mean_nll':heldout['mean_nll'],
            'training_beta_range':[heldout['min_beta'],heldout['max_beta']]}
    return out


def validate_against_archived(now: dict, archived: dict, atol:float=1e-7) -> None:
    if now['subjects']!=archived['selected_subjects'] or now['first_high']!=12 or now['first_low']!=12:
        raise ValueError('sample identity mismatch')
    for name in ('author','boundary'):
        a,b=now['models'][name],archived['models'][name]
        if a['counts'] != b['counts']:
            raise ValueError('raw-source sufficient counts disagree: '+name)
        for field in ('beta_optimal','in_sample_mean_nll','fixed_beta5_mean_nll','looo_mean_nll'):
            if not math.isclose(a[field],b[field],rel_tol=0,abs_tol=atol):
                raise ValueError('source replay differs: '+name+' '+field)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--processed',type=Path,required=True)
    ap.add_argument('--raw-dir',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    archived=json.loads(args.manifest.read_text(encoding='utf-8'))
    result=replay(args.processed.read_bytes(),args.raw_dir,archived)
    validate_against_archived(result,archived)
    rendered=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(rendered,encoding='utf-8')
    print(json.dumps({'status':'PASS','subjects':result['subjects']}))
if __name__=='__main__':main()
