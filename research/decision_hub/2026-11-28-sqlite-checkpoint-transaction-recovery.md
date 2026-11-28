# SQLite检查点事务恢复
2026-11-28。RESEARCH_CANDIDATE / EXECUTED_LOCAL_SYNTHETIC / NATIVE_NOT_RUN / authority NONE。基线be39fee3420482fa7c5ea77e786dfdb9543c4fa5。实际容器Python标准库SQLite磁盘临时数据库，100次重复，每次三个事务场景，300次断言通过。关闭连接导致未提交事务回滚；不是进程强杀、断电或真实设备故障。参数由研究者选定，重复非独立样本。
```python
import sqlite3,tempfile,os
n=0
for i in range(100):
 with tempfile.TemporaryDirectory() as d:
  p=os.path.join(d,'state.db'); c=sqlite3.connect(p); c.execute('create table state(seq integer, pending integer)'); c.execute('insert into state values(0,10)'); c.commit()
  for mode in range(3):
   c.execute('begin'); c.execute('update state set seq=1')
   if mode!=0:c.execute('update state set pending=9')
   if mode==2:c.commit()
   c.close();c=sqlite3.connect(p);assert c.execute('select * from state').fetchone()==((1,9) if mode==2 else (0,10));n+=1
  c.close()
print(n)
```
输出300。未接入求解器、认证、授权或生产存储，未验证并发、WAL、磁盘满、回滚攻击、进程强杀或断电。前轮18项索引补归档因HEAD变化未写入，需重新核对。未重新核对开放PR、唯一交接及全库去重。无生产修改、训练、合并、部署或新增费用。