# v3.2 自主认知专项第9轮（累计第68轮）：精确派生量的原生硬约束接口桥接

2026-11-25。RESEARCH_CANDIDATE / NATIVE_MODULES_EXECUTED_ISOLATED / SUPPORTED_RUNTIME_NOT_RUN。main 7ba253bfa138f4382ea444a9f78607fc01e0c172；13个开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核对最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题及历史阅读，非全文）、第54轮412a98c4bd335864a32f27aa796fc8a42414e7f4、第67轮ca51e90ab907c50524243231dc905f7ad1067ea8。第54轮已经完成共享参数线性推导及身份模拟，本轮不重做该大规模枚举；增量为精确派生量通过真实原生Pydantic输入类及真实C028 METHOD.validate/execute的隔离执行，测量数值可表示性及严格边界。未运行完整语言链及第67轮规划器。

## 真实来源与环境
读取固定main的两个完整模块，经本地逐字转录，用git hash-object独立核对完整Git blob字节身份：
- platform/future_model/src/psychohistory/decision_state.py 0840855431fbc88fe212785584277aa01be74d93
- platform/future_model/src/psychohistory/decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f
另读取decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497、plugins.py 1777a1c4d5d32fac69df94f132fcc5a457fc231b，未执行；pyproject.toml 98b211adda09baadafa58007a49bdb18a382e0bd要求Python>=3.12,<3.13、Pydantic 2.13.4。容器git ls-remote实际DNS失败，Python3.12未发现，实际Python3.13.5/Pydantic2.13.5，均超出锁定环境。无额外安装和费用。隔离包使用空__init__.py、仅提供Method=SimpleNamespace的测试替身（原生METHOD构造只用于保存函数和元数据，未执行实际注册表）；context亦用SimpleNamespace。两个真实模块内容未经修改，运行了真实Constraint/Quantity/DecisionState、METHOD.validate和METHOD.execute，非全原生hub/run_method、API、CLI、注册表、支持环境或设备测试。不能将本轮结果算正式验收。历史C028来源卡身份沿用第67轮7cb8d5e3631dd17c0650cec06139d88b5bfcc700，未重审外部原论文。

## 推导与接口
示例为已获资格的单次通勤时间闭界[l,h]及已确认同一周的确切非负次数n。每次均受同一界约束并包含全部应计通勤时，周总量界[n*l,n*h]，按秒/分钟/小时换算；不需要统计独立即可得到外界。若端点可联合达到则为紧界；本轮夹具假定可达到，不推断实际通勤规律。单次平均值、未知次数、周范围变化、往返定义及主体未核时不得自动乘算。所有数值与权限、来源资格为人工合成夹具，无真实个人记录。用Fraction保留精确有理数，统一秒再投影Decimal，验证往返等于原数。原生Number最大18位数字、12位小数、绝对值<=10^12等约束继续生效；不可精确表达或超域返回UNREPRESENTABLE，绝不取中点或静默舍入。本轮没有实现更换等价单位、保守向外舍入、完整收据、原始字段的真实身份与撤回；source字符串为合成来源标记而非真实鉴权。若无资格或范围不一致则以unknown空界送入原生，底线未确认则原生validate阻断。没有将合成假设升级成事实或取得生产授权。

## 实际实验
15个单次时间闭区间×3单位×4次数×8阈值×4比较符=5760个原生筛查；参照逐次累加端点后直接判定单项及总体结果。836个跨阈值或严格边界未决例全部保持POSSIBLE/UNRESOLVED。中点基线418个强行通过、418个强行拒绝；指对可能区间的不当确定性，不是实际发生错误或原生产品缺陷。11项控制包括无资格、次数未知、范围错误、等号、无限循环小数、超小数精度、超范围、单位、周范围、底线未确认。原型与参照同研究者设计，非独立留出；样例为ChatGPT研发辅助生成的项目原创合成材料，非真人、训练或真实使用效果。无实际真机资源测试。实验脚本使用普通assert，在正常解释器执行，不能用python -O作为验收。

## 复算
从上列固定commit复制两个原始模块至隔离psychohistory目录，空__init__.py；仅在本实验中建立decision_registry.py如下：
```python
# Test-only stand-in for metadata constructor; not native registry.
from types import SimpleNamespace
Method = SimpleNamespace
```
将以下脚本保存为probe.py（本轮实际运行版本SHA256 b184293d8a3e49d078cefe9022ab169cc85971614eacf39c459f42b049a0917c），使用上述隔离环境运行python probe.py。脚本开头核对真实模块字节；不得在正式生产代码中使用测试替身。

```python
import json, platform, hashlib, itertools, operator
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
from types import SimpleNamespace
import pydantic
from pydantic import ValidationError
from psychohistory.decision_state import DecisionState, Quantity, Constraint
from psychohistory.decision_feasibility import METHOD

ROOT = Path(__file__).parent
EXPECTED = {'decision_state.py':'0840855431fbc88fe212785584277aa01be74d93', 'decision_feasibility.py':'6181d6c578c7ef251e9708d0ffcf65e95d35f88f'}
for name, sha in EXPECTED.items():
    b=(ROOT/'psychohistory'/name).read_bytes()
    assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==sha

# A qualified fixture supplies same subject, week, scenario, permission and constant count.
# No extrapolation from average trip to future weekly total without explicit bounds.
def derive(lo, hi, unit, count, qualified, count_known, same_scope):
    if not qualified or not count_known or not same_scope or type(count)!=int or count<0 or unit not in ('s','min','h') or lo<0 or lo>hi:
        return None
    scale={'s':1,'min':60,'h':3600}[unit]
    return lo*scale*count,hi*scale*count

def exact_decimal(x):
    with localcontext() as ctx:
        ctx.prec=80
        d=Decimal(x.numerator)/Decimal(x.denominator)
    if F(d)!=x: raise ValueError('nonterminating decimal')
    return str(d)

def native(bounds, threshold, op, confirmed=True, unit='s', horizon='2027-W01'):
    try:
        c=Constraint(id='c',label='weekly commute',unit='s',operator=op,threshold=exact_decimal(threshold),source='synthetic confirmed limit',horizon='2027-W01')
        q=Quantity(unit=unit,kind='unknown' if bounds is None else 'synthetic',source='' if bounds is None else 'synthetic formula v1',horizon=horizon,**({} if bounds is None else dict(lower=exact_decimal(bounds[0]),upper=exact_decimal(bounds[1]))))
        s=DecisionState(decision_id='a'*32,revision=1,question='synthetic weekly commute',confirmed=True,constraints_confirmed=confirmed,constraints=[c],options=[dict(id='A',label='A',measurements={'c':q})])
    except (ValueError,ValidationError):
        return 'UNREPRESENTABLE',None
    ctx=SimpleNamespace(state=s)
    if METHOD.validate(ctx): return 'UNCONFIRMED',None
    r=METHOD.execute(ctx)['feasibility'][0]
    return r['checks'][0]['status'],r['status']

def main():
    counts=dict(cases=0,matches=0,pass_=0,fail=0,possible=0,naiveWrongPass=0,naiveWrongFail=0,controls=0)
    witness=None
    ops={'>=':operator.ge,'>':operator.gt,'<=':operator.le,'<':operator.lt}
    vals=[F(0),F(1,10),F(1),F(3,2),F(2)]
    for lo,hi in itertools.combinations_with_replacement(vals,2):
        for unit,count,threshold,op in itertools.product(('s','min','h'),(0,1,2,5),(F(0),F(1,10),F(1),F(6),F(60),F(360),F(3600),F(7200)),ops):
            b=derive(lo,hi,unit,count,True,True,True)
            # Independent explicit per-trip addition and endpoint comparison.
            factor={'s':1,'min':60,'h':3600}[unit]
            endpoints=[sum([x*factor]*count,F(0)) for x in (lo,hi)]
            truth=[ops[op](x,threshold) for x in endpoints]
            gold='CERTAIN_PASS' if all(truth) else 'CERTAIN_FAIL' if not any(truth) else 'POSSIBLE'
            got,overall=native(b,threshold,op)
            assert got==gold and overall=={'CERTAIN_PASS':'ACCEPT','CERTAIN_FAIL':'REJECT','POSSIBLE':'UNRESOLVED'}[gold]
            counts['cases']+=1;counts['matches']+=1;counts[{'CERTAIN_PASS':'pass_','CERTAIN_FAIL':'fail','POSSIBLE':'possible'}[gold]]+=1
            # Deliberately simplistic midpoint in seconds, ignores interval uncertainty.
            naive=ops[op](sum(endpoints)/2,threshold)
            if gold=='POSSIBLE':
                counts['naiveWrongPass' if naive else 'naiveWrongFail']+=1
                if witness is None: witness=dict(lo=str(lo),hi=str(hi),unit=unit,count=count,threshold=str(threshold),op=op,native=got,midpoint=naive)
    for qualified,known,scope in [(False,True,True),(True,False,True),(True,True,False)]:
        assert native(derive(F(1),F(2),'h',2,qualified,known,scope),F(3600),'<')[0]=='UNKNOWN';counts['controls']+=1
    for b,t,op,kw,e in [((F(1),F(1)),F(1),'<',{},'CERTAIN_FAIL'),((F(1),F(1)),F(1),'<=',{},'CERTAIN_PASS'),((F(1,3),F(1,3)),F(1),'<',{},'UNREPRESENTABLE'),((F(1,10**13),F(1,10**13)),F(1),'<',{},'UNREPRESENTABLE'),((F(10**12+1),F(10**12+1)),F(1),'<',{},'UNREPRESENTABLE'),((F(1),F(1)),F(1),'<',{'unit':'h'},'UNKNOWN'),((F(1),F(1)),F(1),'<',{'horizon':'2027-W02'},'UNKNOWN'),((F(1),F(1)),F(1),'<',{'confirmed':False},'UNCONFIRMED')]:
        assert native(b,t,op,**kw)[0]==e,(b,t,kw,e,native(b,t,op,**kw));counts['controls']+=1
    return dict(counts=counts,witness=witness,python=platform.python_version(),pydantic=pydantic.__version__,source=EXPECTED,probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__': print(json.dumps(main(),ensure_ascii=False,indent=2))
```

实际输出：
```json
{
  "counts": {"cases":5760,"matches":5760,"pass_":2462,"fail":2462,"possible":836,"naiveWrongPass":418,"naiveWrongFail":418,"controls":11},
  "witness":{"lo":"0","hi":"1/10","unit":"s","count":1,"threshold":"0","op":">","native":"POSSIBLE","midpoint":true},
  "python":"3.13.5","pydantic":"2.13.5",
  "source":{"decision_state.py":"0840855431fbc88fe212785584277aa01be74d93","decision_feasibility.py":"6181d6c578c7ef251e9708d0ffcf65e95d35f88f"},
  "probe_sha256":"b184293d8a3e49d078cefe9022ab169cc85971614eacf39c459f42b049a0917c"
}
```

## 后续
优先连接实际语言语义IR、来源身份/派生收据和第67轮补证前沿；研究在原生有限Decimal表示中选择合法等价单位或可验证向外舍入证书，保留不可表示的未知及精度损失，避免改写数学核心。下一轮可在零费用条件内研究通用数值投影与原生结果不误判，先检查历史精度验收。独立轨负责支持版本环境、真实原生完整入口及未见输入，产品轨维护唯一交接。无生产代码变更、训练、Codex任务、CI、合并、部署或新增费用，冻结协议不变。