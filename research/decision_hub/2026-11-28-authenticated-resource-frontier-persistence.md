# 认证资源前沿持久化
2026-11-28。基线 c51707d59e6e30f0c2689a8e5c3067e3b65bfb4a，开放PR63/62/61/60/59。实际容器Python执行输出252 504 252。固定合成密钥，参数由研究者选定。
```python
import sqlite3,json,hmac,hashlib,itertools,tempfile,os
key=b'fictional-test-key'
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def mac(x):return hmac.new(key,enc(x).encode(),hashlib.sha256).hexdigest()
def frontier(v):return sorted({x for x in v if not any(y!=x and all(a>=b for a,b in zip(y,x)) for y in v)})
n=resume=reject=0
with tempfile.TemporaryDirectory() as d:
 for c,a,b,g in itertools.product(range(7),range(1,4),range(1,4),range(4)):
  p=os.path.join(d,'db'); db=sqlite3.connect(p);db.execute('create table if not exists s(rev,grant_id,seq,payload,tag,result)');db.execute('delete from s');scope=[c,a,b,g,1,1];s=dict(scope=scope,seq=0,pending=[0,1],points=[]);db.execute('insert into s values(1,1,0,?,?,NULL)',(enc(s),mac(s)));db.commit()
  for i in range(2):
   db.close();db=sqlite3.connect(p);r,k,q,raw,tag,_=db.execute('select * from s').fetchone();s=json.loads(raw);assert hmac.compare_digest(mac(s),tag) and s['scope']==scope and s['seq']==q and [r,k]==scope[-2:];resume+=1
   j=s['pending'].pop();balance=c-j*a;final=balance+j*g-b
   if balance>=0 and final>=0:s['points'].append([j,final])
   s['seq']+=1;assert db.execute('update s set seq=?,payload=?,tag=? where rev=? and grant_id=? and seq=?',(s['seq'],enc(s),mac(s),r,k,q)).rowcount==1;db.commit()
  f=frontier([tuple(x) for x in s['points']]);ref=frontier([(0,c-b)]*(c>=b)+[(1,c-a+g-b)]*(c>=a and c-a+g>=b));assert f==ref
  assert db.execute('update s set result=? where rev=1 and grant_id=1 and seq=2',(enc(f),)).rowcount==1;db.commit();db.execute('update s set grant_id=2,result=NULL');db.commit();assert db.execute('update s set result=? where rev=1 and grant_id=1 and seq=2',(enc(f),)).rowcount==0;db.commit();assert db.execute('select result from s').fetchone()==(None,);reject+=1;db.close();n+=1
print(n,resume,reject)
```
252配置前沿匹配，504正常重开认证，252正向发布及撤回后拒绝。解析参照共享前沿函数，非独立验收。完整数学输入限四整数，非完整产品作用域；无条件世界、真实崩溃、可信回滚、覆盖证书、真实密钥或原生入口。撤回仅清空结果列，检查点仍存，非隐私删除。与前期资源模型重叠。唯一交接和全库去重未核实。无生产修改、训练、合并、部署或新增费用。