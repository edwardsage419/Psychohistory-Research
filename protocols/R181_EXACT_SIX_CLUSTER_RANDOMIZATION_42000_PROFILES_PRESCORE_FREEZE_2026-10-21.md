# R181 置换检验：六群组随机化与24条错误独立置换的完整零假设误报率，计算前冻结

日期：2026-10-21。239候选目录 P0/08-005 Permutation Test。状态PRESCORE_FROZEN_E1_ARTIFICIAL_RANDOMIZATION。**先冻结本协议，随后才允许生成原始R181的结果。** 实际研究样本全部为从已验证R177人工计数PMF构造的数学世界，不是本人真人群组实验、真实政策评估或某篇原作者真实论文复现。

## 原始文献及理论边界

1. R. A. Fisher (1935), *The Design of Experiments*, Oliver and Boyd；原始随机分配与Fisher sharp null条件检验的历史来源，出版记录：https://books.google.com/books/about/The_Design_of_Experiments.html?id=-EsNAQAAIAAJ。
2. Imbens and Rubin (2015), *Causal Inference for Statistics, Social, and Biomedical Sciences*, [Chapter 5 Fisher's Exact P Values for Completely Randomized Experiments](https://www.cambridge.org/core/books/abs/causal-inference-for-statistics-social-and-biomedical-sciences/fishers-exact-pvalues-for-completely-randomized-experiments/23AF990D2EF9C90D0A424D555FACE578)。Fisher可精确检验所有单位处理效应均为零的sharp null。该结论依赖实际随机分配机制已知。
3. Cameron, Gelbach and Miller (2008), [Bootstrap Based Improvements for Inference with Clustered Errors](https://doi.org/10.1162/rest.90.3.414)，说明跨群组依赖对于推断的重要性，但本轮的置换计算与该文章的bootstrap t不是同一方法。
4. [2023年JRSS B随机化推断](https://doi.org/10.1093/jrsssb/qkad080)区分sharp null与更复杂的bounded null。本轮固定研究sharp null，无真实人类处理效应观察。

## 事前固定人工潜在结果与独立群组分配机制

六个**具有群组身份**的单位g=0..5，每群组内部恰好4次二元事件机会，群组总事件数K_g∈{0,...,4}；6个群组之间独立同分布，其完整群组计数PMF来自R177的**固定原始源码与固定数据结果**：

* 原源码`research/R177/r177_four_finite_count_families_exact.py` Git blob SHA1 `2d032513ce84141214b6b3f84df9c0ed9976a02b`。
* 原R177结果`research/R177/R177_EXACT_RESULTS.json` SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`。

固定原真群组边际概率p∈{1/4,1/2}，固定5个训练来源：IID_BIN (BIN r0)、CLUSTERED_BB_C2 (BB r0)、CLUSTERED_BB_C8 (BB r2)、INACTIVE_ZIB_Z1_8 (ZIB r0)、INACTIVE_ZIB_Z1_4 (ZIB r1)。2×5=**10个人工sharp null世界**。每个群组的潜在结局在处理0与处理1时都等于同一K_g。不存在任何处理效应；全因果潜在结果被人工完全观测，属于验证随机化检验性质的数学演示，绝不是真实无效政策的检验。

实验者在6个群组层级完整随机抽取3个群组接受处理，剩下3个是对照。共有C(6,3)=**20个等概率处理分配**，与每个群组内部4次观察的随机性分开。**处理只在群组层随机化**，从未独立随机化24次行为记录。

冻结观察统计：每个群组等权，以处理组与对照组的平均成功比例差作为统计量；在观察计数总和S与分配后处理组总成功数T条件下，其绝对值比例为 `abs(2*T−S)/12`。所有置换检验固定双侧绝对值统计量，采用`>=`计入同分布的全部同分数分配，不能随意破平局或只计算极端方向。

## 两种固定对照检验，四种拒绝判定

* **正确群组Fisher随机化检验**：以已观测的六组K为固定潜在结果，在全部20个等概率选择3群组的分配中计算处理组T的完整PMF，真实观察的`|2T−S|`越极端或同等极端的分配数除以20为精确双侧p。独立方法A直接穷举全部20分配；方法B从六个完整群组逐个选择或跳过，以二维状态(已选择组数,成功计数)的整数DP统计等权分配，必须每一可能T完全一致。
* **错误逐条独立置换**：把24次组内二元事件全当作可独立重新分配的等价观察，在总成功数S给定后任取12次事件视作处理。名义处理成功数T的完整分布为超几何`C(S,T) C(24−S,12−T)/C(24,12)`。独立方法C使用该组合公式；方法D模拟从24条观测不放回抽取12个处理事件的逐步Bernoulli成功个数DP并精确Fraction验收。**这是反事实的错误处理分配方案**，不能被称为真实群组随机化检验。

固定名义拒绝阈值α∈{1/10,1/5}。给出两种方法在两个α下的**真实sharp null误报率**，检验事件定义为精确双侧p≤α。采用每个固定人工真分布下正确来源概率，对所有观察样本和真实20组随机分配取期望：

* 六个群组计数所有有序组合共有5^6=15,625个；由于六群组独立同分布且真实随机分配对其标签可交换，按六个计数排序后的**210种无序多重集**加以原始多项式排列倍数，足以无损表达全部有序样本来源概率。必须明确输出每个profile的排列重数和真实profile概率，并证明210种profile总概率为1。
* 每个profile下实际20个群组处理分配等概率，主数据表共 210×20×10=**42,000条带真实来源权重的分析记录**。必须核验profile加权后与5^6源有序全体的理论质量一致，禁止把210个profile直接等权。
* 对每组真实来源机制，完整计算两种精确p值及α=0.1、0.2时的真实误报率。群组随机化检验因为sharp null、正确分配与包含平局极端事件，条件误报率不得超过α；这不是一个大样本近似结论。错误个体置换方法没有此随机化保障，其结果必须由完整R177生成机制真正穷举，禁止事先宣称一定反保守。
* 固定对照打印两种概率分布相异的一个排序profile K=(0,0,0,0,4,4)，并报告所有20个真实群组分配下的准确双侧p以及错误个体模型的双侧p。如果实际结果相同，则如实保留相同数值。

## 严格独立算法、测试和科学边界

群组PMF的A/B两法各自进行全分配枚举与选择DP；错误逐事件PMF的C/D两法分别使用超几何组合数与有限总体逐次不放回DP。所有整数计数和全部概率Fraction精确，不调用任何随机数、不使用蒙特卡罗估计。生成包含10个机制世界的机器结果JSON，210个profile全部条件随机化PMF与独立方法验收JSON库，42,000条观察分配 CSV，固定时间戳完整源码/协议/数据ZIP，以及至少20个单元测试。

全部来源SHA及计算验收通过且Python3.11和3.12双环境测试均success、档案已经永久提交main后，才能标记`CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RANDOMIZATION`。如果观察概率或CI失败则严格显示失败并修复程序，保留全部失败轨迹。任何真人因果效应、制度干预或历史外推都未在这里检验；E2/E3新增0。R073与PESEN v0.1继续冻结。仍按原先全部R系列先完成、统一归纳分类后才模型熔炼。下一R182经原目录应为08-006 Linear Regression，需独立核对后再进入。
