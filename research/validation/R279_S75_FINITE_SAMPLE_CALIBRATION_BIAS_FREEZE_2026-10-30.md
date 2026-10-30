# R279 S75 有限样本校准分解偏差，探索性协议冻结

日期：2026-10-30 UTC。目标键：(r,R279,original-R279-prescore+S75-v1,finite-four-bit-empirical-vs-population-calibration)。研究类型：新补充的非盲态 E1 精确数学研究。已阅读原 R279 九世界结论及公式，事前盲态不成立。本冻结先于 S75 结果脚本和归档收据执行，不能反向改变原 R279 的冻结或正式验收。

## 研究问题与来源
原 R279 固定三种真 DGP：CALIBRATED_RATE=(1/4,3/4)、DETERMINISTIC_GROUP=(0,1)、INVERTED_RATE=(3/4,1/4)。每个世界 L1,L2,H1,H2 四个独立 Bernoulli 位；三政策 ORIGINAL_BUCKETS=(1/4,3/4)、FLAT_HALF=(1/2,1/2)、REVERSED_BUCKETS=(3/4,1/4)。九个 DGP/政策世界各16个完整有序来源，保留零质量来源，合计144行。引用原冻结 protocols/R279_FORECAST_CALIBRATION_9_WORLDS_144_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md。理论来源 Murphy (1973), DOI 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2。

## 新增冻结统计量
对每条四位来源，按**相同预测概率 q 合并桶**，样本桶权重 w=n_q/4，桶内经验率 o_q=成功数/n_q，总经验率 o=四位成功数/4。定义 empirical_REL=sum w(q-o_q)^2；empirical_RES=sum w(o_q-o)^2；empirical_UNC=o(1-o)；sample_Brier=四个逐位平方误差的均值。逐来源检验 sample_Brier=empirical_REL-empirical_RES+empirical_UNC。

对每个 DGP/政策，用原始完整来源概率加权得到 E[empirical_REL/RES/UNC/sample_Brier]，与原 R279 population REL/RES/UNC/Brier 比较，记录偏差。另记录 P(empirical_REL=0) 与 P(empirical_REL<=population_REL)。九组全覆盖，精确有理数输出。零概率来源保留并核验概率质量为0。

## 方法上独立的对照路线
R 路线直接枚举16个四位有序来源。B 路线按两组成功次数 kL,kH 的独立二项分布乘积共9个组合计算，不能调用 R 路线的四位来源表；各桶样本率由计数构造。额外使用方差公式检查：vL=thetaL(1-thetaL)，vH=thetaH(1-thetaH)；FLAT_HALF 的 E[empirical_REL]-population_REL=(vL+vH)/8，E[empirical_RES]=0，E[empirical_UNC]-population_UNC=-(vL+vH)/8；其他两桶政策的 REL 偏差=(vL+vH)/4，RES 偏差=(vL+vH)/8，UNC 偏差=-(vL+vH)/8。两路线所有统计量必须完全相等。

## 判定、停止及证据范围
若任何九组来源质量、逐来源分解恒等式、二项路线、解析偏差或原 R279 population 风险不一致，记录 FAIL 并停止宣称计算完成。禁止事后改变阈值、政策、来源、评分。结果仅是人工 E1 有界数学反例；不得推广到真人预测或经验校准的实际有效性。R073 模型及评分、PESEN v0.1 冻结。E2/E3=0。CI 仅在费用明确免费后才可启动，否则 NOT_RUN。