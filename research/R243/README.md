# R243 随机微分方程（11-003）：九个有限非高斯EM式路径代理、144完整原来源

日期2026-10-23。原239目录 `11-003 Stochastic Differential Equations`（P2），正式科学边界 `CLOSED_BOUNDED_E1_FINITE_NON_GAUSSIAN_EULER_STYLE_SURROGATE`。**严格注明：这里的四步独立噪声是±1/2 Rademacher，非真实Brownian高斯增量；仅匹配单步均值/方差，不是连续SDE的精确模拟或收敛测试。**

[事前冻结协议](../../protocols/R243_SDE_9_RADEMACHER_EULER_SURROGATE_WORLDS_144_PATHS_PRESCORE_FREEZE_2026-10-23.md) · [科学报告及非高斯四阶矩约束](R243_SCIENTIFIC_REPORT_2026-10-23.md) · [全部144四位噪声原路径CSV](R243_ALL_144_ORIGINAL_FOUR_NOISE_INCREMENT_PATHS.csv) · [完全Fraction源码](r243_exact_finite_sde_noise_surrogate.py) · [九世界完整观察路径与矩](R243_EXACT_RESULTS.json) · [原来源SHA256机器收据](R243_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界验收](R243_FINAL_ACCEPTANCE_STATUS.json)。

ADDITIVE_SYMMETRIC和ADDITIVE_NEGATIVE_SIGMA的完整五时点路径概率同分布（逐epsilon全符号互换而非同一原source同值）；静止真隐藏但观测随噪声变化的人工传感器、以及隐藏尺度两倍的版本则和ADDITIVE_SYMMETRIC在相同epsilon下全部观察逐原路径相等。独立噪声的四步方差1，共享同一噪声每步重复的四步方差4；一时点边际不足以证明噪声独立。乘法离散噪声世界各时点均值与方差和解析公式严格相同。但二点噪声单步四阶矩1/16不等同同方差Gaussian的3/16，四步端点四阶矩5/2也不同Gaussian的3，**严禁外推到Brownian真实路径Law**。

[GitHub Actions run39889392631](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889392631)三job success，Python3.11及3.12各84项真实测试，共168通过；144完整人工路径机器人永久归档[d8940924](https://github.com/edwardsage419/Psychohistory-Research/commit/d894092493ed62f0a0423d58398e8b0d6b117ff7)。真人E2及真实历史E3新增0；R073和PESEN v0.1持续冻结。下一原目录11-004 Markov Stochastic Processes（R244，P1），先完成原R全部后才分类与融合。
