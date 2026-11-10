#!/usr/bin/env python3
"""Audit fetched PR Git objects using a saved gh snapshot; no network/merge/checkout.

merge-tree writes only Git objects. Stdout is caller-managed, never a success file.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def git(repo, *args):
    result=subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True)
    if result.returncode:
        raise ValueError('git failed: '+str(args[:2])+': '+result.stderr[:300])
    return result.stdout.rstrip("\n")


def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=value
    return result


def validate(rows):
    if type(rows) is not list or not rows:raise ValueError('nonempty PR list required')
    seen=set()
    for row in rows:
        required={'number','headRefOid','baseRefName','title','url','isDraft','statusCheckRollup'}
        if type(row) is not dict or not required<=set(row):raise ValueError('snapshot fields missing')
        number=row['number']
        if type(number) is not int or number<=0:raise ValueError('positive integer PR number required')
        if number in seen:raise ValueError('duplicate PR number')
        seen.add(number)
        if type(row['headRefOid']) is not str or not re.fullmatch('[0-9a-f]{40}',row['headRefOid']):
            raise ValueError('full SHA required')
        if row['baseRefName']!='main':raise ValueError('non-main base needs separate audit')
        if type(row['isDraft']) is not bool or type(row['statusCheckRollup']) is not list:
            raise ValueError('draft/check types')
        if any(type(row[k]) is not str for k in ('title','url')):raise ValueError('title/url types')
    return sorted(rows,key=lambda row:row['number'])


def merge(repo, a, b):
    result=subprocess.run(['git','-C',str(repo),'merge-tree','--write-tree','--name-only',a,b],
                          capture_output=True,text=True)
    if result.returncode not in (0,1):raise ValueError('merge-tree failed: '+result.stderr[:300])
    return {'exit':result.returncode,'output':result.stdout}


def audit(repo, rows):
    rows=validate(rows)
    main=git(repo,'rev-parse','--verify','refs/remotes/origin/main^{commit}')
    # Authenticate every advertised head before producing any merge results.
    for row in rows:
        actual=git(repo,'rev-parse','--verify',f"refs/remotes/pr/{row['number']}^{{commit}}")
        if actual!=row['headRefOid']:raise ValueError('snapshot/local head mismatch: '+str(row['number']))
    prs=[]
    for row in rows:
        head=row['headRefOid'];base=git(repo,'merge-base',main,head)
        tokens=git(repo,'diff','--name-status','--no-renames','-z',base,head).split('\0')[:-1]
        changes=list(zip(tokens[::2],tokens[1::2]))
        files=[path for change,path in changes]
        code=[]
        for change,path in changes:
            if path.endswith(('.py','.js')):
                if change=='D':
                    code.append({'path':path,'change':'D','git_blob':None,'sha256':None})
                    continue
                # Source is Git bytes, not text decoded and re-encoded.
                raw=subprocess.check_output(['git','-C',str(repo),'show',head+':'+path])
                code.append({'path':path,'change':change,'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
                             'sha256':hashlib.sha256(raw).hexdigest()})
        prs.append({'number':row['number'],'head':head,'merge_base':base,'files':files,'code_identity':code,
                    'behind_main':int(git(repo,'rev-list','--count',head+'..'+main)),
                    'merge_with_main':merge(repo,main,head),'remote_observation':row,
                    'ci_interpretation':'NO_CHECKS_REPORTED' if not row['statusCheckRollup'] else 'CHECKS_REPORTED_UNEVALUATED'})
    pairs=[]
    for i,a in enumerate(prs):
        for b in prs[i+1:]:
            result=merge(repo,a['head'],b['head'])
            result.update(a=a['number'],b=b['number'],overlap=sorted(set(a['files'])&set(b['files'])))
            pairs.append(result)
    return {'status':'COMPLETE_PINNED_GIT_AUDIT','main':main,'prs':prs,'pairs':pairs,
            'pair_count':len(pairs),'conflicts_present':any(p['exit']==1 for p in pairs) or
            any(p['merge_with_main']['exit']==1 for p in prs),
            'limits':'Analysis covers only the supplied snapshot; no proof it lists every open PR. Pairwise Git text mergeability is not whole-queue sequential integration, tests, CI or scientific acceptance.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo',type=Path);parser.add_argument('snapshot',type=Path)
    args=parser.parse_args()
    try:
        raw=args.snapshot.read_bytes();rows=json.loads(raw,object_pairs_hook=unique)
        result=audit(args.repo,rows)
        result['snapshot_sha256']=hashlib.sha256(raw).hexdigest()
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)}));return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':sys.exit(main())
