# A 数据侦察：Montero 2022 候选相对 R073 冻结外部复现的来源独立性硬排除

日期：2026-10-26 Asia/Singapore
状态：SOURCE_DEDUP_VERIFIED；SECOND_INDEPENDENT_R073_EXPERIMENT=NO；E2新增=0
性质：对已有公开候选的来源同一性补充核验。没有下载人级记录，也没有重新评分。

## 实际核验的英文一手材料与项目归档
1. 项目原始 `research/R073/README.md`：R073 原有 E2 采用 Montero-Porras 等 2022，Scientific Reports DOI `10.1038/s41598-022-11654-2`，原作者 `eladiomontero/PairwiseStrategies` 的 submission 提交 `4743f74d8a03a031b8f70aff64956f8ad5155182`。原实验 12 场、188 人、固定对手 6 场、随机配对 6 场，已有 18424 个留场次预测目标。
2. Dryad 官方公开页面 `https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk` 明确引用完全相同的论文 DOI，并列出 `fix.csv`、`rand.csv`、`README.txt`、`UserInformation.csv` 与实验说明。来源与 R073 是同一项实验。
3. 项目已有 `research/data_scout/MONTERO_2022_12_SESSION_FIXED_SHUFFLED_PD_SOURCE_GATE_2026-10-25.md` 误将其作为独立候选，后续 `research/data_scout/MONTERO_2022_R096_PRIOR_USE_2026_10_25_CORRECTION_2026-10-25.md` 已纠正 R096 重复使用。本记录补齐对 **R073 自身原始实验** 的直接比对，避免下一轮再次误计第二个独立数据集。

## 字段、时间、可获得性、许可及评分门槛
Dryad 描述为真实双人重复囚徒困境，12场，固定或更换对手，100轮，原始 C/D 行为。项目 R073 原有提交已实际取得作者 Git 固定 CSV 并完成场次留出；本轮未再次获取 Dryad 正式版本原始字节。Dryad CSV 与作者投稿版 Git CSV 的字节等价性仍未证实。
官方 Dryad 文件下载此前返回 403，逐行版本差异及文件级许可仍未在本轮核验。不得因公开页面存在而声称数据字节取得或已取得新的授权。
冻结 R073 模型、特征、评分规则不变。由于实验身份完全相同，即使将来成功取得 Dryad 版 CSV，也只能视为原来源版本核对，不能作为第二个独立真人实验。
独立来源需要不同的原始受试者与实验设计；还必须有完整独立场次、双方逐轮 C/D 行动、身份及先后顺序、许可和冻结模型的可迁移语义。

## 判定
`R073_SAME_ORIGINAL_EXPERIMENT=YES`
`R096_SAME_ORIGINAL_EXPERIMENT=YES`
`NEW_INDEPENDENT_DATASET=NO`
`DRYAD_FINAL_BYTES_MATCH_AUTHOR_GIT=UNVERIFIED`
`SECOND_R073_EXTERNAL_E2_REPLICATION=BLOCKED`
`NEW_E2=0`; `NEW_E3=0`; `ADDED_COST=0`
没有付费账户、收费 API 或非公开数据访问。
