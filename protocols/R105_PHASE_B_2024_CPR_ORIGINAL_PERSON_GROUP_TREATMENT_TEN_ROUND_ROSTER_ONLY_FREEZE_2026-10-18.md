# R105 Phase B：官方原CPR数据人物、处理、四人组与10轮非行为完整身份冻结

日期：2026-10-18。阶段状态：FROZEN_BEFORE_SOURCE_PERSON_OR_GROUP_ID_VALUES_AND_BEFORE_ALL_EXTRACTED_RESOURCE_ACTION_VALUES。R105 A3已由真Zenodo官方完整MD5 `a3afbb4e52179a0e1d8b1b533f076cc9`、项目SHA256 `a7d959361075ae88dc2fc4945b8a7ecd3c8fe3a234ff25dc53b28b9c2c5cdeae`核验整个`data_long_format.csv` 1,131,426 bytes、37列其中**恰1个空白列名**、4120个物理数据行。真实源原头已明确含`player_id,Treatment,group_id,round,extraction,extraction_last_round,group_extraction,others_extraction_last_round`等字段。这是一个不同于R096 2022双人PD和R102 2025六人PGG的**2024 Prolific线上四人CPR实验**；有R096共同作者，不能宣称团队完全无交叉。

## 此阶段仅可读取哪些原source字段

再次GET完全相同Zenodo源精确URL与完整MD5和上述完整SHA，不得替换版本；完整UTF8 CSV读取时必须保留原37字段包括唯一空列，其他原字段名字必须与A3真正header收据逐项一致。CSV解释器虽需在内存临时解析完整行，**应用层仅可取原4个原人分组字段**：
`player_id`（一个原数据匿名人号）、`Treatment`（条件）、`group_id`（源组编号）、`round`（本人的来源真实轮）。
严禁访问任何`extraction`、`extraction_last_round`、`group_extraction`、`others_extraction_last_round`、时间、默认选项、SVO、性别年龄或支付等原单元格。源原始人号/组号、少数标签和任何逐行值不输出Git或日志，只匿名汇总。

解析源人号、组号、Treatment为非空、长度≤128的ASCII字母数字/下划线/点/连字符/空格/斜杠/括号（但不容许反斜杠、换行或路径穿越）；`round`只可为ASCII十进制正整数1至10。每个原人按 `(Treatment,player_id)` 唯一，原组按`(Treatment,group_id)` 唯一。**不允许以组号在其它处理重复就将两组当相同来源组**。组员组成全十轮恒定，每人不得同轮出现在不同组；每个`(Treatment,player_id,round)`只出现一次，且每人的轮必须`1..10`全部存在；每个固定原组四人且每轮这同一四人实际有四条唯一记录；全部source原行数必须4120。若少一行、重复行、源ID不一致、组员在组间移动，都明确fail-closed，不能以删样本凑成正式真场次。

匿名收据仅输出总原人、原组、处理各自原人和组数、原组大小直方图、原人10轮完整人数、处理内各轮记录数概况、来源原group键真实唯一数、任何跨处理重用人号的计数（**重用字符串不直接证明同一真人跨条件**，需码本证明）；不输出原source identifier值、不输出任何`extraction`或个体行为。参与者真实实验室独立`session`字段**不存在**，严格明确未来只能按**整个原四人组完整留出LOOG**，不能写成按原实验室session留出LOSO或103次独立实验。

## 下一阶段C前瞻冻结界限

只有B真正官方通过，才能预先冻结第2至第10轮全部真实下一轮个体提取Y／30为目标的同源组完整留出评分。候选固定模型M1本人上轮提取，M2同一权重的本人上轮＋同处理**其它留出组之外**上一轮平均提取（普通收缩安慰剂），M3本人上轮＋自身上一轮原组三位真实同伴上轮平均提取，M4可考虑来自另一组同轮真实历史的确定性置换安慰剂；具体分母、权重、训练及缺失规则**必须另行完整冻结**，才能首次应用读取原`extraction`。M2与M3用相同前轮信息时点和相同自己权重，直接检查**真实同伴相较一般收缩的额外增量**；禁止在同源真实收益出现后改权重。为避免反馈字段的不同时点歧义，仅允许从已合格源group/人物关系重建前一轮真实同组成员，不能使用本期合计量预测本期人行为。跨原组互相依赖与同一在线募集环境不构成真正独立实验场次。R073/PESEN v0.1保持FROZEN。
