# A：OpenNeuro ds007822三人囚徒困境EEG行为文件逐项来源审计

日期：2026-10-26。来源：OpenNeuro公开GitHub仓库 `OpenNeuroDatasets/ds007822`，固定main HEAD `bba8cdf86f03c0e37c0740e9c788790e7cea2602`。原始README称其为三人EEG hyperscanning囚徒困境实验，包含11组三人组，合计33个参与者标识。其原作者、伦理审批和采集论文信息在本次可读的README和dataset_description中缺失，真人数据出处需进一步核实，当前按“宣称真人，来源证明待核”登记。

## 本轮实际读取

通过GitHub连接器逐个读取全部33份 `sub-GxxS0y_task-pddecision_events.tsv`，均含8个字段：`onset,duration,trial_type,trial,group,subject,choice,triad_outcome`。每份40轮，合计**1320条决策记录**。全部33份均满足轮次1至40连续、group和subject与路径身份一致；选择编码均在{1,2}，其中1对应coop、2对应def。33份文件的1320/1320行均满足 `triad_outcome=coop iff choice=1`，`triad_outcome=def iff choice=2`。因此该字段在这些文件中只是个人选择的冗余标签，**不能当作真正独立的三人群体结果变量**。例如G01第11轮S02选择2，其余两人选择1，三人文件的triad_outcome按各自选择分别赋值。

样本的时间单位为trial轮次，`onset`和`duration`是EEG任务内的秒数。11组三人组可用作潜在聚类单位，尚无独立实验场次或批次标识；33名参与者在组内有重复行为，1320行绝非1320个独立实验。读取G01S01的feedback事件文件，发现40轮`choice`和`triad_outcome`与decision事件逐轮一致，说明至少这一份反馈记录不可重复计为新行为样本。其余反馈文件的一致性仍待全量核验。

## 许可与资格

`dataset_description.json`声明 `License: CC0`，但仓库 `LICENSE` 原文写明“License information was not provided with the source files.”，存在可见的元数据与来源许可说明不一致。只登记文件元数据及统计摘要，暂不再分发原始文件。EEG .set文件采用数据管理指针，未下载EEG二进制数据。

该任务为三人囚徒困境，缺少可直接使用的双人对手身份、双人收益矩阵与对手逐回合行为映射。R073冻结模型不具备直接迁移资格，未执行评分或调参。当前结论：`33_DECISION_TSV_READ / 1320_ROWS_STRUCTURALLY_VALID / OUTCOME_LABEL_REDUNDANT / HUMAN_PROVENANCE_UNVERIFIED / LICENSE_CONFLICT / R073_DIRECT_TRANSFER_INELIGIBLE`。本轮新增E2预测0项，费用0。

公开来源： https://github.com/OpenNeuroDatasets/ds007822/tree/bba8cdf86f03c0e37c0740e9c788790e7cea2602 ；数据集DOI在元数据中写为 `10.18112/openneuro.ds007822.v1.0.0`，本轮尚未独立验证DOI解析。
