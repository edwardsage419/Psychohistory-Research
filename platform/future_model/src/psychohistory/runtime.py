"""Bounded trusted-process scheduler. Process isolation is NOT a hostile-code sandbox."""
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import threading
import time
import uuid
from .contracts import canonical
from .engine import code_identity, run_experiment
from .storage import TERMINAL, checked_path, write_new
from .v02_execution import ComparisonProcess, RUN_KIND, digest, source_snapshot, validate_result


def _worker(config, output, memory_mb, cpu_seconds, expected_code, expected_parent):
    limits={'memory':'NOT_ENFORCED','cpu':'NOT_ENFORCED','parent_death':'NOT_ENFORCED','hostile_code_sandbox':False}
    try:
        if platform.system()=='Linux':
            import ctypes,signal
            libc=ctypes.CDLL(None,use_errno=True)
            if libc.prctl(1,signal.SIGTERM,0,0,0)!=0:raise OSError(ctypes.get_errno(),'Cannot install parent-death guard')
            if os.getppid()!=expected_parent:return
            limits['parent_death']='PR_SET_PDEATHSIG'
            import resource
            resource.setrlimit(resource.RLIMIT_AS,(memory_mb*1024**2,memory_mb*1024**2))
            resource.setrlimit(resource.RLIMIT_CPU,(cpu_seconds,cpu_seconds+1))
            limits.update(memory='RLIMIT_AS',cpu='RLIMIT_CPU')
        if code_identity()!=expected_code:raise ValueError("Worker code identity changed before execution")
        result=run_experiment(**config)
        data={'ok':True,'result':result,'worker_pid':os.getpid(),'limits':limits}
    except BaseException as exc:
        data={'ok':False,'error':f'{type(exc).__name__}: {str(exc)[:500]}','worker_pid':os.getpid(),'limits':limits}
    write_new(Path(output),canonical(data).encode())

def validate_execution_identity(run,result=None):
    expected_versions={'platform':'0.1.0','contract':'1.0.0','individual':'1.0.0','group':'1.0.0','adapter':'1.0.0','protocol':'synthetic-paired-1.0.0','dataset':'generated-1.0.0'}
    current_env={'python':platform.python_version(),'os':platform.system(),'machine':platform.machine()}
    if run.get('code_sha256')!=code_identity() or run.get('versions')!=expected_versions or run.get('environment')!=current_env or run.get('protocol')!=expected_versions['protocol'] or run.get('data_version')!=expected_versions['dataset'] or run.get('platform_version')!='0.1.0':
        raise ValueError('Execution identity incompatible with approved code/version/environment; submit a new run')
    if result and (result.get('versions')!=expected_versions or result.get('environment',{}).get('core_code_sha256')!=run['code_sha256'] or result.get('environment',{}).get('python')!=current_env['python'] or result.get('input')!=run['config']):
        raise ValueError('Worker result identity differs from approved run')

class Scheduler:
    def __init__(self,store,max_concurrency=1,max_queue=16,dispatch=True,comparison_verifier=None):
        if max_concurrency!=1 or not 1<=max_queue<=16:raise ValueError('v0.1 uses one trusted worker and at most 16 queued tasks')
        self.comparison_verifier = comparison_verifier
        self.dispatch_targets=None if dispatch else set()
        self.store=store;self.max_queue=max_queue;self.active={};self.lock=threading.RLock();self.closed=False
        self.staging=checked_path(store.root/'staging');self.staging.mkdir(exist_ok=True,mode=0o700)
        # Prevent two schedulers owning one database. POSIX flock is available on Linux/macOS.
        import fcntl
        self._owner_file=open(checked_path(store.root/'scheduler.lock'),'a')
        try:fcntl.flock(self._owner_file.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            self._owner_file.close();raise ValueError('Another scheduler already owns this data root') from None
        for run in self.store.active_runs():
            if run['status']=='RUNNING' or run.get("holdout_started_at") is not None:
                self.store.update_run(run['id'], status='FAILED',
                                      error='Worker lost after scheduler restart; no result claimed')
        self.thread=threading.Thread(target=self._monitor,name='psychohistory-scheduler',daemon=True);self.thread.start()

    def submit(self,config,timeout=15):
        if type(timeout) not in (int,float) or not math.isfinite(timeout) or not 0<timeout<=60:raise ValueError('Wall timeout must be (0,60] seconds')
        with self.lock:
            if self.closed:raise ValueError('Scheduler closed')
            if sum(r['status'] not in TERMINAL for r in self.store.active_runs())>=self.max_queue:raise ValueError('Queue budget exhausted')
            config={'seed':7,'rounds':8,'population':24,'intervention':.2,**config}
            r=self.store.create_run(uuid.uuid4().hex,config)
            return self.store.update_run(r['id'],timeout=timeout,memory_mb=512,cpu_seconds=5,protocol='synthetic-paired-1.0.0',
                code_sha256=code_identity(),platform_version='0.1.0',data_version='generated-1.0.0',
                versions={'platform':'0.1.0','contract':'1.0.0','individual':'1.0.0','group':'1.0.0','adapter':'1.0.0','protocol':'synthetic-paired-1.0.0','dataset':'generated-1.0.0'},
                environment={'python':platform.python_version(),'os':platform.system(),'machine':platform.machine()},
                logs=['Submitted: awaiting explicit synthetic approval'])

    def submit_comparison(self, config, holdout_id, code_sha256, *, retry_of=None):
        with self.lock:
            if self.closed or not self.comparison_verifier:
                raise ValueError("Comparison scheduler is unavailable")
            previous = self.store.holdout_runs(holdout_id)
            if any(run["config"]["protocol_id"] != config["protocol_id"] for run in previous):
                raise ValueError("This holdout already belongs to another experiment")
            for run in previous:
                if run["status"] not in {"FAILED", "CANCELED", "BLOCKED"}:
                    return run
            if previous and retry_of != previous[0]["id"]:
                return previous[0]
            if previous and any(run.get("holdout_started_at") is not None for run in previous):
                raise ValueError("Holdout already used by a dispatched run. Use a different seed.")
            if len(self.store.active_runs()) >= self.max_queue:
                raise ValueError("Queue budget exhausted")
            return self.store.create_run(
                uuid.uuid4().hex, config, kind=RUN_KIND, holdout_id=holdout_id,
                code_sha256=code_sha256, config_sha256=digest(config),
                platform_version="0.2.0", timeout=15, retry_of=retry_of,
                versions={"platform": "0.2.0", "protocol": config["spec"]["protocol_version"],
                          "dataset": config["spec"]["dataset_version"], "r123-degroot": "1.0.0"},
                environment={"python": platform.python_version(),
                             "os": platform.system(), "machine": platform.machine()},
                logs=["Approved protocol pinned. Experiment awaiting execution approval."],
            )

    def _verify_run(self, run, result=None):
        if run.get("kind") != RUN_KIND:
            validate_execution_identity(run, result)
            return
        if not self.comparison_verifier:
            raise ValueError("Comparison source verification unavailable")
        if (run["code_sha256"] != digest(source_snapshot())
                or run["config_sha256"] != digest(run["config"])
                or run["environment"] != {"python": platform.python_version(),
                                           "os": platform.system(), "machine": platform.machine()}):
            raise ValueError("Comparison code, input or environment identity changed")
        self.comparison_verifier(run["config"])

    def approve(self,run_id):
        with self.lock:
            r=self.get(run_id)
            if r['status']!='PENDING':raise ValueError('Only pending task can be approved')
            return self.store.update_run(run_id,status='APPROVED',logs=r['logs']+['Approved for built-in synthetic protocol only'])

    def execute_approved(self,run_id):
        """Opt one explicit CLI target into dispatch, without running its neighbors."""
        with self.lock:
            if self.closed or self.get(run_id)['status']!='APPROVED':raise ValueError('Approved task required')
            if self.dispatch_targets is not None:self.dispatch_targets.add(run_id)

    def get(self,run_id):return self.store.get_run(run_id)

    def _stop(self,run_id):
        active=self.active.pop(run_id,None)
        if active:
            process,_,output=active
            if process.is_alive():process.terminate()
            process.join(1)
            if process.is_alive():process.kill();process.join(1)
            checked_path(output).unlink(missing_ok=True)

    def cancel(self,run_id):
        with self.lock:
            r=self.get(run_id)
            if r['status'] in TERMINAL:raise ValueError('Task already terminal')
            self._stop(run_id)
            return self.store.update_run(run_id,status='CANCELED',logs=r['logs']+['Canceled; worker terminated if active'])

    def _tick(self):
        with self.lock:
            for run_id,(process,started,output) in list(self.active.items()):
                r=self.get(run_id)
                if process.is_alive() and time.monotonic()-started>r['timeout']:
                    self._stop(run_id);self.store.update_run(run_id,status='FAILED',error='Wall timeout exceeded',logs=r['logs']+['Timeout: worker terminated']);continue
                if not process.is_alive():
                    process.join()
                    try:
                        if not output.is_file() or output.stat().st_size>32*1024**2:raise ValueError(f'Worker exit {process.exitcode}, missing/oversized output')
                        import json
                        data=json.loads(checked_path(output).read_bytes())
                        if not data['ok']:raise ValueError(data['error'])
                        if process.exitcode != 0:raise ValueError(f'Worker exited with {process.exitcode}')
                        result = data['result']
                        self._verify_run(r, result)
                        if r.get("kind") == RUN_KIND:
                            validate_result(r, result)
                        h = self.store.put(result)
                        self.store.lock_versions(r['versions'])
                        self.store.update_run(run_id,status='COMPLETED',result_hash=h,worker_pid=data['worker_pid'],limits=data['limits'],
                                              logs=r['logs']+result.get('logs',[])+['Completed; content hash verified'])
                    except Exception as exc:
                        self.store.update_run(run_id,status='FAILED',error=f'{type(exc).__name__}: {str(exc)[:500]}',logs=r['logs']+['Worker failed; error retained'])
                    finally:self.active.pop(run_id,None);checked_path(output).unlink(missing_ok=True)
            if self.closed:return
            if not self.active:
                queued=[r for r in self.store.active_runs() if r['status']=='APPROVED' and (self.dispatch_targets is None or r['id'] in self.dispatch_targets)]
                if queued:
                    r=queued[0]
                    try:self._verify_run(r)
                    except (ValueError, PermissionError, KeyError, OSError) as exc:
                        self.store.update_run(r['id'],status='BLOCKED',error=str(exc),logs=r['logs']+['Compatibility check blocked execution'])
                        return
                    output=self.staging/f"{r['id']}.json"
                    if r.get("kind") == RUN_KIND:
                        if r.get("holdout_started_at") is not None:
                            self.store.update_run(r["id"], status="FAILED",
                                                  error="Interrupted dispatch already reserved the holdout")
                            return
                        # Commit the reservation before the process can read held-out labels.
                        r = self.store.update_run(r["id"], holdout_started_at=time.time())
                        p = ComparisonProcess(r, output)
                    else:
                        p = mp.get_context('spawn').Process(
                            target=_worker,
                            args=(r['config'],str(output),r['memory_mb'],r['cpu_seconds'],r['code_sha256'],os.getpid()),
                            daemon=True)
                    try:
                        p.start();self.active[r['id']]=(p,time.monotonic(),output)
                        self.store.update_run(r['id'],status='RUNNING',started_at=time.time(),worker_pid=p.pid,logs=r['logs']+['Spawned isolated trusted worker'])
                    except Exception as exc:
                        self.store.update_run(r['id'],status='FAILED',error=f'Process start failed: {type(exc).__name__}')

    def _monitor(self):
        while not self.closed:
            try:self._tick()
            except Exception as exc:
                # Storage errors cannot silently masquerade as success.
                self.store.audit({'scheduler_error':type(exc).__name__})
            time.sleep(.02)

    def wait(self,run_id,timeout=30):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            r=self.get(run_id)
            if r['status'] in TERMINAL:return r
            time.sleep(.02)
        raise TimeoutError('Caller wait expired; inspect durable task status')

    def backup(self,destination):
        with self.lock:return self.store.backup(destination)

    def close(self):
        with self.lock:
            self.closed=True
            for run_id in list(self.active):self.cancel(run_id)
        self.thread.join(2)
        self._owner_file.close()
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
