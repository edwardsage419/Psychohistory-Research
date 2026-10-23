# 心理史学：R311通用有界信任、R066旧HK证据再归属及R312 Deffuant异步意见更新（原239 v2.9）

日期2026-10-23 Asia/Taipei。严格保持研究顺序：完成全部原R系列候选学习/必要复算及科学分级→统一归纳分类→最后构造原创熔炼模型。个人辅助决策系统具体建设继续暂缓。**本轮真实新增的是两项人工数学E1限定机制研究，不新增真人/动物E2或历史E3；完整239项科学总结题未成立。** 保持R073与PESEN v0.1冻结。

## 一、原著分类和三项研究对象互不偷换

Hegselmann & Krause (2002), *Opinion Dynamics and Bounded Confidence: Models, Analysis and Simulation*, 原始[JASSS全文](https://www.jasss.org/5/3/2.html)；Deffuant、Neau、Amblard、Weisbuch (2000), *Mixing beliefs among interacting agents*, DOI https://doi.org/10.1142/S0219525900000078；Lorenz (2007), *Continuous Opinion Dynamics Under Bounded Confidence: A Survey*, DOI https://doi.org/10.1142/S0129183107011789。两种典型有界信任模型均选择意见足够接近的伙伴，但**HK同步按整个邻域更新**，**Deffuant按一次随机选出的两人异步折中**，而二者共同的“置信关系几何”还不足以定义更新过程。于是本轮明确分开以下三项，不把旧研究数据计入新模型：

| 原始候选编号 / 机制 | 实际归属 | 科研证据范围 | 本轮**新**来源行 |
|---|---|---|---:|
| 04-011 Bounded Confidence Models：阈值关系图结构 | **R311新研究** | 324个人工图世界，精确邻接和连通分量 **E1** | **1,944** |
| 04-012 Hegselmann Krause：同步意见平均化 | **既有R066研究** | 旧人工HK E1，加16村真实内部条件预测E2（非网络因果识别） | **0** |
| 04-013 Deffuant Weisbuch：相遇对异步折中 | **R312新研究** | 48人工参数世界、288配对事件、异步顺序反例 **E1** | **1,152** |

本轮**3,096条新增人工原source行**并非3,096名真实被试；R066旧真实1,872条配对家庭意见记录已在2026-10-16旧研究中完成严格来源/限定验证，本次只做档案归属，不重复生成E2或宣称第二项独立实验。

## 二、R311：置信图整体连通不意味着所有人直接相容

[先行冻结协议](../protocols/R311_BOUNDED_CONFIDENCE_FOUR_NODE_1944_PAIR_SOURCE_PRESCORE_FREEZE_2026-10-23.md) [commit98f463ac](https://github.com/edwardsage419/Psychohistory-Research/commit/98f463acd827ab9535ae134c4d22bbe3235da837)。四个虚拟独立编号对象的意见各取{0,1/2,1}，81种有序配置×ε={0,1/4,1/2,1}共**324人工世界**，每世界6个完整人工意见对，共**1944条原始source**；彼此有边当且仅当|xi−xj|≤ε。没有任何意见学习动态、群体讨论或真实社交网络。

固定意见(0,1/2,1,1)：

| 允许差异ε | 直接互信边数/6 | 图中连通分量数 | 所有人两两相容? |
|---|---:|---:|---|
| 0 | 1 | 3 | 否 |
| 1/4 | 1 | 3 | 否 |
| 1/2 | **4** | **1** | **否** |
| 1 | 6 | 1 | 是 |

因此“0与1/2可互动、1/2与1可互动”不意味着“0与1可直接互动”：阈值相容关系不传递。图路径连通≠完全相容≠下一时期必达成意见共识。全81种有序配置、四阈值组合中，增大ε时原相容边永不消失，连通分量数量不增加，ε=0只有相同观点可连边，ε=1全六对都连边；全部使用精确Fraction。

[R311完整科学报告](../research/R311/R311_SCIENTIFIC_REPORT_2026-10-23.md)、[1944原CSV](../research/R311/R311_ALL_1944_ORIGINAL_CONFIDENCE_DYAD_SOURCES.csv)、[324世界JSON](../research/R311/R311_EXACT_BOUNDED_CONFIDENCE_GRAPH_RESULTS.json)、[来源与结果字节SHA256](../research/R311/R311_MACHINE_RECEIPT.json)、[正式机器验收](../research/R311/R311_FINAL_ACCEPTANCE_STATUS.json)、[独立Union-Find完整来源审计](../research/catalogue_audit/independent_r311_source_audit.py)。主程序双Python各**5845项真unit tests**，独立不导入原模型程序用并查集（主程序用BFS）完整复算全部source。GitHub [科学CI39956812166](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956812166) **3/3 completed/success**；来源永久归档[commit2e5674e6](https://github.com/edwardsage419/Psychohistory-Research/commit/2e5674e6251718475372b485b6443592540bea23)。

## 三、原04-012 HK直接继承R066真实证据，不能冒充新实验

[事前冻结重归属协议](../protocols/ORIGINAL239_04_012_R066_HK_EXISTING_E1_E2_INTERNAL_SOURCE_REATTRIBUTION_FREEZE_2026-10-23.md) [commit086175f2](https://github.com/edwardsage419/Psychohistory-Research/commit/086175f230fe05f2ec0979a8252b8150b7971a09)和[完整04-012审计报告](ORIGINAL239_04_012_EXISTING_R066_HK_E1_E2_CONDITIONAL_SCOPE_AUDIT_2026-10-23.md)已固定：**不创建新的HK模型编号，不重新跑旧人工或真人预测**。

旧[R066正式科研验收](../research/R066/R066_FINAL_ACCEPTANCE_STATUS.json)确实完成同步HK原生机制对照和真实16村内部留一评价，原已通过[HK合成CI38845611874](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38845611874)与[16村真实条件预测CI38866210819](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866210819)。真实来源Harvard Dataverse DOI https://doi.org/10.7910/DVN/RAHSVM，16乌干达村、1872条基线/末次完整家庭态度配对，每折用其他15个村训练参数和共同漂移，评估留出村末次态度。**预测输入包括即时干预后态度**，不是纯基线未来预测。

留出村等权态度MSE：persistence加漂移0.04227103404620483、DeGroot0.028614616600241692、FJ0.0266149141842743、HK **0.0265478188648263**。HK与FJ差值仅约0.0000670953，未完成配对村级差异不确定性估计；按家庭加权评分FJ还略低于HK。**HK与FJ的信息结构不等价**：HK把全村主体按意见阈值选邻居，不使用实际测得的家庭网络边，而FJ使用真实家庭网络。因而不能称HK已经按真实网络重现个体影响、建立人类机制因果、在外部独立村实验复制，或预测长期制度历史E3。真实研究原文件、结果和失败边界一律不变；本次只确定04-012旧E1与有界E2的正确研究来源R066。

[HK旧研究来源重归属目录CI39957392369](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957392369) **3/3成功**，逐项核验上述真实来源、原作者网络边核查、模型公式、旧结果和未闭合的因果/外部验证门，不重复生成新的E2。

## 四、R312：Deffuant随机配对异步更新的路径依赖性

[事前协议冻结](../protocols/R312_DEFFUANT_RANDOM_DYAD_ONE_STEP_1152_PERSON_SOURCES_PRESCORE_FREEZE_2026-10-23.md) [commit2c8c9bfd](https://github.com/edwardsage419/Psychohistory-Research/commit/2c8c9bfd15a27574f0fffb02517eb5893aedfee9)。明确预设8种四人意见模式、三阈值ε=0,1/2,1、两种折中μ=1/4,1/2，共**48人工参数世界**；每世界6个等概率1/6的潜在两人相遇，生成**288配对事件×4个人工节点=1152完整原source**。选中二人只有意见距离≤ε时才按xi'=xi+μ(xj−xi)、xj'=xj+μ(xi−xj)改变；另外两人原意见不变。任何一个已选择相遇对的总意见和精确守恒，六可能相遇后的条件预期群体均值也守恒。

固定意见F=(0,1/2,1,1)、ε=1、μ=1/2：
- 两次相遇顺序**(0,1)→(1,2)**产生**(1/4,5/8,5/8,1)**；
- 完全反转顺序**(1,2)→(0,1)**产生**(3/8,3/8,3/4,1)**。

所以有限异步更新具有非交换性，不能偷换成HK同步一轮平均化。在C=(0,0,1/2,1)和ε=1/2时，相遇(1,2)允许更新二人至1/4，而(0,3)距离1超过阈值，必须严格不变。所有结果是项目冻结人工数值，不具有现实人类社会收敛的统计外推。

[R312完整科学报告](../research/R312/R312_SCIENTIFIC_REPORT_2026-10-23.md)、[1152完整原source](../research/R312/R312_ALL_1152_ORIGINAL_DEFFUANT_PERSON_SOURCE_ROWS.csv)、[48世界288配对事件原结果](../research/R312/R312_EXACT_DEFFUANT_PAIR_EVENT_RESULTS.json)、[完整SHA256机器凭证](../research/R312/R312_MACHINE_RECEIPT.json)、[正式E1机器验收](../research/R312/R312_FINAL_ACCEPTANCE_STATUS.json)和[独立中点/差值收缩审计](../research/catalogue_audit/independent_r312_source_audit.py)。双Python各**3469项主unit tests**，独立无导入公式全source逐值核验。真实[科研CI39957585074](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957585074) **3/3成功**，原CSV/JSON/SHA永久归档[commit53052edb](https://github.com/edwardsage419/Psychohistory-Research/commit/53052edbe7a1f87a476f7c9297db5a961095667d)。未证明原作者的长期群体分群定理，也未重跑实测人类意见轨迹。

## 五、全部239模型原目录版本化来源台账

| 科研档案来源分级 | v2.6本轮之前 | v2.7 R311后 | v2.8复用HK R066后 | **v2.9 R312后** |
|---|---:|---:|---:|---:|
| 已建立专属主R研究归属 | 200 | 201 | 202 | **203** |
| 共享旧有界数学关联 | 3 | 3 | 3 | **3** |
| 仅旧有限审计无主R | 2 | 2 | 1 | **1** |
| 资料已查未建立逐项主R | 34 | 33 | 33 | **32** |
| 主R来源仍待核 | 36 | 35 | 34 | **33** |
| 原239唯一候选 | 239 | 239 | 239 | 239 |

[完整239原候选证据交叉索引v2.9](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.9_2026-10-23.json)相对v2.8只增04-013的R312；v2.8相对v2.7只把04-012归属既有R066；v2.7相对v2.6仅给04-011新增R311，原始239候选编号、原名称、P1/P2、顺序及历史其他模型来源全部不变。R066同时在04-010 FJ、04-012 HK两种独立模型下被复用，因此**203项主R关联不是203个互不重叠的独立真人实证，更不是203个已验证的历史预测模型**。

[33项剩余P1/P2主R待核队列](ORIGINAL_239_PENDING_33_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，P1 **6**、P2 **27**，下一条**04-014 Axelrod Cultural Dissemination**。应先核对原著局部文化互动/文化同质化机制，不以普通意见距离置信阈值代替离散多特征文化复制；再保持全部R系列先完成、归纳分类后开展模型熔炼。

本轮**5个已独立验证成功的三作业工作流，共15个CI作业全部completed/success**：
[R311科学39956812166](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956812166)、
[R311目录v2.7 39957112283](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957112283)、
[旧HK R066目录v2.8 39957392369](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957392369)、
[R312科学39957585074](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957585074)、
[R312目录v2.9 39957912593](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957912593)。

新增人工数学主单元测试在两个解释器合计**2×(5845+3469)=18628项通过**，两套源码另有独立逐行复算和反例审计。**真实人类E2新增数0、动物E2新增数0、历史E3新增数0**。R073/PESEN v0.1继续冻结，原始239完整科研验收/跨尺度整合仍开放。
