#!/usr/bin/env python3
"""Verify prior positive-suite receipts from an immutable Git commit, compare sources.

Never executes tests, authorizes reuse, authenticates runtime/time, or upgrades science.
A changed whole source snapshot conservatively requires revalidation.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from audit_queue import unique

PREFIX='research/codex_a/pr_queue/final_sync_20261110/evidence'


def require(ok, reason):
    if not ok:raise ValueError(reason)


def sha(value):return type(value) is str and re.fullmatch('[0-9a-f]{40}',value) is not None


def relative(value):
    return (type(value) is str and bool(value) and value!='.' and
            not PurePosixPath(value).is_absolute() and '..' not in PurePosixPath(value).parts and
            str(PurePosixPath(value))==value)


def heads(inventory):
    require(type(inventory) is dict and sha(inventory.get('main')),'main SHA required')
    require(type(inventory.get('prs')) is list and bool(inventory['prs']),'PR inventory required')
    result={}
    for row in inventory['prs']:
        require(type(row) is dict and type(row.get('number')) is int and row['number']>0 and sha(row.get('head')),'PR identity/type')
        require(row['number'] not in result,'duplicate PR identity')
        result[row['number']]=row['head']
    return result


def verify(old, matrix, current, read_log):
    before,after=heads(old),heads(current)
    require(type(matrix) is dict and matrix.get('main')==old['main'] and matrix.get('candidate_head_after')==old['main'],'prior source binding')
    require(type(matrix.get('tracked_main_diff_exit')) is int and matrix['tracked_main_diff_exit']==0 and matrix.get('failed_scopes')==[],'prior dirty/failed state')
    rows=matrix.get('scopes');require(type(rows) is list and bool(rows),'nonempty suite receipts required')
    seen=set();seen_logs=set();modes={};total=0
    for row in rows:
        require(type(row) is dict and {'pr','scope','optimized','exit','status','tests','log','sha256'}<=set(row),'suite fields missing')
        require(type(row['pr']) is int and row['pr'] in before and relative(row['scope']) and type(row['optimized']) is bool,'suite identity/type')
        key=(row['pr'],row['scope'],row['optimized']);require(key not in seen,'duplicate suite/mode');seen.add(key)
        require(type(row['exit']) is int and row['exit']==0 and row['status']=='PASS','suite outcome')
        require(type(row['tests']) is int and row['tests']>0,'positive test count required')
        require(relative(row['log']) and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'log identity/path')
        require(row['log'] not in seen_logs,'log receipt reused across suites/modes');seen_logs.add(row['log'])
        raw=read_log(row['log']);require(type(raw) is bytes,'raw log bytes required')
        require(hashlib.sha256(raw).hexdigest()==row['sha256'],'log hash mismatch')
        text=raw.decode('utf-8')
        require(re.search(r'\nOK\s*\Z',text) is not None and not re.search(r'(?m)^FAILED|skipped=|expected failures=|unexpected successes=',text),'log outcome not plain passing')
        count=re.search(r'(?m)^Ran ([0-9]+) tests? in [^\r\n]*\r?\n\s*\r?\nOK\s*\Z',text)
        require(count is not None and int(count.group(1))==row['tests'],'log count mismatch')
        for field in ('skipped','expected_failures','unexpected_successes'):
            if field in row:require(type(row[field]) is int and row[field]==0,'nonpassing suite counter')
        total+=row['tests'];modes.setdefault(key[:2],set()).add(row['optimized'])
    require(all(value=={False,True} for value in modes.values()),'both modes required')
    require(type(matrix.get('positive_executions')) is int and matrix['positive_executions']==total,'aggregate count mismatch')
    changed=sorted(n for n in before.keys() & after.keys() if before[n]!=after[n]);added=sorted(after.keys()-before.keys());removed=sorted(before.keys()-after.keys());main_changed=old['main']!=current['main']
    return {'status':'RERUN_REQUIRED' if main_changed or changed or added or removed else 'SOURCE_CONTEXT_MATCHES',
            'scope':'PRIOR_POSITIVE_SUITE_RECEIPTS_AND_SOURCE_CONTEXT_ONLY',
            'verified_prior_method_executions':total,'new_test_executions':0,
            'main_changed':main_changed,'changed_prs':changed,'new_prs':added,'removed_prs':removed,
            'runtime_context_verified':False,'worktree_context_verified':False,
            'limits':'Matching source is necessary, not sufficient for reuse; no new execution, runtime/time/author authentication, extras or scientific acceptance.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo',type=Path);parser.add_argument('record_commit');parser.add_argument('current_inventory',type=Path)
    args=parser.parse_args()
    try:
        require(sha(args.record_commit),'fixed full record commit required')
        def read(path):
            require(relative(path),'unsafe evidence path')
            return subprocess.check_output(['git','-C',str(args.repo),'show',args.record_commit+':'+PREFIX+'/'+path],stderr=subprocess.PIPE)
        old=json.loads(read('inventory.json'),object_pairs_hook=unique);matrix=json.loads(read('matrix.json'),object_pairs_hook=unique)
        current=json.loads(args.current_inventory.read_bytes(),object_pairs_hook=unique)
        current_heads=heads(current)
        actual_main=subprocess.check_output(['git','-C',str(args.repo),'rev-parse','refs/remotes/origin/main^{commit}'],text=True).strip()
        require(actual_main==current['main'],'current inventory/local main mismatch')
        for number,expected in current_heads.items():
            actual=subprocess.check_output(['git','-C',str(args.repo),'rev-parse',f'refs/remotes/pr/{number}^{{commit}}'],text=True).strip()
            require(actual==expected,'current inventory/local head mismatch: '+str(number))
        result=verify(old,matrix,current,read);result['record_commit']=args.record_commit
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)}));return 1
    print(json.dumps(result,indent=2));return 2 if result['status']=='RERUN_REQUIRED' else 0


if __name__=='__main__':sys.exit(main())
