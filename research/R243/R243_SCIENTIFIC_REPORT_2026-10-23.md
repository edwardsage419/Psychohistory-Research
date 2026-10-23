# R243 随机微分方程：九个人工有限噪声积分代理、144完整四步来源与高斯布朗边界

日期2026-10-23 Asia/Taipei。原239目录 **11-003 Stochastic Differential Equations（P2）**。科学范围 `CLOSED_BOUNDED_E1_FINITE_NON_GAUSSIAN_EULER_STYLE_SURROGATE`。**特别限制：所有结果仅为有限二点Rademacher噪声的Euler–Maruyama式递推，不是标准布朗运动的高斯增量，也不是严格连续时间SDE解。** 无真实噪声过程数据、真实人类实验E2或历史E3。

## 原始方法、冻结和严格的非高斯证据

Higham (2001), [*An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*](https://doi.org/10.1137/S0036144500378302), *SIAM Review* 43:525–546，明确为Itô型`dX=f(X)dt+g(X)dW`使用一步Euler–Maruyama式`X_{n+1}=X_n+f(X_n)Δt+g(X_n)ΔW_n`。真正Brownian增量`ΔW_n∼N(0,Δt)`且独立。为了全文使用Fraction精确穷举，本R将其替换为四个**独立离散Rademacher**符号`ε_n∈{−1,+1}`、`ΔZ_n=ε_n/2`、每步`Δt=1/4`。这个有限代理只保留高斯增量的均值0和方差1/4，故同方差Brownian高斯增量四阶矩应为`3/16`、人工离散增量只有`1/16`；独立四步真实高斯端点第四矩为3，此有限代理端点第四矩则是`5/2`。因此**不能宣称复现高斯增量的四阶、尾部、连续路径Law，亦不能将数学E1检验等同Higham数值强/弱收敛结论**。

[代码评分前先行冻结九人工机制与全部路径协议](../../protocols/R243_SDE_9_RADEMACHER_EULER_SURROGATE_WORLDS_144_PATHS_PRESCORE_FREEZE_2026-10-23.md)提交 [4733342e](https://github.com/edwardsage419/Psychohistory-Research/commit/4733342e3fd16083468541f557f3bb2bffa3ce69)。参数、观测别名与所有来源检验都先于代码、CI及结果冻结，未事后修改。

## 九模型、完整144原噪声路径和独立公式

每世界四个独立人工`ε1…ε4`，共有16条完整等概率四步原外生路径，每条质量1/16。九模型合计**144完整结构原路径**，文件逐路径保存ε1…ε4、全部五时点真实隐藏h0…h4、实际可见y0…y4、四个实际观察增量以及源概率。对于某些世界只有ε1控制动态，未使用的其他ε仍完整保留，但不冒称原观察有16条不同轨迹。第一路线根据人工结构递推生成真实隐状态与可见信号。**独立第二路线不使用来源模拟函数**，对每条完整ε序列直接使用封闭公式：加性Y_n=n μ/4+σΣ_{j≤n}ε_j/2，共同shock Y_n=n ε1/2，乘法Y_n=∏_{j≤n}(1+d+ε_j/2)，d=0或1/8；对每世界全部可见五元联合路径及独立一/二阶解析矩作逐格Fraction核验。

九world：ADDITIVE_SYMMETRIC(σ=1)、ADDITIVE_NEGATIVE_SIGMA(σ=−1)、ADDITIVE_DOUBLE_SIGMA(σ=2)、ADDITIVE_DRIFT_ONE(μ=1,σ=1)、COMMON_SHOCK_REPEAT(每步重复ε1)、STATIC_HIDDEN_STOCHASTIC_SENSOR(真隐藏0，随机传感器显示ΣΔZ)、HIDDEN_DOUBLE_SCALE(真隐藏加2ΔZ，传感器显示隐藏的一半)、MULTIPLICATIVE_EM_ZERO_DRIFT(h0=1,每步乘1+ΔZ)、MULTIPLICATIVE_EM_POSITIVE_DRIFT(h0=1,每步乘1+1/8+ΔZ)。

## 九机制完整观察矩和真实隐藏机制

| 人工机制 | n=4观察均值 | n=4观察方差 | 完整可见五元路径支持数 |
|---|---:|---:|---:|
| ADDITIVE_SYMMETRIC | 0 | 1 | 16 |
| ADDITIVE_NEGATIVE_SIGMA | 0 | 1 | 16 |
| ADDITIVE_DOUBLE_SIGMA | 0 | 4 | 16 |
| ADDITIVE_DRIFT_ONE | 1 | 1 | 16 |
| COMMON_SHOCK_REPEAT | 0 | 4 | 2 |
| STATIC_HIDDEN_STOCHASTIC_SENSOR | 0 | 1 | 16 |
| HIDDEN_DOUBLE_SCALE | 0 | 1 | 16 |
| MULTIPLICATIVE_EM_ZERO_DRIFT | 1 | 369/256 | 16 |
| MULTIPLICATIVE_EM_POSITIVE_DRIFT | 6561/4096 | 710665/262144 | 16 |

**完整随机轨迹观察等价：** ADDITIVE_SYMMETRIC与ADDITIVE_NEGATIVE_SIGMA对全部五时点路径分布严格同分布，但不是同一ε原路径逐点一样；按全噪声向量逐位符号互补`ε→−ε`存在双射，其路径概率保持1/16，因此在此独立对称噪声机制中无法仅从y的分布区分扩散系数+1/−1的符号。这不意味着扩散强度大小普遍不可识别。

ADDITIVE_SYMMETRIC、STATIC_HIDDEN_STOCHASTIC_SENSOR及HIDDEN_DOUBLE_SCALE在**每条相同的人工ε来源上都生成完全一样的y0…y4**，而第一世界的隐藏h是随机游走，第二世界隐藏h永远0、全部随机波动由独立仪器/报告产生，第三世界隐藏h的单位是可见向量的两倍。由于模型允许动态随机传感器及隐藏尺度自由，完整路径亦不能无外部测量假设区分真物理噪声与测量噪声/坐标自由度；这只是一组有明确限制的人造源，不是现实全部SDE的不可识别定理。

**一步边际相同不等于噪声独立：** COMMON_SHOCK_REPEAT的第一步观察均值0、方差1/4，与真正独立的ADDITIVE_SYMMETRIC一致；但其每步重复第一个ε导致时点4观察方差`4`、16完整原source只折叠为2条可见路径，而真正四个独立ε的模型时点4方差`1`、有16条不同可见五时点路径。独立性需用跨时间联合与条件信息审计，单个时间局部分布不足。

**非线性乘法增长的精确矩：** MULTIPLICATIVE_EM_ZERO_DRIFT的离散条件均值保持1，但方差按`(5/4)^n−1`增长，n=4为`369/256`；人工正漂移乘法模型每步均值因子9/8，终端均值`(9/8)^4=6561/4096`，方差`[(9/8)^2+1/4]^4−(9/8)^8=710665/262144`。它们是**Rademacher离散积分递推的确切概率矩**，不应未经高斯收敛及时间步细化检验视作连续乘性Itô或Stratonovich SDE的精确解。

## CI来源归档和最终证据

[九模型独立Python计算程序](r243_exact_finite_sde_noise_surrogate.py) · [144完整四步人工噪声原源CSV](R243_ALL_144_ORIGINAL_FOUR_NOISE_INCREMENT_PATHS.csv) · [观察完整联合和各时点矩JSON](R243_EXACT_RESULTS.json) · [机读SHA256来源验收](R243_FINAL_MACHINE_ACCEPTANCE.json)。

[CI run39889392631](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889392631)总体completed/success，三个job均completed/success，Python3.11/3.12实际各`Ran 84 tests`并`OK`，**168次双版本真实单测通过**。第三独立审核作业重新生成144全部完整四位噪声原source、九模型来源概率、完整五时点路径分布、负sigma全路径同分布、静止隐藏与尺度别名、独立/公共扰动方差、乘法均值与方差、非高斯四阶矩与源文件SHA。真实归档日志输出`R243_144_FINITE_NON_GAUSSIAN_EM_SURROGATE_ORIGINAL_PATHS_AND_ALIASES_VERIFIED`。全部原CSV/JSON/SHA机器人永久提交[ d8940924](https://github.com/edwardsage419/Psychohistory-Research/commit/d894092493ed62f0a0423d58398e8b0d6b117ff7)。

原CSV SHA256 `d63b6acd378979a6e0cadbd016aea3edd37d6d93f310d93d1686d0a06a9675dd`；完整结果JSON SHA256 `dff3ffccae8decacf82c105b7af83f1c27f17497d11d9e91f99ca9032b5cbc73`。

科研结果严格限于**有限非高斯离散EM式代理E1**，并不构成真实随机微分方程的Brownian数值收敛、真实噪声幅度估计或外部历史预测检验。新增真人E2=0、真实历史E3=0；R073与PESEN v0.1保持冻结。下一原239目录`11-004 Markov Stochastic Processes`，拟R244（P1），仍先完成原R研究后分类及熔炼。
