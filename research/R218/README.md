# R218 倾向评分匹配（09-009）：六人工世界、101来源正式有界E1结题

2026-10-22。原239目录真实编号 **09-009 Propensity Score Matching（P1）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_PROPENSITY_STRATIFICATION**。

[正式科学报告](R218_SCIENTIFIC_REPORT_2026-10-22.md) · [原计算前冻结](../../protocols/R218_PROPENSITY_6_WORLDS_101_ORIGINAL_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md) · [六世界精确结果](R218_EXACT_RESULTS.json) · [101条完整人工处理原分配数据CSV](R218_ALL_101_ORIGINAL_PROPENSITY_ASSIGNMENT_SOURCES.csv) · [SHA机器验收](R218_FINAL_MACHINE_ACCEPTANCE.json) · [事后正式科学结题收据](R218_FINAL_ACCEPTANCE_STATUS.json) · [原生Python与34单测](r218_exact_propensity_matching.py)。

八个人工单位有预观察X∈{0,1}，隐藏人工U∈{0,1}，每世界真有限ATE固定2；六个处理配额/选择机制世界，全部101条真正人工处理分配原来源。处理分配单位均有明确真发生概率，只有观察X/Yobs/Z可进入观察估计器。已观察倾向分数e(X)按冻结配额为1/4|3/4、1/2|1/2或0|1。方法是完全X子层多对多配对及人口加权，**不是最近邻匹配**；平衡时X匹配比仅用相等e(X)更细，必须保留差别。

六世界估计期望（真实ATE均2）：可观测X混杂世界，未匹配3、X匹配2；隐藏共同原因世界，未匹配15/4=3.75、X匹配3、知道真个体包含率的**oracle** HT为2；隐藏U选择但结果与U无关世界，X匹配2；处理效果异质世界X匹配2；配额平衡世界X匹配与未匹配每条原来源完全相同；**无共同支持世界e(X)=0|1，naive=4但X匹配/HT明确null，不伪造真效应估计**。真个体处理率p_i需要未观测U或真完整选择机制，不是使用观察e(X)可获得的现实倾向资料。

[GitHub Actions run39746158457](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39746158457)：Python3.11/3.12各34项、合计68全过，第三原来源/双Fraction/SHA数据永久归档success，机器人[原数据提交f20ab94a](https://github.com/edwardsage419/Psychohistory-Research/commit/f20ab94a181125c994f25a58e415f74b187964f9)。研究只有人工E1，新增真人E2=0、历史E3=0，R073/PESEN v0.1继续冻结。

下一真实目录 **09-010 Inverse Probability Weighting（R219）**。完成原R全系列后统一分类，最后熔炼。
