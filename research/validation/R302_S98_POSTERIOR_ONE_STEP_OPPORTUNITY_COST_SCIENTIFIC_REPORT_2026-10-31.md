# R302 S98 科学报告：有限后验下一次决策的机会成本

UTC日期：2026-10-30。目标键：(r,R302,S98-v1,posterior_predictive_one_step_opportunity_cost)。
事前冻结：research/validation/R302_S98_POSTERIOR_ONE_STEP_OPPORTUNITY_COST_PRESCORE_FREEZE_2026-10-31.md，commit cfd7991944488c4424870d00cb94e7174d6aefa4。
原R302正式验收状态及全部原文件保持不变。新增研究属于有限人工E1。

## 原始理论、版本及研究问题

原R302对应原始239目录02-016 Multi Armed Bandits。Thompson (1933), *Biometrika*, DOI 10.1093/biomet/25.3-4.285；Auer等(2002), *Machine Learning*, DOI 10.1023/A:1013689704352。
读取原R302完整冻结协议、81世界/162来源报告、Python Beta后验计算源码及原始CSV（Git blob 628c7db9b6d046dc20a63651773d8444ee53857e）。本研究只在既定81个人工后验计数世界上评估一次行动的后验期望奖励，探索的未来信息收益不纳入目标函数。

对每个世界，m_A和m_B为Beta后验均值，p为Thompson选择A的概率。贪婪奖励=max(m_A,m_B)，Thompson奖励=p m_A+(1-p)m_B，均匀随机奖励=(m_A+m_B)/2。机会成本为贪婪奖励减去相应奖励。所有值用Python Fraction精确计算，原始162行后验概率与本轮81世界逐一配对核对。

## 实际计算结果

81个人工世界完整记录：research/validation/R302_S98_ALL_81_POSTERIOR_ONE_STEP_WORLDS.csv，Git blob ec23bcd5152d37beda224564b0f723cd107a643f。
机器结果：research/validation/R302_S98_EXACT_POSTERIOR_ONE_STEP_RESULTS.json，Git blob 3989d33bd843300dc932d46adec322a6616d813c。

| 冻结指标 | 精确结果 |
| --- | --- |
| 世界数 | 81 |
| Thompson平均单次机会成本 | 1219/34020，约0.03583186 |
| 均匀随机平均单次机会成本 | 34/405，约0.08395062 |
| Thompson机会成本严格正的世界 | 66 |
| Thompson机会成本为零的世界 | 15 |
| 后验均值相等的世界 | 15 |
| 最大Thompson机会成本 | 1/16 |
| 最大成本对应世界 | A=0,0 B=0,2；A=0,0 B=2,0；A=0,2 B=0,0；A=2,0 B=0,0 |

参考世界：A成功1失败0，B完全未观测时，p=2/3，m_A=2/3，m_B=1/2，Thompson机会成本1/18。A成功2失败0、B成功0失败2时，p=19/20，成本1/40。相同后验均值时，单次机会成本严格为零，尽管Thompson行为可能仍随机。

### 解释与反例

在当前一次性、线性后验期望奖励目标下，后验均值贪婪策略始终不劣于Thompson。66个非平局世界中Thompson仍有非零概率选择后验均值较低的行动。该成本可能换取未来信息，但本研究没有后续选择、反馈、探索收益或累计遗憾模拟，不能推断多轮最优策略。81世界是人为等权的完整计数网格，平均值不具有真实总体统计含义。

## 实际复算及科学门

本地Python 3标准库执行 R 程序 5个单元测试全部通过，并生成81世界CSV、JSON及SHA256收据；本地B程序使用独立交错多项式双重积分，逐世界复算所有主要字段及汇总，8个预设变异全部被拒绝。原始CSV/JSON远端Git blob与本地生成文件Git blob完全一致；归档R/B脚本的原生远端下载后逐字节重放未完成。独立B属于同一项目内部非盲态复核，不属于外部研究团队独立复现。

机器收据 SHA256：CSV fb1364bf9bd1f6a5fa75d9a014d48132a639b5db2cb3bd2c29491787e3582f08；JSON b25cb85e1c380c78afb3d8b36d241ca3af712567227691feb093de230de77862。
B审计详见 research/evidence_audit/B_R302_S98_NONBLIND_DOUBLE_INTEGRAL_AND_EIGHT_MUTATIONS_2026-10-31.md。

A01范围PASS，A02原R302数学及人工来源PASS，A03本地计算PASS而远端原生重放OPEN，A04负例PASS，A05 E1边界PASS，A06新研究独立归档PARTIAL。新增S98状态PARTIAL，原R302 CLOSED_BOUNDED状态不变。真人E2=0，历史E3=0，外部独立复现=0，CI=NOT_RUN。R073及PESEN v0.1持续冻结。下一阶段沿既定R队列研究R303互补问题。
