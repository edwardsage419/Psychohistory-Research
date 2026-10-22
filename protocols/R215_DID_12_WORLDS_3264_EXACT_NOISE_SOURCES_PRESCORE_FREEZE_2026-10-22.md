# R215 双重差分（真实239目录09-006）：12人工两期面板、3264条原完整噪声来源、平行趋势与不可区分共同冲击反例，评分前冻结

日期2026-10-22 Asia/Taipei。真实原239模型目录 **09-006 Difference in Differences（P1）**，研究编号R215，状态 **PRESCORE_FROZEN_E1_ARTIFICIAL_TWO_PERIOD_DID**。

## 原始研究与范围
Abadie (2005), [Semiparametric Difference-in-Differences Estimators](https://doi.org/10.1111/0034-6527.00321), Review of Economic Studies 72(1):1–19，指出识别平均处理效应的反事实平行趋势要求。Bertrand, Duflo and Mullainathan (2004), [How Much Should We Trust Differences-In-Differences Estimates?](https://doi.org/10.1162/003355304772839588), QJE 119(1):249–275，讨论序列相关下常见DiD推断失效；本研究**不复现**论文的真实工作场景、原数据、估计器渐近性质或标准误方法。只对**固定两组×两期、完整四个同一人工单位**进行有限来源精确数学审计。

## 完整生成源与人工世界
固定控制组C={0,1}、处理组T={2,3}；t=0（政策实施前）、t=1（政策实施后）。只在t=1对处理组两单位实施政策，其他单位从不直接被该政策处理，保留四个人各期完整面板。

冻结人工潜在无政策结果Y0_i,t=`b_i + q_t + trend_i*t + shock_i,t`，b、trend、共同冲击q以及附加的有意错配机制由下面12世界预先指定。人工真因果目标`ATT=(tau_2+tau_3)/2`，指若保持其他并发环境相同，改变处理组个人政策D从0到1给t=1的**直接政策增量**tau。观察结果Yobs可含额外**与政策同期但独立于政策**的处理组同时冲击post_cointervention、对照组同伴溢出post_control_spillover，以及处理组t=0已存在的政策预期效应pre_anticipation。它们均**不被算作**政策本身真ATT。对每来源同时保存没有目标政策的潜在结果Y0、政策处理后的Y1（只有t1处理组）和实际观察8个结果，明确oracle和估计器权限。

初始基线向量b默认(0,1,2,3)；个体自然趋势向量默认(1,1,1,1)，共同t=1冲击默认0；其他偏离由世界明确指定。12世界如下：
1 VALID_CONSTANT_TWO: tau=(2,2)；
2 VALID_LEVEL_GAP: b=(0,1,10,11)，tau=(2,2)；
3 VALID_COMMON_SHOCK: q_post=5，tau=(2,2)；
4 VALID_HETEROGENEOUS: tau=(1,3)；
5 VALID_NULL: tau=(0,0)；
6 VALID_NEGATIVE: tau=(−2,−2)；
7 NONPARALLEL_TREATED_UP: treated natural trend 3，control 1，tau=(2,2)；
8 NONPARALLEL_TREATED_DOWN: treated natural trend 0，control 1，tau=(2,2)；
9 CONTROL_SPILLOVER: control post outcomes receive additional +1 not attributable to each control's direct policy exposure; tau=(2,2)；
10 ANTICIPATION: treated pre outcomes receive policy anticipatory +1, tau=(2,2)；
11 SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL: tau=(0,0) and treated post outcomes receive independent coincident +2. **这与世界1在全部8真实观察条件均值与相同噪声来源逐源完全同观察分布，真政策ATT却分别0/2**；
12 HETEROGENEOUS_TRENDS_BALANCED: natural trends=(0,2,0,2)，treated、control组均值趋势都1，tau=(2,2)，以明确DiD只要求**组均值**反事实平行，不要求每个个体趋势相同。

两个预冻噪声方案：
A **CELL_INDEPENDENT**：每个四人×两期共8个原单位时期噪声ε_i,t独立±1等概率。完整`2^8=256`种真实原噪声向量，单条原条件概率1/256。
B **UNIT_PERSISTENT**：每单位有一个±1噪声ε_i，完全同值施加于该人的t=0、t=1，四个独立单位共`2^4=16`原来源，单条原条件概率1/16。两方案均有单位与两期的同一来源，比较时间相关如何影响DiD的真正误差方差；**并非**声称估计了 Bertrand等文章中的任意大样本聚类稳健标准误。12世界×(256+16)=**3264条完整原来源记录**，24个世界×噪声型的精确评价单元。每世界每噪声方案概率和为1；所有完整原噪声、全部潜在结果、实际观察8值与真ATT保留进原CSV。

## 三种事前固定估计/评估
- **DiD**：`[mean_T(Y1obs−Y0obs)]−[mean_C(Y1obs−Y0obs)]`，只用8个实际Yobs，控制与处理都各两人工单位完整追踪，不从真潜在结果计算估计器；等价独立第二路`(treated_post−treated_pre)−(control_post−control_pre)`逐Fraction核验。
- **POST_ONLY**：处理组t1观察均值减控制组t1均值，只用4个实际t1值，衡量基线群差的偏差与噪声方差，不应推断它一定比DiD弱。
- **PRETEND_ATT_FROM_KNOWN_STRUCTURES_ORACLE**：真源政策tau平均，作为审计目标/有全反事实权限的先验上界，并不是现实可从8观测直接估计的第三可行估计器。

对每个世界×噪声方案，完整原来源等权算DiD与POST_ONLY的期望、真ATT偏差、均方误差MSE、方差，并逐Fraction验证`MSE=Bias²+Var`。锁定解析噪声方差：单位期独立±1时DiD=2，POST_ONLY=1；单位内持久±1时DiD=0，POST_ONLY=1，且12世界全部同一噪声机制下可独立验证。完整报告世界1 vs 11观察分布逐原噪声记录一致但ATT不同；非平行趋势、政策预期、并发外部干扰三种无效推断分别留存。

不能从仅一个前期和一个后期检验**未处理反事实趋势**真实满足平行趋势；真实潜在Y0只对人工审计oracle可知，不能作为任何现实DiD估计器可观察的信息。世界11同观察表而不同政策效果的非识别，是两期数据缺附加结构假设时的真实人工反例；不要声称两世界的全部结构方程或干预分布都一致。

## 成功门槛与研究顺序
纯Python标准库Fraction、≥30测试、双Python3.11和3.12测试job、第三完整生成12世界×2噪声方案=24世界结果JSON、**3264原完整噪声来源CSV**、两路计算与原真实SHA验证并永久写回main。仅三作业success、真原来源确实入库、科研报告与事后机读验收完成，才标为**CLOSED_BOUNDED_E1_ARTIFICIAL_TWO_PERIOD_DID**。新增真人E2=0、历史E3=0；R073、PESEN v0.1保持冻结。下一原目录需从239JSON核验真实09-007条目，拟R216。维持所有R主线完毕后分类、最后熔炼。
