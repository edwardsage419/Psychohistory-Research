#!/usr/bin/env python3
"""R325 S121 independent nonblind row/aggregate audit, stdlib only. E1."""
import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

PROFILES={'U':(Q(1,3),Q(1,3),Q(1,3)),
          'EARLY':(Q(1,2),Q(1,3),Q(1,6)),
          'LATE':(Q(1,6),Q(1,3),Q(1,2)),
          'CENTER':(Q(1,4),Q(1,2),Q(1,4))}
WORLDS=[('linear_eu',Q(0)),('mild_cubic',Q(1,4)),('strong_cubic',Q(1))]
BLOBS={'csv':'8df84f30ad1d680758aa526d3f8f05a911523bd0',
       'json':'b1c4bf4d07f0479fdefb1dc22aa202b8e6526531'}

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def sign(x):
    return 'A' if x>0 else 'B' if x<0 else 'TIE'

def audit(csv_bytes,json_bytes,verify_blobs=True):
    if verify_blobs and (git_blob(csv_bytes)!=BLOBS['csv'] or git_blob(json_bytes)!=BLOBS['json']):
        raise ValueError('persisted Git blob identity mismatch')
    rows=list(csv.DictReader(csv_bytes.decode('utf8').splitlines()))
    obj=json.loads(json_bytes)
    if len(rows)!=4116 or obj['rows']!=4116 or obj['evidence']!='E1_PROJECT_CONSTRUCTED_ONLY':
        raise ValueError('row count or E1 scope')
    if obj['human_E2']!='NOT_RUN' or obj['historical_E3']!='NOT_RUN':
        raise ValueError('invalid evidence promotion')
    keys=set();summary=[]
    for profile,ps in PROFILES.items():
        for w,(name,k) in enumerate(WORLDS):
            part=[]
            for ds in itertools.product(range(-3,4),repeat=3):
                key=(profile,str(w),*map(str,ds))
                if key in keys: raise ValueError('duplicate key')
                keys.add(key)
                part.append((key,ds))
            got={(r['profile'],r['world_id'],r['d1'],r['d2'],r['d3']):r
                 for r in rows if r['profile']==profile and r['world_id']==str(w)}
            if len(got)!=343: raise ValueError('duplicate or missing profile world')
            counts=Counter();rev=changes=strict=0
            for key,ds in part:
                r=got.get(key)
                if r is None: raise ValueError('missing key')
                eu=sum((p*d for p,d in zip(ps,ds)),Q(0))
                f=sum((p*(d+k*d**3) for p,d in zip(ps,ds)),Q(0))
                f0=sum((Q(1,3)*(d+k*d**3) for d in ds),Q(0))
                c=sign(f);u=sign(f0)
                expected={'policy':name,'kappa':str(k),'p1':str(ps[0]),'p2':str(ps[1]),
                          'p3':str(ps[2]),'eu':str(eu),'regret':str(f),
                          'eu_choice':sign(eu),'regret_choice':c,
                          'strict_reversal':str(int(eu*f<0)),'uniform_choice':u,
                          'changed_vs_uniform':str(int(c!=u)),
                          'strict_disagreement_vs_uniform':str(int(c!='TIE' and u!='TIE' and c!=u))}
                if any(r.get(col)!=val for col,val in expected.items()):
                    raise ValueError('incorrect mathematical row '+str(key))
                counts[c]+=1;rev+=int(eu*f<0);changes+=int(c!=u)
                strict+=int(c!='TIE' and u!='TIE' and c!=u)
            summary.append((profile,w,counts['A'],counts['B'],counts['TIE'],rev,changes,strict))
    if len(keys)!=4116 or len(obj['summary'])!=12: raise ValueError('coverage')
    for s,t in zip(obj['summary'],summary):
        actual=(s['profile'],s['world_id'],s['choice_A'],s['choice_B'],s['choice_TIE'],
                s['strict_eu_regret_reversals'],s['changed_choice_vs_uniform'],
                s['strict_sign_disagreements_vs_uniform'])
        if actual!=t: raise ValueError('summary mismatch')
    return {'rows':len(rows),'profile_worlds':len(summary),'sha_csv':git_blob(csv_bytes),
            'sha_json':git_blob(json_bytes)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,required=True)
    p.add_argument('--json',type=Path,required=True);p.add_argument('--selftest',action='store_true')
    a=p.parse_args();cb=a.csv.read_bytes();jb=a.json.read_bytes()
    out=audit(cb,jb)
    if a.selftest:
        variants=[('csv_cell',cb.replace(b',1/3,1/3,1/3,',b',1/2,1/3,1/3,',1),jb),
                  ('json_scope',cb,jb.replace(b'E1_PROJECT_CONSTRUCTED_ONLY',b'E2_HUMAN',1)),
                  ('csv_missing',cb[:cb.rfind(b'\n',0,len(cb)-1)+1],jb),
                  ('csv_duplicate',cb+cb.splitlines()[1]+b'\n',jb)]
        for name,c,j in variants:
            if c==cb and j==jb:raise ValueError('dead mutation '+name)
            try:audit(c,j,False)
            except ValueError:pass
            else:raise ValueError('mutation accepted '+name)
        out['negative_controls']=len(variants)
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
