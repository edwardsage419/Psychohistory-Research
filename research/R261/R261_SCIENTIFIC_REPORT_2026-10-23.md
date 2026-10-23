# R261 平均场近似：九人工二行动者两时格、9216完整原10bit来源及有限人口均值偏差/共同随机性

日期2026-10-23（Asia/Taipei）。原239目录`11-021 Mean Field Approximation`（P1）；正式科研资格`CLOSED_BOUNDED_E1_TWO_AGENT_TWO_STEP_MEAN_FIELD_VS_FINITE_MARKOV`。**只研究固定N=2的有限随机人工动力与确定性平均场近似，不证明N→∞的传播混沌极限、实际群体行为或历史传播预测。**新增真人E2=0、历史E3=0；R073与PESEN v0.1保持冻结。

## 一手来源与研究对象
H. P. McKean Jr (1966), [*A class of Markov processes associated with nonlinear parabolic equations*, PNAS 56(6):1907–1911](https://doi.org/10.1073/pnas.56.6.1907)，是与非线性群体分布依赖随机过程相关的早期理论文献之一。本项只检验一个**具体、两人、离散两时步**的代理，避免从有限N精确算例冒称McKean–Vlasov渐近分布或无限人群相关性消失。九world原随机结构和数学分布/方差目标已在代码评分前冻结，[协议](../../protocols/R261_MEAN_FIELD_9_TWO_AGENT_9216_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，提交[32ed7974](https://github.com/edwardsage419/Psychohistory-Research/commit/32ed797483cd47496cf83a9d24d251b9aac3f15b)。

## 完整十bit随机源与有限计数状态的独立数学路线

每world最初两个个体各一独立公平bit，两个时间格t=0,1每格两个人各两独立公平bit作r∈{0,1,2,3}，因此每world2^10=**1024完整外生原source**、每source设计概率1/1024，九world共**9216原结构source**。每步先根据当期两人可见行为求群体份额`M_t=(x_{t,0}+x_{t,1})/2∈{0,1/2,1}`，然后按冻结概率q(M_t)确定下一期各人状态，原10bit逐agent源位和两时点真实/报告状态均完整保存。外生source不是9216位不同真实参与者，且同一个外生原源的两时点明显依赖，不可充作可独立重复观察的实验人数。若给定初态人数K0=0或2，则各256原bit来源、条件概率1/256；K0=1则分别有初始01和10两种×256随机位=512原来源、每条条件概率1/512。

前七个world的两个个体给定当前K，均**条件独立**依概率q(K/2)重新抽样。独立第二路线不读取外生原bit、生成器或真实前期状态，按理论严格构造三计数状态K=0,1,2的行随机Markov转移核：
[
T(k,0)=(1-q)^2,quad T(k,1)=2q(1-q),quad T(k,2)=q^2.
]
第8个COMMON_NOISE_NEUTRAL世界让两个个体读**相同原公平两bit**抽样，条件共同随机性导致一个时点之后两人状态完全相同，故真实计数核是`(1−q,0,q)`，不能用前述条件独立二项核。第9个OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR的**公开报告**同样用第8个共同噪声核，却由另一并行隐藏真实个体状态世界执行独立q(m)=m核，表示人为允许一个报告器伪造真实状态。在同一全部10bit原source上，公开两时点的每个人报告行为与第8world**逐source完全相同**，但实际隐藏个人行为可能不同；这个机制别名只有在真实动作未获独立核查的人工设定下成立，不是现实社会欺诈的统计估计。

将T自给定初始K0的point mass连乘两次，得到条件K1、K2完整三态联合边际分布，计算E[M_t|K0]、Var(M_t|K0)、群体同向概率P(K_t∈{0,2}|K0)，再与每个world完整1024源按K0正确加权的直接积分**逐初态、逐时点、逐概率格子Fraction完全一致**。同时，独立确定性平均场近似设`m^MF_{t+1}=q(m^MF_t)`，允许q在整个m∈[0,1]上定义。该数理近似不是有限2人Markov人口的真实随机状态，因此不得忽略有限N非线性Jensen偏差和随机性引起的方差。

## 五组关键精确反例（给定初始K0=1，m0=1/2）

| 人工world | MF预测m1,m2 | 精确有限N平均E M1,E M2 | 有限N方差 Var M1,Var M2 |
|---|---|---|---|
| FINITE_NEUTRAL_IDIOSYNCRATIC，q(m)=m | 1/2,1/2 | 1/2,1/2 | 1/8,3/16 |
| FINITE_CONVEX_SQUARE，q(m)=m² | 1/4,1/16 | 1/4,5/32 | 3/32,99/1024 |
| FINITE_CONCAVE_CONFORMITY，q(m)=2m−m² | 3/4,15/16 | 3/4,27/32 | 3/32,99/1024 |
| COMMON_NOISE_NEUTRAL，q(m)=m | 1/2,1/2 | 1/2,1/2 | 1/4,1/4 |
| OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR，公开报告q(m)=m | 1/2,1/2 | 公开1/2,1/2 | 公开1/4,1/4，真私下第1时点1/8 |

**均值恰好等于确定性近似，不表示行为波动为零。** FINITE_NEUTRAL_IDIOSYNCRATIC使用中性q(m)=m，两期有限人口条件均值都是1/2，恰等于确定性平均场的1/2。但两个原个体在首期从同一原群体比率独立抽样，给定K0=1时K1取0,1,2的概率为(1/4,1/2,1/4)，其经验平均M1的方差为1/8；第二期仍有不可消失的Var(M2)=3/16。若只检验均值就认为平均场可以完美预测具体小群体行为，是错误的解释。第8个共同噪声world不改变条件均值，在初始K0=1时却使首期两人完全同向、Var(M1)=1/4，第二期吸收于两种同向状态Var(M2)=1/4；**条件独立与共同冲击不应在同一二项核里混用**。

**非线性Jensen偏差具有明确方向但有限N证明不等于无限人口证明。** FINITE_CONVEX_SQUARE的初值m0=1/2，首期群体份额分布为M1=0的概率9/16、M1=1/2的概率6/16、M1=1的概率1/16，首期E[M1]=1/4。下一步真实期望`E[q(M1)]=0×9/16+(1/4)×6/16+1×1/16=5/32`；若无误差地把首期均值塞进非线性q，则只得`q(E[M1])=q(1/4)=1/16`，两者相差**+3/32**。对FINITE_CONCAVE_CONFORMITY，首期均值3/4，第二期真实`E[M2]=27/32`，确定性q(3/4)=15/16，两者相差**−3/32**。因此即使全部模型的原噪声参数完全已知，非线性平均场算子也不一般与有限系统概率期望交换。

**阈值与逆反世界需要明示概率映射。** FINITE_CONTRARIAN令q(m)=1−m，虽然其两期中性初值条件均值同样维持1/2且首期/次期方差1/8、3/16，它的相邻时间因果规则与中性世界相反，因此不应以同一两个均值判定微观社会行为相同。INDEPENDENT_HALF令q=1/2不读群体，t1及t2条件经验平均各1/2，方差均1/8；UNANIMOUS_ONLY定义只在m=1时下一期全体为1，K0=1立即全部0；MAJORITY_TIE_UP在m≥1/2时立即全部1。二者可产生没有方差的终端状态，但归因于明确确定性阈值与tie规定，不能说这是现实群体共识形成的经验规律。

## GitHub双版本真实CI与完整原source归档

[原生Fraction人工二人模型/独立3×3计数核程序](r261_exact_finite_meanfield.py) · [九world9216完整十bit原source CSV](R261_ALL_9216_ORIGINAL_TENBIT_MEAN_FIELD_AGENT_SOURCES.csv) · [全部9×3初态×3时点完整概率、有限均值/方差及平均场差JSON](R261_EXACT_RESULTS.json) · [CSV与结果SHA256机器完整性验收](R261_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39898621445](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39898621445)整体completed/success，三个job全部success。Python3.11与3.12实际日志各`Ran 82 tests`、`OK`，合计**164次真实双版本测试通过**。第三独立job直接读取9216全原source，验证每world1024原10bit唯一组合与概率1/1024、个体两时步完整状态与原随机bit阈值独立重构、九world的三态转移矩阵、每world三个初态K0的条件来源质量、全部三时点概率分布逐格与独立Markov T严格Fraction一致、全部中性/共同噪声方差1/8、3/16、1/4和正负3/32非线性偏差、两个公开报告世界逐原source一致且真实隐藏状态可能不同、完整原CSV/JSON SHA。真实日志`R261_ALL_9216_ORIGINAL_AGENT_SOURCE_AND_INDEPENDENT_N2_MEAN_FIELD_BIASES_VERIFIED`、`R261_ALL_9216_ORIGINAL_MEAN_FIELD_SOURCES_PERMANENTLY_ARCHIVED`。完整原CSV、计算JSON和独立SHA机器凭证均机器人永久提交main [a03ac450](https://github.com/edwardsage419/Psychohistory-Research/commit/a03ac450cc4199bffbc2b7dab5837f04ab353e4c)。

原CSV SHA256 `955d74861f431d10f23850af531fe0816c944caeeffed7a162c62cc8a99b4364`；结果JSON SHA256 `24211fc4c7647255e28e7ffadbf6e6d6bce96765360d9793114bd50279fb5789`。

本项科学验收只`CLOSED_BOUNDED_E1_TWO_AGENT_TWO_STEP_MEAN_FIELD_VS_FINITE_MARKOV`：两个体并不是无限大样本，未证明大人口收敛速度、真实社会网络均场近似正确性或群体历史演化。新增E2/E3均0，R073/PESEN v0.1仍冻结，下一原目录11-022 Cellular Automata（拟R262，P1），原R完成后再统一分类、最后模型熔炼。
