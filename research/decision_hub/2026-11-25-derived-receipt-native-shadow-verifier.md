# v3.2 自主认知专项第11轮（累计第70轮）：派生收据、原生影子计算与独立数学核验

2026-11-25。RESEARCH_CANDIDATE / NATIVE_MODULES_EXECUTED_ISOLATED / SUPPORTED_RUNTIME_NOT_RUN。基线 740fb7beed0555c6a0b0e3dadafe5694f0dca4f5，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核对最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题及历史阅读，非全文审计）、第54轮412a98c4bd335864a32f27aa796fc8a42414e7f4、第58轮ad1f8ab7be83d28391ee62ce77a44d5f59804bef、第48轮84a8abdd595152a81b270f7cc21c8361ceee71f8、第64轮da54c5b88ed0f19f5c5d272230a1959b811f5b5e、第66轮1a7a8560ff3349635966857a07a4e71b1680f7f6、第69轮f72aaacdf7253505cde3ad8050c45a5a2a99ea50。新增范围：实际复用第69轮原生投影与筛查函数，绑定两条义务及同一派生量，数学核验器独立计算原始量及影子检查的逻辑，验证原始快照变化、摘要重算和证明覆盖。既有共享线性参数、一般义务覆盖及后悔证书不重复枚举。无新增外部文献事实，未重审原论文。

## 合同及边界
可信宿主夹具给定单次持续时间硬界、同一周确切非负次数（0..100）、两条已确认阈值义务、共同scope（会话、主体、周、情景、用途、授权代次）、完整覆盖、来源合格、授权状态、修订、允许单位。每次均受界约束且次数覆盖全部应计事件，乘算得到周总量外界；不从平均值推断硬界，不宣称实际预测。阈值与总量以秒为共同精确表示；允许秒/分钟/小时正比例投影。所有布尔、来源及语义为合成可信夹具，不是独立事实来源、身份认证或实际授权。当前不自动解析自然语言、验证真实来源、推导真实义务集合或运行完整原生hub。计算收据的快照摘要覆盖完整输入，绑定公式、投影版本、原生方法、两模块身份及Python/Pydantic版本；源码身份与前序脚本哈希在实际运行时检查。摘要使用规范化JSON的SHA256，仅用于内容比较，不具秘密或签发权，不是个人信息匿名化。生产应避免公开私人数据或其可猜测摘要。

生产器用Fraction计算派生界，复用R69的project和native进行两阈值影子比较；保留原始约束（快照）、投影、两个影子状态与合并结果。每个义务完整出现且顺序与可信宿主一致，禁止漏项或重复替代。逐项独立核验器使用逐次相加复算量，检查外界包含、单位、实际Number验证器可表示性、精确/外界类型、原始阈值、严格边界和两个影子状态，不调用project、native、produce。共享Fraction、单位、比较算符、资格夹具及可表示性实现，不能声称独立科学验收。通过逻辑：任何义务确定失败则拒绝；每项确定通过才接受；其余保留未决。单项合取的充分筛查不能求得所有联合不可行（例如每项可能但相互矛盾），第63轮联合域研究仍需连接，不宣称本轮联合完备。两条临时影子调用均为隔离模型运行，未写入用户底线；overall仅此研究合同内单方案硬约束状态，不是完整推荐或真实授权。NO_CERTIFICATE仅证明保留未知，不证明无可行投影；检查器允许保守降级（损失可用性，不能因核验通过称最优或完整），完整性由另行调度和验收解决。核验器可接受任何满足合同的数学证明，不要求与生产器选择的最优/固定网格一致。代码未实现通用输入schema、恶意超大输入防护、真实并发、持久化及发布事务，生产失败关闭仍需另行开发。

## 真实环境和实测
容器复用/tmp/ph68，重新检查probe.py SHA256 b184293d8a3e49d078cefe9022ab169cc85971614eacf39c459f42b049a0917c、probe69.py 38ee5dd6b0e39995822bc76d68a0672f835cd8651e208e638839e7a7cf493161，导入时核对两个原生模块Git blob。沿用第68/69轮测试Method与Context替身、真实DecisionState/Quantity/Constraint及METHOD.validate/execute；Python3.13.5/Pydantic2.13.5非正式支持版本（要求3.12及2.13.4），未运行完整注册表/API/CLI/设备。6区间×3次数×5阈值对×4操作对=360个合成情景，每个2义务；主循环728次原生execute，不含专项控制。逐项确定性与精确有理端点参照无冲突。5328个故意非法收据变异均重算SHA256，单独摘要自检全部通过，而数学/身份核验均拒绝（不是密码学攻击或真实产品漏洞）；4320个旧收据在变更后的可信输入上均拒绝，未伪造快照摘要重绑定。额外9个控制含显式限制见证：修改修订号但保持数值一致并重绑定快照及摘要，数学核验通过；将有证书行降级为无证书且正确更新整体未决也通过。前者表明本算法无法证明真实签发、实际运行或跨修订授权，后者表明保守数学正确性不能证明结果完整性。两项均为设计边界而非声称安全防伪完成。生产需受信签发者或本地受信核验事务、快照一致性及权限重核，不将无密钥摘要当鉴权。所有样例为ChatGPT研发辅助原创合成开发夹具，非真人/独立留出/训练，无实际用户效果或设备性能结论。实际结果见下。

## 复算
按第68/69轮报告恢复固定源码及隔离脚本（本轮沿用已存在字节并验证历史脚本SHA256）。下列probe70.py为实际运行代码的转录，本机执行文件SHA256 d3681bbf0d4bd771bdb7d8c816ff0adfcc99a59397ef3d944841803e784f970e；未另验归档转录字节。普通Python执行python probe70.py，不依赖外网；非支持环境结果不得作为正式验收。

```python
import hashlib, json, itertools, operator, copy, platform
from pathlib import Path
from fractions import Fraction as F
import pydantic
from probe69 import project, native, representable, EXPECTED

SCALES={'s':1,'min':60,'h':3600}
OPS={'<':operator.lt,'<=':operator.le,'>':operator.gt,'>=':operator.ge}
P=Path(__file__).parent
for f,h in {'probe.py':'b184293d8a3e49d078cefe9022ab169cc85971614eacf39c459f42b049a0917c','probe69.py':'38ee5dd6b0e39995822bc76d68a0672f835cd8651e208e638839e7a7cf493161'}.items():
    if hashlib.sha256((P/f).read_bytes()).hexdigest()!=h: raise RuntimeError('probe identity')
META={'formula':'weekly_total@1','projection':'R69@1','method':'c028_interval_feasibility@1.0.0','modules':EXPECTED,'python':platform.python_version(),'pydantic':pydantic.__version__}
def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def check(x,msg):
    if not x: raise RuntimeError(msg)
def qual(s):
    r=s['root']; c=s['count']; cs=s['constraints']; scope=s['scope']
    return (s['authorized'] is True and s['coverage'] is True and s['confirmed'] is True and s['sourcesOK'] is True and r['qualified'] is True and c['qualified'] is True and r['scope']==scope==c['scope'] and type(c['n']) is int and 0<=c['n']<=100 and r['unit'] in SCALES and 0<=F(r['lo'])<=F(r['hi']) and bool(cs) and len({x['id'] for x in cs})==len(cs) and all(x['scope']==scope and x['confirmed'] is True and x['op'] in OPS and x['unit'] in SCALES and F(x['t'])>=0 for x in cs) and bool(s['allowed']) and all(u in SCALES for u in s['allowed']))
def finish(r):
    r['digest']=digest({k:v for k,v in r.items() if k!='digest'}); return r

def produce(s):
    if not qual(s): return None,0
    r=s['root']; n=s['count']['n']; lo,hi=(F(r[k])*n*SCALES[r['unit']] for k in ('lo','hi'))
    rows=[]; calls=0
    for c in s['constraints']:
        t=F(c['t'])*SCALES[c['unit']]; op=c['op']; mode,pr=project(lo,hi,t,s['allowed'])
        if pr is None:
            rows.append(dict(id=c['id'],mode='NO_CERTIFICATE',result='UNKNOWN'));continue
        u,l,h,tl,th=pr; pt,ft=(tl,th) if op.startswith('<') else (th,tl)
        a=native((l,h),pt,op,u)[0]; b=a if pt==ft else native((l,h),ft,op,u)[0];calls+=1+(pt!=ft)
        rows.append(dict(id=c['id'],mode=mode,unit=u,ends=list(map(str,(l,h,tl,th))),shadow=[a,b],result='PASS' if a=='CERTAIN_PASS' else 'FAIL' if b=='CERTAIN_FAIL' else 'UNKNOWN'))
    overall='REJECT' if any(x['result']=='FAIL' for x in rows) else 'ACCEPT' if all(x['result']=='PASS' for x in rows) else 'UNRESOLVED'
    return finish(dict(meta=copy.deepcopy(META),snapshot=digest(s),derived=list(map(str,(lo,hi))),rows=rows,overall=overall,authority='NONE')),calls

def verify(s,r):
    # Independent mathematical path; no call to produce/project/native.
    # Trusted snapshot and identity gates are fixture inputs, not authentication.
    try:
        if not qual(s) or not isinstance(r,dict) or set(r)!={'meta','snapshot','derived','rows','overall','authority','digest'}: return False
        if r['meta']!=META or r['snapshot']!=digest(s) or r['authority']!='NONE' or r['digest']!=digest({k:v for k,v in r.items() if k!='digest'}): return False
        root=s['root']; n=s['count']['n']; factor=SCALES[root['unit']]
        actual=[sum([F(root[k])*factor]*n,F(0)) for k in ('lo','hi')]
        if r['derived']!=list(map(str,actual)) or not isinstance(r['rows'],list) or len(r['rows'])!=len(s['constraints']): return False
        statuses=[]
        for c,row in zip(s['constraints'],r['rows']):
            if row['id']!=c['id']: return False
            if row['mode']=='NO_CERTIFICATE':
                if row!={'id':c['id'],'mode':'NO_CERTIFICATE','result':'UNKNOWN'}: return False
                statuses.append('UNKNOWN');continue # no proof of impossibility; safe incomplete result
            if set(row)!={'id','mode','unit','ends','shadow','result'} or row['unit'] not in s['allowed'] or len(row['ends'])!=4: return False
            if any(type(v)!=str or len(v)>100 for v in row['ends']): return False
            l,h,tl,th=map(F,row['ends']); f=SCALES[row['unit']]; t=F(c['t'])*SCALES[c['unit']]
            if not all(map(representable,(l,h,tl,th))) or not (l*f<=actual[0]<=actual[1]<=h*f and tl*f<=t<=th*f):return False
            exact=(l*f==actual[0] and h*f==actual[1] and tl*f==t==th*f)
            if row['mode']!=('EXACT' if exact else 'OUTER'):return False
            # Evaluate each shadow on the physical-unit endpoints, independently.
            op=OPS[c['op']]; thresholds=(tl,th) if c['op'] in ('<','<=') else (th,tl)
            def shadow(x):
                truth=[op(v*f,x*f) for v in (l,h)]
                return 'CERTAIN_PASS' if all(truth) else 'CERTAIN_FAIL' if not any(truth) else 'POSSIBLE'
            a,b=map(shadow,thresholds); verdict='PASS' if a=='CERTAIN_PASS' else 'FAIL' if b=='CERTAIN_FAIL' else 'UNKNOWN'
            if row['shadow']!=[a,b] or row['result']!=verdict:return False
            statuses.append(verdict)
        want='REJECT' if 'FAIL' in statuses else 'ACCEPT' if all(v=='PASS' for v in statuses) else 'UNRESOLVED'
        return r['overall']==want
    except (ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError,OverflowError):return False

def fixture(lo,hi,n,t1,t2,op1,op2):
    scope={'session':'S','subject':'self','week':'2027-W01','scenario':'A','purpose':'decision','generation':1}
    return dict(scope=scope,revision=1,authorized=True,coverage=True,confirmed=True,sourcesOK=True,allowed=['s','min','h'],root=dict(id='trip',version=1,source='fixture:trip',kind='synthetic',qualified=True,lo=lo,hi=hi,unit='s',scope=copy.deepcopy(scope)),count=dict(id='count',version=1,source='fixture:count',n=n,qualified=True,scope=copy.deepcopy(scope)),constraints=[dict(id=k,version=1,source='fixture:'+k,scope=copy.deepcopy(scope),confirmed=True,t=t,unit='s',op=o) for k,t,o in [('c1',t1,op1),('c2',t2,op2)]])

def main():
    counts=dict(cases=0,nativeCalls=0,verified=0,exactRows=0,outerRows=0,noCertificateRows=0,accept=0,reject=0,unresolved=0,wrongCertain=0,mutations=0,rejectedMutations=0,stale=0,rejectedStale=0,hashOnlyFalseAccept=0,controls=0)
    for (lo,hi),n,(t1,t2),(o1,o2) in itertools.product([('0','0'),('0','1/7'),('1/7','1/3'),('1','1'),('1200000','1200000'),('1000000000000000000','1000000000000000000')],(0,1,5),[('0','1'),('1/7','1/3'),('1','60'),('1200000','3600'),('1000000000000000000','1')],[('>=','<='),('>','<'),('<=','<='),('>=','>=')]):
        s=fixture(lo,hi,n,t1,t2,o1,o2);r,calls=produce(s)
        check(verify(s,r),'valid certificate');counts['cases']+=1;counts['verified']+=1;counts['nativeCalls']+=calls;counts[r['overall'].lower()]+=1
        for row in r['rows']:counts[{'EXACT':'exactRows','OUTER':'outerRows','NO_CERTIFICATE':'noCertificateRows'}[row['mode']]]+=1
        # Check only sound certainty, not completeness of joint feasibility.
        for row,c in zip(r['rows'],s['constraints']):
            v=[OPS[c['op']](F(x)*n,F(c['t'])) for x in (lo,hi)]
            gold='PASS' if all(v) else 'FAIL' if not any(v) else 'UNKNOWN'
            if row['result']!='UNKNOWN' and row['result']!=gold:counts['wrongCertain']+=1;raise RuntimeError('false certainty')
        variants=[]
        for key,val in [('authority','EXECUTE'),('overall','ACCEPT' if r['overall']!='ACCEPT' else 'REJECT'),('derived',['-1','-1']),('snapshot','0'*64)]:
            x=copy.deepcopy(r);x[key]=val;variants.append(x)
        x=copy.deepcopy(r);x['meta']['formula']='other';variants.append(x)
        x=copy.deepcopy(r);x['rows'].pop();variants.append(x)
        x=copy.deepcopy(r);x['rows'].reverse();variants.append(x)
        x=copy.deepcopy(r);x['rows'][0]['id']='c2';variants.append(x)
        for i,row in enumerate(r['rows']):
            x=copy.deepcopy(r);x['rows'][i]['result']='PASS' if row['result']!='PASS' else 'FAIL';variants.append(x)
            if row['mode']!='NO_CERTIFICATE':
                for k,v in [('unit','USD'),('ends',['-1','-1','0','0']),('shadow',['FORGED','FORGED'])]:
                    x=copy.deepcopy(r);x['rows'][i][k]=v;variants.append(x)
        for x in variants:
            finish(x);counts['mutations']+=1
            check(x['digest']==digest({k:v for k,v in x.items() if k!='digest'}),'rehash');counts['hashOnlyFalseAccept']+=1
            check(not verify(s,x),'mutation admitted');counts['rejectedMutations']+=1
        for key,val in [('revision',2),('authorized',False),('coverage',False),('confirmed',False),('sourcesOK',False),('allowed',['s'])]:
            x=copy.deepcopy(s);x[key]=val;counts['stale']+=1;check(not verify(x,r),'stale admitted');counts['rejectedStale']+=1
        for field,key,val in [('root','version',2),('count','version',2),('root','source','new'),('count','n',n+1),('scope','generation',2),('scope','purpose','other')]:
            x=copy.deepcopy(s);x[field][key]=val;counts['stale']+=1;check(not verify(x,r),'stale field');counts['rejectedStale']+=1
    s=fixture('1','1',1,'0','2','>=','<=');r,_=produce(s)
    for key in ('authorized','coverage','confirmed','sourcesOK'):
        x=copy.deepcopy(s);x[key]=False;check(produce(x)[0] is None,'blocked');counts['controls']+=1
    x=copy.deepcopy(s);x['root']['scope']['subject']='other';check(produce(x)[0] is None,'scope');counts['controls']+=1
    x=copy.deepcopy(s);x['constraints'].append(copy.deepcopy(x['constraints'][0]));check(produce(x)[0] is None,'duplicate');counts['controls']+=1
    x=copy.deepcopy(s);x['revision']=2;new,_=produce(x);check(verify(x,new) and not verify(x,r),'reissue');counts['controls']+=1
    # A deliberately conservative incomplete receipt is allowed, never an ACCEPT.
    x=copy.deepcopy(r);x['rows'][0]={'id':'c1','mode':'NO_CERTIFICATE','result':'UNKNOWN'};x['overall']='UNRESOLVED';finish(x);check(verify(s,x),'incomplete');counts['controls']+=1
    # A re-bound mathematically valid payload can pass: no signature/issuance attestation.
    x=copy.deepcopy(s);x['revision']=2;rebound=copy.deepcopy(r);rebound['snapshot']=digest(x);finish(rebound)
    check(verify(x,rebound),'expected mathematical equivalence');counts['controls']+=1
    return dict(counts=counts,environment=META,limitations={'reboundSameValuesAccepted':True,'conservativeDowngradeAccepted':True})
if __name__=='__main__':print(json.dumps(main(),indent=2))
```

```json
{
  "counts": {
    "cases": 360,
    "nativeCalls": 728,
    "verified": 360,
    "exactRows": 304,
    "outerRows": 272,
    "noCertificateRows": 144,
    "accept": 71,
    "reject": 185,
    "unresolved": 104,
    "wrongCertain": 0,
    "mutations": 5328,
    "rejectedMutations": 5328,
    "stale": 4320,
    "rejectedStale": 4320,
    "hashOnlyFalseAccept": 5328,
    "controls": 9
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
  },
  "limitations": {
    "reboundSameValuesAccepted": true,
    "conservativeDowngradeAccepted": true
  }
}
```

## 后续
优先实际连接第62/63轮语义与联合数量推理，检查底线原文义务、派生量身份、原生筛查及条件解释能否以同一快照运行；联合不可行与局部充分筛查需明确区分。进一步研究受信签发/本地事务的权威来源与撤权并发，复用已有原生状态、确认、存储恢复，不重造架构。应先核查支持版本运行条件，逐步从隔离模块走向真实原生完整入口；独立轨冻结未见案例并核验实际能力，产品轨维护唯一交接。未修改生产代码、启动训练、Codex、CI、PR合并、部署或增加费用，冻结协议不变。