# 自主认知与科学知识：原生目标发现的引述与跨句作用域片段审计
2026-11-26。RESEARCH_CANDIDATE / REAL_NATIVE_SOURCE_FRAGMENTS_EXECUTED / SYNTHETIC_FIXTURE / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
起点main 8b1b34158d85ff458656a5e21e9cae3c6df7dc6e，本轮初始main 856ae2abaed5baa2391cd3e73c14d806b43c7c45，已核对25近期提交、15开放PR、v3.2及同步规程，#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。唯一交接尝试路径404，未核对最新交接。前阶段白话检索a1e5cc2f80e61e9cb3c6322a52931f11c175d093、粗角色桥接ae9b55bf072d45a80e3126cf6390d92ef226a7c7；已有原文引述、条件和候选研究不重复计。本轮只审真实native discover的跨分句边界，不发明引号扫描或完整语义。
固定原生源码 platform/future_model/src/psychohistory/decision_knowledge_planning.py blob d32854c4909df858ee851634747234ed5dec657b，8行至末尾去尾空白，4112字符，连接器实际FNV c2ae52aa。首次手工转录将scores的依赖元组分行，校验0b6a069c不符，未执行；依据固定源修正后FNV匹配，在Linux容器Python3.13.5实际执行两次，完整输出一致。FNV不是完整字节密码学验证。原生GOALS/TASKS/REQUIREMENTS/_methods/_task/discover原样执行；Method/registry/index/search/source_status替换为明确夹具，未运行真实索引、真实注册表、完整原生、网络、独立留出或设备。未修改生产。
## 实验
5个原生明确目标×13模板×2来源复审状态=130组配对诊断；模板人工给定是否为无条件直接请求。另1不存在方法的控制。native使用原文本，实验引号掩蔽保持非引述分隔符、栈处理指定五种引号及嵌套、失衡拒绝；仅作结构候选对照，未建立原文映射、未执行真实语义授权、未处理所有引号和无标记转述。每组核对authority NONE及原生来源复审或scope待确认状态，缺方法保留NATIVE_UNAVAILABLE。以下为实际容器输出摘要（每行10组）：
```json
{
  "checks": 130,
  "rows": [
    {
      "template": "direct",
      "expectedDirect": true,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    },
    {
      "template": "direct punctuation",
      "expectedDirect": true,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    },
    {
      "template": "fullwidth semicolon",
      "expectedDirect": true,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    },
    {
      "template": "same clause negative",
      "expectedDirect": false,
      "native": 0,
      "quoteMasked": 0,
      "checks": 10
    },
    {
      "template": "simple quote",
      "expectedDirect": false,
      "native": 0,
      "quoteMasked": 0,
      "checks": 10
    },
    {
      "template": "quote inner clause",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 0,
      "checks": 10
    },
    {
      "template": "nested quote",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 0,
      "checks": 10
    },
    {
      "template": "newline quote",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 0,
      "checks": 10
    },
    {
      "template": "unclosed quote",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 0,
      "checks": 10
    },
    {
      "template": "prior negation",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    },
    {
      "template": "prior conditional",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    },
    {
      "template": "hypothetical list",
      "expectedDirect": false,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    },
    {
      "template": "quote then direct",
      "expectedDirect": true,
      "native": 10,
      "quoteMasked": 10,
      "checks": 10
    }
  ],
  "nativeFalseDirectCandidates": 70,
  "maskedFalseDirectCandidates": 30,
  "nativeDirect": 40,
  "maskedDirect": 40,
  "unavailableControl": 1
}
```
## 结论
完整分句匹配仍会将多句引述内的独立分句识别为方法候选，原源码注释关于引述隔离在此限定语境不充分。掩蔽在本组40次引述内误触发中全部阻断，保留40次直接请求候选；跨句否定、未来条件、假设列表的30组仍触发。此处“误触发”仅指候选被视为直接请求时的语义不符，不是现有产品执行越权，所有原生候选仍须scope/review且无权限。不能用该实验宣布真实错误率、完整自然语言理解、科学准入或真实用户改善；引号方案不具备独立验收，不能直接上线。继续从原文作用域及跨句语义确认建立共享接口，避免把候选改写成用户确认的精确目标。研究者自行选定模板、来源状态夹具和掩蔽对照。未修改生产、PR、冻结、证据等级、交接、训练、部署、主动CI或费用。
## 复算
以下为等价文件读取包装，实际容器采用转录源码并校验FNV，测试核心两次执行；此文件读取包装未执行。只允许固定已审查项目源码。
```python
import sys,re,unicodedata,json
from pathlib import Path
from functools import lru_cache
from types import SimpleNamespace
source="\n".join(Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")[7:]).rstrip()
def fnv(s):
 h=2166136261
 for c in s:h=((h^ord(c))*16777619)&0xffffffff
 return f'{h:08x}'
assert fnv(source)=='c2ae52aa',fnv(source)
exec(source,globals())
class Method:
 def __init__(self,key):self.key=key;self.title=key
 def describe(self):return {'key':self.key}
registry=list(map(Method,GOALS.values()))
def v05_registry():return SimpleNamespace(methods=lambda:registry)
class Index:
 def __init__(self,review):self.review=review
 def search(self,goal,limit):return {'authority':'NONE','limit':limit}
 def method_sources(self,method):return ('REVIEW_REQUIRED' if self.review else 'MATCHED_REFERENCE_ONLY',[])
PAIRS={'“':'”','‘':'’','「':'」','『':'』','"':'"'}
def mask_quotes(s):
 stack=[];out=[]
 for c in s:
  if stack and c==stack[-1]:
   stack.pop()
   if not stack:out.append('□')
  elif c in PAIRS:
   if not stack:out.append('□')
   stack.append(PAIRS[c])
  elif not stack:
   if c in set(PAIRS.values())-set(PAIRS):return None
   out.append(c)
 return None if stack else ''.join(out)
def pick(z):
 assert z['authority']=='NONE' and all(x['authority']=='NONE' for x in z['methods'])
 return {m['method'] for m in z['methods']}
T=[('direct','{g}',True),('direct punctuation','{g}。',True),('fullwidth semicolon','{g}；{g}',True),('same clause negative','不要{g}',False),('simple quote','他说“{g}”',False),('quote inner clause','他说“先考虑。{g}。”',False),('nested quote','他说「前文。『前文。{g}。』结束。」',False),('newline quote','他写道：“\n{g}\n”',False),('unclosed quote','他说“前文。{g}。',False),('prior negation','不要执行下面的请求。{g}。',False),('prior conditional','只有以后获得许可才执行。{g}。',False),('hypothetical list','假设另一个人的请求是：\n{g}\n这次只讨论措辞。',False),('quote then direct','他说“别急。{g}。”。{g}',True)]
summary={}
for name,t,want in T:
 row={'template':name,'expectedDirect':want,'native':0,'quoteMasked':0,'checks':0}
 for g,k in GOALS.items():
  q=t.format(g=g);masked=mask_quotes(q)
  for review in [False,True]:
   z=discover(q,Index(review),limit=3);n=pick(z)
   zz=discover(masked,Index(review),limit=3) if masked is not None else {'authority':'NONE','methods':[]};mm=pick(zz)
   assert n<={k} and mm<={k}
   row['native']+=int(k in n);row['quoteMasked']+=int(k in mm);row['checks']+=1
   for x in z['methods']:
    assert x['status']==('REVIEW_REQUIRED' if review else 'NEEDS_SCOPE')
    assert x['frontier'][0]['id']==('reviewSources' if review else 'scope')
 summary[name]=row
key=list(GOALS.values())[0];registry=[m for m in registry if m.key!=key];_methods.cache_clear()
z=discover(list(GOALS)[0],Index(False),limit=3);assert z['methods']==[{'method':key,'status':'NATIVE_UNAVAILABLE','authority':'NONE'}]
print(json.dumps({'fnv':fnv(source),'python':sys.version.split()[0],'summary':summary,'checks':sum(r['checks'] for r in summary.values()),'nativeFalseDirectCandidates':sum(r['native'] for r in summary.values() if not r['expectedDirect']),'maskedFalseDirectCandidates':sum(r['quoteMasked'] for r in summary.values() if not r['expectedDirect']),'nativeDirect':sum(r['native'] for r in summary.values() if r['expectedDirect']),'maskedDirect':sum(r['quoteMasked'] for r in summary.values() if r['expectedDirect']),'unavailableControl':1},ensure_ascii=False))
```
