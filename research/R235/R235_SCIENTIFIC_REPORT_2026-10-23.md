# R235 差异项目功能：九有限IRT世界、432完整响应来源与MH匹配的假阳性和假阴性

日期：2026-10-23（Asia/Taipei），真实239目录 **10-009 Differential Item Functioning（P1）**。正式科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_DIF_MH_MATCHING_LIMITS**。全部是三题二元作答的九个预先规定的人工概率模型；不涉及真实群体考试、真人受试者公平性实证结论或历史E3数据。

## 方法原著、项目定位与事前冻结

Holland & Thayer (1986), [*Differential Item Functioning and the Mantel-Haenszel Procedure*](https://www.ets.org/research/policy_research_reports/publications/report/1986/hwnk.html), ETS RR-86-31, DOI [10.1002/j.2330-8516.1986.tb00186.x](https://doi.org/10.1002/j.2330-8516.1986.tb00186.x)。ETS原稿及原期刊摘要说明MH是一种在2×2×K分层表中统计公共两组关联的非迭代方法；当前数学反例用的是**总体人口概率MH公共优势比，不是MH样本χ²显著性检验**。Camilli & Shepard (1994), [*Methods for Identifying Biased Test Items*](https://www.sagepub.com/shop/buy-a-book/methods-for-identifying-biased-test-items-1-3416), SAGE原出版方对项目差异检测与证据如何解释作出方法综述，强调统计项目DIF与实质的不公平偏差评价之间仍有距离。当前既未取得这些作者的真实项目数据，也未复现原书内实际测验拟合与经验统计。

在源代码与程序验收提交前，已独立冻结[九个条件IRT世界、配额及匹配方案](../../protocols/R235_DIF_9_3ITEM_WORLDS_432_ORIGINAL_RESPONSE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，提交 [b71bff10](https://github.com/edwardsage419/Psychohistory-Research/commit/b71bff10ce9e21affd0a7619fa9c7fd72551e080)。本R原机制按冻结条件计算，数学结果经原始源码及完整人工概率遍历，未事后更改模型方向、随机源或评分。

## 完整有限原来源与独立算法

每世界两人工群体G0/G1（比例各1/2），三潜在能力索引k∈{-1,0,1}和三道二元题`Y1,Y2,Y3`，固定真实生成反应为底数2 logistic`P(Yj=1|G,k)=2^[a_jg(θ_kg−b_jg)]/(1+2^[a_jg(θ_kg−b_jg)])`。原始G0三能力索引概率均为1/3；部分模型G1先验刻意改为(1/6,1/3,1/2)。默认项目难度(-1,0,1)、区分度(1,1,1)，真实焦点题为Y2，两个非焦点锚题为Y1及Y3。G、k与完整8种三题反应均保留，故每世界2×3×8=48原来源，九世界共**432条完整原结构来源**，所有概率严格正，且逐世界总和1。源码用Fraction构造概率及贝叶斯边际，不冒充432真人考试。

独立验证路线一从完整48原来源的**实际可见G、Y1、Y2、Y3**积分得到观察完整四变量联合、两组焦点题成功率与锚分`S_anchor=Y1+Y3`下的2×2列联表；路线二直接按潜在k的分组概率乘冻结IRT题目成功机率，独立积分恢复相同观察联合。全部MH分层仅依赖实际可见分数。

固定MH式`OR_MH=Σ_s(A_sD_s/N_s) / Σ_s(B_sC_s/N_s)`，其中在每个s=0,1,2锚题得分层，A=P(G1,Y2=1,S=s)，B=P(G1,Y2=0,S=s)，C=P(G0,Y2=1,S=s)，D=P(G0,Y2=0,S=s)，N=A+B+C+D。每个格在冻结有限世界严格有正概率，MH用全人口Fraction精确积分；没有人为选阈值判显著或报告真实人的置信区间。作为独立真机制检查另存固定潜在能力k下的人工oracle反应率差向量`p2(G1,k)−p2(G0,k)`，必须严格与MH区分。

## 九人工世界的真实与观察结果

| 冻结世界 | G1焦点题总体通过率 | MH公共优势比G1/G0 | 真固定能力焦点差(k=−1,0,1) |
|---|---:|---:|---|
| BASE_NO_DIF | 1/2 | 1 | (0,0,0) |
| ABILITY_MIX_NO_DIF | 5/9 | 1304723/1069477 | (0,0,0) |
| UNIFORM_FOCAL_HARDER | 31/90 | 19907/38107 | (−2/15,−1/6,−1/6) |
| UNIFORM_FOCAL_EASIER | 59/90 | 38107/19907 | (1/6,1/6,2/15) |
| NONUNIFORM_FOCAL_DISCRIMINATION | 1/2 | 1 | (−2/15,0,2/15) |
| ANCHOR_ITEM1_DRIFT | 1/2 | 156452/149773 | (0,0,0) |
| ANCHOR_ITEM3_DRIFT | 1/2 | 110465081/106549396 | (0,0,0) |
| GLOBAL_REANCHOR_ALIAS | 1/2 | 1 | (0,0,0) |
| COMPOSITION_PLUS_TRUE_DIF | 71/180 | 9229381/14581955 | (−2/15,−1/6,−1/6) |

全部G0焦点题总体通过率=1/2。所有结果均为固定人工联合人口源的精确分数，真实群体解释不适用。

**假阴性的强反例：** 在`NONUNIFORM_FOCAL_DISCRIMINATION`中两群固定题目难度都为0，而G1焦点Y2的能力区分度由1增至2。低人工k=−1时焦点题G1−G0反应率−2/15，k=0时0，高k=1时+2/15，是真实的跨能力交叉DIF。两群焦点题总体通过率恰均为1/2，若先按Y1+Y3锚题总分s分层，G1−G0焦点题条件通过率差分别为`−18/325,0,18/325`，在单一人口MH合并时恰好相互抵消，**MH OR=1**。所以只用一个总体或共同优势比等于1不能宣布该人工项目在每个能力范围都不存在DIF。它不能外推为所有非均匀DIF都不会被MH或其他交互检验检测。

**能力混合导致的统计假阳性：** `ABILITY_MIX_NO_DIF`的每个固定k下焦点题作答机制与G0**完全相同**，真实DIF=0，但G1在高潜在能力k=1权重更大，总体通过率5/9高于1/2，按只有两个锚题Y1+Y3分层的MH OR仍为`1304723/1069477>1`。因为锚题得分只是有限、有噪声的能力代理，不是完美固定真实k，分层后剩余能力混杂，不能将MH偏离1独立判断为真焦点题跨群差异。

**锚题污染导致的假阳性：** `ANCHOR_ITEM1_DRIFT`或`ANCHOR_ITEM3_DRIFT`中焦点Y2在每个能力水平仍完全相同，且两群总体焦点题通过率同为1/2，但一题锚项目在G1变难使同锚分层的实际能力构成不同，MH OR分别偏离1至`156452/149773`和`110465081/106549396`。这进一步强调**只有提供稳定锚题或可辩护的匹配机制，才能把匹配后的群体差异解释为焦点项目DIF证据**。

**真实DIF与混合并存：** G1潜在能力组成改变与真焦点题变难可同时存在，`COMPOSITION_PLUS_TRUE_DIF`里尽管G1焦点总体率由1/2降至71/180，对每个k的真实反应率差必须另行比较，不可仅依边际观测率判断真能力交互与测验内容偏差。

**项目坐标原点不能直接当作偏差：** `GLOBAL_REANCHOR_ALIAS`中G1的潜在θ数值与全部三个题目难度一起增加1，所有k、G、反应模式的实际条件概率与BASE_NO_DIF严格相同，整个观察完整联合每一格一样；裸数值参数变更只是未锚定量尺原点重标定，不是实际同一能力量尺下的真项目差异。计算机模型输出了潜在θ的数值以便人工审查，观察MH绝不借用此隐藏源。

## 失败重跑、最终CI和永久原来源

[完整原生Python Fraction源码](r235_exact_differential_item_functioning.py) · [432条完整人工IRI响应原来源CSV](R235_ALL_432_ORIGINAL_DIF_ITEM_RESPONSE_SOURCES.csv) · [九世界观察率/MH及oracle真DIF结果](R235_EXACT_RESULTS.json) · [机器SHA收据](R235_FINAL_MACHINE_ACCEPTANCE.json)。

初次[GitHub Actions run39882331741](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39882331741)两Python作业均失败，归档job被skipped。实际日志`Ran 77 tests`，`FAILED (errors=35)`，共因实现时部分函数误引用了未定义的零常量`Z`，而全文件正确声明的Fraction常量是`ZERO`。严格保持冻结九世界、源机率、结果评分公式不变，只将全部错误独立引用由`Z`修正为已定义`ZERO`；公开修复提交[b05febb9](https://github.com/edwardsage419/Psychohistory-Research/commit/b05febb9e9fcf41915f8b72ee26db95b282bb865)。失败run及原始日志完整留痕，不误计为科研验收。

修复后[最终CI run39882474328](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39882474328)总体completed/success，三个作业均completed/success，真实Python3.11与3.12独立job分别`Ran 77 tests`与`OK`，**154次实际测试执行通过**。第三归档作业真实日志输出`R235_ALL_432_DIF_SOURCES_AND_EXACT_MH_FALSE_POSITIVE_NEGATIVE_BOUNDS_VERIFIED`，逐48来源概率归一、9世界源完整、oracle固定能力差、MH方向与精确数值、完整观察等价及SHA256全部核验并永久写入main。机器人全原来源归档提交[bb940f7a](https://github.com/edwardsage419/Psychohistory-Research/commit/bb940f7a327b37e55dd514892ac597014e02c632)。

原来源CSV SHA256 `b0f95b32b71c4fe10002080db798a9b5274b73760b76e66cdf17e4426e56b87b`；九世界完整结果SHA256 `29442c0e338e15c0a62814288282a06dbaad6320337878a3fe7d622e1fb627e8`。

结论局限于有限人工E1，不构成对现实任何人口群体、教育公平性、实际偏误或跨时代项目效度的判断。真实人的实验/历史E2/E3皆新增0；R073/PESEN v0.1冻结。下一原239目录**10-010 Survey Response Bias Models（R236）**，继续先全部R，再统一归纳分类，最后熔炼。
