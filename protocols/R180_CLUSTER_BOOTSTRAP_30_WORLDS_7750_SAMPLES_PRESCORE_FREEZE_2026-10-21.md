# R180 自助法：30组有限群体完整重抽样与覆盖率检验，计算前冻结协议

日期：2026-10-21。原始239候选目录 P0 / 08-004 Bootstrap（自助法）。预期证据等级 E1_ARTIFICIAL_FINITE_EXACT。必须先将本协议永久提交主分支，再编写或运行R180完整正式结果。历史真实数据、真人观测与原作者原数据复现均不包含在本次计划。

## 原始研究来源及相关推断限制

1. Efron (1979), *Bootstrap Methods: Another Look at the Jackknife*, Annals of Statistics 7(1):1–26, https://doi.org/10.1214/aos/1176344552，原刊引入基于经验分布重抽样估计统计量抽样分布的方法。
2. Davison and Hinkley (1997), *Bootstrap Methods and Their Application*, Cambridge University Press, https://doi.org/10.1017/CBO9780511802843，复验方法设计与抽样结构必须一致。此处仅使用理论原则，不声称重算原书示例。
3. Cameron, Gelbach and Miller (2008), *Bootstrap-Based Improvements for Inference with Clustered Errors*, Review of Economics and Statistics 90(3):414–427, https://doi.org/10.1162/rest.90.3.414，原文指出少量cluster的统计推断具有复杂有限样本问题，研究的是更丰富的cluster bootstrap t推断。本项目的简易常规组重抽样、Wald及百分位区间属于独立指定的人工模型，不能称作该文章的方法精确复现。

## 原始生成机制与冻结30个世界

唯一训练样本来源为R177已经正式验收的人工计数分布，来源必须同时重新验证 `research/R177/r177_four_finite_count_families_exact.py` Git blob SHA1为 `2d032513ce84141214b6b3f84df9c0ed9976a02b` 以及 `research/R177/R177_EXACT_RESULTS.json` SHA256为 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`。禁止使用模糊最新分支替换已固定原始分布。

每个独立群组含 **n=4** 次二元事件机会，群组内计数K_g∈{0,1,2,3,4}，p∈{1/4,1/2}为单位事件边际真概率。各群组之间独立同分布；群组内部允许依以下完整机制有相关性：
* IID_BIN 使用R177 BIN regime0。
* CLUSTERED_BB_C2 使用R177 BB regime0（浓度2，群内正相关）。
* CLUSTERED_BB_C8 使用R177 BB regime2（浓度8）。
* INACTIVE_ZIB_Z1_8 使用R177 ZIB regime0（结构零比例1/8）。
* INACTIVE_ZIB_Z1_4 使用R177 ZIB regime1（结构零比例1/4）。

群组数m∈{2,3,4}，n=4固定，每群组同一来源机制。因而3种m×2种p×5种机制＝**30个世界**。每个世界完全枚举**所有有身份顺序的观测群组计数向量**(K_1,...,K_m)∈{0,...,4}^m，以真正原始生成概率∏_gP(K_g)加权。每一m取25、125或625个有序样本数据，30世界累计**7,750个完整人工观察样本**。禁止将组内4条潜在二元记录当成真正独立的群组来源。

群体边际成功率估计值固定 `p_hat=∑K_g/(4m)`，不对真实p拟合额外机制。其真实抽样方差在**已知人工真生成分布**下为 `Var(K)/(16m)`，所有世界直接用原始完整PMF求出精确有理数。

## 冻结重抽样方法和完整自助样本分布

对于每个有序观察样本，固定以下**两类bootstrap**：

* `IID_BOOT`：错误或正确地将4m条二元观测当作独立事件，从经验二元分布抽取4m次，每次成功概率为p_hat；总成功数T*∼Bin(4m,p_hat)，预测率T*/(4m)。必须分别用封闭二项公式与独立逐次成功计数动态规划逐项Fraction严格验证。
* `CLUSTER_BOOT`：将m个完整观察群组作为重抽样单位，有放回、独立均匀抽取m个群组编号，每次保留组内完整4次事件计数；bootstrap总成功数为T*=∑_{j=1}^mK_{I_j}，预测率T*/(4m)。必须分别用**全部m^m个有序群组编号序列穷举**与**m阶段重抽样计数分布动态规划**，独立计算所有可能总计数的完整概率质量，并严格Fraction一致。对于所有组值相同的样本，正确组重抽样分布为单点，不能私自添加噪声。

对上述两类完整bootstrap条件分布精确求条件方差V_iid^*(p_hat*)、V_cluster^*(p_hat*)。另定义预先固定的有限群组样本方差修正 `V_cluster_corrected = (m/(m−1)) V_cluster^*`，m≥2。不做其它修正或事后选择。

## 冻结评价指标和区间

所有7,750样本逐行留存：有序群组计数、真实样本概率、p_hat、三种bootstrap方差、两种方法完整条件bootstrap分布的SHA或机器可读概率信息、四种区间端点、四种是否覆盖真实p的标记。原始全条件分布可按已归档程序从每一组的样本行复算；若输出完整分布则在单独机器JSON内提供，避免双算结构含糊。

四种固定区间，严格区别算法：
1. IID常规Wald区间：`p_hat ± 49/25 sqrt(V_iid^*)`。
2. CLUSTER小样本修正Wald区间：`p_hat ± 49/25 sqrt(V_cluster_corrected)`。
3. IID无中心修正的95%百分位区间：IID_BOOT总计数T*分布的2.5%与97.5%离散最左分位数除以4m。
4. CLUSTER无中心修正的95%百分位区间：CLUSTER_BOOT总计数的相同离散分位数除以4m。

对于Wald覆盖，以有理数比较`(p_hat-p)^2 <= (49/25)^2 V`，不靠浮点精度猜测边界；百分位区间以严格有理数判断p落入由离散分位数组成的闭区间。百分位的明确定义为**累计分布最先达到α的最小整数T***，α∈{1/40,39/40}。禁止把所有四种区间误称作同一“95%置信区间”，其95%只是名义水平。

每一个30世界用真实原始样本概率对上述7,750种样本分布进行完全枚举积分，正式输出：

* 真实p_hat均方误差与真实抽样方差，且必须全组一致（p_hat边际无偏）。
* `E[V_iid^*]`、`E[V_cluster^*]`、`E[V_cluster_corrected]`；解析预期为`E[V_cluster^*]=((m−1)/m) Var(p_hat)`、`E[V_cluster_corrected]=Var(p_hat)`，务必精确Fraction相等。
* 四种固定区间真实覆盖率以及零方差群组样本概率；不能据区间覆盖的某个有利或不利数字主张某种bootstrap对所有现实数据优越。
* 预先固定主比较取 `m=4,p=1/4`，五种来源机制一律并列披露全部评价结果；必须另外给出m=2的退化风险反例（各群组计数恰好相同，cluster bootstrap方差为0但真分布有正方差）。
* 额外报告单个训练群组计数样本数据内缺乏组内事件时序，故与R177中正相关和结构零的边际观测可能出现机制别名，仅利用这些计数无法单独识别内部来源。

## 证据分类和正式验收

算法采用标准Python库Fraction、组合枚举、独立动态规划，无随机抽样，无蒙特卡罗误差。需至少20项自动化测试，验证R177来源SHA、全部30世界与7,750样本、群组编号枚举与动态规划的全概率相等、IID二项公式与DP相等、条件重抽样方差、无偏性、真实覆盖、全零/全同数退化、各世界Var修正期望恒等式、来源隔离与失败条件。Python3.11和3.12独立运行，CI后再对完整永久JSON、逐有序样本CSV、确定性ZIP固定SHA256并核验归档main。全部测试和归档成功后才可正式标记 R180 为 `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_BOOTSTRAP`。

本轮没有新真人独立预测E2和历史外推E3。R073/PESEN v0.1保持冻结；先完成所有R系列研究，再统一分类，最后熔炼。下一原目录R181为P0/08-005 Permutation Test，最终科研结题后方可进入。
