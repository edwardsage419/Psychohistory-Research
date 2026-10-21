# R191 混合效应模型：24个已知方差离散随机截距世界、BLUP与真实后验及群组迁移风险

日期2026-10-21。原目录P1/08-015 Mixed Effects Models。科研验收 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MIXED_EFFECTS**。全部输入为人工有理数随机截距与离散误差样本，新增真人行为E2=0、真实历史独立预测E3=0。

## 一手来源及严格适用范围

Nan Laird and James Ware (1982), [Random-Effects Models for Longitudinal Data](https://doi.org/10.2307/2529876), Biometrics 38(4):963–974，讨论群组/受试单位的随机效应与重复测量观察间相关。G.K. Robinson (1991), [That BLUP is a Good Thing: The Estimation of Random Effects](https://doi.org/10.1214/ss/1177011926), Statistical Science 6(1):15–32，系统解释随机效应最佳线性无偏预测（BLUP）及其基础。这些原始来源用于概念框架，不声称复现原著的真实纵向数据、REML或一般高斯LMM拟合。

本研究特意构造**非高斯、离散随机截距和非高斯三点误差**，且组间截距方差与误差方差均由人工源**事前已知**。我们检验的是此条件下四种预测方式的可验证数学风险，尤其区分最佳线性投影与真实离散潜在后验；没有从有限真实数据估计方差组件、检验社会因果效应或预测外部历史事件。

## 事前冻结机制及初次验收订正的审计

[初始计算前冻结协议](../../protocols/R191_MIXED_EFFECTS_24_WORLDS_1440_PATHS_PRESCORE_FREEZE_2026-10-21.md)最先以提交`f657a5a9001a5077a71a693da0caf5efa72ed219`入库main，先于完整R191评分。真实群组随机截距`U∈{−τ,+τ}`等概率取值，`τ∈{0,1/2,1}`；误差`ε∈{−2σ,0,+2σ}`分别概率1/4、1/2、1/4，`σ∈{1/2,1}`，重复测量次数`n∈{1,2,3,4}`。真观测`Y_i=U+ε_i`，所有ε条件及边际互相独立、群组U独立；群组内不同观察有协方差τ²，单次误差方差v=2σ²。完整人工因子设计3×2×4=**24个世界**。每世界逐条枚举潜在两标签×所有3^n原始有序误差序列，合计**1440条完整带潜在真值的原始训练路径**，全部概率严格Fraction求和。τ=0时两个隐标签的数值U都为0，但为忠实保留等权来源仍保留两个标签及各自概率。

首次[GitHub Actions39578606061](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578606061)有30测试中的29项通过，仅一项错误要求`τ=σ=1/2`时Bayes在n=1与n=2均严格优于线性BLUP。初始实际精确数学显示n1两者完全相同，故该测试断言失败，首次结果未被归档为通过。随后先写[单独测试边界纠错档案](../../protocols/R191_N1_BAYES_BLUP_TEST_ASSERTION_ERRATUM_2026-10-21.md)，明确n1时`E(U|Y)=Y/3`而线性收缩`κ=1/3`，即n1严格相等；n2才有严格改善。更新测试后，另一次中间工作流[39578807306](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578807306)虽双Python测试成功，却因ZIP已加入订正审计第七文件，而CI断言仍期望六文件而失败。最后按真实七文件修改ZIP验收条件。三条CI时间线与所有代码提交均原样保留；**所有24来源世界、原始概率、四预测器、风险数学与阈值从未变更**。最终成功验收[39578838588](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578838588)三job均success，取代此前失败作为正式结题证据。

## 同一群组下一次响应的四种预测方法

训练者只观察重复测量向量`Y=(Y1,...,Yn)`，不知道真实U：

1. GLOBAL预测为0，不使用历史；
2. RAW_GROUP_MEAN预测为`Ybar`，对每个群组的观察均值不收缩；
3. LINEAR_BLUP预测`κYbar`，其中`κ=τ²/(τ²+v/n)`，是**在已知二阶矩条件下的最佳线性预测系数**。高斯随机截距的条件后验也具有这个线性形式，但本研究实际误差是三点离散分布，**不保证与真实后验相等**。
4. EXACT_DISCRETE_POSTERIOR预测`E(U|Y)`，从两种潜在U假说的完整序列似然和各自先验等概率准确计算。两套完全独立的序列概率连乘及观测值直方图频数幂计算每个后验，逐Fraction严格一致。

预测同群未来新响应时使用新的独立ε，但仍属于同一个U，因此给定真实U和训练样本时的期望平方损失为`v+(U−预测)^2`。全部1440条来源路径都直接加权得到完整测试风险。另一条独立解析数学路线用已知方差与可观察训练的后验概率二阶矩得到：

* 总体均值风险`R0=τ²+v`；
* 未收缩组均值风险`Rraw=v+v/n`；
* 线性BLUP风险`Rblup=v+τ²v/(nτ²+v)`；
* 精确离散后验风险`Rbayes=v+τ²−E[E(U|Y)^2]`。

所有24世界四种风险与直接完整来源原始训练枚举逐Fraction**完全一致**。在每个世界`Rbayes≤Rblup≤min(Rraw,R0)`，且τ=0时`Rbayes=Rblup=R0=v`，未经收缩的组均值多出`v/n`的纯噪声预测误差。

## 预冻结零随机效应和非高斯后验反例

τ=σ=1/2，单次v=1/2。在n=1时，所有可观察Y仅取`{−3/2,−1/2,1/2,3/2}`，经精确离散Bayes条件概率求得`E(U|Y)=Y/3`；已知方差最佳线性收缩系数亦是1/3，两预测**完全相同**，独立未来MSE都是`2/3=0.666667`。这项原未预料的相等边界被明确记录并通过测试。

n=2时，最佳线性收缩系数=1/2；一些原始训练序列可以揭示更精确的潜在U类型，离散非线性后验与`Ybar/2`不同。完整源概率加权MSE：

| 在同一个已观察群组预测新的独立响应 | n=1 | n=2 |
| --- | ---: | ---: |
| GLOBAL | 3/4 = 0.750000 | 3/4 = 0.750000 |
| RAW_GROUP_MEAN | 1 = 1.000000 | 3/4 = 0.750000 |
| LINEAR_BLUP | 2/3 = 0.666667 | 5/8 = 0.625000 |
| EXACT_DISCRETE_POSTERIOR | 2/3 = 0.666667 | 49/80 = 0.612500 |

在n=2时准确离散后验相较已知二阶矩线性BLUP的独立测试MSE改善`1/80=0.0125`。不能由该非高斯有限例直接声称Gaussian LMM的BLUP天然失效；当真实条件后验恰为线性时两个方法本来就一致。

另一个有代表性已知τ=1、σ=1的真机制中，n=2同群未来MSE：GLOBAL=3，RAW=3，LINEAR_BLUP=2.5，EXACT_BAYES=2.45。n=4时分别为3、2.5、7/3≈2.333333、2.20846。所有24个来源完整输出保留，未挑选优越情形后修改参数。

## 群组迁移负对照

若预测对象是从人工源独立抽取的**完全新群组**，它的随机截距与原有训练群组U相互独立，其条件最优平方预测就是全局均值0，独立新群未来风险为`τ²+v`。错误地把旧群的随机截距估计`κYbar_old`用于新群，风险严格增加`E[(κYbar_old)^2]`。例如上述τ=σ=1/2、n=2的固定源，新群正确风险=3/4=0.75，错误复用旧群BLUP则风险=7/8=0.875。τ=0的负对照下BLUP始终为0，迁移并无新增误差。以上属于人工数学风险，不是现实群组是否相似的结论。

## 完整审计、哈希、科研分级

最终[GitHub Actions39578838588](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578838588)在Python3.11和Python3.12各30项完整单元测试共**60次全部通过**，第三job真实计算全部24世界、1440源路径、**1136种可观察后验profile**，核对独立似然算法、未来风险的两种精确算法、结果SHA、七文件确定性ZIP，并将所有实际结果永久提交main。[结果提交a6db677](https://github.com/edwardsage419/Psychohistory-Research/commit/a6db6777c81ae09145af78a2c5981abb6c7dc0d0)。

永久文件：
* [R191_EXACT_RESULTS.json](R191_EXACT_RESULTS.json)：24人工世界完整原始源参数、4模型真正同群测试风险、未见新群迁移风险、预锁定n1等价及n2差别，SHA256`b4a4b211e7eca8a96db72e42c635485c5ce755587d9b76f6d1c6893bb4f385a4`。
* [R191_ALL_1440_LATENT_TRAINING_PATHS.csv](R191_ALL_1440_LATENT_TRAINING_PATHS.csv)：带隐藏U、各次误差、训练原始响应、源概率、拟合预测及真未来测试损失的1440条完整样本，SHA256`2f09d9b40b25e056434f4d25fe5893cb0aad945225692cd5a94aae445fb8ea8c`。
* [R191_ALL_OBSERVABLE_POSTERIOR_PROFILES.json](R191_ALL_OBSERVABLE_POSTERIOR_PROFILES.json)：全部1136个可见训练向量、两潜在类别概率、完整后验和oracle线性收缩；SHA256`732c37eb157d63e6dc0ebd5014600ec2f6b2725e68d9f32480cf03ad70727659`。
* [R191_FINAL_MACHINE_ACCEPTANCE.json](R191_FINAL_MACHINE_ACCEPTANCE.json)：双数学源、四风险解析和枚举一致性、已见未见群区分及SHA。
* [r191_exact_finite_mixed_effects.py](r191_exact_finite_mixed_effects.py)：原生Fraction潜在来源枚举、双后验概率、所有24风险和30项测试。
* [R191_Exact_24_Mixed_Effect_Worlds.zip](R191_Exact_24_Mixed_Effect_Worlds.zip)：源码、完整协议、n1测试纠错、三数据结果、机器验收的七文件固定日期ZIP。
* [原冻结协议](../../protocols/R191_MIXED_EFFECTS_24_WORLDS_1440_PATHS_PRESCORE_FREEZE_2026-10-21.md)及[独立订正记录](../../protocols/R191_N1_BAYES_BLUP_TEST_ASSERTION_ERRATUM_2026-10-21.md)构成可审计决策顺序。

本项科学证据仅**E1人工离散随机截距与BLUP收缩机制精确研究**，未估计真实受试者、文化机制、制度或历史随机效应，亦无现实场次留出预测。R073和PESEN v0.1冻结，E2/E3新证据均0。

下一既定原目录 **R192 P2/08-016 Latent Class Models（潜在类别模型）**。维持全部R完成后统一归纳分类，最后熔炼。
