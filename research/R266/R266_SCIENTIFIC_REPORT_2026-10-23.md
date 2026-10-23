# R266 正式科学报告：有限蒙特卡洛抽样与对偶变量的方差增减反例

日期：2026-10-23（Asia/Taipei）
原239目录编号：11-026 Monte Carlo Simulation（P0）
研究编号：R266
结果等级：E1，人工数学完整样本空间的精确复算；不含真实人类行为或真实历史观察。
本报告的科研结论与GitHub归档完整性分开核验。

## 1. 理论来源与问题
Metropolis, N. & Ulam, S. (1949). *The Monte Carlo Method*, Journal of the American Statistical Association 44(247):335–341，DOI https://doi.org/10.1080/01621459.1949.10483310 。该论文为蒙特卡洛方法的早期经典，R266没有对原文方程、软件或真实场景进行复现。对偶变量的协方差关系参见Waterloo课程章节 https://sas.uwaterloo.ca/~dlmcleis/s906/chapt4.pdf 。

问题：固定相同的函数评价次数n，比较独立随机数抽样IID与反射对偶a(u)=3-u对积分p=E[f(U)]的估计质量。预先构建一个对偶降低方差的单调事件，一个对偶方差降至0的阈值事件，以及一个会**增加**方差的非单调对称事件。

## 2. 预先固定的人工样本空间
见[事前冻结协议](../../protocols/R266_MONTE_CARLO_NINE_WORLDS_5328_FINITE_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，冻结提交[634230df](https://github.com/edwardsage419/Psychohistory-Research/commit/634230df411eca00badadaa0c593f28ae08773c8)。

基础U在{0,1,2,3}均匀。THRESHOLD_Q1、THRESHOLD_HALF、THRESHOLD_Q3分别在U∈{0}、{0,1}、{0,1,2}为1，三种p分别1/4、1/2、3/4。SYMMETRIC_EXTREMES只在U∈{0,3}为1，p=1/2。前三函数分别n=2与4，后一函数n=2、4、6，合计九个冻结world。

IID每world使用n个相互独立的U和n次函数评价。ANTITHETIC使用n/2个独立U，每U作f(U)与f(3-U)两次函数评价。因此函数评价次数相同，**原始独立随机源调用次数不同**；同一对函数输出的相关性绝不被误写为IID。

完整人工来源类型：IID 5184条、ANTITHETIC 144条，共5328条。每条包含全原随机源元组、原始质量、输出计数、估计值和平方误差。此5328不是抽取到的独立观测样本数。

## 3. 两条独立计算与第三解析核对
路线A：遍历所有4^n IID元组或4^(n/2)对偶基础元组，用确切概率质量4^(-n)或4^(-n/2)聚合估计值完整PMF及其原点矩、方差和MSE。

路线B：另起单U的四点边际计数，不调用来源枚举器。IID对单次事件成功计数分布卷积n次，对偶对单对成功计数f(U)+f(3-U)的分布卷积n/2次。9 world × 2 design的**全部18个完整PMF逐Fraction精确相同**。

第三条解析核对：两种估计器对p无偏，MSE=Var；
```text
Var(IID estimator) = p(1-p)/n
c = E[f(U) f(3-U)] - p^2
Var(ANTITHETIC estimator) = [p(1-p)+c]/n
```
相同n是函数评价次数。对偶中的n次f评价只有n/2个独立源。完整样本空间的原矩与三项解析式严格一致。

## 4. 冻结九世界精确结果

| 冻结世界 | p | n次评价IID方差 | n次评价对偶方差 | 对偶/IID方差比 |
|---|---:|---:|---:|---:|
| THRESHOLD_Q1_N2 | 1/4 | 3/32 | 1/16 | 2/3 |
| THRESHOLD_Q1_N4 | 1/4 | 3/64 | 1/32 | 2/3 |
| THRESHOLD_HALF_N2 | 1/2 | 1/8 | 0 | 0 |
| THRESHOLD_HALF_N4 | 1/2 | 1/16 | 0 | 0 |
| THRESHOLD_Q3_N2 | 3/4 | 3/32 | 1/16 | 2/3 |
| THRESHOLD_Q3_N4 | 3/4 | 3/64 | 1/32 | 2/3 |
| SYMMETRIC_EXTREMES_N2 | 1/2 | 1/8 | 1/4 | 2 |
| SYMMETRIC_EXTREMES_N4 | 1/2 | 1/16 | 1/8 | 2 |
| SYMMETRIC_EXTREMES_N6 | 1/2 | 1/24 | 1/12 | 2 |

阈值1/4与3/4的对偶配对协方差=-1/16，方差较IID降低1/3。阈值1/2协方差=-1/4，反射组合每对恰一成功一次失败，估计器恒1/2，故对偶方差为0。对称两端事件f(u)=f(3-u)，每对结果完全一致、配对协方差=+1/4；按相同函数评价数对比，对偶方差是IID的两倍。这也直接否定“对偶方案一定比IID好”和“所有f评价可以按独立样本计算标准误”两个无条件说法。

## 5. 实际计算与归档证据
源码：[r266_finite_monte_carlo.py](r266_finite_monte_carlo.py)
完整来源：[R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv](R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv)
精确结果：[R266_EXACT_FINITE_MC_RESULTS.json](R266_EXACT_FINITE_MC_RESULTS.json)
来源哈希：[R266_MACHINE_RECEIPT.json](R266_MACHINE_RECEIPT.json)
CI：[run 39900969661](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39900969661)；Python3.11及3.12各136项真实unittest通过，共272；独立原source审计job success，总计三job completed/success。永久原数据归档提交：[e46f0e06](https://github.com/edwardsage419/Psychohistory-Research/commit/e46f0e06afb637ba2bb0cc2e267f2c36c1cc9c35)。

机器receipt中原source CSV SHA256：`5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a`。
结果JSON SHA256：`1ce039fd5ce94fb59741ea45fa2e62f052ac7ea28c99b172379ec1f8e195b218`。

## 6. 严格边界
此研究完整枚举的是**人为设置的有限概率空间**；没有实际执行伪随机模拟样本、没有测定通用伪随机数品质、没有复现连续蒙特卡洛积分估计器或高维计算复杂性、没有以真实数据评估方差缩减。九个world内的公式对应本研究明确的分布和反射关系，不能将某个方差比推广至任意复杂随机过程。当前没有心理学、社会互动或历史预测方面的新外部验证。新增E2=0，新增E3=0，R073与PESEN v0.1保持冻结。

研究主线保持：R系列学习优先；原239目录下一项已核实11-027 Latin Hypercube Sampling（P1，拟R267）；全部原R模型完成后才统一归纳、分类并开展模型熔炼。
