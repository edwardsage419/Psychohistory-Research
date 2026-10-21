# R195 马尔可夫链蒙特卡洛：24人工Metropolis–Hastings起点、9288完整精确概率单元、有限64步ESS及96条随机模拟

日期：2026-10-21。原目录P1/08-019 Markov Chain Monte Carlo。验收级别 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MCMC**。全部目标权重和模拟轨迹均系预先定义的三态人工数学对象，新增真人E2、历史E3均为0。

## 一手理论来源、冻结协议及边界

Metropolis, Rosenbluth, Rosenbluth, Teller and Teller (1953), [Equation of State Calculations by Fast Computing Machines](https://doi.org/10.1063/1.1699114), J.Chem.Phys.21:1087–1092，为Metropolis型随机模拟的原始研究。W.K. Hastings (1970), [Monte Carlo Sampling Methods Using Markov Chains and Their Applications](https://doi.org/10.1093/biomet/57.1.97), Biometrika57:97–109，推广到更一般提议和接受拒绝。C.J. Geyer (1992), [Practical Markov Chain Monte Carlo](https://doi.org/10.1214/ss/1177011137), Statistical Science7:473–483，讨论样本相关、Monte Carlo估计方差和混合效率。本项直接核对上述问题在**自造的有限三态MH过程**中的数学机制，不是原始论文作者数据和算法计算的直接复现，也不声称近似高维真实参数后验或严格认证任何实际链已收敛。

[正式计算前冻结协议](../../protocols/R195_MCMC_24_WORLDS_9288_EXACT_CELLS_PRESCORE_FREEZE_2026-10-21.md)先以commit`ed615d692e8e1b342d4f3fecd9fff46cf9527515`永久提交main，早于本轮程序和正式验收结果。固定三态i=0,1,2，四类目标未归一化权重：
* UNIFORM (1,1,1)，真π=(1/3,1/3,1/3)；
* CENTER (1,4,1)，真π=(1/6,2/3,1/6)；
* BIMODAL (4,1,4)，真π=(4/9,1/9,4/9)；
* SKEW (1,2,4)，真π=(1/7,2/7,4/7)。

四真目标×两个对称邻居提议强度q∈{1/8,1/4}×三个单状态启动δ0、δ1、δ2，合计**24个独立定义的人工初始世界**；只有8个不同MH转移矩阵与8套平稳分布。每个世界的0..128每一步完整精确状态分布都归档，**24×129×3=9288个有理数概率单元**，不是9248也不是模拟统计量。另冻结平稳指标f(X)=1{X=2}的连续64状态有限ESS定义，及每初始世界4条真实执行的固定随机种子轨迹，共96条，均先burn64次，再记录2048次移动后的状态。

## 完整目标不变、详细平衡与有限步收敛严格区分

在三态路径0↔1↔2，仅相邻边做对称提议Qij=q，未提议时原地；提议从i到j采用`min(1,wj/wi)`接受，否则保留当前状态。

两条相互独立的Fraction构造逐矩阵分量一致：
1. 从完整对称proposal Q及各边接受/拒绝概率直接形成转移矩阵T；
2. 从任一邻边的对称概率流`q min(w_i,w_j)`除以来源权重w_i构成非对角Tij，再取对角行剩余。

八个T全部行和1、状态间邻边权严格正、对角严格正，精确满足`π_iT_ij=π_jT_ji`和`πT=π`。因此π是平稳分布且链在有限三态路径上不可约、非周期；**这只保证长程极限目标，不等于某一有限步分布已等于π**。每个24起点全部129步直接行向量递推，另在t∈{0,1,2,4,8,16,32,64,128}独立用3×3矩阵重复平方幂验算，全部逐Fraction严格相同。每一步概率非负和1，到目标的总变差TV`=(1/2)Σ|p_t(i)−π_i|`在全部24世界129时间节点中非增加。定义TV≤1/20及≤1/100两个预冻结具体阈值，首次到达时间从完整精确分布计算；若128步未到，则标`NOT_REACHED_BY_128`，不从平稳等式臆测收敛时间。

特别冻结BIMODAL π=(4/9,1/9,4/9)从状态0起的精确阈值：

| 提议q | TV首次≤1% | 第64步TV |
| --- | ---: | ---: |
| 1/8 | 第124步 | ≈0.065542 |
| 1/4 | 第61步 | ≈0.008038 |

提议移动率从1/8提高到1/4，虽然没有改变任何目标概率，128步内的精确TV收敛状况却有明显差异。低权中心节点的双峰瓶颈限制端点间迁移；要区分链处于数学平稳目标、有限时间起点偏差仍存在，以及单条实际Monte Carlo链出现的随机估计偏差这三件事。

## 两个独立Fraction方案定义并计算N64的ESS

本轮ESS不是直接从96条随机路径的经验自相关估计，而是在**真平稳启动**下、对固定指标f=1{i=2}从N=64个连续状态的样本均值，计算有限N下确切方差，并换算成同方差独立观测数量。真指标均值μ=π2，单时方差V=π2(1−π2)。路径一由真T全部63个滞后协方差`Cov_k=π2 (T^k)_{22}−π2²`推得`ρ_k=Cov_k/V`，再计算

`Var(M64)=(V/64)[1+2Σ_{k=1}^{63}(1−k/64)ρ_k]`，
`ESS64=V/Var(M64)=64/[1+2Σ_{k=1}^{63}(1−k/64)ρ_k]`。

完全独立路径二**不使用上述ρ数组**：从平稳状态起逐次传播每个时点状态质量、到该时点状态所累积访问次数S的第一与第二未归一化矩。64状态累计到末端后计算`Var(S64/64)=[E(S²)−E(S)²]/64²`。两个数学方法对全部八个T的有限样本方差及ESS逐Fraction完全一致，并保存每个ρ1..ρ63与全部精确分数。ESS仅对指定单个指标和平稳初始条件成立，既不是高维链整体验收，也不是任何经验`R̂`收敛诊断的代名词。

| 目标 | q=1/8，平稳N64 ESS | q=1/4，平稳N64 ESS |
| --- | ---: | ---: |
| UNIFORM | 5.825402 | 11.891613 |
| CENTER | 5.551709 | 11.321867 |
| BIMODAL | 1.937048 | 2.975396 |
| SKEW | 4.713688 | 9.275819 |

同样64个时间上连续的状态，在双峰目标q=1/8下，针对状态2事件的平稳估计精度仅与≈1.94个同目标独立样本相当；q=1/4也仅≈2.98。模型中所有目标和q均具有相同的状态空间，改善提议跳转强度可以增加有限样本ESS，但变更目标分布的双峰结构会显著改变ESS。**此结果不能推论任意MH算法提高proposal幅度都必然有益**，因为本项提议仅是预先固定的对称相邻路径q与受控接受率。

## 96条确定性重放Monte Carlo轨迹与有限经验误差

每个24个世界用四个可复现`random.Random(seed)`轨迹，seed固定为`195000 + target_index×10000 + proposal_index×1000 + start×100 + replicate`。每条恰好进行64次burn转移，随后2048次独立Uniform伪随机数决定T的下一状态，全部状态频数与f样本均值、完整源码、随机种子及与π2的绝对误差逐条保存。固定种子仅保证代码重放；96条样本不属于实际社会实验，也不能证明短链收敛或没有初始偏差。

按各目标的24条模拟记录做纯描述性汇总，`|hatπ2−π2|`的最小/平均/最大绝对误差：

| 人工目标 | 平均绝对误差 | 最大绝对误差 |
| --- | ---: | ---: |
| UNIFORM | 0.022095 | 0.061198 |
| CENTER | 0.023688 | 0.073079 |
| BIMODAL | 0.053783 | 0.183214 |
| SKEW | 0.029814 | 0.090681 |

BIMODAL且q=1/8、从状态0初始、seed=215000这一固定样本的误差最大，约0.183214即18.32个百分点。它是**指定随机种子下的一个实际抽样实现**，不是未来任何实测误差必须如此大的预言，也不改变精确目标π=(4/9,1/9,4/9)。没有对任一单条模拟样本设人为达到置信阈值的“必定通过”条件，真正科研验收依赖精确转移与矩算法及完整来源归档。

## 双版本机器验收和可重复计算永久归档

[GitHub Actions39585843192](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39585843192)：Python3.11与3.12分别执行33项单测，共**66次全部success**；第三job真实运行24世界的129步分布、两套核矩阵与ESS公式、96条固定随机种子链及全部档案的SHA核验与七文件确定性ZIP，并将实际输出提交main，三个job结论均success。原始机器数据归档提交[36b84e68](https://github.com/edwardsage419/Psychohistory-Research/commit/36b84e68aa4c95803adfe52e127a5f89e8cd9b17)。

永久数据包：
* [R195_EXACT_RESULTS.json](R195_EXACT_RESULTS.json)：全部24世界精确起点TV阈值、固定例、各来源hash与E1分级，SHA256`0464f870cfb53e75952d8f16291c5d4c8fca6156eb6a790fad72914290aec2f8`。
* [R195_ALL_9288_EXACT_DISTRIBUTION_CELLS.csv](R195_ALL_9288_EXACT_DISTRIBUTION_CELLS.csv)：24世界×129时点×3态的9288个Fraction完整源概率及总变差，SHA256`b6c4aab99051a9d7764f77c5ac444ace94a47a9b79b65d84aaede00ad2e73792`。
* [R195_ALL_8_EXACT_MCMC_KERNELS_AND_ESS.json](R195_ALL_8_EXACT_MCMC_KERNELS_AND_ESS.json)：8个精确MH矩阵、π、63阶全部自相关、独立双Fraction ESS及方差，SHA256`14b73ab3fcfc68bc1d9e836b3e50a8a7de3d1a6b4ca61154e8b1a3fa832f146f`。
* [R195_ALL_96_SEEDED_MCMC_REPLICATES.csv](R195_ALL_96_SEEDED_MCMC_REPLICATES.csv)：96条固定seed、2048保留状态的原始频数、误差与末状态，SHA256`920ecac9c65643c204de57fa6b8b987a7e6928ed5f44375f8d81b169044ded3a`。
* [R195_FINAL_MACHINE_ACCEPTANCE.json](R195_FINAL_MACHINE_ACCEPTANCE.json)：精确双数学路径、分布与ESS、SHA、真实E2/E3禁止外推标记。
* [r195_three_state_metropolis_exact.py](r195_three_state_metropolis_exact.py)：独立MH核、线性递推和矩阵幂、协方差和访问次数DP、可重放模拟及33项双版本测试。
* [R195_24_Exact_ThreeState_MCMC_Worlds.zip](R195_24_Exact_ThreeState_MCMC_Worlds.zip)：含源码、冻结协议、人工精确分布、八矩阵ESS库、96模拟样本、最终JSON和机器验收的七文件固定时间可复现ZIP。

科研验收只达**E1人工离散MH算法、平稳目标、有限时间收敛与平稳指标ESS**，没有真实心理、社会、历史参数后验或外部历史预测，新增E2=0、E3=0，R073与PESEN v0.1仍冻结。下一原目录 **R196 P2/08-020 Variational Bayes（变分贝叶斯）**。研究顺序保持全部R完成后统一归纳分类，最后模型熔炼。
