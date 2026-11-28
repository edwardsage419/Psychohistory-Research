# 持久化执行证据补核
2026-11-28，基线 8bb12f8e37a2f8a690d888c6811c3d4e00858467。本轮实际容器Python执行，SQLite 3.46.1。此前HMAC、SQLite事务、SIGKILL、条件发布报告的执行证据不充分，不追认原计数。本轮独立于历史报告执行记录，但同一研究方。
实际输出 DELETE 0/1/2 PASS; WAL 0/1/2 PASS; SQLite 3.46.1。复用sqlite-sigkill-recovery报告脚本，增加断言 pragma journal_mode 返回值与请求一致。条件发布报告脚本重新执行，20 PASS。
HMAC实际执行：
```python
import hmac,hashlib,json,itertools
key=b'synthetic-test-key'; n=bad=0
for c,g,r,m in itertools.product(range(6),range(1,6),range(3),range(1,5)):
 p=dict(cash=c,goal=g,revision=r,method=m,grant=1,instance=1,seq=1,pending=[1],frontier=[],path=[])
 enc=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
 mac=lambda x:hmac.new(key,enc(x),hashlib.sha256).digest()
 tag=mac(p);assert hmac.compare_digest(tag,mac(json.loads(enc(p))));n+=1
 for k in p:
  q=dict(p);q[k]=None;assert not hmac.compare_digest(tag,mac(q));bad+=1
print('HMAC',n,bad)
```
实际输出 HMAC 360 3600。不同于旧报告3960拒绝，不追认。未测试当前宿主范围匹配、可信序号、真实密钥管理、回滚、并行竞争、断电或原生集成。此前300次正常关闭事务仍未复算。参数由研究者选择，非独立验收。未重新核实开放PR、唯一交接及全库去重。无生产修改、训练、合并、部署或新增费用。