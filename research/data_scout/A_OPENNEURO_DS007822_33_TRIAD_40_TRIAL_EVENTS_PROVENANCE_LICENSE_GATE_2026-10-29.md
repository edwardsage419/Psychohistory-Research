# A轨：OpenNeuro ds007822 三人囚徒困境EEG数据，公开逐轮事件实际读取与来源资格审计

日期：2026-10-29（Asia/Singapore）。证据状态：SOURCE_BYTES_PARTIALLY_READ / HUMAN_ORIGIN_UNVERIFIED / R073_DIRECT_REPLAY_NO。无新增E2预测。

## 英文公开一手来源及数据身份
原始仓库 https://github.com/OpenNeuroDatasets/ds007822 ，数据集标识 doi:10.18112/openneuro.ds007822.v1.0.0。仓库README称为三人同步EEG囚徒困境实验，11组三人、合计33个匿名受试者槽位，三个任务pddecision、pdfeedback、pdrest。participants.tsv实际读取，确有G01至G11各S01、S02、S03，共33行。GitHub main完整树列出672个条目，包含33个决策任务events.tsv、33个反馈任务events.tsv及其他文件。完整EEG无需下载，本轮仅检查公开行为元数据。

实际读取dataset_description.json（Git blob c6d51a07c3a5b3821b8ffabea51a502ea99835e4），包含BIDSVersion 1.10.0、DatasetDOI和License CC0。仓库LICENSE文件却写“License information was not provided with the source files.”；两处许可元数据并不一致。数据集级声明为CC0，原始来源文件级授权及来源链尚待核实，不据此自动认定所有底层记录再分发许可已独立证明。

## 实际逐行核验
已读取G01、G02、G03三个三人组全部9个决策事件文件，共360行。每个匿名槽位40个trial，字段onset、duration、trial_type、trial、group、subject、choice、triad_outcome。观察到choice=1对应coop、choice=2对应def；360行中262个choice=1、98个choice=2。字段group/subject与文件名一致，观察到的choice与triad_outcome语义一致，字段级不一致0。三组共120个组内轮次，其中39个轮次三人triad_outcome标签并不一致，表明该字段在已读样本中更接近个人行动标签，不能直接当成共同小组结果。

例如G01S01的40轮决策文件Git blob 594269370f3bb11ed54b5c02ff978fb762de5381；G01S02 blob 9aff7fc7ca02f36fe250f607fca4e96e8689695e；G01S03 blob a2908aa3237c757cbf5a53724a48158696846821。G02和G03另六个文件的原始blob及实际行数在本轮执行收据中已核验，尚未将全33个决策文件逐行读取。单个决策文件的onset从0.0开始，每轮4.0秒，表示任务事件的相对时间；真实采集时钟和实验日期尚未验证。

## 资格与复现准备
研究是三人组互动、每人40轮。没有R073冻结的真人双人100轮实验场次结构；R073直接复验资格NO。33槽位是README声称的参与者结构，原始README无作者身份，dataset_description的Authors为n/a，当前未找到对应实验论文、伦理说明或采集链，故真实人类来源身份仍为UNVERIFIED。该数据即使可见公开决策文件，也不得在来源真实性核验前作为已认证真人E2研究证据。

复现准备下一步：取得论文/作者与采集元数据，确认数据集许可冲突；逐行读取剩余24个决策文件，检查33人×40轮的完整性、跨三人组的独立性、反馈时间与行动是否重复，分组留出而非随机按轮拆分；如证据充分，作为三人社会互动独立研究设计，不能调整R073冻结评分后冒充其复验。

本轮没有下载EEG二进制、参与者面孔或私人身份资料，没有调用付费API、注册账户或引入费用。