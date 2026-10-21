# R202 加速失效时间 AFT，正式人工 E1 有界结题

2026-10-21，原239模型目录P2/08-026。**CLOSED_BOUNDED_E1_ARTIFICIAL_DISCRETE_AFT**。

事前[冻结协议](../../protocols/R202_AFT_6_WORLDS_96_SOURCE_TRAINING_PRESCORE_FREEZE_2026-10-21.md)，后续严格枚举三种时间倍率a∈{1/2,1,2}、两种删失截止C∈{2,4}的**6个人工世界与96个有序来源训练组合**，标准库Fraction双方式严格校验被删失样本候选likelihood，模型只看人工两名训练人的实际观察资料。独立第三人的时间目标为T≤3，Brier与logloss按所有未来真事件状态积分。

[正式科学报告](R202_SCIENTIFIC_REPORT_2026-10-21.md) · [完整6世界机读结果](R202_EXACT_RESULTS.json) · [96条原训练CSV](R202_ALL_96_ORIGINAL_CENSORED_TRAINING_WORLDS.csv) · [机器哈希验收](R202_FINAL_MACHINE_ACCEPTANCE.json) · [Python原源码与24单测](r202_exact_discrete_aft.py)。

固定a1未来Brier 0.25。真a1/2在C2观察下训练选择后独立新事件Brier **0.28125**，C4下0.234375；真a1在C2/C4分别0.28125/0.265625，均不及已知真a1；真a2在C2/C4分别0.203125/0.21875，观察窗口增加时这一有限拟合程序的独立预测反而变差。已准确区分观测时刻2的删失与同刻事件，a2、C2、x1前者概率3/4，后者1/4。与R201事件身份风险目标完全区分，且a2的离散事件风险率组间比在t2、t4分别为3/4和2/3，不能一般当作比例风险系数。

[GitHub Actions run 39597684034](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39597684034)两Python版本各24项共48通过，加上第三原资料完整归档job全部success，[完整结果写回main提交54f27587](https://github.com/edwardsage419/Psychohistory-Research/commit/54f2758729233dab18e841dfb654f611386cac41)。仅数学E1，新增真人E2=0、历史E3=0，R073/PESEN v0.1仍冻结。

**下一R203 P1/08-027 Spatial Regression**，所有R完成后再统一分类、再熔炼。
