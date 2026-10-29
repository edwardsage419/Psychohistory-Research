# A轨公开实证数据审计：OpenNeuro ds007822 三人囚徒困境行为事件

日期：2026-10-29 UTC。来源：OpenNeuroDatasets/ds007822（https://github.com/OpenNeuroDatasets/ds007822），数据集DOI `10.18112/openneuro.ds007822.v1.0.0`，`CHANGES`记录v1.0.0为2026-05-21。此次只读取公开GitHub上的文本行为事件和元数据，未获取EEG二进制、未使用私人资料、未进行模型拟合。

## 实际读取及完整性
读取 `README`、`dataset_description.json`、`LICENSE`、`participants.tsv`、`participants.json`、`CHANGES`，以及11组×3人=**33份** `sub-GxxSyy_task-pddecision_events.tsv`，各文件经GitHub connector返回Git blob。实际逐行解析33份TSV：每人40行、trial=1..40、group/subject匹配文件身份、`trial_type=decision`、`choice`只能为1或2，且`choice=1`时`triad_outcome=coop`、`choice=2`时`triad_outcome=def`。全部1320行通过这些确定性字段检查，33/33文件PASS，失败0。合作choice=1共**1024/1320**（描述比例77.5758%，没有做独立样本推断）。

各组三名参与者的40轮合作计数（S01,S02,S03）：
G01=(17,20,28)，G02=(40,40,37)，G03=(28,25,27)，G04=(35,35,33)，G05=(11,23,17)，G06=(38,38,39)，G07=(40,40,39)，G08=(29,33,22)，G09=(17,24,34)，G10=(39,40,36)，G11=(34,39,27)。分组总数11，参与者槽33，独立实验单元最多按triad计11；不能把1320行或33人当成1320或33个独立场次。

文本字段依次为 `onset,duration,trial_type,trial,group,subject,choice,triad_outcome`。例如G01S01第一轮onset=0.0、duration=4.0、trial=1，第四十轮onset=156.0。这个时间是BIDS事件相对时刻，跨任务的时钟原点及EEG同步尚未验证。`triad_outcome`在本轮全部1320条文本中与个人choice一一对应，不能直接当作独立的三人群体支付或其他两人行动。原始数据没有单独`opponent_action`字段；在同一group/trial内可从另外两名成员的公开choice构造群体行为向量，但是否所有人真实同步、是否存在随机重配对或观察延迟仍需实验方案证据。

## 来源、许可和身份限制
`dataset_description.json`明确写`License=CC0`，根目录`LICENSE`同时写`License information was not provided with the source files.`。两处上游文件存在**明确的许可元数据不一致**，在进一步核实前不重新分发原始数据。作者字段`Authors=["n/a"]`，README声称为三人EEG hyperscanning囚徒困境；尚未定位完整作者、实验论文、招募记录、实验条件及原始行为生成过程的独立来源。参与者槽匿名，缺少跨研究身份链接。EEG .set为二进制，本轮无法由连接器读出，未验证EEG数据或同步质量。

## R073冻结模型的资格
每人40轮且为三人互动，原R073双人100轮冻结评分条件无法直接套用。`R073_DIRECT_REPLAY=NO`。可以作为后续新的三人合作网络研究候选，但必须单独冻结新问题、评分、分组留出及许可；本轮新增正式真人预测E2=0，历史E3=0。文件中的行为记录来自标称真人实验，尚未完成原作者身份和采集机制的外部真实性核验。不得把本次字段审计称为独立人类行为预测复现。

## 再现路径和来源锚点
根目录 https://github.com/OpenNeuroDatasets/ds007822/tree/main ，数据集页面 https://openneuro.org/datasets/ds007822 ，单个样例 https://github.com/OpenNeuroDatasets/ds007822/blob/main/sub-G01S01/eeg/sub-G01S01_task-pddecision_events.tsv 。样例Git blob `594269370f3bb11ed54b5c02ff978fb762de5381`，另一组G11S03 blob `bf602f89007953aec862b07855005e97e1a59771`。GitHub源仓库默认分支和具体提交未锁定，本次固定了文本文件Git blob样例，全部33份各自SHA见本轮运行记录；未来应以源仓库固定commit重新核验所有33个blob。GitHub事件文件可读取，EEG原始二进制及授权边界开放。

状态：`PUBLIC_TEXT_33_FILES_READ_AND_FIELD_VALIDATED`，`RAW_EEG_UNREAD`，`LICENSE_CONFLICT_OPEN`，`ORIGINAL_STUDY_PROVENANCE_OPEN`，`R073_DIRECT_REPLAY_NO`。
