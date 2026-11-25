# 自主认知专项累计第95轮候选：共享仿射变量、原生C028与联合可行性精确分区

2026-11-25。RESEARCH_CANDIDATE / NATIVE_MODULES_EXECUTED_ISOLATED / SHARED_AFFINE_FINITE_FIXTURE / SUPPORTED_RUNTIME_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main fdeb77f0dd0cdd9f98867bce1de73a3d0e2a7043。核查近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R94首20行。R94每解释内数值为独立矩形；本轮增量为跨方案及跨指标同一共享连续变量，保留数值相关性及语义解释并集。R71有限单量逻辑作为历史参考，不重跑其算法。无真实语言自动提取、训练或生产修改。

## 实际环境与源
复用实际存在的/tmp/ph94/ph隔离目录，git hash-object本轮重新核验原生decision_state.py 0840855431fbc88fe212785584277aa01be74d93、decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f，与R94固定仓库源一致。Python3.13.5/Pydantic2.13.5（非正式支持版本），空包init、Method注册替身、SimpleNamespace上下文沿R94。实际执行DecisionState及METHOD.validate/execute，未运行完整注册表、hub、API、CLI、设备。实验脚本/tmp/ph94/probe95.py SHA256 328f99983f08918722fd6f28037f45ee57ae8f3ab191e85f0e6057c906c80709。以下代码为转录，未单独核验归档文本字节；本轮实际容器输出见下。主实验155632次点值原生执行及31104次外包区间原生执行，另2次资格失败执行（未确认在validate阻断）。不把重复调用当独立样本。未更改原生文件。

## 合同及推导
两方案各两指标，均为共享标量x的仿射函数s*x+t。6种形式见代码，取值范围含零、正斜率、负斜率；域[0,4]、[2,6]、[4,4]，阈值5和7，四种有限解释由是否严格小于及作用范围构成，部分解释实际上等价，非四种真实语言歧义。没有把原本的数值相关关系误作概率。金额、单位、期限、来源、共享变量身份及覆盖由人工夹具给定，真实单位系数、来源资格、原文义务未验证。B>A是人工固定序位，不是用户偏好。可能优选表示在各可行世界中依固定序位得到的结果，并非鲁棒最优决策、实际收益或推荐。

对一维闭区间，所有非零仿射阈值根(c-t)/s与端点构成分区。每个根及端点单独求值以区分严格/非严格边界，每相邻开区间以中点代表，因各仿射不等式真值区间内恒定，故完整联合可行掩码集合精确。零斜率常量直接比较。此夹具全部根为整数或半整数，中点为四分之一整数，Decimal投影精确；一般有理数不得直接用本代码的Decimal除法宣称精确。参照为独立四分之一网格枚举：在本夹具端点为整数、根为半整数，网格覆盖所有真值类。每点对A/B分别构造原生单方案状态，要求点输出唯一且无UNKNOWN原子。原生C028在全区间投影每项仿射上下界的矩形外包；用各方案状态集合笛卡尔组合，包含真实共享变量结果，但UNRESOLVED可能只是外包，不能称为真实可达。没有把这种保守外包定性为C028缺陷。各语义世界的掩码并集保留条件内相关性。掩码1为A、2为B、3两者、0无可行。没有真实多维相关域、非线性、连续多期决策、参数不确定、模型自主调度或完整语义覆盖。任何结果authority NONE（研究范围约束，代码未独立输出该字段），不写入用户状态。缺少覆盖返回UNKNOWN_COVERAGE，预估点调用超过预算返回LIMIT且未执行；预算仅限单解释点调用数，未覆盖全部请求或实际设备资源。资格失败返回UNKNOWN_QUALIFICATION，真实授权另核。

## 实验及局限
6^4形式×3区间×4解释=15552世界，主实验全部与独立网格参照一致；每形式区间组合遍历15个非空解释域，58320组合、233280端口。原生矩形外包对照可能引入不可达可行组合、额外可能优选，或损失本可确定端口；这些是已知共享关系的人工模型差异，不代表真实产品准确率。另8项控制、12覆盖缺失与12预算检查。主循环断言用于科研，非生产安全门。所有样例为ChatGPT研发辅助原创合成夹具，非真人或独立留出；没有新外部资料、训练、真实设备/用户效果、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。形式、阈值、作用域、预算及固定序位由研究者选定。保留完整版本范围及验收门。后续优先研究真正多共享变量的可证可行性及长期决策资源依赖，以及原文义务、知识证据与方法准入连接。数据轨、独立验收轨、产品轨职责不变。

## 复算
按R94恢复固定原生模块至ph/及同样的注册替身，运行以下Python。
```python
import itertools as I,json,hashlib
from fractions import Fraction as F
from types import SimpleNamespace
from ph.decision_state import DecisionState
from ph.decision_feasibility import METHOD
from decimal import Decimal
from pathlib import Path

def dec(x):
    x=F(x);return str(Decimal(x.numerator)/Decimal(x.denominator))
# Each action two distinct metrics, common shared latent x. Affine expressions
# have slopes +-1 or +-2, so all roots are half integers, grid quarters complete.
FORMS=[(1,0),(1,2),(-1,8),(2,0),(-2,12),(0,5)]
W=list(I.product(range(2),repeat=2)) # threshold strictness, A/B scope
DOM=[(0,4),(2,6),(4,4)]
def spec(w,forms):
    strict,scope=w
    return [[(s,t,('<' if strict and (not scope or a==1) else '<='),5 if j==0 else 7) for j,(s,t) in enumerate(forms[2*a:2*a+2])] for a in range(2)]
def evaluate(spec,interval,bad=None):
    lo,hi=interval;calls=0;flags=[]
    for a,cs in enumerate(spec):
        cons=[];meas={}
        for j,(s,t,op,c) in enumerate(cs):
            k=f'c{j}';v=sorted([s*lo+t,s*hi+t]);cons.append(dict(id=k,label=f'metric{j}',unit='USD',operator=op,threshold=dec(c),source='synthetic threshold',horizon='month'))
            meas[k]=dict(lower=dec(v[0]),upper=dec(v[1]),kind='synthetic',unit='USD',source='synthetic affine bound',horizon='month')
        if bad=='unit':meas['c0']['unit']='KRW'
        if bad=='source':meas['c0']['source']=''
        st=DecisionState(decision_id='0'*32,revision=1,question='合成共享变量预算',confirmed=True,constraints_confirmed=bad!='unconfirmed',deadline='month',constraints=cons,options=[dict(id='AB'[a],label='AB'[a],measurements=meas)])
        ctx=SimpleNamespace(state=st)
        if METHOD.validate(ctx):return None,calls
        r=METHOD.execute(ctx)['feasibility'][0];calls+=1
        if any(c['status']=='UNKNOWN' for c in r['checks']):return None,calls
        flags.append({'ACCEPT':{1},'REJECT':{0},'UNRESOLVED':{0,1}}[r['status']])
    return {a+2*b for a,b in I.product(*flags)},calls

def exact(spec,interval,covered=True,cap=64):
    if not covered:return 'UNKNOWN_COVERAGE',None,0
    lo,hi=map(F,interval);cuts={lo,hi}
    for cs in spec:
        for s,t,op,c in cs:
            if s:
                p=F(c-t,s)
                if lo<=p<=hi:cuts.add(p)
    cuts=sorted(cuts);pts=cuts+[(a+b)/2 for a,b in zip(cuts,cuts[1:])]
    if len(pts)*2>cap:return 'LIMIT',None,0
    out=set();calls=0
    for p in pts:
        v,n=evaluate(spec,(p,p));calls+=n
        if v is None or len(v)!=1:return 'UNKNOWN_QUALIFICATION',None,calls
        out|=v
    return 'CONDITIONAL',out,calls

def oracle(w,forms,interval):
    lo,hi=interval;out=set()
    for k in range(4*lo,4*hi+1):
        x=F(k,4);flags=[]
        for a in range(2):
            ok=True
            for j in range(2):
                s,t=forms[a*2+j];v=s*x+t;c=(5,7)[j]
                ok &= v<c if w[0] and (not w[1] or a==1) else v<=c
            flags.append(int(ok))
        out.add(flags[0]+2*flags[1])
    return out

def ports(s):return [set(x&1 for x in s),set(x>>1 for x in s),s,set('B' if x&2 else 'A' if x&1 else 'NONE' for x in s)]
def main():
    # Four forms from six, exhaustive for this finite family.
    o=dict(worlds=0,world_checks=0,native_point_calls=0,native_outer_calls=0,outer_extra_worlds=0,outer_wrong_certain=0,outer_extra_preferred_worlds=0,domains=0,ports=0,stable_ports=0,outer_extra_domains=0,outer_extra_preferred_domains=0,outer_lost_stable_ports=0,coverage_checks=0,budget_checks=0,controls=0)
    witnesses={}
    for forms in I.product(FORMS,repeat=4):
        for interval in DOM:
            rows=[];outer=[]
            for w in W:
                cs=spec(w,forms);status,s,n=exact(cs,interval);g=oracle(w,forms,interval)
                assert status=='CONDITIONAL' and s==g,(w,forms,interval,s,g)
                a,k=evaluate(cs,interval);assert s<=a
                o['worlds']+=1;o['world_checks']+=1;o['native_point_calls']+=n;o['native_outer_calls']+=k
                o['outer_extra_worlds']+=s!=a;o['outer_extra_preferred_worlds']+=ports(s)[3]!=ports(a)[3]
                o['outer_wrong_certain']+=sum(len(y)==1 and x!=y for x,y in zip(ports(s),ports(a)))
                if s!=a:witnesses.setdefault('outer',dict(w=w,forms=forms,interval=interval,exact=sorted(s),outer=sorted(a)))
                if ports(s)[3]!=ports(a)[3]:witnesses.setdefault('preferred',dict(w=w,forms=forms,interval=interval,exact=sorted(s),outer=sorted(a)))
                rows.append(s);outer.append(a)
            for mask in range(1,16):
                s=set.union(*[rows[i] for i in range(4) if mask&(1<<i)]);a=set.union(*[outer[i] for i in range(4) if mask&(1<<i)])
                o['domains']+=1;o['outer_extra_domains']+=s!=a;o['outer_extra_preferred_domains']+=ports(s)[3]!=ports(a)[3]
                for x,y in zip(ports(s),ports(a)):
                    assert x<=y;o['ports']+=1;o['stable_ports']+=len(x)==1;o['outer_lost_stable_ports']+=len(x)==1 and len(y)>1
    for w in W:
        cs=spec(w,(FORMS[0],)*4)
        for interval in DOM:
            assert exact(cs,interval,False)==('UNKNOWN_COVERAGE',None,0);o['coverage_checks']+=1
            assert exact(cs,interval,cap=1)==('LIMIT',None,0);o['budget_checks']+=1
    for bad in ['unit','source','unconfirmed']:
        assert evaluate(spec(W[0],(FORMS[0],)*4),(0,4),bad)[0] is None;o['controls']+=1
    assert o['worlds']==6**4*3*4;o['controls']+=1
    assert o['domains']==6**4*3*15;o['controls']+=1
    assert o['outer_wrong_certain']==0;o['controls']+=1
    assert o['outer_extra_worlds']>0;o['controls']+=1
    assert o['coverage_checks']==o['budget_checks']==12;o['controls']+=1
    print(json.dumps(dict(counts=o,witnesses=witnesses),ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
```

## 实测
```json
{
  "counts": {
    "budget_checks": 12,
    "controls": 8,
    "coverage_checks": 12,
    "domains": 58320,
    "native_outer_calls": 31104,
    "native_point_calls": 155632,
    "outer_extra_domains": 23345,
    "outer_extra_preferred_domains": 9386,
    "outer_extra_preferred_worlds": 3419,
    "outer_extra_worlds": 6976,
    "outer_lost_stable_ports": 754,
    "outer_wrong_certain": 0,
    "ports": 233280,
    "stable_ports": 80716,
    "world_checks": 15552,
    "worlds": 15552
  },
  "witnesses": {
    "outer": {
      "exact": [
        0,
        3
      ],
      "forms": [
        [
          1,
          0
        ],
        [
          1,
          0
        ],
        [
          1,
          0
        ],
        [
          1,
          0
        ]
      ],
      "interval": [
        2,
        6
      ],
      "outer": [
        0,
        1,
        2,
        3
      ],
      "w": [
        0,
        0
      ]
    },
    "preferred": {
      "exact": [
        0,
        3
      ],
      "forms": [
        [
          1,
          0
        ],
        [
          1,
          0
        ],
        [
          1,
          0
        ],
        [
          1,
          0
        ]
      ],
      "interval": [
        2,
        6
      ],
      "outer": [
        0,
        1,
        2,
        3
      ],
      "w": [
        0,
        0
      ]
    }
  }
}
```
