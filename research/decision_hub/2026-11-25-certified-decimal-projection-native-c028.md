# v3.2 自主认知专项第10轮（累计第69轮）：原生十进制投影与双向阈值证书

2026-11-25。RESEARCH_CANDIDATE / NATIVE_MODULES_EXECUTED_ISOLATED / SUPPORTED_RUNTIME_NOT_RUN。基线 56d73be4f3ce700938a4bbd52a7e8cf288600c37，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核对最新8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题，非全文审阅）、第62轮ada3d84a46e4d9a411ebf762884d13a5c5e87686、第68轮f814cd526166dc3b3105d2987f75c8d3e13827d6、第31轮a04076828e5094365f3efcbb1b22f5dc8b58cd44及相关目录题名。区别于已有C031后悔精度、共享线性依赖及第68轮严格拒绝不可精确投影：本轮实际连接原生Number验证、等价单位选择与保守双阈值筛查。非全库无重复证明。没有新外部来源或重审原论文。

## 数学合同
已合格的非负持续时间闭界[l,h]与确切阈值t，固定同主体、时间、语义、权限及场景。只允许已确认的正比例单位变换，秒/分钟/小时的比例沿用第62轮；不允许日月年、货币或非比例单位偷换。先尝试所有允许单位的精确投影；每个数通过实际原生Number验证且有理数往返相同。否则在每种单位的十进制网格10^-p（p从12到0）寻找向外舍入可表示四端点，取第一个合法网格，按物理量总外扩误差挑选单个候选（非全局最优网格/证明搜索）。记变回原单位的外界L<=l<=h<=H及阈值外界Tlo<=t<=Thi。对x<t或x<=t，以Tlo做通过检查，Thi做失败检查；对x>t或x>=t反向。因为比较单调，整个外部测量界满足更严格阈值必推出原条件确定满足；整个外界违反更宽松阈值必推出原条件确定违反。否则UNKNOWN，包含原本可以精确判定但投影损失导致未决的情况。不把两个临时阈值视为新的用户底线；只对同一原始约束生成分开的隔离影子检查，最终仅输出合并证书状态。绝不把影子状态直接投入真实多约束决策或修改持久记录。原型保留投影单位、四端点，尚未实现真实原文/来源/修订/授权收据、撤回和跨模块发布验证。未研究联合多变量、概率、非线性或对效用数值的舍入；结论不能直接用于C029等模型。可进一步利用网格约束和严格比较提升完备性，但本轮不主张最优。数学推导为基本单调性，不主张原创定理。

## 真实环境与失败修正
实际容器复用/tmp/ph68两个未修改模块，重新git hash-object及代码内SHA1核对：decision_state.py 0840855431fbc88fe212785584277aa01be74d93、decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f。沿用第68轮空包入口和测试Method=SimpleNamespace、Context替身；使用原生Number的Pydantic TypeAdapter及真实Quantity/Constraint/DecisionState、METHOD.validate/execute。Python3.13.5/Pydantic2.13.5非锁定支持环境（Python3.12/Pydantic2.13.4）；本轮无需重新检出，未验证完整原生registry/hub/API/CLI或设备。首次尝试复用第68轮native函数时发现其constraint单位固定为秒，而测量按新单位转换，导致原生UNKNOWN及实验断言失败；未归档为通过。修正测试适配函数使两个影子输入均使用同一已获资格单位，未改原生代码。修正后初步3744例通过，但精确单位恢复例为0；增加1200000秒及有效整数边界专项控制后执行最终实验。实际当前TypeAdapter接受999999、拒绝1000000（即18 max_digits和12 decimal_places还影响整数位数，而非仅绝对值<=10^12）；1200000秒直接表示失败，换为20000分钟可精确表示。此为本实验环境实测，不替代支持环境验证；补充第68轮数值说明，不修改历史原文。原生拒绝时脚本实验抛错，不具生产异常恢复；实际部署须失败关闭。

## 实验结果
13个非负有理点（含超域压力点，非现实通勤样本）构成91个闭区间×13阈值×4关系=4732情景，主循环实际4212次原生METHOD.execute（不含专项控制）。参照为原始有理端点直接比较；候选确定性输出均一致，0不当确定通过/失败。固定秒严格投影仅504情景可表示，允许单位精确投影592，增加88；向外投影2312；不可投影1828。可表示不代表能得出确定性判断。较第68轮式固定秒严格投影（无表示则保留未知），恢复1474个确定结论；1438个精确参照本可确定但候选仍保留UNKNOWN，1456个参照本来就不确定，合计2894未知。不得将未知误计为错误放行/拒绝。12项控制。未独立留出、真实用户效果、设备性能或科学验收。所有参数为ChatGPT研发辅助生成的项目原创合成开发夹具，无个人数据或训练。只测试有限合法范围及少量无效输入，不支持任意巨大有理数的资源限制或完整运行时鉴权；exact_decimal使用第68轮80位精度转换并检查往返，因此可能拒绝本可表示的超长中间数。候选网格选择及总误差度量为研究选择，未获正式产品规则授权。

## 实际复算
按第68轮报告复原两个原生模块、测试替身和probe.py；保存下列probe69.py，普通解释器执行python probe69.py。实际本机probe69.py SHA256 38ee5dd6b0e39995822bc76d68a0672f835cd8651e208e638839e7a7cf493161；以下为运行代码的文本转录，未另验归档代码的原始字节哈希。完整结果来自本机stdout。原生文件哈希核对由脚本执行。非支持环境不得用作正式验收。

```python
from probe import F, exact_decimal, EXPECTED
from psychohistory.decision_state import DecisionState, Quantity, Constraint
from psychohistory.decision_feasibility import METHOD
from types import SimpleNamespace
import itertools, operator, json, platform, pydantic
from pathlib import Path
import hashlib

for name, sha in EXPECTED.items():
    b=(Path(__file__).parent/"psychohistory"/name).read_bytes()
    if hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest()!=sha: raise RuntimeError("source identity")

SCALES={'s':1,'min':60,'h':3600}
OPS={'<':operator.lt,'<=':operator.le,'>':operator.gt,'>=':operator.ge}

def check(ok,msg):
    if not ok: raise RuntimeError(msg)

def floor(x): return x.numerator//x.denominator
def ceil(x): return -floor(-x)
def grid(x,p,up):
    k=10**p
    return F((ceil if up else floor)(x*k),k)

# Use actual native Number adapter rather than approximating the schema.
from pydantic import TypeAdapter, ValidationError
from psychohistory.decision_state import Number
ADAPTER=TypeAdapter(Number)
def representable(x):
    try:return F(ADAPTER.validate_python(exact_decimal(x)))==x
    except (ValueError,ValidationError):return False

def native(bounds,t,op,unit):
    c=Constraint(id='c',label='weekly duration',unit=unit,operator=op,threshold=exact_decimal(t),source='synthetic shadow comparison',horizon='week')
    q=Quantity(unit=unit,kind='synthetic',source='synthetic outer projection',horizon='week',lower=exact_decimal(bounds[0]),upper=exact_decimal(bounds[1]))
    state=DecisionState(decision_id='a'*32,revision=1,question='synthetic shadow check',confirmed=True,constraints_confirmed=True,constraints=[c],options=[dict(id='A',label='A',measurements={'c':q})])
    ctx=SimpleNamespace(state=state)
    check(not METHOD.validate(ctx),'native validation')
    row=METHOD.execute(ctx)['feasibility'][0]
    status=row['checks'][0]['status']
    check(row['status']=={'CERTAIN_PASS':'ACCEPT','CERTAIN_FAIL':'REJECT','POSSIBLE':'UNRESOLVED'}[status],'native overall')
    return status,row['status']

def project(lo,hi,t,allowed):
    exact=[]; rounded=[]
    for u in allowed:
        f=SCALES[u]; a,b,c=lo/f,hi/f,t/f
        if all(map(representable,(a,b,c))):exact.append((u,a,b,c,c));continue
        for p in range(12,-1,-1):
            l,h,tl,th=grid(a,p,False),grid(b,p,True),grid(c,p,False),grid(c,p,True)
            if all(map(representable,(l,h,tl,th))):
                error=(h-l-b+a+th-tl)*f
                rounded.append((error,u,l,h,tl,th));break
    if exact:return 'EXACT',exact[0]
    if rounded:return 'OUTER',min(rounded,key=lambda x:x[0])[1:]
    return 'UNREPRESENTABLE',None

def solve(lo,hi,t,op,allowed=tuple(SCALES),qualified=True):
    if op not in OPS or not qualified or not allowed or any(u not in SCALES for u in allowed) or lo<0 or lo>hi or t<0:return 'UNKNOWN','BLOCKED',None,0
    mode,r=project(lo,hi,t,allowed)
    if not r:return 'UNKNOWN',mode,None,0
    u,l,h,tl,th=r;f=SCALES[u]
    check(l*f<=lo<=hi<=h*f and tl*f<=t<=th*f,'containment')
    pt,ft=(tl,th) if op.startswith('<') else (th,tl)
    a,_=native((l,h),pt,op,unit=u); b=a if ft==pt else native((l,h),ft,op,unit=u)[0]
    check(a in ('CERTAIN_PASS','CERTAIN_FAIL','POSSIBLE') and b in ('CERTAIN_PASS','CERTAIN_FAIL','POSSIBLE'),'native rejected projection')
    check(not(a=='CERTAIN_PASS' and b=='CERTAIN_FAIL'),'inconsistent certificate')
    return ('PASS' if a=='CERTAIN_PASS' else 'FAIL' if b=='CERTAIN_FAIL' else 'UNKNOWN'),mode,r,1+(ft!=pt)

def main():
    vals=sorted(set(map(F,['0','1/10000000000000','1/1000000000000','1/7','1/3','333333333333/1000000000000','1','60','3600','1000000','1200000','1000000000000','1000000000000000000'])))
    counts=dict(cases=0,nativeCalls=0,exactSeconds=0,exactAny=0,outer=0,unrepresentable=0,pass_=0,fail=0,unknown=0,oracleUnknown=0,conservativeLoss=0,baselineRecovered=0,controls=0)
    examples={}
    for (lo,hi),t,op in itertools.product(itertools.combinations_with_replacement(vals,2),vals,OPS):
        truth=[OPS[op](x,t) for x in (lo,hi)]
        gold='PASS' if all(truth) else 'FAIL' if not any(truth) else 'UNKNOWN'
        old=all(map(representable,(lo,hi,t)))
        got,mode,r,calls=solve(lo,hi,t,op)
        check(got=='UNKNOWN' or got==gold,'wrong certainty')
        counts['cases']+=1;counts['nativeCalls']+=calls;counts['exactSeconds']+=old;counts['exactAny']+=mode=='EXACT';counts['outer']+=mode=='OUTER';counts['unrepresentable']+=mode=='UNREPRESENTABLE';counts[{'PASS':'pass_','FAIL':'fail','UNKNOWN':'unknown'}[got]]+=1;counts['oracleUnknown']+=gold=='UNKNOWN';counts['conservativeLoss']+=gold!='UNKNOWN' and got=='UNKNOWN';counts['baselineRecovered']+=not old and got!='UNKNOWN'
        def witness():return dict(lo=str(lo),hi=str(hi),threshold=str(t),op=op,gold=gold,got=got,mode=mode,projection=list(map(str,r)) if r else None)
        if not old and mode=='EXACT' and got!='UNKNOWN' and 'unit' not in examples:examples['unit']=witness()
        if mode=='OUTER' and got!='UNKNOWN' and 'outer' not in examples:examples['outer']=witness()
        if gold!='UNKNOWN' and got=='UNKNOWN' and 'loss' not in examples:examples['loss']=witness()
    for lo,hi,t,op,allowed,q,want in [(F(1200),F(1200),F(1200),'<',('min',),True,'FAIL'),(F(1,7),F(1,7),F(1,7),'>=',('s',),True,'UNKNOWN'),(F(1,7),F(1,7),F(1),'<',('s',),True,'PASS'),(F(1),F(1),F(1,7),'<',('s',),True,'FAIL'),(F(1),F(1),F(2),'<',('s',),False,'UNKNOWN'),(F(1),F(1),F(2),'<',('USD',),True,'UNKNOWN'),(F(2),F(1),F(2),'<',('s',),True,'UNKNOWN'),(F(1),F(1),F(2),'<',(),True,'UNKNOWN')]:
        check(solve(lo,hi,t,op,allowed,q)[0]==want,'control');counts['controls']+=1
    check(not representable(F(1000000)) and representable(F(999999)), 'native whole-digit boundary');counts['controls']+=1
    check(solve(F(1200000),F(1200000),F(1200000),'<')[1]=='EXACT','unit rescue');counts['controls']+=1
    check(solve(F(1200000),F(1200000),F(1200000),'<',('s',))[1]=='UNREPRESENTABLE','restricted unit');counts['controls']+=1
    check(solve(F(1),F(1),F(1),'=')[0]=='UNKNOWN','operator');counts['controls']+=1
    return dict(counts=counts,examples=examples,python=platform.python_version(),pydantic=pydantic.__version__,source=EXPECTED)
if __name__=='__main__':print(json.dumps(main(),indent=2))
```

```json
{
  "counts": {
    "cases": 4732,
    "nativeCalls": 4212,
    "exactSeconds": 504,
    "exactAny": 592,
    "outer": 2312,
    "unrepresentable": 1828,
    "pass_": 919,
    "fail": 919,
    "unknown": 2894,
    "oracleUnknown": 1456,
    "conservativeLoss": 1438,
    "baselineRecovered": 1474,
    "controls": 12
  },
  "examples": {
    "loss": {
      "lo": "0",
      "hi": "0",
      "threshold": "1/10000000000000",
      "op": "<",
      "gold": "PASS",
      "got": "UNKNOWN",
      "mode": "OUTER",
      "projection": [
        "s",
        "0",
        "0",
        "0",
        "1/1000000000000"
      ]
    },
    "outer": {
      "lo": "0",
      "hi": "0",
      "threshold": "1/10000000000000",
      "op": "<=",
      "gold": "PASS",
      "got": "PASS",
      "mode": "OUTER",
      "projection": [
        "s",
        "0",
        "0",
        "0",
        "1/1000000000000"
      ]
    },
    "unit": {
      "lo": "0",
      "hi": "0",
      "threshold": "1200000",
      "op": "<",
      "gold": "PASS",
      "got": "PASS",
      "mode": "EXACT",
      "projection": [
        "min",
        "0",
        "0",
        "20000",
        "20000"
      ]
    }
  },
  "python": "3.13.5",
  "pydantic": "2.13.5",
  "source": {
    "decision_state.py": "0840855431fbc88fe212785584277aa01be74d93",
    "decision_feasibility.py": "6181d6c578c7ef251e9708d0ffcf65e95d35f88f"
  }
}
```

## 下一步
优先将影子结果绑定至可信原始量身份、推导公式、版本、单位允许列表与原始约束，研究由独立核验器重算投影及判定并拒绝篡改/过期/撤权；核查第54/58/64/66轮及已有收据研究后选择真实原生跨模块接入，避免继续只增加合成枚举。需保持完整用户底线与数学口径，不将条件假设或投影结果升级为现实事实。产品轨维护唯一交接，独立轨冻结未见测试并验证支持环境。未修改生产代码、启动训练、Codex、CI、合并或部署；零新增费用，冻结协议不变。