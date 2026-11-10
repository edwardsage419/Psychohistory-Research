from pathlib import Path
import concurrent.futures,datetime,hashlib,json,re,subprocess,time
meta=json.loads(Path('/workspace/codex-a/authorized-merge/candidate.json').read_text());root=Path(meta['candidate']);e=Path('/workspace/codex-a/authorized-merge/evidence');logs=e/'tests';logs.mkdir(parents=True,exist_ok=True)
jobs=[(s,optimized) for s in meta['scopes'] for optimized in (False,True)]
def run(job):
 scope,opt=job;label=f"pr{scope['pr']}-{Path(scope['directory']).name}-"+('optimized' if opt else 'normal');command=['python3','-B']+(['-O'] if opt else [])+['-m','unittest','discover','-s',scope['directory'],'-v'];start=time.monotonic()
 try:
  p=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=90);raw=p.stdout+p.stderr;match=re.search(r'(?m)^Ran (\d+) tests? in [^\r\n]*\r?\n\s*\r?\nOK\s*\Z',raw);count=int(match.group(1)) if match else 0
  status='PASS' if p.returncode==0 and count>0 else 'FAIL_OR_ZERO_TESTS'
  (logs/(label+'.log')).write_text(raw)
  return dict(pr=scope['pr'],scope=scope['directory'],optimized=opt,command=command,cwd=str(root),exit=p.returncode,tests=count,status=status,seconds=round(time.monotonic()-start,3),log='tests/'+label+'.log',sha256=hashlib.sha256(raw.encode()).hexdigest())
 except subprocess.TimeoutExpired as exc:
  raw=(exc.stdout or b'')+(exc.stderr or b'');raw=raw.decode(errors='replace') if isinstance(raw,bytes) else raw;(logs/(label+'.log')).write_text(raw)
  return dict(pr=scope['pr'],scope=scope['directory'],optimized=opt,command=command,exit=None,tests=None,status='TIMEOUT',log='tests/'+label+'.log')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,jobs))
extras=[]
for label,command,expected in [
 ('pr1-probe',['python3','-B','research/codex_audit/2026-10-29-r257-s53/probe_comparator.py','.'],0),
 ('legacy-r077-normal',['python3','-B','research/codex_b/2026-11-10-r077-exact-paired-ties/legacy_regression.py'],1),
 ('legacy-r077-optimized',['python3','-B','-O','research/codex_b/2026-11-10-r077-exact-paired-ties/legacy_regression.py'],1)]:
 p=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=60);raw=p.stdout+p.stderr;(logs/(label+'.log')).write_text(raw)
 record=dict(label=label,command=command,exit=p.returncode,expected_exit=expected,log='tests/'+label+'.log')
 if label.startswith('legacy'):
  record.update(outcome='KNOWN_ORIGINAL_DEFECT_REPRODUCED',failure_subcases=len(re.findall(r'^FAIL:',raw,re.M)),is_passing_suite=False)
 else:
  data=json.loads(p.stdout) if p.returncode==0 else {};record.update(probe_expectations_passed=data.get('probe_expectations_passed'),false_acceptances=sum(x.get('accepted_by_archived_comparator',False) for x in data.get('probes',{}).values()))
 record['expectation_matches']=p.returncode==expected and (record.get('failure_subcases')==11 if label.startswith('legacy') else record.get('probe_expectations_passed')==7)
 extras.append(record)
tracked=subprocess.run(['git','diff','--exit-code','--'],cwd=root,capture_output=True,text=True)
summary=dict(time=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),main=meta['main'],candidate=str(root),scopes=results,extras=extras,tracked_main_diff_exit=tracked.returncode,positive_executions=sum(r['tests'] or 0 for r in results if r['status']=='PASS'),failed_scopes=[r for r in results if r['status']!='PASS'],all_extra_expectations_match=all(x['expectation_matches'] for x in extras),local_merge_commits_created=True,remote_merge_not_yet_attempted=True,ci='NOT_DISPATCHED')
(e/'matrix.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'scopes':len(results),'positive_executions':summary['positive_executions'],'failed_scopes':[(r['pr'],r['status']) for r in summary['failed_scopes']],'extras':extras,'tracked_main_diff_exit':tracked.returncode},indent=2))
if summary['failed_scopes'] or not summary['all_extra_expectations_match'] or tracked.returncode:raise SystemExit(1)
