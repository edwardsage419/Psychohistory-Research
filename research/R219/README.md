# R219 逆概率加权（09-010）：1281真赋值来源及有限偏差-方差识别E1结题

日期2026-10-22。真实原239目录 **09-010 Inverse Probability Weighting（P1）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_IPW**。

[正式科学报告](R219_SCIENTIFIC_REPORT_2026-10-22.md) · [原计算前冻结协议](../../protocols/R219_IPW_6_WORLDS_1281_EXACT_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md) · [六人工世界完整JSON](R219_EXACT_RESULTS.json) · [1281真处理赋值及各HT/ratio实际结果CSV](R219_ALL_1281_ORIGINAL_TREATMENT_ASSIGNMENT_SOURCES.csv) · [原数据SHA机器验收](R219_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题机读收据](R219_FINAL_ACCEPTANCE_STATUS.json) · [Python程序与39单测](r219_exact_inverse_probability_weighting.py)。

六个固定八人工单位来源世界，前五各全部256种独立Bernoulli赋值、最后正值性失败仅一原来源，完整1281来源真实概率逐Fraction和1。公众只知观测协变量X与预先给定的层内真实e(X)，不读隐藏U；oracle额外知每人真选择p。四套固定HT：正确公开e(X)、特权每人真p、故意错固定1/2、公开clip[1/4,3/4]；另计算处理/对照自归一Hájek并明确记录空处理/对照导致undefined情况与条件来源概率，不和HT无条件期望混淆。20套固定HT来源积分均值方差与独立Bernoulli解析公式逐Fraction完全一致。

全部六世界真ATE=2。公共e(X)正确且可观测交换性成立时HT期望2；隐藏U既影响治疗选择又影响Y0时，即使公共e(X)正确为层均值，公共HT期望**8/3**且偏差**+2/3**；U仅影响选择时仍HT期望2。弱重叠p=1/16/15/16下未裁公开HT方差**257/30**，裁剪后最大倒数权重由16降4、方差**85/96**，但期望2变**5/2**产生偏差1/2。完全不正值时所有因果HT与Hájek输出严格null状态`UNIDENTIFIED_NO_POSITIVITY`，不会冒充识别。

[GitHub Actions run39749875165](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39749875165) Python3.11及3.12各39单测，共**78全部成功**，第三归档job也success；[原全部数据机器人永久提交e75fd5dc](https://github.com/edwardsage419/Psychohistory-Research/commit/e75fd5dc9452b3ca02d972e690f8746619c7b568)。

**仅人工E1，新增真人E2=0、真实历史E3=0**，R073/PESEN v0.1继续冻结。下一原239目录 **09-011 Doubly Robust Estimation（P2）**，连续研究R220。完成全部原R后统一分类、最后模型熔炼。
