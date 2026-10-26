# A：Kuper-Smith与Korn真人重复囚徒困境数据候选，固定Git来源审查

日期：2026-10-26。来源：作者公开仓库 https://github.com/dnhi-lab/losses_gains_2x2 ，固定main提交 `345348cdc0018e8e030b05fb47dc845fd3e0d29a`。相关论文《Loss avoidance during social interactions》，Communications Psychology 2025，DOI 10.1038/s44271-025-00288-5。作者README声明仓库包含研究数据及分析代码。

## 实际验证的文件和字段

公开数据文件 `data/data_Exp_1_2_3.csv` 3354445字节，Git blob `1c9de60df93b8d404588df7d4f8410d8edf57d0e`；清洗版本 `data/data_Exp_1_2_3_cleaned.csv` 3139058字节，Git blob `ffd6776f3e9fd1444c84e50e4c61e3ff418a2488`。两者均在固定提交的Git树中。作者字段说明来源 `analysis/format_data_Exp_1_2_3.m` Git blob `6965e66ac05ec67b519f0674a708fcdcef917785`，另交叉读取 `analysis/Analysis_Exp_1_2_3.m` Git blob `cd40f2bcfa32dc32c352b18b2f17e7034ea8db1c`。

字段映射：第1列实验编号；第2列组编号，Exp1为1至4、Exp2为5至12、Exp3为13至20；第3列参与者编号；第4列对手编号；第5列参与者全程试次1至300；第6列区块内试次1至60；第7列同一收益矩阵对同一对手的重复次数，Exp1为1至5、Exp2和3为1至3；第8列区块编号；第10至13列收益矩阵；第20、21列是否有效作答；第25、26列双方合作或背叛的二元行为；第30、31列上一轮自身与对手行为。作者源码明确：Exp1的第4列对手身份没有记录，被置为NaN。该事实是R073可迁移性的重要限制。

实验中有多种收益矩阵，不能假定不同处理下具有相同支付结构。数据观察单位为参与者逐次决策；组和实验是相关性与留出划分的重要单位。原始CSV为3.3MB，当前GitHub文本读取接口返回空内容，未取得CSV逐行字节；实际行数、组内身份唯一性、对手配对、缺失率、每组独立场次和时间顺序仍未核验。

仓库根目录 `LICENSE` Git blob `6bf40c69fcd7c7b046e4ff932d1786f274a0f812` 为MIT文本，许可措辞针对软件及附带文档。对逐行真人行为数据是否完整适用该许可，当前尚无文件专属授权确认。没有下载或重新分发原始数据。

## 复现资格判定

优先级：HIGH。相较公开品实验，这一候选具备双人二元重复PD、双方逐回合行动及部分实验中的对手身份，具有R073真正独立实验复验潜力。须先排除与R073原始Montero 2022实验的来源重叠，再取得原始CSV字节、校验Git blob和字段、明确独立实验组及许可，预先冻结跨任务收益矩阵差异处理与留出规则。不得修改R073冻结模型或评分，不得在候选数据上调参。Exp1因对手身份缺失，应先隔离；Exp2与3仍待真实逐行核验。

当前状态：`SOURCE_BLOB_AND_CODEBOOK_VERIFIED / RAW_CSV_ROWS_PENDING / DATA_LICENSE_SCOPE_PENDING / R073_TRANSFER_NOT_APPROVED`。E2预测评分0，费用0。