# R270 正式科研报告：后验预测检验中观测顺序统计和尾部方向的模型检查差异

日期2026-10-23 Asia/Taipei。原239目录：11-030 Posterior Predictive Checks（P1），对应R270。证据类别：**CLOSED_BOUNDED_E1_EXACT_ARTIFICIAL_POSTERIOR_PREDICTIVE_ORDER_CHECK**，没有新增真人E2或真实历史E3。

## 理论背景与限定任务
Gelman, A., Meng, X.L., and Stern, H. (1996), *Posterior predictive assessment of model fitness via realized discrepancies*, Statistica Sinica 6:733–807（主论文733–760，含后续评论讨论），原作者公开论文 https://sites.stat.columbia.edu/gelman/research/published/A6n41.pdf 。本项没有作者原始数据或算法同构性主张。研究目标为对一个固定的六次Bernoulli模型，在相同观测成功次数而时间排序不同的情况下，检验不同的后验预测差异统计量及尾部报告。检查结果是**模型内生成概率的诊断**，并非独立预测准确性或常规频率p值校准证明。

## 原协议事前冻结与完整来源
[事前冻结文件](../../protocols/R270_POSTERIOR_PREDICTIVE_9_SIXBIT_WORLDS_576_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，先行GitHub提交[57711245](https://github.com/edwardsage419/Psychohistory-Research/commit/5771124558a4c033cca9f5e2d0e6d7ea5315cc8c)。Beta(a,b)三种先验：(1,1)、(2,2)、(1,3)。三个冻结观察序列：BLOCKED `111000`、ALTERNATING `101010`、MIXED `110010`，长度皆6且恰好成功K=3，各自的相邻相同次数分别4、0、2。

先验×观察序列共9个world。二元条件独立Bernoulli(θ)，posterior θ|y=Beta(a+3,b+3)。每world完整枚举全部2^6=64种**有序**posterior predictive复现y_rep，按Beta后验积分的来源质量 `rising(a+3,Krep)*rising(b+3,6-Krep)/rising(a+b+6,6)` 严格Fraction计算。全world合计576种人工复现原source配置。同一先验下三个观察序列产生相同后验，因此复现分布也完全相同，跨world不得视为576个独立真实实验。

## 独立数学与来源复核
路线A直接读取所有64个有序复现序列，汇总Krep成功次数与Tadjrep相邻相同次数的完整精确概率质量及与观测数比较的上尾/下尾。
路线B从Beta-binomial完整Krep概率 `C(6,k)rising(A,k)rising(B,6-k)/rising(A+B,6)` 开始，再按游程r=6−Tadj拆解固定成功次数k的序列数：第一个游程是1时，1-run数量ceil(r/2)、0-run数量floor(r/2)，第一个游程是0时互换；每种游程组成由正整数分拆组合数 `C(k-1,runs1-1)*C(6-k-1,runs0-1)` 决定；全0与全1极端序列单独正确处理。此路线不依赖逐序列原source枚举器，九世界全部7类count和6类adjacent的完整PMF与路线A逐Fraction严格一致。

第三GitHub独立来源审计直接重读全部CSV逐项重建六位字串、原Beta后验权重、两类统计量及双方完整PMF、上下尾、源SHA256与结果SHA256，跨独立实施层核实。

## 九world精确模型内后验预测尾部

|Beta先验|观测排序|相邻Tobs|P(Trep≥Tobs)|P(Trep≤Tobs)|P(Krep≥3)|
|---|---|---:|---:|---:|---:|
|Beta(1,1)|111000|4|26/99|129/143|529/858|
|Beta(1,1)|101010|0|1|10/429|529/858|
|Beta(1,1)|110010|2|28/33|175/429|529/858|
|Beta(2,2)|111000|4|71/286|131/143|89/143|
|Beta(2,2)|101010|0|1|7/286|89/143|
|Beta(2,2)|110010|2|241/286|11/26|89/143|
|Beta(1,3)|111000|4|196/715|49/55|5/11|
|Beta(1,3)|101010|0|1|16/715|5/11|
|Beta(1,3)|110010|2|122/143|283/715|5/11|

同一先验下观察的Kobs固定为3，Bernoulli/Beta模型只按K更新后验，所有单纯Krep≥3统计得到完全相同的检验概率；而观察相邻序列结构明显不相同。特别ALTERNATING的Tobs=0时，上尾P(Trep≥0)=1完全没有告警信息，而预冻结下尾P(Trep≤0)在三个先验分别为10/429、7/286、16/715，均小于0.05。该例直接说明“针对统计量选择哪侧偏差”是模型检查内容的一部分；上述0.05只是演示比较尺度，不允许被转写成任何真人实验显著性证明。

## 仓库证据与执行结果
[标准库原生运行程序](r270_exact_posterior_predictive.py) · [全部576完整原复现source CSV](R270_ALL_576_ORIGINAL_POSTERIOR_PREDICTIVE_REPLICATES.csv) · [全部九world完整概率质量与上下尾JSON](R270_EXACT_POSTERIOR_PREDICTIVE_RESULTS.json) · [机器SHA256来源凭证](R270_MACHINE_RECEIPT.json)。[GitHub Actions run39902465686](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39902465686) Python3.11/3.12各83项真实unittest全部通过，共166项；第三独立原source审核与永久GitHub机器人归档job也成功，三个job completed/success。完整CSV/JSON/SHA永久归档[commit33e6663e](https://github.com/edwardsage419/Psychohistory-Research/commit/33e6663e903b16f8c31e2d9e219696b6e99a3338)。

原CSV SHA256 `6d28b991f912ba6a365a1d788eede5d2dc4773507f75908d46084db22de11dcd`；结果JSON SHA256 `60137ade2efdb253426432cf27b60de468e475ceba95b4635431b30ebf40feaa`。

## 科研边界及原目录接续校正
三个观察向量都是**冻结构造的人工例子**，未对现实心理历史变量拟合，也没有从真实分布随机抽样观察到异常；先验选择、统计量选择、尾部方向事前固定。后验预测尾概率一般没有经典频率检验p值的均匀性保证，不能用其代替外部留组预测或因果识别。新增E2=0、E3=0，R073和PESEN v0.1保持冻结。

**目录校正**：原239候选目录在11-030后直接接续`12-001 Preregistration and Registered Reports`，因此下一模型应为**R271（12-001，P0）**。冻结协议曾提出“下一编号须检查11-031”，该编号并不在目录中；后续实查使用12-001，保留原冻结协议不做追改。项目继续先完成原R系列全部学习研究，再统一归纳分类，最后开始模型熔炼。
