# A轨：OpenNeuro ds007822 真人三人囚徒困境行为事件来源核验

日期：2026-10-27（Asia/Singapore）。状态：SOURCE_BYTES_READ / R073_FROZEN_GATE_NO / REDISTRIBUTION_LICENSE_CONFLICT。来源为英文公开仓库，未使用中文网站。

## 原始来源与版本

公开归档：https://openneuro.org/datasets/ds007822 ，DOI https://doi.org/10.18112/openneuro.ds007822.v1.0.0 ；公开镜像：https://github.com/OpenNeuroDatasets/ds007822 。实际固定Git树SHA `bba8cdf86f03c0e37c0740e9c788790e7cea2602`，main。仓库README Git blob `4bbc8c259406e8a1cce00c6549cba41ff556f2c8`，参与者索引 `participants.tsv` blob `7555eca1349703e6b1683fce828756d703012eab`，首个行为文件 `sub-G01S01/eeg/sub-G01S01_task-pddecision_events.tsv` blob `594269370f3bb11ed54b5c02ff978fb762de5381`。

README记载三人EEG超扫描囚徒困境实验，11组三人，每组三个被试槽位，任务含pddecision、pdfeedback、pdrest。参与者索引实际读取33个不同匿名participant_id，组号G01至G11，每组三人。未访问个人健康问卷、身份信息或EEG原始数据。

## 实际读取的行为来源与结构

已逐个读取33份`task-pddecision_events.tsv`原始UTF8文本，覆盖全部G01至G11及每组S01、S02、S03。每份恰40条事件，共**1320条逐人逐轮决策记录**。33份表头一致，均为`onset,duration,trial_type,trial,group,subject,choice,triad_outcome`八列。每份trial严格从1至40递增，33份均未出现轮次顺序错误。

实际汇总33份choice编码：1共1024条，2共296条。样本文件中1对应coop、2对应def；全部33份choice与triad_outcome的逐行语义一致性仍需专门校验。首份文件的onset从0秒开始、每轮增加4秒，duration=4秒；这属于BIDS事件时标，不能直接等同于每个社会互动回合的真实决策耗时。相同组的三人共同参与40轮，三人记录高度相关，独立评价单元至少需要以三人组为单位；11组是否真正独立招募与随机分配仍待原实验设计核实。

## 许可、可用性与风险

仓库`dataset_description.json` blob `c6d51a07c3a5b3821b8ffabea51a502ea99835e4` 声称 `License: CC0`；仓库顶层`LICENSE` blob `7cf9928dd50e0b154c7e5d09f91f16674dff64fc` 却明确写着 `License information was not provided with the source files.`。两者冲突，原始实验数据的再分发权限不能仅凭JSON确定。本轮只在远端读取公开事件文本，未复制参与者级数据进入项目仓库；仅归档汇总统计、字段与Git blob身份。存在公开数据不代表已核实全部伦理同意范围，后续不得将敏感表型信息混入研究。

## R073冻结协议资格与后续复现准备

本数据为三人三元组、每人40轮，R073冻结实验为双人逐轮100轮且具有既定对手历史和评分协议；当前没有足够的二人对手行动映射，也没有100轮留出场次。**R073第二独立真人实验冻结评分资格：NO**。禁止事后改模型、缩短评分或把三人合作标签当成双人对手行动。该来源可供未来独立的三人网络合作E2研究设计，但须先验证真实组间独立性、时间可用性、标签一致性和许可，另行事前冻结，不计入R073复现。

可复现的下一步：以固定Git树重读33份decision事件，核验choice与triad_outcome的全行映射、检查三人同轮记录一致性与反馈是否包含未来信息；读取原论文或原实验说明核实独立组和处理条件；先澄清顶层LICENSE与元数据CC0矛盾。现阶段新增真实人类预测评分0项，E2新验收0项。
