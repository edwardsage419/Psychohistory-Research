# R269 交叉验证：完整群组留出与逐行留出（11-029，P0）

科研状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_GROUP_CROSS_VALIDATION**。九个冻结人工world由三种独立6群组Bernoulli(p)生成率与三种模型构成，64×9=576条原source，六组每组两条相同标签，共12个相关行，不可当作12个独立组。

[事前冻结协议](../../protocols/R269_GROUP_VS_ROW_CROSS_VALIDATION_576_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [源码](r269_exact_group_cross_validation.py) · [全部576原来源和逐行预测CSV](R269_ALL_576_ORIGINAL_CLUSTERED_CV_SOURCE_TYPES.csv) · [九world与18设计评分结果](R269_EXACT_RESULTS.json) · [SHA256证据](R269_MACHINE_RECEIPT.json) · [科研报告](R269_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](R269_FINAL_ACCEPTANCE_STATUS.json)。

同组记忆器LOOR逐行留出时因复制行仍在训练中，精确预测损失0；LOGO整组留出时未知组回退半概率，精确损失1/4。全局Laplace预测在p=1/4或3/4时LOOR与LOGO平均Brier分别31/169和31/144；p=1/2时分别41/169和41/144。两套训练集大小不同，差异不应全部归因于纯泄漏。

[正式GitHub CI run39902238505](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39902238505)三job全部success；Python3.11和3.12各83项真实单测，共166项，通过独立人工来源全CSV解析折次审计，并永久归档[commit23b88012](https://github.com/edwardsage419/Psychohistory-Research/commit/23b88012cc4811666aa47d51e16f2df3d79e9760)。

新增真人E2=0，真实历史E3=0，R073/PESEN v0.1冻结；下一原目录11-030 Posterior Predictive Checks（拟R270），仍按全R学习完成后再统一分类与熔炼。
