# R089：171个完整六人群体五折留出下一轮合作预测，加入实验前社会认同（正式有界结题）

**2026-10-17：R089=CLOSED_BOUNDED，原作者回顾性E2组间完整留出预测成立；E3新外部实验、身份心理因果、历史层因果继续OPEN；PESEN v0.1继续FROZEN。**

基于原作者Pilgrim/Stewart/Raihani（*Scientific Reports* DOI [10.1038/s41598-025-30979-2](https://doi.org/10.1038/s41598-025-30979-2)）2025/2026已发表数据，由R088固定 Git blob 完整组CSV、原始R脚本及身份认同作者原始时间标签再核验。171个6人组×20轮、3处理各57组，原始1026人、20520人轮机会中64项行为缺失。受试者实验前全球群体认同DIFI原始值在全部171组具备六人完整合法测量，**仅实验前`survey.1.player.DIFI_big_group_distance`** 被允许用于模型；game.5/10/15/20与事后问卷没有使用。

[完整留出5折评分前冻结协议](../../protocols/R089_171_GROUP_COMPLETE_HOLDOUT_HISTORY_AND_BASELINE_IDENTITY_PREDICTION_FREEZE_2026-10-17.md) commit `8f303a8e7b4e2275f177d3e50aa903dd199d48b7`：三个处理每个57组六人群体按固定SHA-256顺序分折为12/12/11/11/11，全部六人及20轮同属一折。训练只用另外45/46个群体，目标本群体前一轮历史可用于下一轮在线预测（不使用该群体将来行动拟合）；t=2至20原始171×19共**3249个完整留出群体-轮预测目标**。M0是其他训练群体同条件同轮均值，M1本群体上一轮全球投资比例，M2两者各半，M3在M2上加小规模仅从训练群体拟合的实验前社会认同一维岭项。实际结果对六人组目标未知global人数穷举可行整数 `k/6` 的平方预测误差**锐界**，不是confidence interval、也未插补个体缺失行动。

[首轮CI39012760897](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39012760897)因合成测试函数名Python语法错误而在任何真人计分前失败，保留负证据；仅修复测试名commit `50bb91a61b11274f94a2e4c9c3c79fec241bcba6`，没修改模型协议及真人程序。[首次真正原始171组六人群体五折成功评分CI39012803376](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39012803376)，40项合成PASS、五原作者Git blob精确、完整3249个原始真正后续轮预测成功。[二次独立原始数据重新取回与全评分SHA逐字节归档CI39012889699](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39012889699)，40synthetic和真实171组完整评分再次SUCCESS；最终[匿名全部组条件/折/模型真实结果](R089_ORIGINAL171_GROUP_FIVEFOLD_HISTORY_VS_PREGAME_IDENTITY_SHARP_E2_RESULTS.json) **20,052字节，SHA256 `9dda5e5fbf4abe2a9d9e7d2fb029e03eb81202c63f0e0af576b7e69882aea266`，Git blob `329f8d56026b0ae792e0e2ebd9fbe050c8a849c0`**。

M0条件+轮次平均平方误差锐界 **0.078922–0.079495**；M1上轮本群体自身行为 **0.033694–0.034130**；M2两者各半 **0.037304–0.037651**；M3加实验前global认同 **0.037316–0.037663**。M1同一不确定真实目标下较M0预测误差改善的锐界 **+0.044918–+0.045671**，三个实验处理均缺失稳健为正：这是明确的**群体短期行动历史提供增量预测信息**的实验内E2证据，而**M3对M2没有显示额外提高**。并非每组都改善：Balanced 52较好、5较差；GlobalBoost 33较好、24较差；GlobalOnly 31较好、25较差、1组方向未确定。继续保留所有实际负例。

[正式A01–A06科学报告](R089_171_SIXPERSON_GROUP_FIVEFOLD_HISTORY_PREGAME_IDENTITY_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [机读正式验收](R089_FINAL_ACCEPTANCE_STATUS.json) · [可复算作者原始来源与5折模型程序](r089_original171_group_heldout_identity_history_predict_E2.py) · [40项完整合成验证](test_r089_original171_group_heldout_identity_history_predict_E2.py)。**方法限制**：这只是同一篇原作者实验的跨组留出、不是跨期日历实时预测或第二独立论文E3；训练折内可读其他群体的预测期相同轮次；选择完整组六人群体本身带有原作者样本排除/选择；群体同session可能关联、无概率置信区间；身份认同因果作用与历史长期演化没有被检验。PESEN v0.1维持FROZEN。
