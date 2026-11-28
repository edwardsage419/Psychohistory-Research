# Atomic incremental policy advance
Baseline 6ad4eddb6793c1b0700e71c415678c165c6684b2; open PRs 63,62,61,60,59.
Actual container execution: policy_incremental.py => 1512 9044 17616 9044; policy_atomic_advance.py => 3.46.1 160 616 616.
New advance function:
```python
def advance(db, expected, budget):
    db.execute('BEGIN IMMEDIATE')
    try:
        host,raw,mac=db.execute('select host,raw,mac from state').fetchone()
        if raw is None:return False
        x=json.loads(raw)
        if not hmac.compare_digest(tag(x),mac) or enc(x['identity'])!=host or x['seq']!=expected or not x['pending']:return False
        for _ in range(budget):
            if not x['pending']:break
            row,pos=step(x['identity'][-1],*x['pending']);x['rows'].append(row);x['pending']=list(pos) if pos[0]<2 else []
        x['seq']+=1
        db.execute('update state set raw=?,mac=?',(enc(x),tag(x)));db.commit();return True
    finally:
        if db.in_transaction:db.rollback()
```
Grid: DELETE/WAL, c=0..4,a,b=1..2,g=0..1,r=0..1, budget=3. Two threads with independent connections synchronize at barrier before calling advance with same expected sequence. Exactly one succeeds each round, 616 rounds; final frontier matches analytical reference and integrity_check ok for 160 runs. Shared frontier implementation. Sequence is not external antirollback anchor; expected sequence alone does not bind caller identity across session replacement. No malformed cursor, crash, concurrent revoke or native app tests. Full script in conversation attachment. Fixed synthetic key and researcher-selected grid overlapping prior tests. Unique handoff and full dedup not verified. No production change, training, merge, deployment or additional cost.