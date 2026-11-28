# SQLite SIGKILL恢复
2026-11-28。RESEARCH_CANDIDATE / EXECUTED_LOCAL_SYNTHETIC / NATIVE_NOT_RUN / authority NONE。基线16c31aea8b55617eec77fe124d475d6c643e844c，开放PR 63,62,61,60,59。前轮正常关闭连接研究的扩展。首批60次超时，不计结果；缩小至6次实际全部通过。
```python
import sqlite3,tempfile,os,subprocess,sys
with tempfile.TemporaryDirectory() as d:
 for mode in ('DELETE','WAL'):
  for stage in range(3):
   p=f'{d}/{mode}{stage}.db';c=sqlite3.connect(p);c.execute('pragma journal_mode='+mode);c.execute('create table s(a,b)');c.execute('insert into s values(0,10)');c.commit();c.close()
   code='import sqlite3,os,signal,sys;c=sqlite3.connect(sys.argv[1]);c.execute("begin");c.execute("update s set a=1");s=int(sys.argv[2]);\nif s>=1:c.execute("update s set b=9")\nif s==2:c.commit()\nos.kill(os.getpid(),signal.SIGKILL)'
   q=subprocess.run([sys.executable,'-c',code,p,str(stage)],timeout=5);assert q.returncode==-9
   c=sqlite3.connect(p);assert c.execute('select * from s').fetchone()==((1,9) if stage==2 else (0,10));assert c.execute('pragma integrity_check').fetchone()==('ok',);c.close();print(mode,stage,'PASS')
```
实际输出 DELETE 0/1/2 PASS，WAL 0/1/2 PASS。未核验实际pragma返回模式，模式标签为请求值。每种仅一次，研究者选择故障点；非独立验收。未覆盖提交中断、断电、并发、认证、可信回滚或原生设备。未核实唯一交接及全库去重，索引尚未补写。无生产修改、训练、合并、部署或新增费用。