# 检查点认证、作用域与重放
2026-11-28。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / authority NONE。
基线3e8adf03d7663dfa65b8da0e98caf0068fa3b324。核对HEAD及开放PR63/62/61/60/59。沿用近期规程、cross-revision-computation-reuse-publication及v0.8已有签名续算合同；本轮是有限认证负向控制，不声称新密码算法或替代既有接口。未重新核对唯一交接及全库去重。
实际Python标准库HMAC-SHA256，固定公开测试密钥，仅用于合成夹具。可信宿主提供当前scope及seq；认证覆盖整个序列化状态。HMAC不能证明签发时计算正确或待处理栈完整，不能独立防止可信序号回滚。生产需密钥隔离、规范编码、严格schema、大小限制、原子持久化、可信代次、授权撤回、完整路径及搜索边界验证。禁止把测试密钥用于生产。
```python
import hashlib,hmac,json,itertools
key=b'synthetic-test-key'
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sign(x):return hmac.digest(key,enc(x),'sha256').hex()
def verify(x,tag,scope,seq):return hmac.compare_digest(sign(x),tag) and x['scope']==scope and x['seq']==seq
counts=dict(valid=0,rejected=0,weak_accept=0)
for cash,goal,rev,seq in itertools.product(range(6),range(1,6),range(3),range(1,5)):
 scope={'cash':cash,'goal':goal,'revision':rev,'method':1,'grant':1,'instance':1}; x={'scope':scope,'seq':seq,'pending':[[0,cash],[1,cash]],'frontier':[[0,0]],'path':[0]};tag=sign(x)
 assert verify(x,tag,scope,seq);counts['valid']+=1
 for field,value in [('pending',[]),('frontier',[[99,99]]),('path',[9]),('seq',seq-1),('scope',dict(scope,revision=rev+1)),('scope',dict(scope,grant=0)),('scope',dict(scope,instance=2)),('scope',dict(scope,method=2))]:
  y=dict(x);y[field]=value;assert not verify(y,tag,scope,seq);counts['rejected']+=1
  counts['weak_accept']+=int(bool(enc(y)))
 for expected,expected_seq in [(dict(scope,revision=rev+1),seq),(dict(scope,grant=0),seq),(scope,seq+1)]:
  assert not verify(x,tag,expected,expected_seq);counts['rejected']+=1
print(counts)
```
实际输出 {'valid': 360, 'rejected': 3960, 'weak_accept': 2880}。weak_accept仅序列化非空，不是实际产品解析或验收基线。研究者选定夹具及攻击类型；重复参数非独立样本。未接入联合求解器，未验证恶意签发、密钥泄漏、可信存储回滚、崩溃、并发或真实设备。下一步独立搜索覆盖证书及联合原型认证恢复。无生产修改、训练、合并、部署、主动CI或新增费用。