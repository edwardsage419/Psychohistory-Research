# 自主引擎扩展接口：跨端数值精度与活动方法版本合同
2026-11-26。RESEARCH_CANDIDATE / VERIFIED_SOURCE_SLICES_EXECUTED / SYNTHETIC_DEVELOPMENT / PYTHON_NODE_PARITY / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。手动科研增量，非生产实现或独立验收。起始main ef2ea2b83ba05907f1c7a5719d7ed8db35c40957，固定Draft #62 e61bbad10932edabc9a87483e5407fdae6c751cc。核对20近期提交、14开放PR、v3.2前30行、同步规程前35行、唯一交接 research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md 前8行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、v0.8整合规格前12行及前轮全文。所有者已要求给出v0.8任务指令及未来接口，本轮仅继续研究，不改变该任务范围或产品轨唯一交接，不代表Codex已实际启动。检索typed/port/adapter/registry/contract/compatibility/rounding/quantization/precision/conversion，读R4 c05bd6b76e1864a5b7649ae4ef93186817f5b88d及R111 7488da9ef7654f5f4ccbbe3fc720217d94bd0c92相关源码和报告前段，既有按需闭包、有类型边、精确量、分层信封及来源失效不重计。本轮新增有限精度适配的保守判定和多版本共存的显式活动清单实验，不宣称全库去重。
## 固定源码及环境
platform/future_model/src/psychohistory/decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f；decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497（4685字节）。两份全文从连接器重构，本地实际计算Git blob SHA1匹配，并用AST执行check_constraint及Context/Method/DecisionRegistry类，Registry基类从plugins.py 1777a1c4d5d32fac69df94f132fcc5a457fc231b转录；未运行完整plugins模块。源码审查decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f（1–164、168–172、209–245、247–末尾）、decision_v05.py bc27cc42e4a8224c86c3113d044a328ae5eeba3e相关调度、decision_candidates.py a697b9f4dbdde12267f883df29de65e4a2d56723、decision_knowledge_planning.py d32854c4909df858ee851634747234ed5dec657b。Python 3.13.5 / Node 22.16.0本地工具容器，无新增依赖。原生输入为人工资格夹具，未跑Pydantic、完整Hub、Web/API/CLI、Mac/iPhone、生产授权、真实计量或科学独立留出。
## A. 数值适配的精确与保守两层
现有C028只接受同单位同时间范围的闭区间及阈值；这是安全基线而非缺陷。未来扩展适配器若将单位换算后结果舍入至有限精度，可能把硬约束错误放行。可信宿主须先核对主体、指标、量纲、时域、评价口径、用途、代次、映射版本和证据资格；禁止仅凭单位名称、数值相等、候选自报或JSON字段授予资格。汇率、购买力、不同月份长度、不同币种/主体/实际与预测口径不自动作为精确换算。研究仅固定正有理比例，无仿射、非线性、实测误差或真实外汇。
给定闭区间[L,U]、固定阈值T及单调比较op，优先保留原值与正有理数换算并精确比较。受限端点若只能使用网格q>0，构造L'=floor(L/q)q、U'=ceil(U/q)q、Tlo=floor(T/q)q、Thi=ceil(T/q)q。对>=或>，用Thi作为最不利阈值检查确定通过，用Tlo检查确定违反；对<=或<，反向。由于原值和阈值在其外包内，所有扩大域通过则原域通过，所有扩大域违反则原域违反。无法给出确定判定时标UNRESOLVED_PRECISION（实验复用C028状态POSSIBLE，不证明原区间跨越原阈值）。外包阈值仅计算证书，不能覆盖用户原始底线。精确输入缺失或资格冲突仍UNKNOWN，不能用保守舍入补资格。不把图表显示舍入后的值重新输入计算。
实验：11个有符号有理格点组成66闭区间，11阈值×4比较符×3测量换算比例×3阈值换算比例×3输出网格，78408组合。Fraction端点直接真值集合为参照；调用固定C028函数（以人工对象绕开原生状态模型）；Node独立BigInt整数交叉相乘、符号正确的向下/上取整，逐行复核Python生成输入及结果。同一研究者和构造设计，不是独立验收或真实发生率。最近舍入基线采用floor(x/q+1/2)，另一基线仅舍入阈值，不代表现有产品实现。
实际结果：
|指标|数量|
|---|---:|
|构造组合|78408|
|精确C028与端点参照一致|78408|
|保守外包错误确定判定|0|
|保守外包丢失原本确定的判定|8776|
|最近舍入错误确定判定|7484|
|最近舍入错误放行（含将POSSIBLE判PASS）|3742|
|最近舍入错误拒绝（含将POSSIBLE判FAIL）|3742|
|仅舍入阈值错误确定判定|2668|
|Node精确及外包逐行一致|78408 / 78408|
|人工宿主资格负例|19/19拒绝|
负值反例 L=U=-5/3,T=-4/3,q=1/2,op>=：精确FAIL，最近舍入PASS，外包未决。正值同类反例：2/3支出<=1/2上限，最近舍入两者均为1/2而错误PASS。严格不等式与等号保留。Python第二次固定源码实验核心循环2.314秒，Node逐行复核约0.070秒；计时工作不同、不含安装/设备/全部序列化，不作速度优势结论。完整本地研究包包含固定源码、Python、Node、逐行构造输入、结果及核心复算脚本。
## B. 方法多版本共存与活动版本清单
现有Registry以(model_id,version)存储，DecisionRegistry校验精确版本、元数据、来源提交格式并全表拓扑排序。Hub固定get(GATE_ID,"1.0.0")，循环对其他同GATE_ID版本跳过，对其他方法版本逐一尝试。此设计对目前固定内置方法没有证明错误；未来若直接在同一生产注册表添加第二个版本，则可能把同一算法的历史与新版本一并显示为不同方法，且新增硬门版本不会自动生效。实际执行固定DecisionRegistry类及转录Registry，用7个人工Method对象；复现Hub选择和依赖成员循环，假设夹具均适用，未运行完整Hub或方法结果。实际注册顺序包含gate@1/2、producer@1/2、consumer_old@1、consumer_new@1、independent@1；循环尝试两个producer及三个消费者/独立方法，gate@2被跳过。这不是现实用户结果或生产漏洞。
候选合同：档案登记、科学准入、活动版本及影子比较分离。可信发布清单固定每个方法家族一个活动精确版本、来源身份、合同版本与资格；历史版本可在独立重放环境保留；影子实验不能进入正式结果、改变硬门、混入同一活跃路径或写回生产。依赖只能匹配显式精确版本，不以latest、同名或语义相似自动替换。宿主实际硬门必须与清单匹配；当前宿主仅支持1.0.0，升级需要原生入口及验收另行变更。缺硬门、硬门来源不合格全局阻断；其他分支版本冲突、缺失或资格不合格只阻断依赖它的结果，独立有效分支可继续研究准备。来源格式和自报元数据不等于真实准入。候选输出PREPARED / authority NONE，不执行生产决策。
实验：2硬门版本×2生产者活动版本×2资格×2来源匹配×8请求子集=128构造配置。固定生产者1/2、消费者依赖各自版本、独立分支。用闭式条件独立核对递归清单计划。64配置因宿主硬门版本冲突全局阻断；剩余配置96项请求中40准备、56阻断；32个符合硬门条件且请求独立分支的情形全部准备；0非活动版本纳入，0重复家族。另5控制（旧版本主动请求、硬门资格撤回、缺精确版本、重复版本登记拒绝、切换活动版本后旧消费者阻断/新消费者准备）。更新和回退仅通过新清单重算，未实现真实签名、原子切换、旧收据撤销、跨端更新或资源上限。清单粒度及单活动版本规则由研究者选择，未来同族多版本竞争可在明确隔离的影子运行中保留，不能假装同一生产合同。
## C. 对v0.8及后续接口的建议
NumericPort：原始有理数/有界区间、正有理映射及版本、显示精度与计算精度分离、严格比较符、主体/指标/量纲/币种/时域/评价口径、来源/用途/授权代次、原始证据引用、当前性、UNKNOWN/UNRESOLVED_PRECISION和覆盖边界。跨端推荐受限十进制字符串或分子分母字符串；完整序列化规范、资源上限、超大整数及恶意输入待测，不默认支持任意精度。保守结果不可被未知适配器升级。适用G02/G03/G04/G08。
ActiveMethodManifest：明确档案登记与活动发布，方法家族、精确版本、源码/合同/依赖身份、独立资格、支持的宿主门版本、活动/影子/历史状态、迁移和回退记录。先验证活动发布完整性，后求精确依赖闭包；不得自动执行未激活候选；同一已批准清单内固定输入快照、资格及代次。适用G00/G04/G07/G08/G09。现有R4、R111等合同应复用而非再建多套schema。新版本实际实现由已授权Codex任务处理，手动窗口仅提交研究依据。
## D. 核心复算
固定检出e61bbad10932edabc9a87483e5407fdae6c751cc，保存以下代码为replay_core.py，在仓库根运行python replay_core.py（可传入包含固定源码的目录）。实际在本地复算成功，两数组依次为上述数值前8项（第2项精确一致）及版本统计。代码不使用网络或第三方包；assert用于研究测试，普通模式运行，非生产安全门。完整Python/Node回放及19+5控制见本轮会话ZIP。
```python
# Run in fixed v0.7 checkout root, or with directory containing *_fixed.py files.
import ast,hashlib,itertools,math,operator,re,sys
from pathlib import Path
from fractions import Fraction as F
from types import SimpleNamespace as NS
from dataclasses import dataclass,field
from collections.abc import Callable
from typing import Any
D=Path(sys.argv[1]) if len(sys.argv)>1 else Path('platform/future_model/src/psychohistory')
def load(name,sha,kind,ns):
 p=D/(name+'.py');p=p if p.exists() else D/(name+'_fixed.py');b=p.read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha
 tree=ast.parse(b);nodes=[n for n in tree.body if kind(n)]
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
OPERATORS={'>=':operator.ge,'>':operator.gt,'<=':operator.le,'<':operator.lt}
load('decision_feasibility','6181d6c578c7ef251e9708d0ffcf65e95d35f88f',lambda n:isinstance(n,ast.FunctionDef) and n.name=='check_constraint',globals())
def native(l,u,t,op):
 c=NS(source='fixture',unit='canonical',horizon='same',operator=op,threshold=t);v=NS(kind='interval',lower=l,upper=u,source='fixture',unit='canonical',horizon='same')
 return check_constraint(c,v,'same')[0]
def oracle(l,u,t,op):
 s={OPERATORS[op](x,t) for x in (l,u)};return 'CERTAIN_PASS' if s=={True} else 'CERTAIN_FAIL' if s=={False} else 'POSSIBLE'
def floor(x,q):return (x//q)*q
def ceil(x,q):return -((-x)//q)*q
def near(x,q):return math.floor(x/q+F(1,2))*q
def safe(l,u,t,op,q):
 lo,hi=floor(l,q),ceil(u,q);tl,tu=floor(t,q),ceil(t,q);w,b=(tu,tl) if op[0]=='>' else (tl,tu)
 if native(lo,hi,w,op)=='CERTAIN_PASS':return 'CERTAIN_PASS'
 if native(lo,hi,b,op)=='CERTAIN_FAIL':return 'CERTAIN_FAIL'
 return 'POSSIBLE'
C=[0]*8; fs=(F(1),F(1,60),F(3,2));qs=(F(1,2),F(1,5),F(1,10))
for i in range(-5,6):
 for j in range(i,6):
  for k,op,sf,tf,q in itertools.product(range(-5,6),OPERATORS,fs,fs,qs):
   l,u,t=F(i,3)*sf,F(j,3)*sf,F(k,3)*tf; truth=oracle(l,u,t,op);a=native(l,u,t,op);s=safe(l,u,t,op,q);n=native(near(l,q),near(u,q),near(t,q),op);z=native(l,u,near(t,q),op)
   wrong=lambda x:x!='POSSIBLE' and x!=truth
   for h,x in enumerate((1,a==truth,wrong(s),s=='POSSIBLE' and truth!='POSSIBLE',wrong(n),n=='CERTAIN_PASS' and truth!='CERTAIN_PASS',n=='CERTAIN_FAIL' and truth!='CERTAIN_FAIL',wrong(z))):C[h]+=x
assert C==[78408,78408,0,8776,7484,3742,3742,2668];print('precision:',C)
# Fixed source DecisionRegistry, transcribed base Registry from plugins.py.
class Registry:
 def __init__(self):self._plugins={}
 def register(self,p):
  k=(p.model_id,p.version)
  if k in self._plugins or p.version=='latest':raise ValueError('Duplicate or unpinned plugin')
  self._plugins[k]=p
 def get(self,m,v):
  try:return self._plugins[(m,v)]
  except KeyError:raise ValueError('Unknown exact model version') from None
 def describe(self):return [x.describe() for x in self._plugins.values()]
DecisionState=Option=object
load('decision_registry','8046de09674af850a456bbccc534e5f6c2511497',lambda n:isinstance(n,ast.ClassDef),globals())
G,P,A,B,I='c028_interval_feasibility','producer','consumer_old','consumer_new','independent';v1,v2='1.0.0','2.0.0';key=lambda n,v:f'{n}@{v}';src=lambda n,v:hashlib.sha1(key(n,v).encode()).hexdigest()
def m(n,v,deps=()):return Method(model_id=n,version=v,title=n,**{x:'fixture' for x in ('applicability','inputs','outputs','units','assumptions','uncertainty','sources','failure_conditions','replay','baseline')},validate=lambda c:[],execute=lambda c:{'summary':'fixture'},depends_on=deps,source_baseline=src(n,v))
r=DecisionRegistry()
for x in [m(G,v1),m(G,v2),m(P,v1),m(P,v2),m(A,v1,(key(P,v1),)),m(B,v1,(key(P,v2),)),m(I,v1)]:r.register(x)
executed={r.get(G,v1).key}
for x in r.execution_order():
 if x.model_id!=G and all(k in executed for k in x.depends_on):executed.add(x.key)
assert key(G,v2) not in executed and {key(P,v1),key(P,v2)}<=executed
M={x.key:x for x in r.methods()}
def plan(active,grants,roots):
 order=[];done=set()
 def one(root):
  local=[];seen=set();visiting=set()
  def visit(k):
   if k in visiting:raise ValueError('CYCLE')
   if k in seen:return
   if k not in M:raise ValueError('MISSING_VERSION')
   x=M[k];a=active.get(x.model_id)
   if not a or a[0]!=x.version:raise ValueError('INACTIVE_VERSION')
   if a[1]!=x.source_baseline or grants.get(k)!=x.source_baseline:raise ValueError('NOT_QUALIFIED')
   visiting.add(k)
   for d in x.depends_on:visit(d)
   visiting.remove(k);seen.add(k);local.append(k)
  try:visit(root)
  except ValueError as e:return str(e)
  for k in local:
   if k not in done:done.add(k);order.append(k)
  return 'PREPARED'
 if active.get(G,(None,None))[0]!=v1:return 'HOST_GATE_MISMATCH',{},[]
 g=one(key(G,v1))
 if g!='PREPARED':return g,{},[]
 return g,{k:one(k) for k in roots},order
C=[0]*6
for gv,pv,grant,source_ok,mask in itertools.product((v1,v2),(v1,v2),(False,True),(False,True),range(8)):
 active={n:(v,src(n,v)) for n,v in ((G,gv),(P,pv),(A,v1),(B,v1),(I,v1))}
 if not source_ok:active[P]=(pv,'0'*40)
 grants={x.key:x.source_baseline for x in r.methods() if grant or x.model_id!=P};roots=[key(n,v1) for j,n in enumerate((A,B,I)) if mask&(1<<j)];g,states,order=plan(active,grants,roots);C[0]+=1
 if gv!=v1:
  assert g=='HOST_GATE_MISMATCH' and not order;C[1]+=1;continue
 assert g=='PREPARED' and order[0]==key(G,v1)
 for root in roots:
  n=root.split('@')[0];want=n==I or (grant and source_ok and ((n==A and pv==v1) or (n==B and pv==v2)));assert (states[root]=='PREPARED')==want;C[2]+=want;C[3]+=not want;C[5]+=n==I and want
 for k in order:
  n,v=k.split('@');C[4]+=active[n][0]!=v
 assert len({k.split('@')[0] for k in order})==len(order)
assert C==[128,64,40,56,0,32];print('versions:',C)
```
## E. 状态与下一责任方
手动窗口：继续研究精确量与证据、参数、跨端序列化及多模型联合支持的真正连接，避免重复R4/R111和v0.8工程任务。模型轨核对适用口径与方法版本；产品轨维护唯一交接，定义能力及失效显示；独立轨检验未见样本、实际原生入口和设备。Codex在其授权版本中可吸收合格候选，不因本报告扩大已定开发目标。无个人资料、真实训练、外部AI运行时、费用、生产源码更改、PR合并、部署、冻结变更；研究提交使用skip ci，未主动运行CI。所有证据等级保持。
