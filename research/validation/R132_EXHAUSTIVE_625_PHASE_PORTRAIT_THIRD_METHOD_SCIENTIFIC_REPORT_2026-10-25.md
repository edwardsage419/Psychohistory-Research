# R132 第三方法：625个二策略复制子相图完整有限格点科研审计

日期：2026-10-25。original239 05-008，既有R132继续保持历史限定结题；本报告是独立增量 E1 复审，不覆盖旧结论。R073 与 PESEN v0.1 冻结。

## 来源与严格执行顺序
一手机制为 Taylor & Jonker (1978), *Evolutionarily Stable Strategies and Game Dynamics*, Mathematical Biosciences 40:145–156，DOI 10.1016/0025-5564(78)90077-9，连续复制子 Eq2。全部625个2×2整数支付矩阵均为本项目自造的有限数学参数世界。

事前冻结：`research/validation/R132_EXHAUSTIVE_625_TWO_STRATEGY_PHASE_PORTRAIT_PROTOCOL_FREEZE_2026-10-25.md`，blob `ef7dbdfa5214f2ab02525f635fc5198829aa8a8e`，先于代码与结果归档。
第三方法源码：`research/validation/r132_exhaustive_625_phase_portrait.py`，blob `9c0f2c7ea480353741945ffc3f6d181d16b4ac2b`。
原始完整分类CSV：`research/validation/R132_EXHAUSTIVE_625_TWO_STRATEGY_PHASE_PORTRAITS_2026-10-25.csv`，625行，18,927字节，blob `6f1a5b18c5fd11aba9a656fa5667516334499e30`。
未修改原R132源码：`research/R132/r132_replicator_1978_exact_invariants_and_trajectories.py`，Git blob `850c01c0a4be95f7884d29e1b9d5ebe15de5f5b8`，由新审计程序在CI中重新计算Git blob身份并实际导入执行。

## 实际计算与分类
遍历 `a,b,c,d∈{−2,−1,0,1,2}` 共625个完整矩阵，每个矩阵按七个冻结初始份额 `x∈{0,1/10,1/4,1/2,3/4,9/10,1}` 计算，合计4,375个严格有理数场比较。新算法使用端点纯策略收益差 `B=b−d` 与 `G=a−c` 的线性 Bernstein 插值，形成 `x(1−x)[(1−x)B+xG]`；另独立以四个原支付直接计算 `x(F_A−Fbar)`。在GitHub CI中再调用原R132未经修改的 `source_original_eq2_exact_field`，4,375/4,375个两维导数完全一致。

完整相图分布：
* A 在全部内点单调增长：200个（含弱端点退化）。
* B 在全部内点单调增长：200个。
* 内点不稳定阈值、两侧不同吸引域：100个。
* 内点稳定共存：100个。
* 全部内点为固定点的中性连续族：25个。

内部固定点严格等于 `x*=−B/(G−B)`，只在端点差异号时存在。全部内点左右侧方向经精确Fraction检查。无内部固定点时检查三个额外非端点份额的导数方向。两种故意错误的竞争计算（反向选择符号、以自身适应度替代总体均值）在固定非退化条件下均被明确拒绝。CSV由原脚本在CI中再生，`git diff --exit-code`通过，确认归档原始行字节未改变。

## 真实CI与科学证据范围
新CI工作流 `.github/workflows/r132_exhaustive_625_phase_portrait_e1.yml`，blob `ac2e66403213222b11f9cdc5bd34311d770b4520`。
GitHub Actions run `40122506509`，head `fc4b72922be3646377f01e2bb94cef0154c37ff2`，job `120956914764`，`completed/success`，日志已实际读取。日志打印 `original_unchanged_source_executed=true`、`original_source_exact_matches=4375`、全部五类正确计数、`negative_controls_rejected=2`。原R132 70项单元测试在同一作业中实际通过，0失败。

结论：`PASS_BOUNDED_INTERNAL_EXHAUSTIVE_625_THIRD_METHOD_E1_CI`。算法在本项目内独立实现，但使用同一个原始数学模型、同一有限格点和同一冻结支付解释，不能等同外部团队复现。分类覆盖的是625个整数支付矩阵，并非所有实数矩阵的独立计算枚举；相图一般性需数学推导。精确数学结果没有训练集、测试集、抽样误差或概率校准对象，因此不能据此宣称真实群体预测能力。

新增真人E2预测0，新增历史E3预测0。未测量任何真实个体的收益、演化速度或行为频率；无外部独立数据。旧R132两批CI与本次新CI严格区分。

## B审计与A侦察分离
B已检查来源冻结、无参数调优、边界退化、符号负对照、原源码身份、真实CI和有限证据范围。A另在 `research/data_scout/ANDREOZZI_PLONER_SARAL_2020_FIXED_GIT_1340_ROW_SOURCE_AUDIT_2026-10-25.md` 实际读取1340行真人三水平互动记录，但R073二元冻结评分不能直接套用。

本轮不修改original239共享交叉索引，保留既有154项待核队列及R127协议偏差。目录完整性与科学有效性分开记录。公开仓库标准Ubuntu runner依据GitHub官方政策免费；未使用收费API、GPU或大型runner，未读取账户账单。
