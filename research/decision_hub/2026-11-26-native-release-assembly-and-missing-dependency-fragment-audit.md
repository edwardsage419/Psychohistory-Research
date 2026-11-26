# 自主科学知识：真实发布装配版本差异与缺依赖阻断片段审计
2026-11-26。RESEARCH_CANDIDATE / REAL_NATIVE_SOURCE_FRAGMENTS_EXECUTED / SYNTHETIC_FIXTURE / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
同一手动轮第四阶段，起点main 97a05e0b9f9f1d7d8cbd70eb98aa5e73f9b45a3d，#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、历史交接固定blob（未核对最新路径）。第三阶段真实索引身份审计blob da528f2b26429f6c2c29729d0181c50b7ccf8f66发现两处历史装配模块版本变更，本轮仅追查这两处，不重复计之前59次读取或分域退化研究。实际读取旧/新blob及两相关模块：
- decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497 → b833a6d45d944f2f1b885ab1a409df28c390c233
- decision_v05.py bc27cc42e4a8224c86c3113d044a328ae5eeba3e → a98f5496b845b2db5884c87cf0af65a2064233bd
- plugins.py 1777a1c4d5d32fac69df94f132fcc5a457fc231b
- decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f
## 静态差分
完整文本按行LCS比较。registry添加封存状态、注册封存检查与for_release：精确版本、源基线比较、每族单版本、硬门固定版、执行顺序及封存。v05_registry末尾由直接返回registry改为以每个登记方法的版本及source_baseline调用for_release。两处差异均是装配层变化，不能由历史blob不符直接推断科学错误，也不能由数学模块匹配直接认定装配正确。execution_order遇不存在的依赖key直接返回，故发布清单本身不是依赖闭合证明；实际DecisionHub循环另检查executed，前置未成功则INELIGIBLE，不进入run_method。这个分工允许存在未执行的候选；是否需要更严格的发布配置审查由所有者和独立验收决定。以下是实际差分摘要（原始行变化可复算）：
```json
{
  "registry": {
    "old": 126,
    "new": 156,
    "added": 30,
    "deleted": 0
  },
  "v05": {
    "old": 102,
    "new": 104,
    "changes": [
      {
        "op": "-",
        "line": 51,
        "text": "    return registry"
      },
      {
        "op": "+",
        "line": 51,
        "text": "    return registry.for_release("
      },
      {
        "op": "+",
        "line": 52,
        "text": "        (method.model_id, method.version, method.source_baseline) for method in registry.methods()"
      },
      {
        "op": "+",
        "line": 53,
        "text": "    )"
      }
    ]
  }
}
```
## 真实固定源码片段执行
Python 3.13.5 标准库，实际转录plugins.py 81..93行 Registry（558字符，FNV e13247bb）、decision_registry.py 67..145行 DecisionRegistry（3254字符，FNV ff7b9046）、decision_hub.py 229..245行循环（931字符，FNV 1e4a1521）；分别与连接器固定源片段去尾空白FNV一致。FNV是转录校验非密码学证明。实际执行一次，未加载完整Pydantic或原生依赖。Method/Context/entry/run_method及已成功硬门由明确合成夹具替代，真正数学函数、完整登记对象describe、授权、输入验证、结果状态、并发、生命周期、API/CLI/App、设备及实际用户未执行；结果不能升级正式验收。真实v05_registry仅静态审阅，不执行。
64种固定拓扑顺序下四节点DAG、4种current/structural分配、16种版本选择子集，共4096次真实for_release调用；每次4种模拟失败掩码与2种当前候选状态，共32768次真实循环执行，对照独立按拓扑递推的前置成功集合及实际调用集合。硬门事先模拟成功，不测试硬门本身；不能将缺依赖一律视为注册拒绝。6项实际异常控制：缺固定硬门、源基线不符、同族多版本、不存在版本、封存后注册、依赖循环。输入均研究者选定；计数是重复合成结构，不是原生应用端到端错误率、真实科学资格或独立样本。
```json
{
  "graphs": 64,
  "releaseSelections": 4096,
  "executionChecks": 32768,
  "ineligibleMissing": 22537,
  "ineligibleCandidates": 16384,
  "called": 26615,
  "controls": 6
}
```
## 建议
知识更新后需要保留方法精确版本、源基线、所有直接与传递依赖及实际成功状态，显示缺失依赖和方法未执行的区别。仍须针对真实装配模块、完整方法表、可信发布清单来源及全原生路径独立验收。此次发现的是边界与已有阻断在有限片段上的验证，无证据认定生产漏洞或全部可靠；不修改源码、发布清单、唯一交接、PR、历史证据等级、冻结、训练、部署、主动CI或费用。研究者选择合成依赖图、失败、scope及候选配置。
## 复算
下面为等价复算包装，输入顺序为三个固定源文件plugins.py、decision_registry.py、decision_hub.py。实际运行以转录的相同三个片段载入，FNV一致；此文件读取包装未实际运行。不得执行任意网络内容，仅执行上述固定审查自有源码。
```python
import sys,re,types,itertools,textwrap,json
from pathlib import Path
def fragment(p,l,h): return "\n".join(Path(p).read_text(encoding="utf-8").splitlines()[l-1:h]).rstrip()
registry=fragment(sys.argv[1],81,93)
source=fragment(sys.argv[2],67,145)
loop=fragment(sys.argv[3],229,245)
def fnv(s):
 h=2166136261
 for x in s: h=((h^ord(x))*16777619)&0xffffffff
 return f'{h:08x}'
assert [fnv(s) for s in [registry,source,loop]]==['e13247bb','ff7b9046','1e4a1521']
GATE_ID='c028_interval_feasibility'; PIN='a'*40
p=types.ModuleType('probe'); p.__path__=[];sys.modules['probe']=p
m=types.ModuleType('probe.decision_feasibility');m.GATE_ID=GATE_ID;sys.modules[m.__name__]=m
class Method:
 def __init__(self,id,dep=(),scope='current',version='1.0.0'):
  self.model_id=id;self.version=version;self.source_baseline=PIN;self.depends_on=dep;self.candidate_scope=scope;self.validate=lambda c:[];self.execute=lambda c:{}
 @property
 def key(self):return self.model_id+'@'+self.version
 def describe(self):return {'id':self.model_id}
ns={'__name__':'probe.registry','__package__':'probe','Method':Method,'re':re}
exec(registry+'\n'+source,ns); D=ns['DecisionRegistry']; compiled=compile(textwrap.dedent(loop),'hub_slice','exec')
ids=['aa','bb','cc','dd'];key=lambda i:ids[i]+'@1.0.0';gate=Method(GATE_ID)
res={'graphs':0,'releaseSelections':0,'executionChecks':0,'ineligibleMissing':0,'ineligibleCandidates':0,'called':0,'controls':0}
for graph in range(64):
 pairs=list(itertools.combinations(range(4),2)); deps=[[] for _ in ids]
 for k,(a,b) in enumerate(pairs):
  if graph&(1<<k):deps[b].append(key(a))
 for scopes in [0,5,10,15]:
  items=[Method(id,tuple(deps[i]),'structural' if scopes&(1<<i) else 'current') for i,id in enumerate(ids)];reg=D()
  for it in [gate,*items]:reg.register(it)
  for select in range(16):
   selected=[gate,*[it for i,it in enumerate(items) if select&(1<<i)]];rel=reg.for_release((it.model_id,it.version,it.source_baseline) for it in reversed(selected)); res['releaseSelections']+=1
   for fail in [0,5,10,15]:
    for current in [(),('option',)]:
     feasible=('option',); executed={gate.key:{}}; attempted=[]; called=[]
     def entry(method,status,reasons):return {'status':status,'result':{},'key':method.key,'reasons':reasons}
     def run_method(method,context):
      called.append(method.key); i=ids.index(method.model_id);return entry(method,'INELIGIBLE' if fail&(1<<i) else 'EXECUTED',[])
     env=dict(methods=rel.execution_order(),GATE_ID=GATE_ID,feasible=feasible,current=current,executed=executed,attempted=attempted,entry=entry,run_method=run_method,Context=lambda *args:args,state=None)
     exec(compiled,env)
     expected={gate.key}; calls=set()
     for i,it in enumerate(items):
      if not select&(1<<i):continue
      if it.candidate_scope=='current' and not current:res['ineligibleCandidates']+=1;continue
      if not set(deps[i])<=expected:res['ineligibleMissing']+=1;continue
      calls.add(it.key)
      if not fail&(1<<i):expected.add(it.key)
     assert set(executed)==expected and set(called)==calls
     res['executionChecks']+=1;res['called']+=len(called)
 res['graphs']+=1
reg=D();reg.register(gate);reg.register(Method('aa'));reg.register(Method('aa',version='2.0.0'))
def reject(f):
 try:f()
 except ValueError:res['controls']+=1;return
 raise AssertionError('expected rejection')
reject(lambda:reg.for_release([('aa','1.0.0',PIN)]))
reject(lambda:reg.for_release([(GATE_ID,'1.0.0','b'*40)]))
reject(lambda:reg.for_release([(GATE_ID,'1.0.0',PIN),('aa','1.0.0',PIN),('aa','2.0.0',PIN)]))
reject(lambda:reg.for_release([(GATE_ID,'1.0.0',PIN),('aa','3.0.0',PIN)]))
rel=reg.for_release([(GATE_ID,'1.0.0',PIN)]);reject(lambda:rel.register(Method('bb')))
reg2=D();reg2.register(gate);reg2.register(Method('aa',('bb@1.0.0',)));reg2.register(Method('bb',('aa@1.0.0',)));reject(lambda:reg2.for_release((it.model_id,it.version,it.source_baseline) for it in reg2.methods()))
print(json.dumps(res));print(sys.version)
```
