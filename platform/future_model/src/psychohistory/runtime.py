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


def _worker(config, output, memory_mb, cpu_seconds):
    limits={'memory':'NOT_ENFORCED','cpu':'NOT_ENFORCED','hostile_code_sandbox':False}
    try:
        if platform.system()=='Linux':
            import resource
            resource.setrlimit(resource.RLIMIT_AS,(memory_mb*1024**2,memory_mb*1024**2))
            resource.setrlimit(resource.RLIMIT_CPU,(cpu_seconds,cpu_seconds+1))
            limits.update(memory='RLIMIT_AS',cpu='RLIMIT_CPU')
        result=run_experiment(**config)
        data={'ok':True,'result':result,'worker_pid':os.getpid(),'limits':limits}
    except BaseException as exc:
        data={'ok':False,'error':f'{type(exc).__name__}: {str(exc)[:500]}','worker_pid':os.getpid(),'limits':limits}
    write_new(Path(output),canonical(data).encode())

class Scheduler:
    def __init__(self,store,max_concurrency=1,max_queue=16):
        if max_concurrency!=1 or not 1<=max_queue<=16:raise ValueError('v0.1 uses one trusted worker and at most 16 queued tasks')
        self.store=store;self.max_queue=max_queue;self.active={};self.lock=threading.RLock();self.closed=False
        self.staging=checked_path(store.root/'staging');self.staging.mkdir(exist_ok=True,mode=0o700)
        # Prevent two schedulers owning one database. POSIX flock is available on Linux/macOS.
        import fcntl
        self._owner_file=open(checked_path(store.root/'scheduler.lock'),'a')
        try:fcntl.flock(self._owner_file.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            self._owner_file.close();raise ValueError('Another scheduler already owns this data root') from None
        for run in self.store.runs():
            if run['status']=='RUNNING':self.store.update_run(run['id'],status='FAILED',error='Worker lost after scheduler restart; no result claimed')
        self.thread=threading.Thread(target=self._monitor,name='psychohistory-scheduler',daemon=True);self.thread.start()

    def submit(self,config,timeout=15):
        if type(timeout) not in (int,float) or not math.isfinite(timeout) or not 0<timeout<=60:raise ValueError('Wall timeout must be (0,60] seconds')
        with self.lock:
            if self.closed:raise ValueError('Scheduler closed')
            if sum(r['status'] not in TERMINAL for r in self.store.runs())>=self.max_queue:raise ValueError('Queue budget exhausted')
            r=self.store.create_run(uuid.uuid4().hex,config)
            return self.store.update_run(r['id'],timeout=timeout,memory_mb=512,cpu_seconds=5,protocol='synthetic-paired-1.0.0',
                code_sha256=code_identity(),platform_version='0.1.0',data_version='generated-1.0.0',
                environment={'python':platform.python_version(),'os':platform.system(),'machine':platform.machine()},
                logs=['Submitted: awaiting explicit synthetic approval'])

    def approve(self,run_id):
        with self.lock:
            r=self.get(run_id)
            if r['status']!='PENDING':raise ValueError('Only pending task can be approved')
            return self.store.update_run(run_id,status='APPROVED',logs=r['logs']+['Approved for built-in synthetic protocol only'])

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
                        result=data['result'];h=self.store.put(result);self.store.lock_versions(result['versions'])
                        self.store.update_run(run_id,status='COMPLETED',result_hash=h,worker_pid=data['worker_pid'],limits=data['limits'],
                                              logs=r['logs']+result['logs']+['Completed; content hash verified'])
                    except Exception as exc:
                        self.store.update_run(run_id,status='FAILED',error=f'{type(exc).__name__}: {str(exc)[:500]}',logs=r['logs']+['Worker failed; error retained'])
                    finally:self.active.pop(run_id,None);checked_path(output).unlink(missing_ok=True)
            if self.closed:return
            if not self.active:
                queued=[r for r in reversed(self.store.runs()) if r['status']=='APPROVED']
                if queued:
                    r=queued[0];output=self.staging/f"{r['id']}.json"
                    p=mp.get_context('spawn').Process(target=_worker,args=(r['config'],str(output),r['memory_mb'],r['cpu_seconds']),daemon=True)
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
