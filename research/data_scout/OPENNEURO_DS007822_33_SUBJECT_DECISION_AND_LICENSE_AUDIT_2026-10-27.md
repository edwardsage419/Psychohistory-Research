# A轨 OpenNeuro ds007822公开三人囚徒困境EEG实验：逐回合字段与资格审计

日期：2026-10-27。状态：SOURCE_BYTES_AND_ROW_SCHEMA_VERIFIED / HUMAN_PROVENANCE_PENDING / R073_DIRECT_TRANSFER_BLOCKED。

## 固定公开来源
OpenNeuroDatasets/ds007822，GitHub主树 bba8cdf86f03c0e37c0740e9c788790e7cea2602。官方仓库 https://github.com/OpenNeuroDatasets/ds007822 ，数据描述 https://github.com/OpenNeuroDatasets/ds007822/blob/main/dataset_description.json ，README https://github.com/OpenNeuroDatasets/ds007822/blob/main/README 。该仓库描述为三人超扫描EEG囚徒困境数据，11个三人组共33名匿名参与者。文件名保留组和组内主体编号。此来源与原R073 Montero固定/轮换双人实验属于不同数据来源，尚未完成研究者、招募和伦理元数据独立核验。

## 实际数据检查
使用GitHub连接器读取全部33个公开 decision events.tsv 文件，分三批12、12、9文件检查，所有文件各40轮，共1320条决策记录，11组共440组轮。检查group、subject、trial从1至40连续、onset每轮递增4秒、duration=4、choice二元编码1/2及triad_outcome字段。33文件结构检查通过。

1320/1320条记录中，triad_outcome字段与该参与者自身choice的coop/def编码逐行完全对应。440个组轮中有160轮三人动作存在差异。因此triad_outcome在此数据中不能直接当作组内三人共同结果标签；若作为群体结局使用，会把个人动作重复编码为群体标签。已观察到两个组内40轮动作序列完全一致的主体对：G02S01/G02S02、G07S01/G07S02。序列一致本身不构成数据伪造或错误的证据。

数据许可存在来源元数据不一致：仓库LICENSE文件明示“License information was not provided with the source files”，dataset_description.json声明CC0。当前只能记录两份来源内容，数据专属再分发授权需要进一步澄清。未复制或重新分发原始逐行记录。原README未提供研究者姓名，dataset_description.json Authors为n/a，真实人类参与者的外部来源认证待核。

## R073迁移门槛
R073冻结协议为双人重复囚徒困境、FP/SP两处理、每人100轮及固定评分对象。该候选是三人组、每人40轮、EEG事件文件，缺少原R073所需的同构处理与实验单位。直接迁移状态BLOCKED。未来可单独设计并事先冻结三人组行为预测协议，严禁修改R073既有冻结模型与评分规则来迎合新数据。

## 可执行准备与证据范围
新脚本 research/data_scout/a_openneuro_ds007822_decision_gate_20261027.js 使用Node标准库读取本地已取得的公开仓库，检查33文件、时间连续性、群组动作分歧和标签映射，仅输出聚合统计。已在33主体的合成输入上运行，并执行错误trial和错误outcome两个负对照，均成功检出。实际1320行来源检查通过连接器分批执行的等价字段核验，归档脚本尚未在本地完整克隆上执行。机器来源收据 research/data_scout/OPENNEURO_DS007822_33_SUBJECT_1320_DECISION_SOURCE_GATE_2026-10-27.json 保存33个Git blob身份、聚合计数和复现阻塞。

此为公开数据结构审计。新增真人E2预测评分=0，历史E3=0，外部独立复现=0。未下载EEG二进制信号，未使用收费资源。
