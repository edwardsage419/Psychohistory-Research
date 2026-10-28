# A轨：OpenNeuro ds007822 三人囚徒困境行为事件审计

日期：2026年10月28日。来源类型：公开真人实验候选；未新增R073 E2正式复评分。

## 原始来源与文件级检查
原始公开GitHub镜像：https://github.com/OpenNeuroDatasets/ds007822
原始数据集标识：OpenNeuro ds007822 v1.0.0，dataset_description.json记载 DOI doi:10.18112/openneuro.ds007822.v1.0.0。
来源数据卡：https://eegdash.org/api/dataset/eegdash.dataset.ON007822.html

实际读取仓库README、LICENSE、dataset_description.json、participants.json、33份各自独立的task-pddecision_events.tsv。按11个三人组G01至G11，每组S01至S03逐个读取。33份文件均可取得，每份有40条决策事件，共33×40=1320条公开决策事件。原始文件位于 sub-GxxSyy/eeg/sub-GxxSyy_task-pddecision_events.tsv，未复制参与者级数据到本项目。额外读取G01S01的pdfeedback事件文件；该文件同样40条反馈事件，属于相同决策的另一任务表示，**禁止与1320条决策事件相加当成独立行为样本**。

实际读取G01至G03共九份文件的首末事件，确认trial 1至40、每条decision事件持续4秒、onset从0.0至156.0秒，观察字段为onset、duration、trial_type、trial、group、subject、choice、triad_outcome。choice示例值1/2，triad_outcome示例coop/def；choice编码与收益含义仍需实验说明核实。其余24份本轮核验了每文件40条事件，未逐行独立审计其全部字段取值及时间连续性。参与者身份以组与组内槽位组合，公开元数据对应11组×3人，不能把组内三人的40轮看作120个独立博弈场次。

## 许可与隐私
dataset_description.json的License字段为CC0，外部数据卡也标记CC0；同一GitHub镜像根目录LICENSE文本却明确写“License information was not provided with the source files.”。两者来源不一致，暂不将该镜像视为获得原始研究者授权再分发的充分证据。需进一步核验OpenNeuro正式发布许可、原始实验提供方、同意书与敏感字段处理要求。本轮没有下载EEG二进制数据或参与者人口统计原始记录，也没有将任何参与者级行归档到本项目。

## R073兼容性门槛
R073冻结模型及评分要求独立的双人重复囚徒困境、100轮及特定FP/SP场次结构。本候选为三人超扫描实验，实际决策事件为每人40轮；未发现FP/SP双人处理和100轮场次。**DIRECT_R073_SCORE=NO**。其价值在于未来单独研究三人合作、神经同步与群体行为，但在R系列完成前不得另起产品开发或更改R073评分规则。

## 复现准备结果
SOURCE_READABLE=YES；33份行为事件文件逐个可读，1320条决策事件数量为文件级实测。IDENTITY_SCOPE=11_TRIADS_33_SLOTS；TRIAL_UNIT=40_DECISIONS_PER_PERSON；LICENSE=CONFLICT_REQUIRES_SOURCE_CONFIRMATION；ORIGINAL_RESEARCH_IDENTITY=UNVERIFIED；R073_FROZEN_COMPATIBILITY=NO；FULL_ROW_CONTENT_AUDIT=PARTIAL；EXTERNAL_REPLICATION=NO。下轮如继续此候选，先核验原始研究身份和正式许可，再检查每轮三人行动是否可重建及跨组独立性。不能将数据卡中的“CC0”单独当作许可闭合。
