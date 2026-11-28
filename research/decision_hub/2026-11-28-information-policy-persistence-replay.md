# 信息条件策略持久化复算
2026-11-28。基线51cbedd19b24d3581462bcebe64791a5bb49ba55，开放PR63/62/61/60/59。实际容器Python执行输出126 378。
```python
import sqlite3,tempfile,json,hmac,hashlib,itertools
key=b'synthetic'
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def mac(x):return hmac.new(key,enc(x).encode(),hashlib.sha256).hexdigest()
n=0
with tempfile.TemporaryDirectory() as d:
 for c,a,b,r in itertools.product(range(7),range(1,4),range(1,4),range(2)):
  p=d+'/db'; db=sqlite3.connect(p);db.execute('create table if not exists s(payload,tag)');db.execute('delete from s');s={'scope':[c,a,b,r],'pending':list(range(9)),'ok':False};db.execute('insert into s values(?,?)',(enc(s),mac(s)));db.commit()
  for _ in range(3):
   db.close();db=sqlite3.connect(p);raw,tag=db.execute('select * from s').fetchone();s=json.loads(raw);assert hmac.compare_digest(mac(s),tag) and s['scope']==[c,a,b,r]
   for j in range(3):
    x,y=divmod(s['pending'].pop(),3);cost=[a,b,a+b];s['ok'] |= (x in (0,2) and y in (1,2) and max(cost[x],cost[y])<=c and (r or x==y))
   db.execute('update s set payload=?,tag=?',(enc(s),mac(s)));db.commit()
  assert s['ok']==(c>=(max(a,b) if r else a+b));db.close();n+=1
print(n,3*n)
```
126配置，378重开认证，全部解析匹配。仅单次行动前后披露，非完整多阶段联合原型；没有延迟收益、前沿、授权、序号、防回滚、路径证书或真实崩溃。固定测试密钥。与前期非预知策略实验重叠，非独立样本。研究者选择参数。唯一交接、全库去重未核实。无生产修改、训练、合并、部署或新增费用。