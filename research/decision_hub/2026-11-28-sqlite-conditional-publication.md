# SQLite条件发布
2026-11-28。RESEARCH_CANDIDATE / EXECUTED_LOCAL_SYNTHETIC / NATIVE_NOT_RUN / authority NONE。基线0a61ab4a20363594cf51ade25b10f00949cbe506，开放PR 63,62,61,60,59。实际容器Python SQLite磁盘双连接，顺序模拟授权变更与旧结果发布，核验日志模式。不是并行压力测试。
```python
import sqlite3,tempfile,os
n=0
with tempfile.TemporaryDirectory() as d:
 for mode in ('DELETE','WAL'):
  for rev in range(1,11):
   p=os.path.join(d,mode+str(rev)); a=sqlite3.connect(p); assert a.execute('pragma journal_mode='+mode).fetchone()[0].upper()==mode; a.execute('create table s(rev,grant_id,result)');a.execute('insert into s values(?,?,NULL)',(rev,1));a.commit();b=sqlite3.connect(p); old=b.execute('select rev,grant_id from s').fetchone();a.execute('update s set grant_id=2');a.commit();assert b.execute('update s set result=42 where rev=? and grant_id=?',old).rowcount==0;b.commit();assert b.execute('select result from s').fetchone()==(None,);assert b.execute('update s set result=42 where rev=? and grant_id=2',(rev,)).rowcount==1;b.commit();assert a.execute('select result from s').fetchone()==(42,);a.close();b.close();n+=1
print(n,'stale rejected and fresh accepted')
```
实际输出20 stale rejected and fresh accepted。当前授权正向控制为固定虚构结果，不证明重新计算或授权资格。仅授权字段变化，修订变化未测；未测并发锁竞争、撤回后已发布结果清理、认证恢复或可信回滚。参数由研究者选定，重复非独立样本。唯一交接及全库去重未核实。此前SQLite及HMAC历史报告执行证据需重新复算，不能由本轮追认。无生产修改、训练、合并、部署或新增费用。