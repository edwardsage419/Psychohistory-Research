# R312 科学报告：Deffuant–Weisbuch 异步双人意见更新的精确有限源实验

日期：2026-10-23（Asia/Taipei）。原239候选**04-013 Deffuant Weisbuch Model** P1。状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_R312_PAIRWISE_CONDITIONAL_UPDATE**。只验证项目预冻结的人工意见轨迹数值，非原作者全规模随机过程复现、真人社会影响或历史预测。

## 1. 一手来源与相邻模型严格分开

Deffuant、Neau、Amblard、Weisbuch (2000), *Mixing beliefs among interacting agents*, *Advances in Complex Systems*，官方论文 https://doi.org/10.1142/S0219525900000078 ：提出当随机相遇的两人意见足够接近时，二者会依据混合系数改变意见；研究长期共识/分群趋势。Lorenz (2007), *Continuous Opinion Dynamics Under Bounded Confidence: A Survey*, https://doi.org/10.1142/S0129183107011789 ，综述Deffuant随机两两和Hegselmann–Krause同步平均化机制的不同。

已完成的[R311](../R311/R311_SCIENTIFIC_REPORT_2026-10-23.md)检验静态置信网络邻接与连通性，不计算任何意见更新。早期[R066](../R066/R066_FINAL_ACCEPTANCE_STATUS.json)涉及HK同步阈值平均化及真人16村内部留出条件预测，不是Deffuant两人更新的原作者数据。当前R312重新单独冻结Deffuant**恰好一个随机选定相遇对**的有限过程，不会伪装长期会聚、可识别的人类学习系数、真实社会边网络或独立E2。

## 2. 事前冻结的完整人工来源

[预先冻结的精确协议](../../protocols/R312_DEFFUANT_RANDOM_DYAD_ONE_STEP_1152_PERSON_SOURCES_PRESCORE_FREEZE_2026-10-23.md)在[commit2c8c9bfd](https://github.com/edwardsage419/Psychohistory-Research/commit/2c8c9bfd15a27574f0fffb02517eb5893aedfee9)早于代码/计算结果固定。

八个独立编号的四人工意见模式A–H，包括全0、全1、异质和重复观点组合。每种模式对阈值ε∈{0,1/2,1}，对称折中步长μ∈{1/4,1/2}，形成**8×3×2=48个人工参数世界**；一轮从所有六个不同节点无序配对中以人为固定均匀概率1/6选择其一，形成**48×6=288种完整配对结果**。每种结果保留全部四位人工代理更新前/更新后意见状态、置信可达性、被选两人原始和更新后距离、全体均值与无条件下一期预期意见，形成**288×4=1152条完整原source**；这些“人”只是四个虚拟agent，非1152真人，也不是1152个独立受试者。

只有被选(i,j)且|xi−xj|≤ε才双人同时折中：xi'=xi+μ(xj−xi)，xj'=xj+μ(xi−xj)，另外两人不改变。若超过阈值全部不变。每种配对概率是1/6，完整下一期期望从六种可能的**状态结果**精确取均值。每步都保存总意见和，全部使用Fraction而不经过浮点。

## 3. 数学机制结果与负例

固定A–H中的F=(0,1/2,1,1)，ε=1、μ=1/2：
- 首先选(0,1)：一步后(1/4,1/4,1,1)；
- 只选(1,2)：一步后(0,3/4,3/4,1)；
- **连续先(0,1)再(1,2)**：最后(1/4,5/8,5/8,1)；
- **连续先(1,2)再(0,1)**：最后(3/8,3/8,3/4,1)。

同一初始状态、阈值和折中程度，仅改变谁先相遇，就得到不同人工两步结果。这是**异步次序的重要性**；与HK同步按所有邻居同时平均的算法机制不等价。

另对于C=(0,0,1/2,1)，ε=1/2、μ=1/2，选(1,2)正好在阈值边界上，因此二者从0和1/2更新为1/4、1/4；选择(0,3)差距1超过阈值，**四人状态全部保持不变**。ε=0时只能与相同意见者相遇，相遇即使被允许也不改变观点；全相同意见模式无论接触对和阈值均保持不变。

每个合格接触对两端的意见总和严格不变（其余两位不变），所以全组平均在每一个配对事件、以及六配对均匀随机混合后下一期**期望**中都守恒。合格配对的意见差距缩小因子为|1−2μ|，μ=1/2时两人直接成为中点。注意“平均守恒”不等于群体方差一定按某个特定速率缩小，也不证明长期共识或真实社会群体的结果。

## 4. 源级独立校验、CI与审计边界

[主原生Fraction程序](r312_exact_deffuant_dyadic_update.py)实现完整48世界与288配对，**3469个实际unit tests**分别在Python3.11与3.12成功。[不导入主程序的独立重算审计](../catalogue_audit/independent_r312_source_audit.py)从独立中点及半差公式 x'i=(xi+xj)/2 + (1−2μ)(xi−xj)/2、x'j=(xi+xj)/2 − (1−2μ)(xi−xj)/2 重新计算全部**1152条原source**，直接复验288种事件、48个预期向量、均值守恒、折中距离及两个事件的顺序敏感性，包含**15项篡改/来源完整性测试**。

所有[1152条人工个体源CSV](R312_ALL_1152_ORIGINAL_DEFFUANT_PERSON_SOURCE_ROWS.csv)、[48世界288配对全结果JSON](R312_EXACT_DEFFUANT_PAIR_EVENT_RESULTS.json)、[原source与结果SHA256收据](R312_MACHINE_RECEIPT.json)已由实际[GitHub Actions run39957585074](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39957585074)完整3/3 completed/success，第三独立作业永久归档[commit53052edb](https://github.com/edwardsage419/Psychohistory-Research/commit/53052edbe7a1f87a476f7c9297db5a961095667d)。源CSV SHA256 `0092c8ee1db8404790dbf4f241ec8074e09d3509e5ec3ea269a6daf9f423bd21`，结果JSON SHA256 `d54f77acfbb108009da5e55a97ef33706ba6260d6efc7cdcf3afc38676312fc6`。

**科学结论界限**：仅固定人工算式和source完整性E1；没有Deffuant作者现场真人实验数据、随机人口图、人类现实接触频率、长期稳态、估计的人类μ/ε、E2或历史E3。R066的既有E2内部村庄留出不在R312重用。R073/PESEN v0.1保持冻结；原239完整模型系列尚需继续。
