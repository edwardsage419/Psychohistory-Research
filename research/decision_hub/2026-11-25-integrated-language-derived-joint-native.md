# v3.2 自主认知专项第12轮（累计第71轮）：有限语言、派生量、联合逻辑及原生数学整合

2026-11-25。RESEARCH_CANDIDATE / NATIVE_MODULES_EXECUTED_ISOLATED / SUPPORTED_RUNTIME_NOT_RUN。基线 6bec0bcfd3129306531b4e0aa17e8adc804bf89c，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核对最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题及历史阅读，非全文审计）、第63轮296465980e23a1d8082f81a8181343668965328b、第70轮1a6572805eaeb9400ca5b8429a14e1f518493a91、第6轮9f3294756c22b012a53863df47984043065f4de7。与R6结构化人工夹具、R63纯JS联合推理、R68-70原生数值与原子合取收据区别：实际从有限中文解析，改编R63单变量阈值分区并连接R70原生原子影子计算及其数学核验器，保留完整逻辑结构，不把原生合取误作复合语义。未重新运行R63完整JS或R67方法发现，不声称全闭环。

## 语义、资格、推理合同
有限语法仅每周通勤+少于/最多/超过/至少+非负ASCII十进制(至多9位整数、6位小数)+秒/分钟/小时及且/或者/并非/全角括号。全文消耗，400字符、25 token、128树限制，保留全部可解析树及Python Unicode字符位置（非UTF16统一协议）。这里仅单一可信绑定周总通勤量，原始单次时间闭界、确切次数及资格由R70同范围人工宿主夹具给定，非白话自动抽取。原文完整一致、逐出现义务清单、主体绑定、范围、来源和授权独立由夹具给定；原子清单由生成器构造，不依赖候选解析器。逻辑树集合由解析器产生，未独立验证任意原文逻辑覆盖；本实验参照预设有限表达式。原生状态的constraints投影仅为原子影子比较集合，不能代表用户全部硬约束的真实合取。逐原子复用R70 produce/verify，核对数值界、投影、资格及收据。源快照绑定文本、原子、逻辑树、同一量身份。单个原子原生确定性与精确参照若冲突则实验失败；UNKNOWN或NO_CERTIFICATE不产生原生通过。对同一派生量闭域，分割在所有阈值与域端点，取端点及相邻中点，对所有树与点求值；证明沿用R63阈值分区。4096树点求值上限；不构造概率。联合全真PASS、全假FAIL、混合UNKNOWN；只在已获资格的连续闭域与有限解释集合内成立。单一域为可靠外界时确定性保守有效，但未知不等于现实可达两端；不冒称预测。多个变量/相关域、任意语言、长期记录、跨轮真实确认、真实用户交互未实现。R70核验器仅复核原子影子收据；本轮的联合结果由实验独立参照核对，未实现生产级联合证书核验器及可信签发、发布事务。authority NONE。原生整体合取字段保留仅用于故意错误基线，严禁直接作为OR/NOT或多解释语句的结果。多个树可能等价，不等于实际语义歧义。对于超原生范围参数，联合有理数研究计算可以有确定结果，但原生仍UNKNOWN，必须在产品中分开标记与审查，不能绕过正式原生准入。

## 实际环境与实验
容器/tmp/ph68实际复用；git hash-object重新核对原生decision_state.py 0840855431fbc88fe212785584277aa01be74d93、decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f；probe.py SHA256 b184293d8a3e49d078cefe9022ab169cc85971614eacf39c459f42b049a0917c、probe69.py 38ee5dd6b0e39995822bc76d68a0672f835cd8651e208e638839e7a7cf493161、probe70.py d3681bbf0d4bd771bdb7d8c816ff0adfcc99a59397ef3d944841803e784f970e实际核对。真实Pydantic原生数据结构、METHOD.validate/execute，测试Method/Context替身，Python3.13.5/Pydantic2.13.5非正式支持版本（3.12/2.13.4），完整注册表、hub、API、CLI、设备未执行。4操作组合×3阈值组×6逻辑表达式=72构造文本，各6原始闭区间×2次数=864情景、2592主循环原生计算，864原子收据验证；参照用独立直接布尔表达式及15秒网格，在本实验阈值和域端点为30秒倍数的有限合同内完整覆盖真值类。289 PASS、292 FAIL、283 UNKNOWN。576多树情景包含同一逻辑运算的结合律等价树，非576真正有语义差异的情景。基线1为独立原子可能真值集合笛卡尔积，丢失同变量关系，多出71 UNKNOWN，无错误确定；基线2为直接将R70原子整体合取视作全文结论，369个不当确定（包含对真实UNKNOWN强行确定或反向），88额外UNKNOWN；非实际产品错误率或普通AI对照。15专项控制及2个额外手动探针（不计主循环和15项）如下。所有样例为ChatGPT研发辅助生成的原创合成开发夹具，非真实决策数据、独立留出或训练。无新增外部文献事实、原论文重审、真实使用效果或资源性能结论。

额外实际执行：单次精确1/7秒、一次，文本“每周通勤超过0.142857秒且每周通勤少于0.142858秒”，两个原生OUTER原子均PASS（2次原生计算），联合PASS。超域压力点10^18秒、一次，文本“每周通勤超过1秒”，原生NO_CERTIFICATE/UNKNOWN（0次原生计算），联合有理数研究PASS；只能按研究结果区分发布资格，不冒充原生支持。复跑：from probe71 import *；integrate(make(text,parts,lo,hi,1))，parts为原文原子、比较符、有理秒阈值三元组。未加入主循环统计。

## 复算
按R68-70报告恢复两个原生模块与实验脚本。本机实际执行probe71.py SHA256 a49869f298c880ff227a7e15ce4e6664a513b088f51b64c1c1638cd2a8641982。以下为运行代码转录，未另验归档脚本字节。普通解释器执行python probe71.py；非支持环境仅探索。

```python
import copy, hashlib, itertools, json, re
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as F
from probe70 import fixture, produce, verify, digest, OPS, SCALES, META, check

check(hashlib.sha256((Path(__file__).parent/'probe70.py').read_bytes()).hexdigest()=='d3681bbf0d4bd771bdb7d8c816ff0adfcc99a59397ef3d944841803e784f970e','R70 identity')
WORDS={'少于':'<','最多':'<=','超过':'>','至少':'>='}
UNITS={'秒':'s','分钟':'min','小时':'h'}
ATOM=re.compile(r'每周通勤(少于|最多|超过|至少)((?:0|[1-9][0-9]{0,8})(?:\.[0-9]{1,6})?)(分钟|小时|秒)')
LEX={'并非':'!','或者':'|','且':'&','（':'(','）':')'}

def parse(s):
    if not isinstance(s,str) or len(s)>400:return None
    atoms=[];tokens=[];p=0
    while p<len(s):
        m=ATOM.match(s,p)
        if m:
            o,v,u=m.groups();end=m.end();atoms.append([p,end,s[p:end],WORDS[o],str(F(v)*SCALES[UNITS[u]])]);tokens.append(('a',len(atoms)-1));p=end
        else:
            k=next((k for k in LEX if s.startswith(k,p)),None)
            if k is None:return None
            tokens.append((LEX[k],));p+=len(k)
        if len(tokens)>25:return None
    def grouped(l,r):
        if r-l<3 or tokens[l][0]!='(' or tokens[r-1][0]!=')':return False
        d=0
        for j in range(l,r):
            d+=(tokens[j][0]=='(')-(tokens[j][0]==')')
            if d<=0 and j!=r-1:return False
        return d==0
    @lru_cache(None)
    def span(l,r):
        out=[]
        def add(t):
            out.append(t)
            if len(out)>128:raise ValueError('tree limit')
        if r-l==1 and tokens[l][0]=='a':add(tokens[l])
        if grouped(l,r):
            for x in span(l+1,r-1):add(x)
        if r-l>=2 and tokens[l][0]=='!' and ((r-l==2 and tokens[l+1][0]=='a') or grouped(l+1,r)):
            for x in span(l+1,r):add(('!',x))
        for j in range(l+1,r-1):
            if tokens[j][0] in ('&','|'):
                for x in span(l,j):
                    for y in span(j+1,r):add((tokens[j][0],x,y))
        return tuple(out)
    try:trees=span(0,len(tokens)) if tokens else ()
    except ValueError:return None
    return (atoms,trees) if trees else None

def evaluate(t,b):
    k=t[0]
    if k=='a':return b[t[1]]
    if k=='!':return not evaluate(t[1],b)
    return (evaluate(t[1],b) and evaluate(t[2],b)) if k=='&' else (evaluate(t[1],b) or evaluate(t[2],b))
def verdict(v):return 'PASS' if all(v) else 'FAIL' if not any(v) else 'UNKNOWN'

def integrate(s):
    # Host manifest is trusted fixture; raw text and each occurrence must match.
    p=parse(s['text'])
    if not p or s['text']!=s['confirmedText'] or p[0]!=s['obligations'] or not s['bindingOK']:return None,0
    atoms,trees=p
    q=copy.deepcopy(s['state']);q['constraints']=[];q['semanticBinding']=dict(text=s['text'],atoms=atoms,trees=trees,root='trip',scope=q['scope'])
    for i,(start,end,source,op,t) in enumerate(atoms):q['constraints'].append(dict(id='a'+str(i),version=1,source=source,scope=copy.deepcopy(q['scope']),confirmed=True,t=t,unit='s',op=op))
    r,calls=produce(q)
    if r is None:return None,0
    check(verify(q,r),'native atom receipt')
    lo,hi=map(F,r['derived']);cuts=sorted({lo,hi}|{F(a[4]) for a in atoms if lo<=F(a[4])<=hi});points=cuts+[(a+b)/2 for a,b in zip(cuts,cuts[1:])]
    if len(points)*len(trees)>4096:return None,calls
    truth=[[OPS[a[3]](x,F(a[4])) for a in atoms] for x in points]
    for i,row in enumerate(r['rows']):check(row['result']=='UNKNOWN' or row['result']==verdict([b[i] for b in truth]),'atom conflict')
    joint=verdict([evaluate(t,b) for t in trees for b in truth])
    # Independent atom truth abstraction, and intentionally incorrect flat AND.
    abstract=verdict([evaluate(t,b) for t in trees for b in itertools.product(*[sorted({b[i] for b in truth}) for i in range(len(atoms))])])
    flat={'ACCEPT':'PASS','REJECT':'FAIL','UNRESOLVED':'UNKNOWN'}[r['overall']]
    return dict(text=s['text'],sourceSnapshot=digest(s),native=r,joint=joint,abstract=abstract,flat=flat,trees=len(trees),points=len(points),authority='NONE'),calls

def make(text,parts,lo,hi,n):
    # Expected occurrence values from generator, not candidate parser.
    pos=0;expected=[]
    for atom,op,t in parts:
        start=text.index(atom,pos);end=start+len(atom);expected.append([start,end,atom,op,str(t)]);pos=end
    return dict(text=text,confirmedText=text,obligations=expected,bindingOK=True,state=fixture(str(lo),str(hi),n,'0','0','>=','<='))

def main():
    counts=dict(texts=0,cases=0,nativeCalls=0,receiptChecks=0,pass_=0,fail=0,unknown=0,extraUnknownAbstract=0,flatWrongCertain=0,flatExtraUnknown=0,ambiguousCases=0,controls=0)
    witness={}
    for ops,ts,mode in itertools.product([('<','>=','<='),('>=','<','>'),('<=','>','<'),('>','>=','<=')],[(0,60,60),(60,60,120),(120,60,0)],['and','or','left','right','bare','neg']):
        parts=[]
        for i,(op,t) in enumerate(zip(ops,ts)):
            word=next(k for k,v in WORDS.items() if v==op);a='每周通勤'+word+(str(t//60)+'分钟' if i==1 else str(t)+'秒');parts.append((a,op,t))
        a,b,c=[p[0] for p in parts];text={'and':a+'且'+b+'且'+c,'or':a+'或者'+b+'或者'+c,'left':'（'+a+'且'+b+'）或者'+c,'right':a+'且（'+b+'或者'+c+'）','bare':a+'且'+b+'或者'+c,'neg':'并非（'+a+'且'+b+'或者'+c+'）'}[mode];counts['texts']+=1
        for (lo,hi),n in itertools.product([(0,0),(0,60),(0,120),(30,60),(60,120),(120,120)],(1,2)):
            s=make(text,parts,lo,hi,n);r,calls=integrate(s);check(r is not None,'integrate')
            # All thresholds and domain endpoints multiples of 30; 15-second grid covers every truth cell.
            vals=[]
            for x in range(lo*n,hi*n+1,15):
                A,B,C=[OPS[o](F(x),F(t)) for o,t in zip(ops,ts)]
                vals.extend({'and':[A and B and C],'or':[A or B or C],'left':[(A and B) or C],'right':[A and (B or C)],'bare':[(A and B) or C,A and (B or C)],'neg':[not((A and B) or C),not(A and (B or C))]}[mode])
            gold=verdict(vals);check(r['joint']==gold,'joint mismatch');counts['cases']+=1;counts['nativeCalls']+=calls;counts['receiptChecks']+=1;counts[{'PASS':'pass_','FAIL':'fail','UNKNOWN':'unknown'}[gold]]+=1;counts['ambiguousCases']+=r['trees']>1
            check(r['abstract']=='UNKNOWN' or r['abstract']==gold,'abstract certainty')
            for key,test in [('extraUnknownAbstract',r['abstract']=='UNKNOWN' and gold!='UNKNOWN'),('flatWrongCertain',r['flat']!='UNKNOWN' and r['flat']!=gold),('flatExtraUnknown',r['flat']=='UNKNOWN' and gold!='UNKNOWN')]:
                if test:counts[key]+=1;witness.setdefault(key,dict(text=text,lo=lo,hi=hi,n=n,joint=gold,abstract=r['abstract'],flat=r['flat']))
    s=make('每周通勤少于60秒且每周通勤至少60秒',[('每周通勤少于60秒','<',60),('每周通勤至少60秒','>=',60)],0,120,1)
    r,_=integrate(s);check(r['joint']=='FAIL' and r['flat']=='UNKNOWN','contradiction');counts['controls']+=1
    for k,v in [('text',s['text']+'。'),('confirmedText','other'),('obligations',s['obligations'][:1]),('bindingOK',False)]:
        q=copy.deepcopy(s);q[k]=v;check(integrate(q)[0] is None,'binding');counts['controls']+=1
    for k in ('authorized','coverage','confirmed','sourcesOK'):
        q=copy.deepcopy(s);q['state'][k]=False;check(integrate(q)[0] is None,'qualification');counts['controls']+=1
    for txt in ['每月通勤少于60秒','每周通勤为60秒','并非（每周通勤少于60秒','每周通勤少于60秒且','每周通勤少于60秒'+'且每周通勤少于60秒'*26]:
        check(parse(txt) is None,'unknown syntax');counts['controls']+=1
    q=copy.deepcopy(s);q['state']['count']['scope']['subject']='other';check(integrate(q)[0] is None,'subject');counts['controls']+=1
    return dict(counts=counts,witness=witness,environment=META)
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
```

```json
{
  "counts": {
    "texts": 72,
    "cases": 864,
    "nativeCalls": 2592,
    "receiptChecks": 864,
    "pass_": 289,
    "fail": 292,
    "unknown": 283,
    "extraUnknownAbstract": 71,
    "flatWrongCertain": 369,
    "flatExtraUnknown": 88,
    "ambiguousCases": 576,
    "controls": 15
  },
  "witness": {
    "flatWrongCertain": {
      "text": "每周通勤少于0秒或者每周通勤至少1分钟或者每周通勤最多60秒",
      "lo": 0,
      "hi": 0,
      "n": 1,
      "joint": "PASS",
      "abstract": "PASS",
      "flat": "FAIL"
    },
    "extraUnknownAbstract": {
      "text": "每周通勤少于0秒或者每周通勤至少1分钟或者每周通勤最多60秒",
      "lo": 0,
      "hi": 60,
      "n": 2,
      "joint": "PASS",
      "abstract": "UNKNOWN",
      "flat": "FAIL"
    },
    "flatExtraUnknown": {
      "text": "每周通勤少于60秒且每周通勤至少1分钟且每周通勤最多120秒",
      "lo": 0,
      "hi": 60,
      "n": 1,
      "joint": "FAIL",
      "abstract": "UNKNOWN",
      "flat": "UNKNOWN"
    }
  },
  "environment": {
    "formula": "weekly_total@1",
    "projection": "R69@1",
    "method": "c028_interval_feasibility@1.0.0",
    "modules": {
      "decision_state.py": "0840855431fbc88fe212785584277aa01be74d93",
      "decision_feasibility.py": "6181d6c578c7ef251e9708d0ffcf65e95d35f88f"
    },
    "python": "3.13.5",
    "pydantic": "2.13.5"
  }
}
```

## 下一步
先核对完整版本研究积累和实际原生运行条件，优先解决源代码获取及正式支持环境、联合证明发布与真实语义/知识输入接口。应研究更广泛的非模板语言能力及自主学习可行路线，避免将有限通勤语法扩张为通用理解。保持原生算法语义与候选联合方法明确区分，不自动登记或放行；产品轨维护唯一交接，独立轨隔离未见真实场景。无生产代码变更、训练、Codex任务、CI、合并、部署或新增费用，冻结协议不变。