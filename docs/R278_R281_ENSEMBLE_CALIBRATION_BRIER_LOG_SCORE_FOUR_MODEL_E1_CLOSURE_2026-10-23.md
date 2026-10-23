# 心理史学 R278 至 R281：模型平均、概率校准、Brier评分及对数评分，四项连续正式研究验收索引

日期2026-10-23 Asia/Taipei。四项依原239候选模型目录顺序：12-008 R278 Model Averaging and Ensembles（P2）、12-009 R279 Forecast Calibration（P1）、12-010 R280 Brier Score（P1）、12-011 R281 Logarithmic Score（P1）。研究状态均为**CLOSED_BOUNDED_E1**，即完整冻结人工概率空间的数学与可复验代码结题；新增真人E2=0、真实历史E3=0，R073和PESEN v0.1冻结。

## R278 贝叶斯模型平均与模型选择
[冻结协议](../protocols/R278_BAYES_MODEL_AVERAGING_12_WORLDS_768_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整源码与原source](../research/R278/README.md) · [科学报告](../research/R278/R278_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R278/R278_FINAL_ACCEPTANCE_STATUS.json) · [成功CI run39904644080](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904644080) · [完整机器人原来源归档0f39a4a7](https://github.com/edwardsage419/Psychohistory-Research/commit/0f39a4a753aa47bc4484b9de429da12a316196cb)。

三人工真率×四冻结预测政策＝**12个人工world、768个带模型标签完整原source**，每source4训练bit及2个独立未来测试bit。对两个候选q=1/4、3/4用真实训练likelihood更新Bayes权重并计算平均预测，与事前固定K=2平局选低q的硬模型选择比较。p=1/4真率下HARD_SELECT未来Brier205/1024优于BMA的87/410；p=3/4时BMA87/410优于HARD_SELECT259/1024；p=1/2未包含于候选族时，两种方法未来损失都不如固定q=1/2。不能声称BMA恒优于选择单一模型。完整原source积分与独立Binomial(4,p)解析结果逐Fraction相同，双Python各108真实测试共**216项通过**，三CI作业均success。

## R279 预测校准及Murphy分解
[冻结协议](../protocols/R279_FORECAST_CALIBRATION_9_WORLDS_144_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整源码与原source](../research/R279/README.md) · [科学报告](../research/R279/R279_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R279/R279_FINAL_ACCEPTANCE_STATUS.json) · [最终成功CI run39904942557](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904942557) · [原来源永久归档1f7275b3](https://github.com/edwardsage419/Psychohistory-Research/commit/1f7275b346824e5b235a9fcdf59bd10d40028d6c)。

三人工两组真率×三固定预测政策＝**9个人工world、144完整原source类型**（其中99正质量），每source真实4bit来自两组各两次独立结果。Murphy总体分解E[Brier]=REL−RES+UNC逐world完整原source积分与独立总体分桶计算严格一致。所有组统一报q=1/2，在整体均值pbar=1/2时population REL=0但RES=0；在两组真率1/4、3/4时平坦预测Brier1/4劣于分组报告的3/16，故仅有总体校准并不保证有分辨力。首次[CI run39904785939](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904785939)因Python assert断行语法错误失败；修复版本[40fa945d](https://github.com/edwardsage419/Psychohistory-Research/commit/40fa945d0273b085279576f52b5abd0e3d24c284)重跑后双Python各84真正测试共**168项通过**，第三来源审计和机器人永久main归档全部success。首次失败历史必须继续保留，不得计为成功。

## R280 Brier严格适当性与有限样本胜负
[冻结协议](../protocols/R280_BRIER_STRICT_PROPRIETY_9_WORLDS_144_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整源码与来源](../research/R280/README.md) · [正式科学报告](../research/R280/R280_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R280/R280_FINAL_ACCEPTANCE_STATUS.json) · [CI run39905121175](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905121175) · [原来源永久归档6d94abb6](https://github.com/edwardsage419/Psychohistory-Research/commit/6d94abb697633a44b12db4db587d38c27fce11c9)。

三人工真率p×三事前固定报告q＝**9world、144个完整四bit原source类型**。期望损失E[(Y−q)^2]=p(1−p)+(q−p)^2严格适当，真率q=p在总体期望上唯一最优；但一次四bit有限样本有正质量让错误q偶然更低分。如真p=1/2、错误q=1/4，错误q四次平均Brier严格优于真p报告的概率为5/16。全source及独立Binomial(4,p)五分类分数、胜出和同分概率全部准确Fraction一致。双Python各83真单测，共**166项通过**，第三审计和三CI job全success。

## R281 符号精确对数评分与无限预测损失
[冻结协议](../protocols/R281_LOG_SCORE_15_WORLDS_240_COMPLETE_SOURCE_SYMBOLIC_FREEZE_2026-10-23.md) · [完整源码和全部原source](../research/R281/README.md) · [正式科学报告](../research/R281/R281_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R281/R281_FINAL_ACCEPTANCE_STATUS.json) · [最终全成功CI run39905387817](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905387817) · [原来源机器人永久归档d038a6b9](https://github.com/edwardsage419/Psychohistory-Research/commit/d038a6b9794152463bf05e058c3d43c22f197cb6)。

三人工真率p×五冻结q∈{0,1/4,1/2,3/4,1}=**15world、240完整四bit原source类型**。有限log-score使用有理系数ln2与ln3精确表达；q=0或1且遇真实矛盾bit的源一律保留INF标记，不截尾。对真p=1/2、报告q=0，四bit源至少一次出现真实1的概率15/16，使样本log损失+∞，理论期望更为+∞；同时全0的有限样本可得到偶然0损失。全部15世界符号期望和无穷事件概率由原source与独立解析推导严格一致，双Python各134项真实测试，共**268项通过**，三CI job全success。

## 四项验收总账及边界

|审计项目|R278|R279|R280|R281|合计|
|---|---:|---:|---:|---:|---:|
|人工冻结世界|12|9|9|15|**45**|
|带模型标签完整原source|768|144|144|240|**1296**|
|通过双Python真单测|216|168|166|268|**818**|
|最终成功GitHub Actions jobs|3|3|3|3|**12**|

全部原source来自人工冻结二元模型，其中不同world共享相同底层随机空间，R279含零质量原source占位，不能将1296称为真实受试数。四个最终CI各三job已completed/success，全部源码/原CSV/完整解析JSON/SHA256机器收据/科学报告/正式验收均在main永久归档。额外单独记录R279一次已修复的初次失败CI，不计入12个最终成功job。

本轮增进的是概率预测评估方法数学性质的**人工E1**，没有新增真实真人E2、真实历史E3、R073跨实验复现或PESEN更新，不代表心理史学已具现实预测效度。原239目录下一项为**12-012 Open Reproducible Workflow and ODD（P0，拟R282）**。按明确顺序先全部原R研究学习、再统一归纳分类、最后熔炼原创模型，个人辅助决策系统具体实施仍暂缓。
