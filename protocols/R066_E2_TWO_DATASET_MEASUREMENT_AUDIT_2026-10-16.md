# R066 E2 数据来源与意见测量可用性审计：双候选预执行协议

日期 2026-10-16。性质：读入两个新的真实公开数据集**之前**冻结的来源/测量门；与三模型参数拟合、经验因果识别及模型验证不同。R066 研究状态 ACTIVE，PESEN v0.1 FROZEN。

## 候选 A：Monti 等 2020 Reddit 社会互动时序

固定原作者仓库 `corradomonti/learnable-opinion-dynamics` 提交 `5d31ba59e716e5bde85e4c56b9cdacc3920aaaf6`（GPL-3.0 仓库许可，数据原生再分发另审）：
- `data/reddit/edges_user.tsv.bz2` Git blob `e2e261b123963b257ed126a66b101fbaef6f937d`，321422 原始字节；
- `data/reddit/edges_feature.tsv.bz2` blob `12b6d3f407697e593bc368b9cd65fca1bfd7ce2d`，490710 字节；
- `data/reddit/feature_scores.tsv.bz2` blob `6c7d8a9e63d9860541d24b1c25c45d1cc2b8c565`，776604 字节；
- `data/reddit/interaction_scores.tsv.bz2` blob `18e367869399850fb4a1f28659a4b375e2ed43a1`，1922336 字节。
- 以上两个 `edges_*.tsv.bz2` 无 header，期望 `edges_user` 行为四列 (yearmonth,parent,author,count)、`edges_feature` 四列 (yearmonth,author,subreddit,count)；后两个作者 README 说明为得分/互动聚合观测，不是个人直接意见测量。
- 只运行严格 bz2 完整解码、UTF-8 行和 TSV 列数检查，压缩源须完全满足 Git blob 哈希。限制每文件最大解压 250MB、最多 5,000,000 行、无行内容回显。记录行数、字段名（非身份）、时间范围和唯一月份数及公开文件 hashes。不向下游输出用户 ID/时间戳级可定位轨迹。
- **实证 DeGroot/FJ/HK 意见变量门**：本来源若只提供互动、社区参与、得分汇总，`DIRECT_REPEATED_OPINION=NO`；即使来源齐全、格式正确，也必须记录 `THREE_MODEL_EMPIRICAL_DISCRIMINATION=BLOCKED_MEASUREMENT`，不得把回复或赞当作主观立场连续分数。若出现带人工标注意见的新字段，需另冻协议后才可测试映射。

## 候选 B：Okawa & Iwata 2022 标注意见时间序列

固定原作者仓库 `mayaokawa/opinion_dynamics` 提交 `32441421a9a012acc64b206f73a2b6525580e3ce`：
- `working/posts_final_sample_twitter_Abortion.tsv`，Git blob `2a88788f32496a8ebe45293ecf95eaf516876df6`，279372 字节。作者 README 说明是活跃度最高的 100 名参与者的样本，内容为 `user_id, opinion, time`，opinions 为人工标注类别，已去除帖子正文以减少隐私泄漏。
- 需逐字节 Git blob 校验；header 精确匹配 `user_id\topinion\ttime`，必须为有限数值意见、有限数值时间、非空可分组 ID；报告匿名总体行数、ID 个数、意见类别分布、时间范围、重复多时间点受试者数量与是否同人时间序列可用。
- 不自动将人工标注的**帖子立场类别**视为直接、无误的个体潜在连续意见。区分 `ANNOTATED_POST_LABELS` 与 `DIRECT_CONTINUOUS_PERSON_LEVEL_OPINIONS`。如果数据只有帖子级观点分类而无曝光网络/关系边，三模型共同社会影响机制拟合仍为 `BLOCKED_MISSING_NETWORK_AND_LATENT_MEASUREMENT`。
- 时间上的测试需事先指定规则；本阶段**不拟合或评估模型预测**，只清查时间与标签的可用性。不能用用户随机行拆分得出跨时间泛化，未来必须单独冻结时间切分/按用户重叠及不泄漏政策。

## 失败优先与档案

- A 文件哈希、解压或指定两份 edge 基本结构失败，`A_SOURCE_INTEGRITY=FAIL`；B 哈希或规定三列表格失败，`B_SOURCE_INTEGRITY=FAIL`。绝不容忍部分缺失自动代为通过。
- 对合法形式却不足以测量意见/外部曝光的数据，记**MEASUREMENT_BLOCKED**，不把严格运行成功混为理论的经验正确性。
- 两套真实数据中只有非个人聚合计数或哈希可以写入本 GitHub；原始帖文本、用户名、用户 ID、逐人轨迹与源文件不得提交到项目。
- CI 须将离线合成测试与远端真实来源下载/校验作业分开，执行结果至少记录 job ID、状态、固定来源标识、非识别性结构统计和经验模型可识别门。
- 同时寻找同时具备时间上重复态度量表、可信曝光网络、可合法复核的新研究数据；此阶段只审计两个候选，不承诺现有数据足以回答人群意见变化因果问题。

`R066_E2_TWO_DATASET_SOURCE_AUDIT_PROTOCOL=FROZEN`
`R066_THREE_MODEL_EMPIRICAL_FIT=NOT_AUTHORIZED_IN_THIS_STAGE`
`PESEN_v0.1=FROZEN`
