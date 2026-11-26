# 自主认知：多义务联合可达性及有界搜索完整性
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与去重
固定 main b47c0f693bf66233d85fead39a0d6fe82951ab48，实际读取25次近期提交、15项开放Draft PR、v3.2全文、AGENTS、同步规程前45行、唯一交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前60行及最近研究相关段落。#63 head 734686980b19da9291bdd08b67d4e2519c011acf，未重跑。直接前序研究 research/decision_hub/2026-11-26-word-lattice-role-span-joint-budget.md blob 5187932b98ecee06db6bba7c8714b9dab0304b18 已证明固定边界集的精确联合成本，并在公开合成开发语料上枚举跨度对。本轮不重新运行其词典或原语料，新增三及以上义务、显式高阶语义禁配关系、有限搜索截断下候选支持/排除/未知三分、独立穷举对照；与已有有界候选搜索和联合条件政策仅作局部去重，不声称全库无重叠。前序原文词格、真实候选和宿主确认尚未接入本轮程序。
## 形式与证明
有限有向无环词格节点为原文位置，边非负整数成本；每个候选组必须选一项，候选有全局唯一ID及有限必经边界集合；显式禁配集合可以含2项或更高阶。所有候选均非可信宿主授权。若某组缺少候选，必须在实际产品保留UNKNOWN/未覆盖，不应用人工虚构的兜底证明完整。实验中的可选空端点仅为控制结构。
对选中候选的边界并集 P，沿用前序最短路公式 C(P)=sum d(p_i,p_(i+1))-d(0,n)，p为排序去重后加首尾。固定P时各段最短路可拼接，因此精确。增加必经边界只能缩小路径集合，故 C 单调不减；增加已选ID不能使已经包含的禁配集合消失。DFS可以安全剪掉超预算或已包含禁配的部分状态。该结论限于显式有限候选和关系，不能推出真实语义义务已覆盖。完整DFS才允许对有限集合内没有任何可行世界支持的候选标记excluded；截断时只能声明已发现的支持，未找到支持者统一unknown。本轮保守地不单列截断时已有局部排除证明。路径成本非概率，组合计数非概率。
控制一：三段独立菱形格各要求一个中间点时成本1，预算2。A/B/C各可行，所有二元组合可行，ABC不可行。控制二：预算3允许全部边界，但显式三元禁配ABC，任何二元组合仍可行。两例均有8个候选组合，真实联合可行7个；独立和二元基线各错误接受ABC。前者验证全局资源约束，后者验证不能把高阶语义关系机械降为二元。
## 实际执行
在当前Python容器运行原创标准库程序，固定seed 20261126，2个控制和300个有限随机图。随机图5至10个边界步长，每节点最多向后3步、至少单步边，边成本0至4；3至5组、每组2至3项，随机必经跨度，0至4个显式禁配集合（2至4元），预算0至8。仅合成结构，不是语言或真实决策样本。独立算法先枚举全部路径及笛卡尔候选，再验证路径访问端点、禁配、预算；不调用DFS成本函数。两种基线在相同候选和预算上比较。
结果：302组完全一致；精确可行世界3813，逐项可行7169（200组有虚假世界），两两可行4486（109组有虚假世界）；两两多673。穷举参照累计路径13098。DFS访问10907节点，未剪枝搜索树24185，减少13278节点即54.90%；预算剪枝2173、关系剪枝720。每例节点预算0/1/5/15/50，1510次截断控制中1117未完成、393完整；完整世界和支持与穷举一致，截断无错误排除且未知覆盖所有未获支持的候选。另8个非法输入（负预算/节点帽、逆边、无完整路径、重复ID、空组、越界端点、未知禁配ID）均显式拒绝。
最后普通Python运行含断言，0.337291秒为本次容器内全实验计时，不是Mac/iPhone、生产入口或可复现性能承诺。另运行python -O仅观察程序可运行，assert不执行，不作为验收。完整本地脚本SHA256 79b10021a84dda4ee4f7ff0f4be75862687e5d600cb54fa71663b955c283c773；本次结果JSON SHA256 23dc9ac038cb8059329f925f42fdb8f9cf8c8bd1dbef3644d559c39d9207c2b9。完整源和结果随当轮聊天交付，下面是核心算法说明性摘录（非完整随机实验脚本，不声称其哈希等同完整文件）。
## 核心复算摘录
```python
def distances(g):
    n = len(g)
    d = [[float('inf')]*(n+1) for _ in range(n+1)]
    for s in range(n+1):
        d[s][s] = 0
        for i in range(s,n):
            for j,c in g[i]:
                d[s][j] = min(d[s][j], d[s][i]+c)
    return d

def finite_search(g, groups, forbidden, budget, cap=None):
    # Validated finite inputs only; full local implementation validates inputs.
    d = distances(g); n = len(g); cache = {}; worlds = []
    nodes = 0; incomplete = False
    def cost(points):
        k = tuple(sorted(set(points)|{0,n}))
        if k not in cache:
            cache[k] = sum(d[a][b] for a,b in zip(k,k[1:]))-d[0][n]
        return cache[k]
    def visit(k, ids, points):
        nonlocal nodes, incomplete
        if cap is not None and nodes >= cap:
            incomplete = True
            return
        nodes += 1
        if any(f <= ids for f in forbidden) or cost(points)>budget:
            return
        if k==len(groups):
            worlds.append(tuple(sorted(ids)))
            return
        for name,ends in groups[k]:
            visit(k+1, ids|{name}, points|set(ends))
            if incomplete:
                return
    visit(0,set(),set())
    universe={name for group in groups for name,_ in group}
    supported=set().union(*map(set,worlds)) if worlds else set()
    return dict(complete=not incomplete,worlds=sorted(worlds),
                supported=sorted(supported),
                excluded=sorted(universe-supported) if not incomplete else [],
                unknown=sorted(universe-supported) if incomplete else [],
                nodes=nodes,authority='NONE')

g=[[(1,1),(2,0)],[(2,0)],[(3,1),(4,0)],[(4,0)],[(5,1),(6,0)],[(6,0)]]
groups=[[('A',(0,1)),('a',())],[('B',(2,3)),('b',())],[('C',(4,5)),('c',())]]
for fs,b in [([],2),([frozenset('ABC')],3)]:
    r=finite_search(g,groups,fs,b)
    assert r['complete'] and len(r['worlds'])==7 and ('A','B','C') not in r['worlds']
    q=finite_search(g,groups,fs,b,1)
    assert not q['complete'] and not q['excluded'] and len(q['unknown'])==6
```
## 接入边界与下一责任
最短路表 O(nE) 时间、O(n²)空间；搜索最坏指数、显式关系检测及缓存内存另计。当前仅节点帽，尚无墙时/内存/序列化限额、恢复令牌、路径见证或跨端一致性证明；不能直接生产启用。需在真实候选上连接角色、主体、数量及单位、条件方向、修订目标和显式关系；所有缺失关系和语义图外情况保留独立义务检测，完整搜索仅对指定图有效。输出建议应比较可行解释的实际决策效果，存在差异时才优先追问，已确认局部计算可继续，所有持久写入及真实行动须原宿主授权。禁止把随机组合比率当真实语言错误率。下一轮建议复用前序真实原文格与角色候选做联合多义务投影，独立轨保管未见案例，验证条件与修订端到端效果、错误放行及资源。研究者自行选择随机图、预算、种子、禁配和节点帽，未变更产品路线、未发新Codex任务、未修改生产文件/唯一交接/冻结协议/证据等级，未训练、合并PR、部署、主动CI或增加费用。
