# R229 Rasch 模型：条件似然、题目对比、测量连接性与八个人工完全有限机制

日期：2026-10-23（Asia/Taipei）。真实原始239目录条目 **10-003 Rasch Model（P2）**。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RASCH_CONDITIONAL_LIKELIHOOD**。全部证据限定为八个人工概率机制，未拟合任何真人测验、文本或真实历史E2/E3资料。

## 一手文献、事前冻结与研究范围

Rasch (1960), *Probabilistic Models for Some Intelligence and Attainment Tests*, 原出版记录 [Danish Institute 1960](https://books.google.com/books/about/Probabilistic_Models_for_Some_Intelligen.html?id=XnlevwEACAAJ) 与[原1960年前言](https://www.rasch.org/memo63.htm)；Andersen (1970), *Asymptotic Properties of Conditional Maximum-Likelihood Estimators*, JRSS B 32(2):283–301, DOI [10.1111/j.2517-6161.1970.tb00842.x](https://doi.org/10.1111/j.2517-6161.1970.tb00842.x)。后一原论文出版社摘要明确涉及用充分统计量消除附带参数的条件最大似然及正则条件下的渐近性质。本研究验证该思想在固定三人三题结构中的有限精确公式，**没有实施一般CML参数极大化、模型比较检验的频率学推断、置信区间或1970年原作者的渐近证明**。

[计算前冻结协议](../../protocols/R229_RASCH_8_WORLDS_4096_FULL_RESPONSE_MATRICES_PRESCORE_FREEZE_2026-10-23.md)以独立提交[93dd2e7f](https://github.com/edwardsage419/Psychohistory-Research/commit/93dd2e7f3dfd76342c3deaff2487edc676160a91)先于Python程序及所有结果入库，指定八个模型、三人三题、真实人工答案、可见mask、零概率保留、条件赔率及完整归档关口。

## 完整来源与真正可观察界限

每世界三人×三题二元回答，共2⁹=512种结构原矩阵，八世界4096条。每条保存九个真正潜在答题位的完整结构状态及其由Bernoulli结构方程计算的分数概率、真正可见的三人三题答题子矩阵、mask、可观察个人总分、零概率标记。八世界中七个世界各512条正概率原来源，第八个复制机制仅64条正概率来源、448条零概率结构矩阵；总计**3648正概率人工结构来源与448零概率矩阵**。所有原矩阵均是完整**概率可能性**，不能误称为4096个受试者或4096次独立真人测验。

DISCONNECTED_ITEM3中前两人仅作答题0、1，第三人仅作答题2，9个结构回答格中每原来源实际只观测5格、不可观察4格，因此128? 注：全部可见观察矩阵仅有2⁵=32个互斥正概率配置。计算观察联合分布时已将不可观察的原潜在回答以概率加总，不将被遮挡潜在值偷用于条件推断。其余全题世界每矩阵隐藏回答0格。

## 有限条件似然与八世界精确结论

对于等区分度、各题给定能力条件独立的Rasch模型，设个人能力θ_i，题目难度b_j，精确底数2 logit响应概率\(2^{θ_i-b_j}/(1+2^{θ_i-b_j})\)。固定个人实际受测题目的总分r，条件回答模式概率在所有合法模式中正比于\(2^{-\sum_j b_j y_j}\)。θ_i与每个个人的归一化项完全抵消。这允许识别具有充分共同施测支持的题目**难度对比**，不识别题目与能力的共同绝对原点。

| 人工机制 | P(100)/P(010) 三人顺序 | P(010)/P(001) 三人顺序 | 机制诊断 |
|---|---|---|---|
| BASE_RASCH | 2,2,2 | 2,2,2 | 标准三题共同难度 |
| SHIFT_ALIAS | 2,2,2 | 2,2,2 | 全部能力与难度同移+1，完整观察等价 |
| ABILITY_SPREAD_RASCH | 2,2,2 | 2,2,2 | 能力变异但条件赔率不变 |
| ITEM_STRETCH_RASCH | 4,4,4 | 4,4,4 | 真实题目难度对比加倍 |
| TWO_PARAMETER_NONRASCH | 4,2,1 | 1,2,4 | 不同区分度造成个人间变化 |
| LOCAL_DEPENDENT_CLONE | 0,0,0 | 未定义 | 第三题复制第一题，违反条件独立 |
| ITEM_DIF_PERSON3 | 2,2,2 | 2,2,4 | 第三人对题2的项目难度不同 |
| DISCONNECTED_ITEM3 | 2,2,未定义 | 未定义 | 题2为单独子图，缺少共同施测对比 |

表中条件赔率本来定义在观察总分为1时，分子分母模式必须在对应真实测量设计内具有正支持；若没有共同施测或分母概率为0，明确记为NULL。LOCAL_DEPENDENT_CLONE中第三项直接等于第一项，只有每个人4个单次模式可能出现，跨三人64个正质量矩阵；在总分r=1条件下只有010一个模式有正质量，导致`P(100)/P(010)=0`，另一赔率分母000? 对应001为0，故无定义。实际复制结构并不能通过独立Rasch三题概率正质量公式解释。条件答题模式对能力的表面不变不足以证明条件独立性成立。

**完整观察等价和条件信息损失：** BASE_RASCH与SHIFT_ALIAS每个完整原三人×三题回答矩阵的可见概率严格相同，原点无法从数据本身固定；ABILITY_SPREAD_RASCH的未条件联合观察分布与BASE不同，但对每名受试者固定总分后的模式条件概率完全相同。这明确展示条件化牺牲了用于个人能力分布的那一部分总分信息；不能把模型的附带能力参数消除当作已经估计真实个人能力。

**项目连接性：** DISCONNECTED_ITEM3第三人只完成题2，没有任何受试者共同完成题2与题0/题1；在个人总分被条件化后，第三人只有一个实测项目，每个可能观测行分数r可对应恰好一个模式、条件概率为1。改变题2难度不改变这名人工受试者的任何已观察行分数条件分布，因此条件似然不能把题2标定到题0/题1尺度。虽然真实概率模型生成的未条件题2结果随难度变化，依赖未知第三人能力的绝对水平仍造成相对标定缺口；这里不声称其他外部固定能力锚定措施也必然失败。

**DIF：** ITEM_DIF_PERSON3的前两人共有难度向量、第三人题2难度+1。在每个人自己那套难度下，各人条件模式仍满足等斜率Rasch计算；但不存在一套共同难度同时满足所有三人的后两题条件赔率，故“共同题目不变性”作为跨人假设被有限真机制直接否证。

完整512原矩阵加权求每个人的可观察行模式边际，与独立从各人最多8种当地模式乘积公式完全一致，再逐分数将权重归一，Rasch合法世界的结果又与独立条件赔率公式严格逐格相等。

## CI、机器来源和纠错审计

1. 原生Python [r229_exact_rasch_conditional.py](r229_exact_rasch_conditional.py)；[完整4096原矩阵CSV](R229_ALL_4096_ORIGINAL_3X3_MATRIX_SOURCES.csv)；[八世界Fraction精确结果JSON](R229_EXACT_RESULTS.json)；[最终SHA机器验收](R229_FINAL_MACHINE_ACCEPTANCE.json)。
2. 首轮[GitHub Actions 39823447220](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39823447220)两个Python job以及原来源归档job均success，但原结果汇总错误地用每人的全部9个矩阵位数减去该人实际3题作答数，导致完全作答模型误报18个隐藏格；同时把零概率的复制结构矩阵误记为正概率观察支持。其原结果提交[47f2b4d2](https://github.com/edwardsage419/Psychohistory-Research/commit/47f2b4d26d9970befb66091442729cc8fd7405b8)保留追溯。
3. 仅修改观察支持的正概率计数和每人3题的mask缺失格数，新增三个针对完整题单、克隆零支持与断开设计的回归测试，固定机制、条件概率、模型参数和原4096源概率保持不变。公开[修复提交23d361f6](https://github.com/edwardsage419/Psychohistory-Research/commit/23d361f65711abeff8ce51505c48268e7f587ff1)。
4. 修复后最终[GitHub Actions run39823620309](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39823620309) run总体completed/success、三项job均completed/success，真实Python3.11和3.12日志各`Ran 71 tests`、`OK`，合计**142项独立环境测试执行成功**；第三完整原资料验证关口及永久归档成功。最终机器人结果提交[e0cd73cf](https://github.com/edwardsage419/Psychohistory-Research/commit/e0cd73cf5fe3f69af8a65ae30414d46a22548b22)。
5. 最终原矩阵CSV SHA256 `1fe05f59bfada0c7b36bb535a46d0d61820245244df66432651ca6469fdad210`；最终结果JSON `ae93ede2c190e4f5286396f421e0cf32286d4eb3635fc5324e306644f906c2a1`。全原源概率在数据与机器凭证中单独留存，未更改先行冻结协议。

本研究仅人工有限E1，新增真人E2=0、真实历史E3=0，无实际学校测验、跨文化项目公平性经验评价、信度置信区间、样本反应缺失机制或任何CML真实参数拟合。R073和PESEN v0.1冻结。原目录下一条 `10-004 Exploratory Factor Analysis`（R230），应继续先完成既定R再统一分类最后熔炼。
