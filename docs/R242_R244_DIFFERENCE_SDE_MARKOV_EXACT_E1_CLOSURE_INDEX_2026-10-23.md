# 心理史学 R242–R244 连续有限动力/随机机制研究：差分、SDE非高斯代理、Markov混合的原始来源归档

日期2026-10-23（Asia/Taipei）。真实性边界：每项是严格独立设计的有限**人工E1数学**研究，不同结构源的数量可以作为工作量加总，却绝不能视为真人受试者、真实观察历史记录或高斯随机过程路径。研究顺序依用户规定：**原239候选R系列全部先做→统一归纳分类→最后熔炼**。R073与PESEN v0.1冻结。

## R242 = 11-002 Difference Equations（P0）

[先行冻结](../protocols/R242_DIFFERENCE_EQUATIONS_9_FINITE_WORLDS_180_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整源码与180来源](../research/R242/README.md) · [科研报告](../research/R242/R242_SCIENTIFIC_REPORT_2026-10-23.md) · [正式有界验收](../research/R242/R242_FINAL_ACCEPTANCE_STATUS.json) · [CI run39889143138](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889143138)。

九个人工离散递推世界，4有理初值×5时点、各人工原来源质量1/20，共**180完整原source类型**。独立多项式函数复合、Horner求值及精确求导的第二数学路线与逐步差分模拟值、初值灵敏度全部一致。完整原source中，真状态衰减vs纯时间传感器缩小vs隐藏坐标重标定；真状态扩张vs纯时间传感器扩张；真隐藏符号翻转vs稳定隐藏状态在平方观测下，分别构成三组**可见五时点全联合分布与初值灵敏度等价**，但源真隐藏动力不同。额外r=2/r=4 logistic map初值1/2、1/4的有限四步精确轨道已验；没有宣称长期混沌或任何真实代际适用性。CI总体及3作业success，Python3.11及3.12各85实际单测、共**170**；完整来源机器人永久归档[44f0bd90](https://github.com/edwardsage419/Psychohistory-Research/commit/44f0bd903d094175306348a24f5f6be8505e1336)。

## R243 = 11-003 Stochastic Differential Equations（P2）

[先行冻结和非高斯限制](../protocols/R243_SDE_9_RADEMACHER_EULER_SURROGATE_WORLDS_144_PATHS_PRESCORE_FREEZE_2026-10-23.md) · [原生完整144路径及源码](../research/R243/README.md) · [完整科研报告](../research/R243/R243_SCIENTIFIC_REPORT_2026-10-23.md) · [正式有界验收](../research/R243/R243_FINAL_ACCEPTANCE_STATUS.json) · [CI run39889392631](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889392631)。

九人工四步**非高斯Rademacher离散增量Euler–Maruyama式代理**，每世界16全原四符号source，共**144完整人工路径**。冻结每步`ΔZ=±1/2`,`Δt=1/4`，其一/二矩与同方差Gaussian Brownian增量匹配，**但**离散单增量第四矩1/16相对Gaussian 3/16，四步端点第四矩5/2相对Gaussian 3，不是Brownian精确路径复现、真实连续Itô SDE解、强/弱数值收敛验证。九世界全部原source路径与独立代数式和一/二阶矩一致。加性扩散σ=+1/−1在ε互补路径双射下同分布；真隐藏纯加性噪声、真隐藏恒定但随机报告传感器与隐藏尺度双倍的世界在相同ε来源下**完整可见路径逐source相同**。公共重复shock的一步方差与独立shock同1/4，但4步方差4 vs1。CI三个作业success，Python3.11及3.12各84真实测试，共**168**；全来源永久机器人归档[d8940924](https://github.com/edwardsage419/Psychohistory-Research/commit/d894092493ed62f0a0423d58398e8b0d6b117ff7)。

## R244 = 11-004 Markov Stochastic Processes（P1）

[先行冻结](../protocols/R244_MARKOV_9_WORLDS_1152_FULL_SEVEN_BIT_PATH_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整1152原路径与Python](../research/R244/README.md) · [科研报告](../research/R244/R244_SCIENTIFIC_REPORT_2026-10-23.md) · [正式有界验收](../research/R244/R244_FINAL_ACCEPTANCE_STATUS.json) · [CI run39889712674](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889712674)。

九人工二态三步路径模型，每世界U隐藏策略类和三步各两位噪声，全部128外原来源且每行1/128，共**1152完整七位来源类型**。从全source计算实际四时间观察联合，与直接按条件转移概率乘积、隐藏类型混合的完全独立第二积分路线逐格一致；齐次Markov矩阵P的`P²/P³`与两三步观察概率严格相符。一个人工隐U选择个体每步stay概率3/4或1/4；只看Y时同样Y2=0，过去Y1=0或1导致`P(Y3=0)`分别7/10、3/10，当前状态条件预测1/2，**可见Y失去一阶Markov性，缺陷1/5**；固定隐藏switch策略使缺陷1/2。时间交替的条件Markov过程虽转移率随时间变，其有限Markov缺陷仍0，不能混淆齐次性与Markov性。另真隐藏Markov、恒定真实隐藏而观测instrument是Markov及标签互补三世界全source可见路径等价。CI三job success，Python3.11及3.12各83真实单测，共**166**；全部1152源及SHA机器人归档[90765065](https://github.com/edwardsage419/Psychohistory-Research/commit/907650659e92e8abff7a07b3eeb2b2e873f67938)。

## 本轮机器科研验收小结与下一条

本轮三项**27个不同冻结人工世界**，共**180+144+1152=1476条独立有限人工结构原类型**和**170+168+166=504次双Python运行实际通过的单测**。每项原评分协议先独立commit，随后源Python/CI，真实三个GitHub Actions run全体及全部9作业success、机读SHA及完整原CSV/JSON经GitHub Actions bot永久提交main，随后独立完整科学报告与正式验收文件。没有真实历史语料或人类数据新增，**真人E2=0、历史E3=0**，不把CI通过、人工模型匹配或完整归档等同外部可检验经验科学成立。

原239目录R244之后已再次核验下项 **11-005 Renewal Processes（P2）**，拟R245；接续11-006 Poisson and Hawkes Processes（P1）及11-007 Branching Processes（P1）。优先完成原R研究后归纳分类再模型熔炼。个人决策系统建设继续暂缓，R073/PESEN v0.1冻结。
