# R166 第三方法科学报告：有限单步文化计数对两类传播机制的可区分能力

日期：2026-10-26 Asia/Singapore
科学等级：`PASS_BOUNDED_INTERNAL_E1_WITH_DISCLOSED_POSTEXEC_ARITHMETIC_AMENDMENT`
原 R166 状态：`CLOSED_BOUNDED_E1`，原结题与48世界均不变；新增研究不重复记一次结题。
实际执行：隔离 JavaScript V8 BigInt 精确有理数计算。新增 Python 事前脚本及修正版已归档，**均未在本轮实际运行**；远端 CI 未运行。

## 来源与冻结
直接继承原 R166 2026-10-21 冻结的 12 套完整转移矩阵，原始数据 `research/R166/R166_EXACT_RESULTS.json` Git blob `998c80ccb4398d65424bbfccfa6d36c51696a9da`。
原作者文献 Alex Mesoudi (2021), *Cultural selection and biased transformation: two dynamics of cultural evolution*, DOI 10.1098/rstb.2020.0053；原作者连续状态 EMG 实现未复现。
事前新增协议 `protocols/R166_ONE_STEP_COUNT_IDENTIFIABILITY_THIRD_METHOD_FREEZE_2026-10-26.md`，冻结提交 `5704ad07c3c61ffe7293ec8c97f4521727989853`。
该协议错误地将 (5+9)*2 计算为56，第一次 JS 执行报 `unexpected observational partition`，没有把失败写成通过。之后另行提交 `protocols/R166_ONE_STEP_COUNT_IDENTIFIABILITY_ARITHMETIC_CORRECTION_2026-10-26.md`，仅将条件数更正为28，保留全部原始网格、公式与阈值。该修订属于**首次执行后的透明计数勘误**。

## 固定观察与数学结果
假定 N∈{4,8}，已知当期 A 计数 k，下一代独立采样 N 个二元子代，只观测下一代 A 总计数 J。
A偏向时两机制成功率：
`q_SEL=2p/(1+p)`，`q_TRF=(1+2p)/3`；
差为 `(1-p)(2p-1)/[3(1+p)]`。
B偏向时：
`q_SEL=p/(2-p)`，`q_TRF=2p/3`；
差为 `p(2p-1)/[3(2-p)]`。
这里 p=k/N，模型参数由原 R166 冻结，未使用现实数据拟合。
因 Binomial(N,q) 的均值为 Nq，两个完整计数分布相等当且仅当 q 相等。
A偏向相等点为 p=1/2 与 p=1；B偏向相等点为 p=0 与 p=1/2。
两种 N 均包含这些点，故28个非中性条件中8个完全相等，20个可区分。中性模型14个条件全部相等。

用 `TV=1/2 Σ_j|P_SEL(J=j)-P_TRF(J=j)|` 衡量单次观测的统计区分度，等先验最优分类错误率 `R*=(1-TV)/2`。精确枚举得到：

| N | 偏向方向 | 单步 TV 最小值 | 单步 TV 最大值 |
| --- | --- | --- | --- |
| 4 | A | 0 | 65/81 |
| 4 | B | 0 | 65/81 |
| 8 | A | 0 | 6305/6561 |
| 8 | B | 0 | 6305/6561 |

例如 A偏向、p=0，选择机制的下一代 A 数恒为0；转化机制的单个子代 A 概率为1/3。
故 `TV=1-(2/3)^N`。N=4 的最优分类错误率 `8/81`；N=8 为 `128/6561`。
A偏向、N=4、p=1/4 的 TV 为 `1627/10000`，等先验最优错误率 `8373/20000`。
p=1/2 时两个机制的完整单步计数分布相同，最优错误率仍为1/2。原 R166 已证明从该起点观察到第二代时，两种机制的分布可能分离。

## 实际执行、负对照与复算
B 独立 JavaScript BigInt 程序采用加权票数与复制后转化的分支计算，再完整枚举每个下一代的 2^N 种二元配置，逐行比较原始12套矩阵。
实际核验84个完整转移矩阵行，全部精确相等；28个非中性条件与14个中性对照通过。
预定变异负对照把 A偏向转化率从1/3改为1/4，在 N=4,p=1/2 时得到变异成功率5/8，与原选择成功率2/3的完整分布 TV=`8161/110592`，实际检测成功。
另一份 B 脚本以二项分布单调似然比的阈值性质，计算最大累计分布差 `max_j |F_SEL(j)-F_TRF(j)|`；28个条件全部与穷举 TV 精确一致。这是内部不同算法的交叉核查，仍共享同一原始人工模型与固定 JSON。

可执行程序及实际收据：
* `research/evidence_audit/r166_b_independent_exhaustive_20261026.js`
* `research/evidence_audit/B_R166_ONE_STEP_EXHAUSTIVE_EXECUTION_RECEIPT_2026-10-26.json`
* `research/evidence_audit/r166_b_cdf_threshold_20261026.js`
* `research/evidence_audit/B_R166_CDF_THRESHOLD_EXECUTION_RECEIPT_2026-10-26.json`
* `research/validation/r166_one_step_identifiability_20261026.py`（保留首次错误计数断言，未执行）
* `research/validation/r166_one_step_identifiability_corrected_20261026.py`（修正版，未执行）

## 科学解释与验收边界
这个结果量化了**已知当前频率与机制参数时，单次下一代总计数的理论辨别能力**。边界初始状态下的极强区分来自模型预设的“无创新选择”与“定向变异”，不能外推为现实人类的可区分程度。
同一代的 N 个子代在模型中条件独立，不能视作 N 次独立真人实验。机制先验各1/2为人为设定；没有现实拟合、样本外预测、概率校准、重采样置信区间、真实独立实验或因果识别。
E1 新增有界数学结果1项；E2 新增0；E3 新增0；外部独立复现0。
原 R166 `CLOSED_BOUNDED_E1` 不变；R073 与 PESEN v0.1 冻结，个人决策产品暂停。继续逐项完成 R 系列后再分类与熔炼。
