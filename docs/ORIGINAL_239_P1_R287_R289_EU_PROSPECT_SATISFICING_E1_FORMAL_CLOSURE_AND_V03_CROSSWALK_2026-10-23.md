# 心理史学：原239目录P1前三项补缺 R287—R289 和共享MNL核查，239条目录v0.3科研边界报告

日期：2026-10-23（Asia/Taipei）。执行顺序继续严格遵循：先完成原R研究目录全部模型学习/验收，后统一归纳分类，最后原创模型熔炼。**本轮完成三个独立有界人工数学模型研究，并对第四个原目录P1项目确认共享数学覆盖。** 原始239条唯一候选目录未添加新行，也没有把旧数学研究重复视为真人独立实验。

## 三项新研究均有先于结果的独立冻结

|原始目录|研究编号|先行协议冻结Git提交|完整带标签人工原source|人工世界|实际双Python3.11/3.12测试通过|三job成功的CI|
|---|---|---|---:|---:|---:|---|
|01-001 Expected Utility Theory (P1)|[R287](../research/R287/README.md)|[52421136](https://github.com/edwardsage419/Psychohistory-Research/commit/524211361d5180624d4350559d53112de31139ab)|2304|9|90+90=180|[39910069650](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910069650)|
|01-002 Prospect Theory (P1)|[R288](../research/R288/README.md)|[d94d9d7f](https://github.com/edwardsage419/Psychohistory-Research/commit/d94d9d7f275082a6672fbea0e191ac76a54bed87)|576|9|81+81=162|[39910074038](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910074038)|
|01-004 Bounded Rationality and Satisficing (P1)|[R289](../research/R289/README.md)|[27fa695d](https://github.com/edwardsage419/Psychohistory-Research/commit/27fa695d5e0c612fd77fb3a3fc5af26a543c0a27)|486|6|70+70=140|[39910079877](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910079877)|
|**本轮三研究合计**|—|—|**3366**|**24**|**482**|**9个成功job**|

- [R287正式科学报告](../research/R287/R287_SCIENTIFIC_REPORT_2026-10-23.md)、[正式机读验收](../research/R287/R287_FINAL_ACCEPTANCE_STATUS.json)、完整2304原数据[机器人归档59196ef0](https://github.com/edwardsage419/Psychohistory-Research/commit/59196ef07a62ea8973727c2333c185de1a3be4f2)：有限两彩票与共同后果期望效用。LINEAR的风险偏好和平方根效用轮廓可不同，**在每一固定效用轮廓内部**混入相同后果后EU_A−EU_B只乘(1−λ)，排序不反转。只验证独立性公理的一个人工代数边界；不证明整套vNM表征定理，亦无真实人类实验数据。
- [R288正式科学报告](../research/R288/R288_SCIENTIFIC_REPORT_2026-10-23.md)、[机读验收](../research/R288/R288_FINAL_ACCEPTANCE_STATUS.json)、完整576原数据[归档301c10dd](https://github.com/edwardsage419/Psychohistory-Research/commit/301c10dd25d5bc0a6e827e0c62a15ef8edccd53b)：参考点与损失厌恶限定子模型。当损失系数L=2且参考点r=0时，彩票G(+3/−2各半)比确定0差−1/2；改参考点r=2后，G相对确定0差+1/2，因而模型排序发生参考点反转。**原1979前景理论的非线性概率权重、编辑过程及原作者被试结果并未复算**，只有人工函数数学。
- [R289正式科学报告](../research/R289/R289_SCIENTIFIC_REPORT_2026-10-23.md)、[机读验收](../research/R289/R289_FINAL_ACCEPTANCE_STATUS.json)、完整486原来源[归档cbfbbdca](https://github.com/edwardsage419/Psychohistory-Research/commit/cbfbbdcaf54a45faea84bc0a00f20b396f31cd41)：四报价顺序搜索，三真分布，愿望阈值3/5，每额外查看收费1/2。UNIFORM报价下两阈值期望净收益67/18与100/27；HIGH_HEAVY下则133/32与35/8，证实最佳人工阈值依分布而改变。**完美看到未来所有报价的无成本最高值不是可实施策略**，不能把其差当真人有限理性的损失测量。

原始理论文献锚：von Neumann & Morgenstern (1944), *Theory of Games and Economic Behavior*, Princeton University Press；Kahneman & Tversky (1979), *Prospect Theory: An Analysis of Decision under Risk*, Econometrica 47(2):263–291, DOI https://doi.org/10.2307/1914185；Simon (1955), *A Behavioral Model of Rational Choice*, QJE 69(1):99–118, DOI https://doi.org/10.2307/1884852。**只核查这些公开书目/摘要及项目中有限数学机制，不声称完整阅读并重算所有原论文实验**。

每项有独立源码和CSV来源；[不导入三主模型的第三审计代码](../research/catalogue_audit/independent_r287_r289_source_audit.py)逐源重算全部原始概率、收益/价值、全世界期望、独立公式和SHA256，且三个GitHub Actions独立来源重验作业实际completed/success。三个源全集合并**3366**为不同世界/模型标签的人工source配置，并非独立真人样本数。

## 不重复研究：01-006 Multinomial Logit Choice与既有R111同源概率机制

原239目录01-006仍属于P1尚无专属主R候选。经审查[R111随机效用数学研究](../research/R111/README.md)及其真实[conditional_logit源码](../research/R111/r111_mcfadden_random_utility_conditional_logit.py)，已实现多备选系统效用的指数归一化概率、可用集合及误差尺度；[R111机读验收](../research/R111/R111_PHASE_A_SYNTHETIC_MATH_CI_ACCEPTANCE_STATUS.json)明确其主目录身份仍01-005、18项人工单测和真人E2=0。

因此01-006在[新v0.3目录交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.3_2026-10-23.json)只标记`SHARED_R111_MULTINOMIAL_LOGIT_FORMULA_NOT_SEPARATE_EMPIRICAL_ESTIMATION`：**已经学过概率机制，但没有独立新研究成果、没有从真实被试选择拟合多项Logit系数**，不会伪造独立实验，也不增加R序列主编号。

## 原239项目录精确状态（v0.2 → v0.3）

|结构/映射状态|v0.2|v0.3|本轮改变|
|---|---:|---:|---|
|已找到后期主R研究链接|174|**177**|+3，新R287/R288/R289|
|共享旧主R核心数学机制，且不额外算独立研究|2|**3**|+1，01-006→R111|
|旧叠加表有相关资料但仍缺主R对应|5|**5**|不变|
|本轮检查来源均尚无对应线索|58|**54**|−4|
|仍需核主R链接的原目录条目|63|**59**|−4|
|原始目录候选总数|239|**239**|未更改|

新的[59项剩余待核P1/P2原目录CSV队列](ORIGINAL_239_PENDING_59_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 32，P2 27，当前已解决三个原P0的有限数学学习归属。但**主研究链接不是实证验证完成、人工测试不是人类样本、归档完整也不是历史外推**。已有177项主链接的科学范围仍有逐项验收任务。

## 源级交叉索引的独立机器复验

[239行P1 v0.3机读审核程序](../research/catalogue_audit/verify_p1_crosswalk_v0_3.py)：逐行与原239目录及v0.2比对，只有01-001、01-002、01-004、01-006四行允许变化；分别读取三个新R正式验收和R111旧源码/原始验收，SHA/hash和链接一致。正式[GitHub Actions run39910417014](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910417014)双Python3.11/3.12各250个真实单测共**500通过**，第三完全独立对照239项与SHA，三个job completed/success。机器人永久归档[目录对账机读结果](ORIGINAL_239_P1_R287_R289_CROSSWALK_MACHINE_RESULTS.json)及[完整SHA256凭证](ORIGINAL_239_P1_R287_R289_CROSSWALK_SHA256_RECEIPT.json)，GitHub提交[13d2e0c0](https://github.com/edwardsage419/Psychohistory-Research/commit/13d2e0c0f40d289fd248411058a3942a89e9ea16)。

本轮**总计三项科学研究482次unit tests + 239行目录审计500次 = 982次真实测试、四个成功CI运行共12个成功job**。全部只有E1数学/档案审查；新增真人E2=0、独立历史E3=0；R073和PESEN v0.1保持冻结。

下一原目录待核优先条目依原队列为**01-011 Signal Detection Theory**，之后01-013 Theory of Reasoned Action、01-014 Theory of Planned Behavior、01-016 Schwartz Basic Human Values等。继续查旧研究材料、共享数学覆盖及实际独立科研缺口，不能为了凑数量在一个机制上重做过量人工实验。始终遵循：全部R学习完成后才统一归纳分类，最后开始熔炼。
