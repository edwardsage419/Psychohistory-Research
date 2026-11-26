# 自主认知：共同路径下的联合修订世界与局部只读收据
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线及增量身份
起点及写前REST branches/main均为7f3c7ba0245e62698a5ea828354d0e281b31b207。核对20近期提交、15开放PR、v3.2及同步规程全文、decision_hub目录224项、docs目录306项、research/coordination目录及唯一交接实际路径research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md，固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07，读取首尾段（其末项2026-11-22，历史交接不优先于v3.2）。非全库内容查重。#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍为候选；实际读取V08_ENGINE、decision_semantics.py 8c6ea6914b5b6e4f01d70331ed5c75c0dc32221b、evaluate_v07_public.py 2752f5cf3ab45e7cc58ecb10d771a7741ac1ab2a；未执行上述生产源。回读前轮共同路径证书 5faa95672f893c60e41433968dd7b4d43f481741。相邻研究：scoped-method-preparation-task-intersection、interpretation-effect-equivalence-and-ledger-boundary 18ae7920f9ca317da66d1d50ba7f0fc3d8951c26、raw-revision-to-confirmed-history-joint-ranking 6e17e892bc7bcc512efed8e28b8f29bee05c5877、field-lineage-semantic-patch 307f8ba1291ec9ad83aca578bd5a02508d1e6110、method-publication-revision-transaction 36b1d776ec4d71ad7f28d27c68feae438a8acb07 前段。此前已研究单修订解释效果等价、读写分离、版本失效与并发事件序列；本轮增量是同一当前轮的多个互相关联编辑组，在共同路径掩码下精确构造联合修订世界和逐输出投影，并将候选组及路径清单显式纳入只读收据身份。重复的失效控制只作定向回归，不计作新发现或生产漏洞。未改唯一交接。

## 数学、接口与边界
给定可信夹具的四个非负整数或未知字段(cap,a,b,fee)，同币种同周期假设。A/B各自开支加共同费用与cap比较，等号通过；两个均通过才比较单项开支，其他情况排名UNKNOWN。每组必须选择恰好一个候选编辑，每编辑含目标字段、替换值（None表示值未知，不代表用户已经撤销该硬约束）、路径掩码。不同组重复写同字段一律排除，暂不支持有顺序的连续覆盖。按每条路径做状态转移，状态为当前四字段值与本轮已写字段集合；转移只允许该路径支持的候选且目标未写。由归纳可知，每一步状态恰是该路径上合法编辑前缀的值及已写集合；最终各路径状态并集等价于笛卡尔积枚举后检查掩码全交与目标冲突。对同一路径同值同已写集合去重只保留只读投影，不能用于合并真正账本记录、来源、修订权或用户意图。多路径的值世界也可能相同，计数不是概率。独立组合对照忽略路径掩码得到相容世界的超集，可能增加不必要的未知；首候选基线可得不属于任何相容世界的输出。输出每维可能值集合；仅可信夹具提供完整域、非空、未超预算且集合恰一已知值时，才称有限假设下该维确定。全部输出authority NONE、math_release false，禁止实际写入或推荐。无世界只代表给定候选池无相容解；覆盖未知及预算触发时不展示确定投影。算法每路径状态数不超过已处理候选组基数乘积，实际尝试受预算控制；预算并非真实内存/墙时上限，输入验证及循环筛选未计入。真实语义、单位、目标身份、原文锚、完整性、授权、证据和原生数学门须独立确认。

例：候选解释(上限10,支出9)或(上限20,支出19)，共同费用0。两个均通过。忽略关联则额外构造(10,19)，导致不必要的不确定。反之任意取第一个解释不能证明后续全部解释均通过。有限结果一致不能作为确认编辑对象的票据。

只读收据原型绑定会话实例、授权代次、修订号、有序路径ID、四值、原文UTF8摘要、解析器版本、候选组与覆盖状态。宿主内存表保存收据，发布及读取均核对当前快照，修订严格递增，撤回清空表并提升授权代次。当前模拟仅信任内部worker；未防护任意调用者伪造job、同代次重复发布或跨实例ID碰撞，未实现并发CAS、持久化、签名、真实清除或撤回后处理权限。即使新修订的值相同也拒绝旧收据；所有收据只是描述性。7类变更均同时递增revision，故拒绝计数不能证明每个单独字段绑定均被独立有效测试；本轮不声称新事务协议已验证。方法和版本绑定未来须覆盖全部依赖及源资格，不能代替已有原生合同。

## 实际执行
Python 3.13.5容器，原创合成，研究者选择分布和基线，无真实个人信息、外部数据、独立样本或训练。study.py普通及-O各一次；除seconds外结果完全一致。receipt.py普通及-O各一次，JSON字节一致。
| 指标 | 穷举 | 随机 |
| --- | ---: | ---: |
| cases | 3888 | 3000 |
| finite | 3768 | 2760 |
| no_world | 120 | 240 |
| coherent_worlds（每场景去重后累加） | 9828 | 12432 |
| independent_worlds（仅finite场景） | 12276 | 19144 |
| independent_spurious_world（no_world场景） | 120 | 129 |
| first_collision（仅finite场景） | 1872 | 1100 |
| first_no_witness（非碰撞首选） | 384 | 263 |
| first_outside_projection（维度） | 396 | 76 |
| first_unjustified_certainty（维度，可与前项重叠） | 2874 | 1348 |
| determined_dimensions | 1684 | 2469 |
| determined_feasibility | 1604 | 2457 |
| independent_lost_determination | 746 | 496 |
| partially_determined_cases | 1180 | 1594 |
| all_determined_cases | 80 | 12 |
| work | 24192 | 83628 |
| max_work | 12 | 155 |

每场景世界集合及逐维投影均与独立笛卡尔枚举一致（两者共用人工verdict函数，非独立数学模型验证）。7专项控制、9拒绝控制。首次总时0.768026506秒，非真机、非完整入口、未测内存。收据1500基础会话×7类修订，每类陈旧发布、读取、恢复值后的旧收据各拒绝10500次；新鲜收据10500次；撤回后陈旧发布、读取、倒退修订各拒绝1500次。完整本地执行源码SHA256 study.py 51f462335b32b127ee3acdbb3ad3e7a1d22f967c0aa2744009b29b681d60211b，receipt.py b268e8a9e76a25eb343211de9ca34528a7a7e1e248526f175d06df11179d50cb；普通结果SHA256 e9346de7c10a254627240b12e52e61a3e53abddb1f75bc9ad920ab475a3879a9、34dc251a16ecb35057e9c072d1e43ef0dadf759bbfa9e0f3bfc207d22ad9a58a。完整执行脚本与回执另有本次对话ZIP；下列为手工转录的核心和主要计数复算包装，未单独运行该转录。

## 复算核心及实验（Python标准库）
```python
from itertools import product
from random import Random
from collections import Counter

F=('cap','a','b','fee')
def output(row):
    c,a,b,f=row
    def gate(x):
        return 'UNKNOWN' if None in (c,x,f) else ('PASS' if x+f<=c else 'FAIL')
    x,y=gate(a),gate(b)
    return x,y,('UNKNOWN' if x!='PASS' or y!='PASS' else ('A' if a<b else 'B' if b<a else 'TIE'))
def project(rows):
    return tuple(frozenset(x) for x in zip(*(output(r) for r in rows))) if rows else ()
def apply(base,edits):
    if len({e[0] for e in edits})!=len(edits):return None
    d=dict(zip(F,base))
    for k,v,m in edits:d[k]=v
    return tuple(d[k] for k in F)
def solve(base,p,groups,budget=100000,coverage=True):
    worlds=set();work=0
    for i in range(p):
        states={(base,0)}
        for g in groups:
            new=set()
            for row,used in states:
                for k,v,m in g:
                    if not m&(1<<i):continue
                    work+=1
                    if work>budget:return 'BOUNDED',set(),(),work
                    j=F.index(k);bit=1<<j
                    if used&bit:continue
                    new.add((row[:j]+(v,)+row[j+1:],used|bit))
            states=new
            if not states:break
        worlds.update(r for r,_ in states)
    if not coverage:return 'COVERAGE_UNKNOWN',worlds,(),work
    return ('FINITE' if worlds else 'NO_WORLD'),worlds,project(worlds),work
def oracle(base,p,groups,coherent=True):
    rows=set()
    for es in product(*groups):
        witness=set(range(p))
        for k,v,m in es:witness.intersection_update(i for i in range(p) if m>>i&1)
        if coherent and not witness:continue
        r=apply(base,es)
        if r is not None:rows.add(r)
    return rows
def ck(ok):
    if not ok:raise RuntimeError('mismatch')
def check(base,p,gs,c):
    stat,rows,proj,work=solve(base,p,gs)
    expected=oracle(base,p,gs);indep=oracle(base,p,gs,False);ip=project(indep)
    ck(rows==expected and proj==project(expected) and expected<=indep)
    c['cases']+=1;c['work']+=work;c['max_work']=max(c['max_work'],work)
    if not rows:
        c['no_world']+=1;c['independent_spurious_world']+=bool(indep);return
    c['finite']+=1;c['coherent_worlds']+=len(rows);c['independent_worlds']+=len(indep)
    es=tuple(g[0] for g in gs);n=apply(base,es)
    if n is None:c['first_collision']+=1
    else:
        joint=(1<<p)-1
        for k,v,m in es:joint&=m
        c['first_no_witness']+=not joint
        for x,s in zip(output(n),proj):
            c['first_outside_projection']+=x not in s
            c['first_unjustified_certainty']+=len(s)>1 and x!='UNKNOWN'
    for j,(a,b) in enumerate(zip(proj,ip)):
        ck(a<=b);d=len(a)==1 and 'UNKNOWN' not in a
        c['determined_dimensions']+=d;c['independent_lost_determination']+=d and len(b)>1
        if j<2:c['determined_feasibility']+=d
    ds=[len(x)==1 and 'UNKNOWN' not in x for x in proj]
    c['partially_determined_cases']+=any(ds) and not all(ds)
    c['all_determined_cases']+=all(ds)
c=Counter()
ts=[('cap','a','b','fee'),('cap','a','cap','b'),('a','b','a','b'),('cap','fee','a','b')]
vs=[(5,9,13,0),(15,6,4,3),(None,8,10,2),(12,None,5,None)]
for base in [(10,8,12,1),(8,4,4,4),(None,7,10,0)]:
    for t,v,m in product(ts,vs,product((1,2,3),repeat=4)):
        es=tuple(zip(t,v,m));check(base,2,(es[:2],es[2:]),c)
print(dict(c))
rng=Random(20261126);c=Counter()
for _ in range(3000):
    p=rng.randint(2,8);base=tuple(rng.choice([None,*range(3,16)]) for _ in F);gs=[]
    for _ in range(rng.randint(1,4)):
        es=[]
        while len(es)<3:
            e=(rng.choice(F),rng.choice([None,*range(16)]),rng.randint(1,(1<<p)-1))
            if e not in es:es.append(e)
        gs.append(tuple(es))
    check(base,p,tuple(gs),c)
print(dict(c))
```

## 后续
保持原生账本及科学硬门独立。优先针对已有公开开发对话中同轮多编辑、跨轮主体、周期、条件及修订根映射，验证能否真实生成联合候选；完整域及未见解释检测由独立轨把关。需要真实的原生事务、并发、存储及App测试。未进行正式版本开发、训练、合并PR、部署、主动CI或额外费用；历史证据等级、R073、PESEN及冻结不变。
