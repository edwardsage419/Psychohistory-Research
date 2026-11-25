# 自主认知专项累计第94轮候选：相关语义解释、原生C028区间可行性与跨方案依赖

2026-11-25。RESEARCH_CANDIDATE / NATIVE_MODULES_EXECUTED_ISOLATED / SUPPORTED_RUNTIME_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main c5fecc311d7b96a0d3e198a50272b9e041f45d00。核对近25提交、13开放PR（#61待审）、v3.2首8行及历史全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R71报告首125行相关段、完整未截断Git树原生目标路径。增量：R93相关有限语义域原为点值人工计算，R71为单一派生量逻辑；本轮真实执行原生C028，在每个解释下保留两个方案的区间可行组合，再进行解释域并集。未执行R93澄清算法或R71原脚本，无自主原文抽取、训练或生产修改。

## 源及运行环境
本轮容器原/tmp/ph68目录不可用，git ls-remote直接联网DNS失败。通过GitHub连接器获取以下固定blob全文，逐字节转录至/tmp/ph94/ph，实际git hash-object核验完全一致，非仅代码重写：
- platform/future_model/src/psychohistory/decision_state.py 0840855431fbc88fe212785584277aa01be74d93，6212字节。
- platform/future_model/src/psychohistory/decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f，4468字节。
- 同树decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497，仅核对树元数据，未执行。
Python3.13.5/Pydantic2.13.5；非项目正式支持版本（历史R71记录3.12/2.13.4）。空包init，Method替身仅保存kwargs，Context为SimpleNamespace；实际原生DecisionState、METHOD.validate/execute均运行。没有运行完整registry/hub/API/CLI或真机。实际probe.py SHA256 acae923cbe7af65d4ea7c55a973312322062d88ce94483ab5401f18b647323f8；报告转录代码，未另作归档脚本字节核验。主实验4096次原生execute，另3次资格失败控制execute，未确认控制在validate阻断（主循环计数不含这3次）。未修改原生源码。

## 合同
沿R93三个二元维度、两个方案两项支出、基础阈值5/7及新6、固定序位B>A。与R93点值不同，每项选闭区间[4,4],[4,6],[6,8],[8,8]；四个支出在每个解释内假设可独立取值（矩形域），解释域是8个世界的任意非空子集，解释之间不赋概率。主体、单位USD、周期month、来源及资格均为人工合成夹具；不代表真实用户或完整语言义务。方案特定阈值无法直接在本C028单个共享constraints字段表达，因此每个解释按方案分别构造隔离DecisionState，不能将这些研究状态视为实际用户已确认或写入记录。原生ACCEPT映射{可行}、REJECT映射{不可行}、UNRESOLVED且全部原子资格充分时映射{可行,不可行}；任何UNKNOWN原子阻断该解释（保守策略），未确认validate阻断。在本夹具独立矩形、每指标单个单调上限下，这三个集合恰为各方案可能可行状态；跨方案矩形组合仅允许在同一解释内。每解释的联合可行掩码集合求并集，保留跨解释相关性；四端口为A、B状态集合、联合掩码集合、固定B>A下可能优选集合（NONE也保留）。掩码1为A可行、2为B可行、3两者、0无。单元素端口只表示在给定覆盖与矩形假设内条件稳定，authority NONE，不作真实用户最终推荐。外部覆盖布尔为人工给定，未实现独立覆盖或语义准入。combine在缺失覆盖、空域、超过解释数预算、任一资格失败时不输出集合；此预算仅计解释个数，未限制构建/运行全部原生计算或真实资源。其他指标、共享随机变量、跨方案数值相关、同量多条件交互、非矩形域不直接套用本原生映射。没有新外部资料。

## 参照和结果
8解释×4^4区间组合=2048世界，逐个调用两次原生，并与独立端点枚举集合核对。单调<=及矩形域保证端点穷举覆盖全部可行布尔类别；同一研究者设计参照，非独立验收。各区间组合缓存8个世界计算，再遍历255非空域，共65280域场景、261120端口。故意简化对照先对A/B分别取全域可行状态集合再自由组合，必然外包但可能虚构联合情景及优选；第一解释单独当全域结论的对照以单元素端口与全域不一致计数。没有比较真实产品错误率或统计泛化。区间、固定偏好、来源、覆盖、预算均研究者选择。12项控制，255覆盖及255预算检查；主循环以外实际3次资格失败execute。未训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留完整版本范围和正式验收门。下一步应接入实际原文义务、可信覆盖及更多数学方法，独立轨评价未见样本，数据轨提供合法真实来源，产品轨维护唯一交接。

## 复算
恢复上述两个固定blob至ph/，空__init__.py，decision_registry.py为：
```python
# Isolated registration stub; no registry execution.
class Method:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
```
以下probe.py与ph同级，普通Python解释器运行；断言为研究实验检查，非生产安全门。
```python
import itertools as I, json, hashlib, subprocess
from pathlib import Path
from types import SimpleNamespace
from ph.decision_state import DecisionState
from ph.decision_feasibility import METHOD

W=list(I.product(range(2), repeat=3))
R=[(4,4),(4,6),(6,8),(8,8)]

def limits(w):
    x,y,z=w
    q=[[5,7],[5,7]]
    for a in range(2):
        if not z or a==1:
            q[a][x]=min(q[a][x],6) if y else 6
    return q

def native(w, v, bad=None):
    q=limits(w)
    # One shared C028 constraint per action-specific threshold is not expressible
    # in a single state. Project each option separately with its own constraints.
    sets=[]
    calls=0
    for a in range(2):
        cons=[dict(id=f'c{i}',label=f'metric{i}',unit='USD',operator='<=',threshold=q[a][i],source='synthetic confirmed fixture',horizon='month') for i in range(2)]
        meas={f'c{i}':dict(lower=v[2*a+i][0],upper=v[2*a+i][1],kind='synthetic',unit='USD',source='synthetic bound',horizon='month') for i in range(2)}
        if bad=='source' and a==0:meas['c0']['source']=''
        if bad=='unit' and a==0:meas['c0']['unit']='KRW'
        if bad=='horizon' and a==0:meas['c0']['horizon']='year'
        st=DecisionState(decision_id='0'*32,revision=1,question='合成预算情景',confirmed=True,constraints_confirmed=bad!='unconfirmed',deadline='month',constraints=cons,options=[dict(id='AB'[a],label='AB'[a],measurements=meas)])
        ctx=SimpleNamespace(state=st)
        if METHOD.validate(ctx):return None,calls
        result=METHOD.execute(ctx)['feasibility'][0];calls+=1
        if any(c['status']=='UNKNOWN' for c in result['checks']):return None,calls
        sets.append({'ACCEPT':{1},'REJECT':{0},'UNRESOLVED':{0,1}}[result['status']])
    return {a+2*b for a,b in I.product(*sets)},calls

def oracle(w,v):
    # Independent point check; endpoints suffice for <= on rectangular cells.
    x,y,z=w
    out=set()
    for vals in I.product(*[sorted(set(t)) for t in v]):
        flags=[]
        for a in range(2):
            f=True
            for j in range(2):
                cap=5 if j==0 else 7
                if j==x and (z==0 or a==1):
                    f &= (vals[a*2+j]<=6 and (not y or vals[a*2+j]<=cap))
                else:f &= vals[a*2+j]<=cap
            flags.append(int(f))
        out.add(flags[0]+2*flags[1])
    return out

def ports(masks):
    return [set(m&1 for m in masks),set((m>>1)&1 for m in masks),set(masks),set('B' if m&2 else 'A' if m&1 else 'NONE' for m in masks)]

def combine(rows,closed=True,cap=8):
    if not closed:return 'UNKNOWN_COVERAGE',None
    if not rows:return 'CONFLICT',None
    if len(rows)>cap:return 'LIMIT',None
    if any(x is None for x in rows):return 'UNKNOWN_QUALIFICATION',None
    return 'CONDITIONAL',set.union(*rows)

def main():
    o=dict(native_calls=0,world_cases=0,world_mask_checks=0,domains=255,scenarios=0,ports=0,stable_ports=0,uncertain_ports=0,flatten_extra_masks=0,flatten_extra_preferred=0,flatten_lost_stable_ports=0,flatten_wrong_certain=0,first_world_false_certain=0,coverage_checks=0,budget_checks=0,controls=0)
    witness={}
    for v in I.product(R,repeat=4):
        rows=[];gold=[]
        for w in W:
            r,n=native(w,v);g=oracle(w,v);assert r==g
            o['world_cases']+=1;o['native_calls']+=n;o['world_mask_checks']+=1;rows.append(r);gold.append(g)
        for mask in range(1,256):
            ix=[i for i in range(8) if mask&(1<<i)]
            status,s=combine([rows[i] for i in ix]);assert status=='CONDITIONAL' and s==set.union(*[gold[i] for i in ix]);o['scenarios']+=1
            # Simplified baseline loses inter-option dependency across interpretations.
            p=ports(s);flat={a+2*b for a,b in I.product(p[0],p[1])};fp=ports(flat);first=ports(rows[ix[0]])
            assert s<=flat
            if flat!=s:o['flatten_extra_masks']+=1;witness.setdefault('extra_masks',dict(v=v,worlds=[W[i] for i in ix],exact=sorted(s),flat=sorted(flat)))
            if fp[3]!=p[3]:o['flatten_extra_preferred']+=1;witness.setdefault('extra_preferred',dict(v=v,worlds=[W[i] for i in ix],exact=sorted(p[3]),flat=sorted(fp[3])))
            for a,b,f in zip(p,fp,first):
                o['ports']+=1;o['stable_ports']+=len(a)==1;o['uncertain_ports']+=len(a)>1
                assert a<=b and f<=a
                o['flatten_lost_stable_ports']+=len(a)==1 and len(b)>1
                o['flatten_wrong_certain']+=len(b)==1 and b!=a
                o['first_world_false_certain']+=len(f)==1 and f!=a
            if v==(R[0],)*4:
                assert combine([rows[i] for i in ix],False)==('UNKNOWN_COVERAGE',None);o['coverage_checks']+=1
                assert combine([rows[i] for i in ix],True,len(ix)-1)==('LIMIT',None);o['budget_checks']+=1
    for bad in ['source','unit','horizon','unconfirmed']:
        q,n=native(W[0],(R[0],)*4,bad);assert q is None and combine([q])==('UNKNOWN_QUALIFICATION',None);o['controls']+=1
    assert combine([],True)==('CONFLICT',None);o['controls']+=1
    assert combine([],False)==('UNKNOWN_COVERAGE',None);o['controls']+=1
    assert o['world_cases']==2048 and o['native_calls']==4096;o['controls']+=1
    assert o['scenarios']==65280 and o['ports']==261120;o['controls']+=1
    assert o['stable_ports']+o['uncertain_ports']==o['ports'];o['controls']+=1
    assert o['flatten_wrong_certain']==0;o['controls']+=1
    assert o['coverage_checks']==255 and o['budget_checks']==255;o['controls']+=1
    assert o['flatten_extra_masks']>0;o['controls']+=1
    return dict(counts=o,witness=witness)
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,sort_keys=True))
```

## 实际结果（容器普通解释器）
```json
{
  "counts": {
    "budget_checks": 255,
    "controls": 12,
    "coverage_checks": 255,
    "domains": 255,
    "first_world_false_certain": 24512,
    "flatten_extra_masks": 1134,
    "flatten_extra_preferred": 756,
    "flatten_lost_stable_ports": 0,
    "flatten_wrong_certain": 0,
    "native_calls": 4096,
    "ports": 261120,
    "scenarios": 65280,
    "stable_ports": 138392,
    "uncertain_ports": 122728,
    "world_cases": 2048,
    "world_mask_checks": 2048
  },
  "witness": {
    "extra_masks": {
      "exact": [
        0,
        1,
        3
      ],
      "flat": [
        0,
        1,
        2,
        3
      ],
      "v": [
        [
          4,
          6
        ],
        [
          4,
          4
        ],
        [
          6,
          8
        ],
        [
          4,
          4
        ]
      ],
      "worlds": [
        [
          0,
          0,
          0
        ],
        [
          0,
          1,
          0
        ]
      ]
    },
    "extra_preferred": {
      "exact": [
        "B",
        "NONE"
      ],
      "flat": [
        "A",
        "B",
        "NONE"
      ],
      "v": [
        [
          6,
          8
        ],
        [
          4,
          4
        ],
        [
          4,
          6
        ],
        [
          4,
          4
        ]
      ],
      "worlds": [
        [
          0,
          0,
          0
        ],
        [
          0,
          1,
          0
        ]
      ]
    }
  }
}
```
