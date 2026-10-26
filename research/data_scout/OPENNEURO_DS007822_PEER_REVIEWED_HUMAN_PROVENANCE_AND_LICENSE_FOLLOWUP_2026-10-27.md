# A轨 OpenNeuro ds007822：2026年同行评议数据论文与原始数据的来源身份、许可复核

日期：2026-10-27。证据类别：公开真人数据的来源及复现资格审计。新增真人E2预测评分0，历史E3评分0。沿用此前已归档的33名主体、11组三人组、每人40轮、合计1320条行为记录的结构审计，不重复登记为新的独立实验。

## 新增外部来源证据

本轮实际检索并核对英文同行评议数据论文：
H. Kim, S. C. Jun, C. S. Nam (2026), *A reproducible EEG hyperscanning dataset for triadic social decision-making during an iterated 3-player Prisoner's Dilemma*, Data in Brief 68, 113064, DOI 10.1016/j.dib.2026.113064，2026-07-10在线发表。PubMed PMID 42541318：https://pubmed.ncbi.nlm.nih.gov/42541318/；开放论文：https://pmc.ncbi.nlm.nih.gov/articles/PMC13427532/ 。

论文明确记载真人参与者33名，分为11个三人组，每人40个博弈试次，采集地点为韩国光州Gwangju Institute of Science and Technology，EEG为19通道300 Hz。论文数据可得性声明明确指向OpenNeuro数据集 DOI 10.18112/openneuro.ds007822.v1.0.0。此项新证据使原先“README与dataset_description未提供作者姓名”的来源缺口得到独立发表论文的补充；论文所称真人来源和已审BIDS行为记录在参与者数、组数、轮次数上相符。

同时实际读取研究代码仓库 https://github.com/heegyukim4043/PD_EEG_hyperscan_processing 的README.md，Git blob 423f0639c5541db75559312602a728ff7bf4c6d9。作者代码说明直接读取BIDS EEG文件及events.tsv，并提供预处理、ERP和脑间同步分析。代码仓库与数据论文中的代码可得性描述一致。该代码用于EEG分析，不能直接视为已验证的R073行为预测程序，也没有在本轮实际执行EEG计算。

## 原始仓库字段与许可冲突仍在

本轮从 https://github.com/OpenNeuroDatasets/ds007822 再次读取三个原始文件：
* dataset_description.json Git blob c6d51a07c3a5b3821b8ffabea51a502ea99835e4，Authors=["n/a"]，License="CC0"，DatasetDOI为上述OpenNeuro DOI。
* LICENSE Git blob 7cf9928dd50e0b154c7e5d09f91f16674dff64fc，文本为“License information was not provided with the source files.”
* README Git blob 4bbc8c259406e8a1cce00c6549cba41ff556f2c8，记录11组三人组与BIDS事件文件。

公开论文为CC BY开放发表，此论文许可与原始数据许可是不同对象。EEGDash/NEMAR镜像亦将数据标为CC0：https://eegdash.org/api/dataset/eegdash.dataset.ON007822.html ，但源仓库LICENSE仍保留无许可声明。当前许可门槛记为DATASET_METADATA_CC0_PRESENT / SOURCE_LICENSE_TEXT_CONFLICT_UNRESOLVED；未经明确消歧，不向本项目仓库复制或重新分发参与者逐行数据、EEG或问卷。

## 预测复现资格与数据泄漏风险

三人同步互动意味着同组三人的40轮轨迹互相依赖。未来如另立冻结协议，必须整组三人组留出，不能把同组三人分别分配训练与测试，也不能把同一轮三人记录作为三个独立组事件。原已发现的triad_outcome字段逐行与个人choice一致，因此不能将其作为独立群体结果变量；需依据三人当轮行动重新定义群体事件，并在评分前冻结定义。原有两个40轮完全一致的主体对仍属需解释的数据现象，不能据此直接推断错误。

R073要求双人FP/SP处理及100轮冻结评分对象。本数据为三人40轮，R073_DIRECT_FROZEN_TRANSFER=BLOCKED，R073模型、评分和PESEN v0.1继续冻结。本轮没有真人样本外预测、没有新参数拟合、没有外部团队独立复现。进一步任务是核验正式数据论文与原BIDS事件标签语义、获取明确的数据授权说明，之后仅在新预注册协议下开展三人组留出评价。

本轮来源均为英文公开科研站点及公开GitHub。没有访问私人数据、购买数据或运行收费服务。
