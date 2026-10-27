# R213工具变量：八单位有限样本Wald比率不稳定性第三方法科学报告

日期：2026-10-27。原始239目录09-004。证据等级E1，人工完整枚举。新增有限方法，不改变R213原2026-10-22正式有界验收。R073及PESEN v0.1保持冻结。

## 研究问题和事前冻结
原R213通过八个人工潜在类型及128条“随机抽取一个类型与鼓励”的来源原子精确检验人口Wald和LATE。原报告明确没有进行有限样本弱工具分布检验。本轮在已有八单位潜在类型表上，事前冻结了新的完整八单位鼓励赋值实验，直接回答：即使人工人口工具满足有效性假设，八单位有限样本的Wald比率会出现哪些未定义和极端结果？

新增协议 `protocols/R213_FINITE_EIGHT_UNIT_WALD_ASSIGNMENT_THIRD_METHOD_FREEZE_2026-10-27.md` 在评分前独立提交，保留八世界、原处理机制、真实潜在结果和个体鼓励概率，锁定全部256种二元赋值向量、概率、阈值和未定义规则。八世界共2048个向量。原 `research/R213/R213_ALL_128_ORIGINAL_INSTRUMENT_SOURCE_ATOMS.csv` 的SHA256为 `071e2eb91185fd7c47d6534363e322ee5f0349862995dfa20dd84542c7d8fe48`，未经修改。

## 完整精确结果
每世界256种赋值，空鼓励组、样本first stage为0和可定义Wald三类互斥。以下均为人工赋值分布上的精确值，均非真人估计。

|人工世界|人口Wald|真实complier LATE|空组数|样本first stage为0数|可定义数|可定义条件Wald均值|P(\|Wald\|≥10)|
|---|---:|---:|---:|---:|---:|---:|---:|
|FULL_COMPLY|5/2|5/2|2|0|254|5/2|0|
|MONOTONE_MIX|3|3|2|6|248|3291/1240|23/256|
|WEAK_COMPLIERS|4|4|2|34|220|254/825|19/256|
|NO_COMPLIERS|未定义|无complier|2|68|186|2|0|
|WITH_DEFIERS|0|2|2|26|228|1537/1995|15/256|
|EXCLUSION_VIOLATION|5|3|2|6|248|113663/26040|47/256|
|WEAK_EXCLUSION|12|4|2|34|220|8513/11550|23/128|
|Z_CONFOUNDING|29/2|3|2|6|248|40470621/2271080|24533/32768|

前七世界每个向量概率1/256。Z_CONFOUNDING世界按个体原冻结的鼓励概率乘积计权，故虽然各世界的256种向量数量相同，Z_CONFOUNDING的概率质量不可按1/256处理。该世界空组概率81/32768、样本first stage为0概率243/32768。八世界每个赋值概率和严格为1。

## 两个关键反例
**弱工具的有限样本放大与比率选择。** WEAK_COMPLIERS人口first stage为1/8、人口Wald与真实LATE均为4；在256种有限赋值中，34种出现零样本first stage、2种鼓励组为空。其余220种的Wald条件均值为254/825，约0.308。无条件概率3/4的赋值产生可定义且绝对误差至少2的Wald。该结果直接说明人口识别等式在本人工设计下不保证小样本比率估计接近LATE。对未定义比率保持缺失，禁止按0填充。此处不计算标准误、置信区间覆盖或弱工具渐近推断。

**零人口第一阶段仍可能产生非零样本第一阶段。** NO_COMPLIERS世界八人均为ALWAYS或NEVER，真实鼓励无法改变任何人的处理，人口first stage严格为0，人口Wald未定义。有限样本随机分配却在186种向量中产生非零样本first stage和数值Wald，条件均值恰好为2，最大绝对值5。这个数值不能证明因果识别成功，原因是随机分组造成固定处理类型比例差异，真实工具相关性仍为零。

另一个有效IV世界MONOTONE_MIX的人口Wald和LATE均为3，可定义条件Wald均值3291/1240，且23/256的全部赋值给出绝对值至少10的比率。有效的人工总体识别条件与小样本稳定性必须分别评价。

## 独立路线和证据范围
R主程序 `research/validation/r213_eight_unit_assignment_exact_20261027.py` 导入原R213冻结的人工生成函数，直接枚举256个八单位鼓励向量。B轨 `research/evidence_audit/b_r213_eight_unit_dp_independent_20261027.py` 独立读取原128行CSV，使用充分状态概率动态规划聚合，不调用R轨枚举函数。B轨对每世界14个精确字段，合计112项逐项核验一致，并对故意改变原观察结果的负对照成功检出差异。原始人口Wald与冻结R213原结果回归一致。

正式主收据为 `research/validation/R213_FINITE_ASSIGNMENT_8_WORLD_REPLAY_MATCHED_RECEIPT_V2_2026-10-27.json`。最早的 `R213_FINITE_ASSIGNMENT_8_WORLD_RECEIPT_2026-10-27.json` 数值字段一致，JSON键排序与Python标准库序列化不同，已保留为V1历史记录；V2严格对应原脚本逐字节输出。B审计收据在 `research/evidence_audit/B_R213_FINITE_ASSIGNMENT_DP_AUDIT_RECEIPT_2026-10-27.json`。

本轮所有数值来自八单位人工机制的完整概率枚举。它不验证任何现实工具变量的独立性、排除限制或外部效度，也不建立真实弱工具置信区间覆盖。没有E2真人预测、E3历史预测或外部研究团队独立复现。当前新提交的远端CI运行须另行核验，禁止把本地精确复算写成CI通过。

## 复现
从仓库根目录执行 `python research/validation/r213_eight_unit_assignment_exact_20261027.py`，应得到与V2主收据逐字节相同的标准输出。执行 `python research/evidence_audit/b_r213_eight_unit_dp_independent_20261027.py`，应得到与B轨审计收据逐字节相同的标准输出。均使用Python标准库，不调用网络或收费计算。原R213正式验收状态保持 `CLOSED_BOUNDED_E1_ARTIFICIAL_BINARY_IV`。后续可按原队列继续R214回归不连续设计的第三方法。
