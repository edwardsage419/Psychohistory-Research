# R076：真实真人实验之间的严格来源参数零样本迁移（回顾性研究）

2026-10-17，正式归档状态：**`CLOSED_BOUNDED`**。R076在R073来源实验**一次性**拟合固定七个M0–M6模型中的条件概率，**完全不使用目标实验的标签来训练**，将相同数值参数直接应用到R074和R075的各18个真实原始场次。两个目标是研究者已经见过之前评分结果的数据，所以本研究具有`RETROSPECTIVE_SCOPE_DECISION`，**绝非真正此前未见数据的新E3前瞻验证**。PESEN v0.1 冻结。

证据入口：[事先（本次迁移结果之前）固定的跨实验数值转移协议](../../protocols/R076_RETROSPECTIVE_SOURCE_ONLY_ZERO_SHOT_CROSS_STUDY_TRANSFER_FREEZE_2026-10-17.md)，commit `a8631257cb92c1e1756ca224b7a82bbd096234a6`；[数据源固定SHA守卫、source-only训练/迁移程序](r076_source_only_cross_study_transfer.py)及[24项纯合成模拟错误/泄漏保护测试](test_r076_source_only_cross_study_transfer.py)。[第一次真实三作者原始数据传输 Actions run 38993686411](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38993686411) 两job success；[第二次独立原始来源重下载、全字节 SHA一致验证、永久归档run 38993752496](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38993752496) success。原始人类行动、具体人员/场次编号和逐场误差不写进Git。

主要预先固定donor `R073_ALL_12_POOLED`：12个真实来源场次、18424个历史完整目标训练，来源合作率 `0.41787885366912725`。采用同一源参数：
- R074（18场、15338真实行为）：M0来源平均Brier **0.229581**，M1 0.098012，M3 0.074710，M4 0.072268。M3−M1 **−0.023302**（18/18好）；M4−M3 **−0.002442**（13/18好）。
- R075（18场、26116真实意向行为）：M0来源平均Brier **0.264839**，M1 0.184623，M3 0.156098，M4 0.143192。M3−M1 **−0.028524**（18/18好）；M4−M3 **−0.012907**（18/18好）。
- 两套固定次级donor分别只在R073 fixed6场和shuffled6场训练，按事先规则全报：R073 fixed6→R074 的 M4−M3 **+0.000823**（只有6/18场改善），负结果不可删；shuffled6→R074的 M4−M3 `−0.008221`。这显示更长历史模型的预测收益对来源训练制度和具体参数敏感。

[正式全七模型、三套donor×两实验、六处理、所有正负差与科学推断边界](R076_RETROSPECTIVE_SOURCE_ONLY_REAL_HUMAN_TRANSFER_RESULTS_2026-10-17.md)。[129,126字节完整版匿名数值JSON](R076_RETROSPECTIVE_R073_SOURCE_ONLY_TO_R074_R075_REAL_HUMAN_RESULTS.json) SHA256 `ecee82cf3686d6c03cef56fb84c84118b252b7c184b46dc45413e34f876a52da`，Git blob `dcf82ca323bb68afc7852e8389c988dc233914a3`；[统一验收A01至A06](R076_FINAL_ACCEPTANCE_STATUS.json) 在本次**有界回顾性**范围均PASS。

R076首次完成「源实验拟合过的数值概率直接带到另外两份真人实验」的真实来源核验，且结果比简单的源基线表现好；但独立新第四实验、人员行为因果机制、实际社会制度演化及宏观历史预测均没有验证。既然研究者已经看过R074与R075，今后优先启动 **R077：全新第四作者原始真人实验来源**，在查看结果前先固定来源与评价，避免回顾性数据继续调参。PESEN v0.1 保持冻结。

`R076=CLOSED_BOUNDED`，`NO_TARGET_TRAINING_LABELS=TRUE`，`TRUE_PROSPECTIVE_NEW_E3=NO`，`PESEN_v0.1=FROZEN`。
