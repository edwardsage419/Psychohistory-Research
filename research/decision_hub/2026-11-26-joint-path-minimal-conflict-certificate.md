# 有限路径最小冲突证书与可信宿主绑定
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_ONLY / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

基线：近期最新提交 efae59c78a65e548b2a4b01d69c6823a344613e8，写前再次查询近期提交同一首项，目标文件读取404。读取v3.2、同步规程、18近期提交、开放PR清单、前序跨段共同见证和段商图报告、#63固定head 734686980b19da9291bdd08b67d4e2519c011acf 的PUBLIC_DEVELOPMENT。未定位唯一近期交接，非全库去重。前序500句结果只引用，未重读语料；本轮仅原创合成有限集合，无训练、外部数据再分发或真实语义准确率声称。#63公开开发条件0/5，账本修订0/10。研究主题、分布、预算和基线由研究者选择。

## 证明与合同
路径集合P有p元素，义务i支持集合M_i。共同见证等价于所有M_i交集非空。两两相容不足以保证整体相容，例如三路径掩码3、6、5。动态规划状态s为当前交集，保存最短义务索引元组（长度相同选字典序小者）。对每义务从旧状态转移至s及s∩M_i；未来只依赖s，因此丢弃更长前缀不会丢失更短最终证书。最多min(2^p,2^n)状态，字典、元组和比较额外消耗。每个包含意义极小冲突核的义务都有一条只被该义务排除的路径，不同义务的这种见证不同，故核大小<=p。简单删除只能保证包含极小，未必基数最小。状态预算触发时报告可复核极小核，禁止宣称最短。

可信宿主持有原文UTF8摘要、修订身份、有序唯一候选路径身份的版本化清单；义务绑定清单ID及唯一义务ID。摘要只是身份核对，非签名、授权或完备性证明；不能接受调用者自授的清单。即使交集非空，仍不得认为主体、关系、守卫、事实已确认；无交集只说明有限候选池中无共同见证，可能存在遗漏路径。空义务集合也不证明覆盖。固定输出 authority=NONE、math_release=False、coverage=UNKNOWN。生产仍需完整强类型解析、路径内容身份、并发修订与真实可信边界、原文锚、证据及方法确认。

## 实际执行收据
Python 3.13.5标准库容器，实际完整核心脚本执行两次，除资源字段外JSON完全一致。穷举不同非零掩码集合：p=2/3/4分别8/128/32768组，冲突2/90/31826组；逐组与独立组合枚举最短核一致。两两检查漏过0/2/434组；删除基线较长0/14/18866组。种子20261126，p=8,n=12及p=16,n=24各500组独立随机均匀非零掩码；冲突500/500，删除基线较长239/412，峰值状态85/962；前100组各自另以组合枚举核对全部一致；cap=8各500组都报告受限冲突且证书验证。6非法输入拒绝、7专项控制。压力实例p=16，16义务各独自排除一个路径，65536状态，最小核16；首轮0.204364秒、tracemalloc峰值12792544字节，非RSS或真机；全核心首轮1.620983秒。绑定原型3正向、6负向检查通过：三义务冲突、两义务见证、空集合覆盖未知；拒绝不同修订、原文变化、路径顺序变化、摘要篡改、重复义务及越界掩码。原型未跑优化模式、生产原生入口、独立留出、真实用户、竞品及Mac/iPhone。完整本地脚本与JSON另作为本次对话附件；以下核心与主要计数复算是同算法精简摘录，未单独执行此摘录。 

## 核心复算（标准库）
```python
from itertools import combinations
from functools import reduce
from operator import and_
from random import Random

def validate(p,masks):
    if type(p) is not int or not 1<=p<=64: raise ValueError('path count')
    full=(1<<p)-1
    if any(type(m) is not int or not 0<=m<=full for m in masks): raise ValueError('mask outside universe')
    return full

def intersection(full,masks,ids):
    return reduce(and_,(masks[i] for i in ids),full)

def shrink(p,masks):
    full=validate(p,masks); ids=list(range(len(masks)))
    if intersection(full,masks,ids): return None
    for i in ids[:]:
        trial=[j for j in ids if j!=i]
        if intersection(full,masks,trial)==0: ids=trial
    return tuple(ids)

def exact(p,masks,cap=65536):
    full=validate(p,masks)
    if type(cap) is not int or cap<1: raise ValueError('state cap')
    joint=intersection(full,masks,range(len(masks)))
    if joint: return ('WITNESSED',joint,None,1)
    fallback=shrink(p,masks); dp={full:()}; peak=1
    for i,m in enumerate(masks):
        nxt=dp.copy()
        for s,ids in dp.items():
            t=s&m; cand=ids+(i,); old=nxt.get(t)
            if old is None or (len(cand),cand)<(len(old),old):
                if old is None and len(nxt)>=cap: return ('CONFLICT_BOUNDED',0,fallback,peak)
                nxt[t]=cand
        dp=nxt; peak=max(peak,len(dp))
    return ('CONFLICT_EXACT',0,dp[0],peak)

def brute(p,masks):
    full=validate(p,masks)
    for k in range(1,len(masks)+1):
        for ids in combinations(range(len(masks)),k):
            if intersection(full,masks,ids)==0: return ids
    return None

def check(p,ms,r,reference=False):
    status,mask,core,states=r; full=validate(p,ms)
    joint=intersection(full,ms,range(len(ms)))
    if joint: assert status=='WITNESSED' and mask==joint and core is None
    else:
        assert status.startswith('CONFLICT') and intersection(full,ms,core)==0
        assert all(intersection(full,ms,[j for j in core if j!=i])!=0 for i in core)
    if reference and status!='CONFLICT_BOUNDED': assert core==brute(p,ms)

for p in (2,3,4):
    u=list(range(1,1<<p)); cases=conflicts=worse=miss=mx=0
    for sel in range(1<<len(u)):
        ms=[m for i,m in enumerate(u) if sel>>i&1]
        r=exact(p,ms);check(p,ms,r,True);cases+=1
        core=r[2]
        if core is not None:
            conflicts+=1;mx=max(mx,len(core));worse+=len(shrink(p,ms))>len(core)
            miss+=all(a&b for a,b in combinations(ms,2))
    print(p,cases,conflicts,worse,miss,mx)
rng=Random(20261126)
for p,n in [(8,12),(16,24)]:
    worse=bounded=peak=0
    for i in range(500):
        ms=[rng.randrange(1,1<<p) for _ in range(n)]
        r=exact(p,ms);check(p,ms,r,i<100)
        assert r[2] is not None
        worse+=len(shrink(p,ms))>len(r[2]);peak=max(peak,r[3])
        b=exact(p,ms,cap=8);check(p,ms,b);bounded+=b[0]=='CONFLICT_BOUNDED'
    print(p,worse,bounded,peak)
```

后续：在相同候选预算下把真实原文义务及分词路径绑定送入可信宿主，比较有限冲突、候选池遗漏与任务结果；独立轨掌控未见案例。保持候选与原文权威、硬约束及计算准入分离。不修改生产、PR、冻结、证据等级、交接、部署、训练或主动CI。零新增费用。
