# R244 马尔可夫随机过程：九个二态三步人工世界、1152完整原来源与隐藏类别混合导致的非Markov性

日期2026-10-23 Asia/Taipei。原239目录真实`11-004 Markov Stochastic Processes`（P1）。正式科研状态 `CLOSED_BOUNDED_E1_EXACT_FINITE_MARKOV_HIDDEN_MIXTURE`。所有世界仅人工二态、三步、七二元外生源的精确概率空间，无真实人类行为数据、人口转移率拟合、长历史资料或跨期历史预测。

## 原始方法、证据范围与冻结协议

MIT OCW 18.366 [*Lecture 13: Discrete and Continuous Stochastic Processes*](https://www.ocw.mit.edu/courses/18-366-random-walks-and-diffusion-fall-2006/d53e40fbfc776b5d616fa87b424731ce_lec13.pdf)，介绍离散状态条件转移、Chapman–Kolmogorov关联与连续极限；Fortini, Ladelli, Petris & Regazzini (2002), [*On mixtures of distributions of Markov chains*](https://doi.org/10.1016/S0304-4149(02)00093-5), *Stochastic Processes and their Applications* 100:147–165，研究混合Markov链分布及相关部分可交换性条件。本R既未使用其真实资料，也未复现其无限序列表征定理，结论只针对下述有限九机制。

[计算之前冻结协议](../../protocols/R244_MARKOV_9_WORLDS_1152_FULL_SEVEN_BIT_PATH_ATOMS_PRESCORE_FREEZE_2026-10-23.md)独立先提交[75ce71f7](https://github.com/edwardsage419/Psychohistory-Research/commit/75ce71f7ca6281f5d14fbfe46a805cbdb3a8e6a3)，然后才提交原生代码、CI以及算出结果。预冻结明确了源全集、两条独立概率公式、Markov缺陷定义、不可观察的隐藏类型与完整路径观察别名，之后没有更换机制及评分。

## 原来源和两个数学路线

每个人工world有隐藏稳定类别`U∈{0,1}`及每步两个公平独立随机bit，三步共六个R，全部是7独立fair原外生位。每world完整2⁷=128个原结构来源、质量各1/128，九world合计**1152条完整原源**。实际观察全部四个时间状态为`(Y0=0,Y1,Y2,Y3)`；另源CSV分开记录U、三个原随机两位对，以及Oracle真实隐藏`H0...H3`，实际路径统计绝不读取这些隐藏oracle量。

第一算法逐七位外生源，经两位0..3等概率阈值实现每一步stay概率1/4、1/2、3/4或1，并边缘化得完整8个可能四态观察路径概率。第二独立算法**不读取source原行和模拟函数**，直接对每个可能`(0,y1,y2,y3)`用`Π_{t=1}^3P_t(y_t|y_{t-1},U)`求路径概率；若有隐藏类别则`(1/2)ΠP^U0+(1/2)ΠP^U1`，而时间变化模型用其各期独立核。所有九world完整八种可见路径联合逐格严格Fraction一致，原完整概率均为1。对观测路径正质量的条件事件计算`P(Y3=1|Y2,Y1)`与`P(Y3=1|Y2)`；**Markov缺陷**定义为支持内这两者差的最大绝对值。没有正支持的条件概率标作null，不会强填0。时间齐次链另用2×2核的`P²`及`P³`矩阵乘积独立核验Chapman–Kolmogorov与实际2、3步边际；时间非齐次链不被错误强迫用单一P描述。

## 九个人工机制的完整观察结果

| 冻结机制 | Markov条件缺陷 | 可见四态路径支持数 | 机制含义 |
|---|---:|---:|---|
| IID_FAIR | 0 | 8 | 时间齐次一阶Markov，独立公平状态转移 |
| PERSISTENT_3OF4 | 0 | 8 | 3/4 stay概率的时间齐次Markov |
| ANTIPERSISTENT_1OF4 | 0 | 8 | 1/4 stay概率的时间齐次Markov |
| ABSORB_ONE | 0 | 4 | 1态吸收，正支持内满足Markov |
| TIME_ALTERNATING_RATE | 0 | 8 | 每步条件Markov但**非时间齐次** |
| LATENT_RATE_MIXTURE | 1/5 | 8 | 个体隐藏U使纯观察Y有额外历史依赖 |
| STATIC_HIDDEN_SENSOR_ALIAS | 0 | 8 | 隐藏真实H静止，观察传感器有Markov波动 |
| COMPLEMENT_HIDDEN_COORDINATE_ALIAS | 0 | 8 | 仅隐藏标签互补的Markov状态表示 |
| FIXED_SWITCH_POLICY | 1/2 | 2 | 隐藏个体策略导致极端历史依赖 |

**隐含类别混合后可见序列不一定Markov。** LATENT_RATE_MIXTURE中人工U=0的人每一步stay概率3/4，U=1的人每步stay概率1/4。每个个体的`(Y,U)`扩展状态满足齐次Markov，但观察者无法测量U，只记录Y。对于相同当前`Y2=0`：
[
P(Y3=0\mid Y2=0,Y1=0)=7/10,qquad
P(Y3=0\mid Y2=0,Y1=1)=3/10,
]
而
[
P(Y3=0\mid Y2=0)=1/2.
]
这三个数是完整128来源对隐藏U条件概率的精确积分；历史Y1有信息，是因为两次stay或两次flip改变了人对隐藏U的后验权重。采用本研究的`P(Y3=1|...)`缺陷定义，该world最大差为1/5。因而**不能只因为个体给定完整潜在状态满足Markov，就断言忽略未观察异质性后群体观察序列也满足一阶Markov**。这不是所有混合Markov模型必然失效的普遍定理。

**隐藏固定策略造成更强反例。** FIXED_SWITCH_POLICY中U=0的人保持初始0不动，U=1的人每步正负状态翻转；其唯一可见轨道0000与0101各概率1/2。当Y2=0时，Y1=0导致Y3=0概率1，Y1=1则此概率0；仅看Y2=0，下一步Y3=0概率仍1/2。观察Markov缺陷1/2。第一步状态边际与IID_FAIR完全一样，但完整后续路径支持数从IID的8降为2，因此**一次转移分布相同绝不等于同一个随机过程的联合路径法则相同**。

**时间非齐次与非Markov不可混为一谈。** TIME_ALTERNATING_RATE中第一和第三步stay概率3/4，第二步1/4；真实`P(Y1=0|Y0=0)=3/4`，但`P(Y2=0|Y1=0)=1/4`，明确无法用一个固定齐次2×2转移矩阵同时解释全部时点。然而给定当前Y2及时间后，过去Y1不改变下一步条件分布，观测Markov缺陷仍0。故测试Markov性与测试时间齐次性是不同问题。

**观测过程性质不证明隐藏物理动态：** PERSISTENT_3OF4、STATIC_HIDDEN_SENSOR_ALIAS、COMPLEMENT_HIDDEN_COORDINATE_ALIAS三world对全部128个相同原七bit来源逐条产生完全相同的观察`Y0...Y3`；第一世界的真实隐藏H按3/4 stay概率改变，第二世界真实隐藏H0...H3永远0、实际随机转移仅存在于观测仪器或编码器，第三世界隐藏坐标取`1−Y`再转回观察Y，仅仅重标记状态类别。虽然可见过程完全遵守Markov性质，不能不经独立传感器验证直接确认实际心理或制度隐藏状态就是这个可见Markov变量。

**吸收态中的不可定义条件不能伪造。** ABSORB_ONE的Y1=1,Y2=0路径在本冻结世界严格概率0，故`P(Y3=0|Y1=1,Y2=0)`没有定义、JSON保留null；它不是一个观测到的负例概率0。这个细节保障对支持不足和逻辑未见配置的证据限制。

## 真实CI、机器SHA和研究验收

[原生Fraction Python源码](r244_exact_markov_hidden_mixture.py) · [1152完整七bit人工原来源CSV](R244_ALL_1152_ORIGINAL_BINARY_MARKOV_SOURCE_PATHS.csv) · [九world全部8格路径、条件缺陷和oracle结果](R244_EXACT_RESULTS.json) · [SHA256原源验收凭证](R244_FINAL_MACHINE_ACCEPTANCE.json)。

[CI run39889712674](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889712674)总体completed/success，三个job均completed/success；Python3.11/3.12日志各`Ran 83 tests`、`OK`，合计**166次真实双版本测试通过**。第三归档作业独立验证每world128唯一原七bit来源、源质量归一、完整四时点概率、时间齐次模型Chapman–Kolmogorov二/三步传播、所有九模型的Markov缺陷、两个隐藏条件数7/10和3/10及固定策略反例、三个完全观察别名与文件SHA，真实日志输出`R244_ALL_1152_MARKOV_SOURCE_PATHS_AND_HIDDEN_MIXTURE_CONDITIONAL_INDEPENDENCE_VERIFIED`。原CSV/结果JSON/机器收据已经机器人永久提交main，[90765065](https://github.com/edwardsage419/Psychohistory-Research/commit/907650659e92e8abff7a07b3eeb2b2e873f67938)。

原CSV SHA256 `2b910986ddfb4ac7e875e1bff64d2ce42c4bf19de29c31f1b7f28ca2beda0981`；九world结果JSON SHA256 `2d3b25949e328ef2691891cee111e1d1aecdbd96ddc8296d38458209a54d4d9f`。

研究状态仅`CLOSED_BOUNDED_E1_EXACT_FINITE_MARKOV_HIDDEN_MIXTURE`，不提供现实个体、群体制度、历史事件的Markov统计拟合或条件充分性识别。新真人E2/真实历史E3皆0，R073及PESEN v0.1冻结。下一原239目录条目须另从catalogue核验，编号拟R245。继续先完成全部原R研究，之后统一归纳分类，最后熔炼。
