# A 数据侦察：Andreozzi 2020 与既有 R079、R087 真实数据来源去重

日期：2026-10-25。状态：SOURCE_DEDUP_CONFIRMED。该数据已经在两项先前的E2研究中使用，本次不计为新增独立实验。

## 核验方法
实时读取 main 上 research/R073/README.md 至 research/R110/README.md 共38份文件，搜索作者名 Andreozzi、Ploner、Saral、仓库 stabilitycondcoop 及 DOI 10.1038/s41598-020-70681-z。38份均成功读取，其中 R079 与 R087 明确指向相同论文、固定 Git commit 和同一原始行为文件。此次扫描范围仅为上述38份README，不代表全仓库全部来源检索已完成。

| 既有研究 | README Git blob | 既有用途 |
| --- | --- | --- |
| R079 | 4d9c1fd7162455d335ad5e159802a784cceb4dda | 134人、6场、1340行的真人双人配对与组级统计 |
| R087 | 3fc02b069d36ecca8a20b1dfc3fbc19f06930ea7 | 同134人十期条件合作策略迁移的真人E2统计 |

两者固定作者仓库 seyhunsaral/stabilitycondcoop commit 979abf87b5d3cfb7aa8be13b81ef233076c3bb75；文件 data/csv/subjects.csv Git blob bd4c1550002621bee7dfb50e0d15d317764d1ea9。已发表来源 Andreozzi, Ploner & Saral (2020), Scientific Reports DOI 10.1038/s41598-020-70681-z。作者仓库数据 CC BY 4.0，软件 MIT。

## 数据与冻结协议适用性
1340行、67列、6个session、134个session内参与者、670个双人配对回合、10期、行动0/50/100。当前对手通常不同于上一期对手，且当轮 earning_kept=100−action、earning_received=3×opp_action，属于严格预测时点不可使用的目标代理。

R073使用 Montero-Porras et al. 2022 的二元双人重复博弈。Andreozzi 2020 的三水平行动及角色机制不能直接用冻结R073的二元模型与评分规则进行外部复现。任何新任务必须先冻结新的三水平评分协议，并保留session级独立性。

## 结论与阻塞
SOURCE_BYTES=PREVIOUSLY_VERIFIED；LICENSE=CC_BY_4_0；SESSION_AND_IDENTITY=PREVIOUSLY_VERIFIED；R079_PRIOR_USE=YES；R087_PRIOR_USE=YES；NEW_INDEPENDENT_EXPERIMENT=NO；R073_FROZEN_EXTERNAL_REPLICATION=BLOCKED_ACTION_SPACE；NEW_E2_SCORE=0；NEW_E3=0。

未取得新的独立数据，也未重新执行原作者六份zTree原始Excel的清洗过程。本报告仅补充来源去重，保持先前E2研究结果不变。
