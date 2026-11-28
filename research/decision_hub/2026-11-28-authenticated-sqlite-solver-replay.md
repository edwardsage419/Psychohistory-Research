# 认证SQLite求解恢复联合原型
2026-11-28。实际容器Python执行输出63 63。基线e6fdd02097ff5a45b3f8d3b07dc0d667dbeab363；开放PR 63,62,61,60,59。
```python
import sqlite3,tempfile,os,json,hmac,hashlib
key=b'fictional-test-key'
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def sign(x):return hmac.new(key,encode(x).encode(),hashlib.sha256).hexdigest()
n=bad=0
with tempfile.TemporaryDirectory() as d:
 for cash in range(7):
  for a in range(1,4):
   for b in range(1,4):
    p=os.path.join(d,'state'); db=sqlite3.connect(p);db.execute('create table if not exists s(rev,seq,payload,tag,result)');db.execute('delete from s');state={'rev':1,'seq':0,'pending':[0,1],'best':0};db.execute('insert into s values(1,0,?,?,NULL)',(encode(state),sign(state)));db.commit()
    for i in range(2):
     db.close();db=sqlite3.connect(p);rev,seq,raw,tag,_=db.execute('select * from s').fetchone();s=json.loads(raw);assert hmac.compare_digest(sign(s),tag) and (s['rev'],s['seq'])==(rev,seq);k=s['pending'].pop();s['best']=max(s['best'], (2 if k==0 else 3) if cash >= (a if k==0 else b) else 0);s['seq']+=1;assert db.execute('update s set seq=?,payload=?,tag=? where rev=? and seq=?',(s['seq'],encode(s),sign(s),rev,seq)).rowcount==1;db.commit()
    assert s['best']==max(2*(cash>=a),3*(cash>=b));db.execute('update s set rev=2');db.commit();assert db.execute('update s set result=? where rev=1 and seq=2',(s['best'],)).rowcount==0;db.commit();bad+=1;db.close();n+=1
print(n,bad)
```
63配置、126次重开及认证、63次旧修订拒绝。固定测试密钥，参数未绑定MAC，缺完整作用域、授权字段、正向发布、真实崩溃、独立覆盖证书及多阶段模型。仅正常重开，非安全产品。参数由研究者选定，非独立验收。此前历史持久化报告不能由本轮追认。唯一交接及全库去重未核实。无生产修改、训练、合并、部署或新增费用。