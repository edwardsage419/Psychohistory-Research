# R248 S44 有限轨道收缩与局部吸引误判事前冻结

日期：2026-10-29（Asia/Singapore）。轨道：R 系列主线。证据等级：E1 人工精确数学。状态：PRESCORE_FROZEN。原 R248 正式验收与其 2026-10-23 原协议均不修改。

## 固定数据与预测问题
仅使用 research/R248/R248_ALL_405_EXACT_MAP_IVP_TIME_SOURCES.csv 的九种原映射、每种九条原初值轨道、n=0,1,2,3,4 共405行。原 CSV Git blob c5eec783ab4199a1824a7fe36b0dfef1bde2b18b，SHA256 cb7fdcc35c212995a2c9d6f520c23d6f351d3b0c834bd6da50343884b553995b。原始研究已通过的局部固定点证明是数学基准，不将五点轨道当成独立样本。

每个 world 预先选择一个参照固定点，顺序与原九世界相同：
AFFINE_CONTRACT_ZERO=0；AFFINE_CONTRACT_ONE=1；AFFINE_ALTERNATE_CONTRACT=0；AFFINE_EXPAND_ZERO=0；IDENTITY_EVERY_POINT_FIXED=0（只作为参照，全实数均固定）；LOGISTIC_R2=1/2；LOGISTIC_R3_BORDER=2/3；LOGISTIC_R4_REPELLER=3/4；CUBIC_NONHYPERBOLIC_ATTRACTOR=0。
其局部数学类型预先固定为：ATTRACTOR、ATTRACTOR、ATTRACTOR、REPELLER、NEUTRAL、ATTRACTOR、ATTRACTOR、REPELLER、ATTRACTOR。

## 预注册指标
对每条原初值轨道，精确计算 d0=|x0-x*|、d4=|x4-x*|。若 d0=0 则 finite_label=AT_FIXED_EXCLUDED；若 d4<d0 则 SHRINK；若 d4=d0 则 TIE；否则 EXPAND。额外记录四个逐步距离、首次精确到达固定点时刻（若在n=0..4出现）、以及有限收缩比 d4/d0（d0>0）。
按世界统计每类个数；误判警报为局部REPELLER或NEUTRAL的SHRINK，以及局部ATTRACTOR的EXPAND。此警报仅用于审计有限观察判据，不能解释为原解析稳定性证明被推翻。
预先指定负对照：LOGISTIC_R4_REPELLER的x0=1/4是排斥固定点3/4的精确前像，预期有限SHRINK；IDENTITY_EVERY_POINT_FIXED的非零x0预期TIE；AFFINE_EXPAND_ZERO的非零x0预期EXPAND。对LOGISTIC_R3_BORDER x0=3/4在已证明的局部邻域边界进行单独标注。
不得以看过结果后的方式变更固定点、初值、观察时域、分类阈值或负对照。

## 验收与审计
R 路线从原CSV按(world,x0,n)重建轨道、检验唯一性与连续时点、各world 45行及每行概率1/45，计算81条轨道及统计。B 路线独立以原R248固定有理映射公式迭代九初值四步，计算同样的距离标签；逐项比较81条轨道的五点距离和分类，并做一次人为错误注入。两路线都使用精确整数/有理数，不使用浮点阈值。
报告须给出实际检查数、失败数、原始文件身份、算法独立性限制、E1/E2/E3边界、未完成项及CI实测状态。所有输出仅新增 research/validation/ 与 research/evidence_audit/ 的 S44 独立路径。A 轨只登记经来源验证的公开候选，优先复用既有候选做实质访问缺口复核。
禁止修改 R073、PESEN v0.1、original239、154待核队列及其他轨道文件。不得以本轮结果改写原R248正式验收或声称真实社会动力预测。