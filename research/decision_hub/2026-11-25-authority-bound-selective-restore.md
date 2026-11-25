# 自主认知专项累计第108轮候选：可信授权锚定的选择性恢复与SQLite事务

2026-11-25。RESEARCH_CANDIDATE / ACTUAL_SQLITE_PROTOTYPE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_PLATFORM_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 2f0c17a303bde8ef3e9711a08fcbbbaa8d5e78ec。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前25行、R18 README前55行（实际全文）、R107前22行、固定Git树及现有存储源码和v03测试名称。固定资产：
* platform/future_model/src/psychohistory/storage.py 8f54dc3f13aa5ce7367d8226d6c745210d33ca22（全文读取并审查395行至末尾）
* platform/future_model/tests/test_storage_v03.py bf27873388e623d83b54198111eff710d7424f0a（全文取得，测试名称审查，未执行）
* research/decision_hub/2026-11-24-feedback-replay-and-rollback/README.md f55a6fb6a801bb765b96530ce71b45e58d802852
* research/decision_hub/2026-11-25-method-publication-revision-transaction.md 36b1d776ec4d71ad7f28d27c68feae438a8acb07
* 唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。
F009及历史恢复研究目录存在，未重验全部F009。现有Store已实现一致SQLite快照、对象和审计完整性、暂存目录发布及异常回滚；不重计这些能力，不认定现有科研存储存在个人授权绕过缺陷。R18只演示canRestore身份条件，R107没有持久化。本轮增量为独立的真实SQLite实验：在同一事务中从可信现行授权元数据逐记录筛选恢复载荷，不执行旧备份内权限或计算结果。

## 合同与必要条件
合成A/B两条独立记录。可信当前锚点含ID、授权代次、修订号、允许标记及完整载荷SHA256。撤回及重新授权推进代次；修订推进修订号；删除以本夹具拒绝状态表示，非物理擦除。备份只提供候选数据，不可写入权威表。每条候选必须与当前资格完全一致。缺失可信锚点全部拒绝；重复ID拒绝整个批次，单条不匹配可保留其他独立记录。选取保守精确匹配政策，可能放弃有历史价值但旧修订的记录；本轮无历史查看出口，不能宣称产品已具历史恢复。原子事务清空候选恢复表并写入合格行，故失败回滚保留上次已提交恢复表。真实产品读取必须每次重核当前权限，不能直接显示旧恢复表；本轮不模拟后续授权并发更新。未实现派生结果依赖、模型版本迁移、跨端同步、真实签发、恶意输入schema、权限鉴权、真实备份文件导入、加密或物理删除。SHA256用于绑定已知载荷，不具认证权，不是匿名化，私有摘要不得公开。anchor_available是可信宿主夹具，尚未实现设备可信锚点。若设备仅持有同一份旧备份及其旧授权状态，存在两个观察完全相同的世界（后来撤权/未撤权），任何仅依赖此备份的确定性恢复算法均作相同判断，无法同时保证两世界正确恢复。随机化亦不能保证两世界都正确。真实可信锚点丢失或与备份共同回滚时，必须隔离并独立重新授权，不能假称已解决防回滚。独立重新授权不得自动复活已删除数据；需独立确定允许恢复的具体内容和来源。现有研究存储可作为未来原生实现基础，尚未接入。

## 实测
Python 3.13.5 / SQLite 3.46.1。实际执行/tmp/ph108.py，SHA256 7c1b62d9e499457238b975b6fb7e4fd93a04f6a1b724148d06c3954406e47c0b；以下代码为转录，未独立核对转录字节。5×5状态组合×2锚点可用状态×5载荷模式=250 SQLite实验，直接条件参照由同一研究者编写；30条记录恢复，420条候选按唯一ID计数拒绝，与参照一致。naiveUnsafe=420为无资格筛查的构造基线错误候选数，含重复批次政策导致拒绝的记录，不是实际平台错误率。另真实磁盘SQLite 5控制，包括事务写入后抛出异常、关闭重开仍保持前次提交、恢复正常及缺锚点清空后关闭重开。非真实断电或kill测试，非正式支持环境验收，非完整平台运行。合成材料由ChatGPT辅助研发生成，项目原创开发夹具，不是真人、训练或独立留出。未启动训练、Codex、CI、正式版本、PR合并、部署或新增费用；冻结协议不变。

```python
import sqlite3, json, hashlib, itertools, tempfile, pathlib, sys

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def entry(i,gen=1,rev=1,value=10):
    return {'id':i,'gen':gen,'rev':rev,'value':value}

def initialize(db):
    db.executescript('CREATE TABLE authority(id TEXT PRIMARY KEY,gen INT,rev INT,allowed INT,fp TEXT); CREATE TABLE restored(id TEXT PRIMARY KEY,value INT);')

def current(i,state):
    if state==0:return entry(i),1
    if state==1:return entry(i,rev=2,value=12),1
    if state==2:return entry(i,gen=2),0
    if state==3:return entry(i,gen=3),1
    return entry(i,gen=2,rev=2),0

def restore(db,backup,anchor_available,fail=False):
    with db:
        db.execute('BEGIN IMMEDIATE')
        db.execute('DELETE FROM restored')
        if not anchor_available:return []
        ids=[r['id'] for r in backup]
        if len(ids)!=len(set(ids)):return []
        for r in backup:
            a=db.execute('SELECT gen,rev,allowed,fp FROM authority WHERE id=?',(r['id'],)).fetchone()
            if a==(r['gen'],r['rev'],1,fingerprint(r)):
                db.execute('INSERT INTO restored VALUES(?,?)',(r['id'],r['value']))
                if fail:raise RuntimeError('injected failure')
        return [r[0] for r in db.execute('SELECT id FROM restored ORDER BY id')]

def experiment():
    out=dict(cases=0,matched=0,restored=0,rejected=0,naiveUnsafe=0,controls=0)
    for states in itertools.product(range(5),repeat=2):
        for anchor,mode in itertools.product([False,True],range(5)):
            with sqlite3.connect(':memory:') as db:
                initialize(db)
                backup=[entry('A'),entry('B')]
                for i,s in zip('AB',states):
                    r,ok=current(i,s)
                    db.execute('INSERT INTO authority VALUES(?,?,?,?,?)',(i,r['gen'],r['rev'],ok,fingerprint(r)))
                db.commit()
                if mode==1:backup[0]['value']=99
                if mode==2:backup.append(entry('A'))
                if mode==3:backup=backup[1:]
                if mode==4:backup=[entry('A',gen=3),entry('B',rev=2,value=12)]
                expected=[]
                if anchor and mode!=2:
                    for i,s in zip('AB',states):
                        if mode==4:good=(i=='A' and s==3) or (i=='B' and s==1)
                        else:good=s==0 and not(i=='A' and mode in (1,3))
                        if good:expected.append(i)
                got=restore(db,backup,anchor)
                assert got==expected,(states,anchor,mode,got,expected)
                out['cases']+=1;out['matched']+=1;out['restored']+=len(got)
                out['rejected']+=len({r['id'] for r in backup})-len(got)
                out['naiveUnsafe']+=len(set(r['id'] for r in backup)-set(expected))
    with tempfile.TemporaryDirectory() as tmp:
        path=pathlib.Path(tmp)/'authority.sqlite'
        db=sqlite3.connect(path);initialize(db)
        for i in 'AB':
            r=entry(i);db.execute('INSERT INTO authority VALUES(?,?,?,?,?)',(i,1,1,1,fingerprint(r)))
        db.commit();assert restore(db,[entry('A')],True)==['A'];out['controls']+=1
        try:restore(db,[entry('B')],True,True)
        except RuntimeError:pass
        else:raise AssertionError('failure absent')
        db.close();db=sqlite3.connect(path)
        assert db.execute('SELECT id FROM restored').fetchall()==[('A',)];out['controls']+=1
        assert restore(db,[entry('A'),entry('B')],True)==['A','B'];out['controls']+=1
        assert restore(db,[entry('A'),entry('B')],False)==[];out['controls']+=1
        db.close();db=sqlite3.connect(path)
        assert db.execute('SELECT id FROM restored').fetchall()==[];out['controls']+=1
        db.close()
    return out

if __name__=='__main__':print(json.dumps({'python':sys.version.split()[0],'sqlite':sqlite3.sqlite_version,'result':experiment()},sort_keys=True))
```

实际输出：
```json
{"python": "3.13.5", "result": {"cases": 250, "controls": 5, "matched": 250, "naiveUnsafe": 420, "rejected": 420, "restored": 30}, "sqlite": "3.46.1"}
```
下一责任：手动轨推进记录到派生决策和复盘的资格传播；产品轨维护唯一交接和设备信任方案；独立轨保留未见案例。正式工程另获授权。
