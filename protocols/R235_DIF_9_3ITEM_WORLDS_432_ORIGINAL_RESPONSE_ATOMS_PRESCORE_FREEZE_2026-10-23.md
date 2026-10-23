# R235 差异项目功能：九人工双群体三题IRT、432结构原来源与能力匹配对照的假阳性/假阴性，代码前机制冻结

日期2026-10-23（Asia/Taipei）。原始239目录真实`10-009 Differential Item Functioning`，P1，编号R235。续R234但独立研究IRT潜在能力匹配、组别原潜在能力组成、锚题污染、uniform/nonuniform DIF、Mantel-Haenszel（MH）汇总共同优势比的有界限制。仅精确人工有限E1，新增真人E2=0、真实历史E3=0；R073与PESEN v0.1不变。

## 原始研究与界限

Holland & Thayer (1986), [*Differential Item Functioning and the Mantel-Haenszel Procedure*](https://www.ets.org/research/policy_research_reports/publications/report/1986/hwnk.html), ETS Research Report RR-86-31, DOI https://doi.org/10.1002/j.2330-8516.1986.tb00186.x，ETS原作者摘要明确MH为非迭代2×2×K表公共优势比检验，须按能力等条件匹配。Camilli & Shepard (1994), [*Methods for Identifying Biased Test Items*](https://www.sagepub.com/shop/buy-a-book/methods-for-identifying-biased-test-items-1-3416), 原出版方强调DIF统计量与实质项目偏误不能直接划等号。本R只精确列举人工作答概率及人工匹配的population共同比值，不用真实考试、χ²显著性、总体公平判定、因果歧视断言，也不伪称原作者实证数据端到端复现。

## 九模型、全部来源与固定评分

群体G∈{0,1}先验1/2，原潜在能力索引k∈{−1,0,1}，三项二元观测`Y1,Y2,Y3∈{0,1}`。统一基准群体G0先验`P(k)=1/3`，题目难度`b=(-1,0,1)`、区分度a=(1,1,1)，真实潜在θ=k。三题给定k/G条件独立；每一项人工作答概率`p_j(k,g)=2^{a_{jg}(θ_{kg}-b_{jg})}/(1+2^{a_{jg}(θ_{kg}-b_{jg})})`，指数在冻结整数网格上取整数且Fraction完全精确。G1默认与G0全部相同。若注明composition shift，G1能力先验改为`(1/6,1/3,1/2)`。G1所有潜在k与三题8模式均完整保留，每世界2×3×8=48条结构概率来源、共**432条**，不存在先删掉零/低概率模式。联合源概率P(G,k,Y)=P(G)P(k|G)∏p_j^{Yj}(1−p_j)^{1−Yj}，每世界概率总和1。

九世界：

1. `BASE_NO_DIF`：全部默认，两群同k下三题成功率相同，组边际焦点Y2成功率均1/2。
2. `ABILITY_MIX_NO_DIF`：仅G1能力先验改为(1/6,1/3,1/2)，三题真实反应机制完全不变；G1焦点题总体通过率5/9、G0为1/2。真实固定能力k条件下焦点题DIF严格0。
3. `UNIFORM_FOCAL_HARDER`：仅G1焦点第二题难度由0增至1，其余不变，G1焦点通过率31/90，真实G1在每个能力点都更难。
4. `UNIFORM_FOCAL_EASIER`：仅G1焦点难度由0降至−1，其余不变，G1焦点通过率59/90，三能力点均更易。
5. `NONUNIFORM_FOCAL_DISCRIMINATION`：仅G1焦点题区分度由1增至2而难度同为0；k=−1时G1更难，k=0相同，k=1时G1更易。**G1/G0总通过率均1/2，且按两锚题总分分层的MH人口共同优势比恰为1**，不能因此误判为不存在能力依赖的nonuniform DIF。
6. `ANCHOR_ITEM1_DRIFT`：只有G1锚题Y1难度从−1变为0，焦点Y2完全不变，但以`Y1+Y3`锚题总分匹配时会出现非1的MH人口优势比（锚题污染导致统计伪DIF）。
7. `ANCHOR_ITEM3_DRIFT`：只有G1锚题Y3难度从1变为2；焦点Y2无真实DIF，但受污染锚题匹配的MH共同优势比可能偏离1。
8. `GLOBAL_REANCHOR_ALIAS`：G1潜在数值坐标改为θ=k+1，三个题目难度也统一同时+1，故每个k及全原来源实际Y的条件概率与BASE_NO_DIF严格相同，整个`P(G,Y1,Y2,Y3)`相同。原始IRT难度参数不同是**潜在单位原点重标定**，不等于对原同一能力标尺下的实质DIF。
9. `COMPOSITION_PLUS_TRUE_DIF`：同时进行G1能力先验shift和焦点题难度+1，二者同时存在，不能用混合的边际通过率消解真题目差异。

## 冻结观察与人工oracle统计

A. 汇总三题完整观测`P(G,Y1,Y2,Y3)`以及`P(Y2=1|G)`，其中**观察算法不读取潜在k或原项目难度**。能力条件oracle`p_2(k,g)`独立直接从冻结题目参数产生；给出三点真G1−G0差向量，区分uniform同号、nonuniform变号、无DIF恒0。
B. 已预定义匹配`S_anchor=Y1+Y3∈{0,1,2}`，不使用被检焦点Y2计算匹配分数；各s从**实际可见G和三题**构造2×2人工概率表`A_s=P(G1,Y2=1,S=s), B_s=P(G1,Y2=0,S=s), C_s=P(G0,Y2=1,S=s), D_s=P(G0,Y2=0,S=s)`。MH人口汇总优势比 `OR_MH= [Σ_s A_s D_s/N_s]/[Σ_s B_s C_s/N_s]`，N_s=A+B+C+D。全部分母固定严格正值，Fraction精确。此处仅报告严格人工总体`OR_MH`，不计算χ²或实际样本效应CI。
C. `BASE_NO_DIF`固定能力下真差向量(0,0,0)，总体G1−G0通过率0，MH=1。 `ABILITY_MIX_NO_DIF`也真差向量(0,0,0)，但观察率差1/18，MH>1（能力组成没有被仅两个锚题完美匹配）。`ANCHOR_ITEM1_DRIFT`/`ANCHOR_ITEM3_DRIFT`真差均0，却有MH>1（错误锚题）。
D. `NONUNIFORM_FOCAL_DISCRIMINATION`真焦点差在k=−1为负、k=0为0、k=1为正，**总体率差0且MH精确1**；三种匹配分数分层的焦点成功率差出现正负交叉。这是有限人工总体抵消，说明单一MH汇总关联=1不够证明没有真实能力交互，但**不是对全部非均匀DIF统计功效的广义定理**。
E. `UNIFORM_FOCAL_HARDER`MH<1、`UNIFORM_FOCAL_EASIER`MH>1，与固定能力真差方向一致；`COMPOSITION_PLUS_TRUE_DIF`仍需oracle固定能力比较而非边际率符号推断。`GLOBAL_REANCHOR_ALIAS`与`BASE_NO_DIF`每个k/G/模式概率严格一致，完整可见四变量联合相同，但潜在原点参数不同。
F. 来源完整性48×9，源CSV、JSON、SHA，纯Python3.11/3.12两版本≥45项真实单测及第三真实原源归档job，所有数学概率和、真能力DIF、完整观察别名、MH方向/抵消须独立核验，永久提交main后方可正式有界验收。禁止认为数学源行=真实个体样本；对真人E2、真实历史E3新增仍0。
G. 下一原239目录`10-010 Survey Response Bias Models`（计划R236）完成此项后再次核验。原R优先完成，分类和融合暂缓。
