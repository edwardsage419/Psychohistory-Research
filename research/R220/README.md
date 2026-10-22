# R220 双重稳健估计（09-011）：七人工世界、1537原真赋值E1结题

日期2026-10-22。原239目录 **09-011 Doubly Robust Estimation（P2）**。科研状态**CLOSED_BOUNDED_E1_ARTIFICIAL_AIPW**。

[正式科学报告](R220_SCIENTIFIC_REPORT_2026-10-22.md) · [评分前模型/来源冻结协议](../../protocols/R220_DOUBLY_ROBUST_7_WORLDS_1537_ORIGINAL_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md) · [全部七人工世界精确结果JSON](R220_EXACT_RESULTS.json) · [1537完整原真处理赋值及五种估计输出CSV](R220_ALL_1537_ORIGINAL_AIPW_ASSIGNMENT_SOURCES.csv) · [SHA机器验收](R220_FINAL_MACHINE_ACCEPTANCE.json) · [正式事后科研验收收据](R220_FINAL_ACCEPTANCE_STATUS.json) · [原生Python和38单测](r220_exact_doubly_robust_aipw.py)。

固定八人工个体、公开X、隐藏U、七种倾向/结果模型正确或错误真来源；前六世界256独立Bernoulli真赋值各一、第七正值性失败唯一原源，完整**1537原赋值数据**。评估只依赖公共q(X)及m0/1(X)、Z及实际Yobs的AIPW，单独对照仅HT、仅结果回归以及不允许公共算法使用的知道每人真p、两种完整潜在结果的人工oracle。全部真实来源期望和方差与独立无源枚举的解析Bernoulli Fraction公式完全一致。

真实ATE均2。倾向和结果都对、只有倾向对、只有X层结果正确的AIPW期望均为**2**；两者都错则AIPW期望**3**。即便q与m均为真正公开X层条件均值，隐藏U同时影响处理及结果且条件交换性失效时AIPW期望**8/3**。在p=1/16或15/16的弱重叠世界q正确、m错误，AIPW期望2但方差高达**1937/120**；完全正值性失败则所有公共因果估计严格null。**正确一模型不是所有假设都免除**，此结论不能替代真人因果验证。

[GitHub Actions run39751096555](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39751096555) Python3.11及3.12各38单测、**76项全部通过**，第三原全源与SHA永久归档job success，[机器人完整原结果提交54491d77](https://github.com/edwardsage419/Psychohistory-Research/commit/54491d772cc93116d826a4ad4da68a25327c0930)。人工E1，真人E2=0、历史E3=0；R073及PESEN v0.1继续冻结。下一真实原目录 **09-012 Causal Mediation Analysis（R221）**。仍先完成全部239条R模型研究，再归纳分类，最后熔炼。
