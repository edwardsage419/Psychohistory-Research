# R098 正式限定来源报告：原2025年真人四人公共品文件身份成立，MAT数据结构未准入（E1）

2026-10-17。**R098=SOURCE_AUTHENTICATED_SCHEMA_BLOCKED_BOUNDED；真实人类行为预测零条，不能验收为E2。** PESEN v0.1=FROZEN。

## 1. 真实出版方作者与来源

独立研究团队 Xiaomin Wang、Christian Hilbe、Boyu Zhang，[2025年Zenodo v2《The dynamics of cooperation in asymmetric public goods games》](https://zenodo.org/records/16918146)，DOI `10.5281/zenodo.16918146`。本次来源严格限定`LinearPGG_4P_ExperimentalData.mat`，与该记录中其它阈值、二人PGG和问卷文件不同。

真实完整官方Zenodo下载**22,347字节**，原出版方MD5 `42153952f8e6614d09c2d903fd97af62` 已与整源一致，计算SHA256 `dcdd23e709ce1c17fadddffb84d07b9cf2f37a0a206e4665317aed31fd4e790b`。所以**E1原始文件身份确实成立**。不是下载源403、没找到文件或猜测字节。无原作者MAT源文件或人物级贡献数据再发布。

Zenodo作者说明三处理FE/AI/MI、各100/104/108名参与者、每次20轮四人合作、同一原人顺次参与两个session并重新配对。这是**出版方设计说明，而不是本研究从MAT行为重算的样本量**。两个session非独立招募样本，正式计算需完整留出组且排除跨session混同独立人群。

## 2. 全部独立冻结协议及真实失败保留

- [Phase A源MD5认证冻结](../../protocols/R098_WANG_HILBE_ZHANG_2025_ZENODO_LINEAR_PGG_4P_MAT_AUTHOR_SOURCE_E1_FREEZE_2026-10-17.md)，[CI39025491235](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025491235) 19synthetic中一项截断MAT异常漏捕，真实任务跳过；之后[Phase A2仅异常兼容](../../protocols/R098_PHASE_A2_SCIPY_TRUNCATED_MAT_HEADER_EXCEPTION_GATE_AMENDMENT_2026-10-17.md)。
- [CI39025545307](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025545307)19synthetic通过，**真出版方MD5验证通过**，SciPy目录无法识别。冻[Phase A3旧/新MAT目录兼容](../../protocols/R098_PHASE_A3_VERIFIED_MD5_MAT_CONTAINER_V73_METADATA_COMPATIBILITY_GATE_2026-10-17.md)；[CI39025710365](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025710365)24synthetic通过，真MAT为Legacy Level5而非HDF5，目录仍拒绝。
- [Phase A4只报告静态异常类型且保留真SHA](../../protocols/R098_PHASE_A4_ORIGINAL_AUTHENTIC_V5_MAT_SAFETY_EXCEPTION_CLASS_DIAGNOSTIC_FREEZE_2026-10-17.md)，[CI39025847448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025847448)24synthetic通过，真来源文件MD5、完整SHA256和MAT版本字段`0001`确认；SciPy目录报`TypeError`。无贡献数组读入。
- [Phase A5独立的stdlib MAT5标签源目录只读冻结](../../protocols/R098_PHASE_A5_WANG_ORIGINAL_MAT5_TAG_DIRECTORY_METADATA_PARSER_FREEZE_2026-10-17.md)，[CI39026065160](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39026065160)49synthetic中47通过、2项压缩块字节对齐失败，真人源任务未触发；另冻[Phase A5b只修compressed块对齐](../../protocols/R098_PHASE_A5B_COMPRESSED_MAT5_TAG_ALIGNMENT_SYNTHTEST_FIX_2026-10-17.md)。
- [CI39026134815](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39026134815)：**49项synthetic全部通过**，真出版方源仍因维度元数据标签不符合严格格式遭`R098A5_MAT_DIMENSIONS_INVALID`安全拒绝。没有数据格被转译或评分。拒绝继续围绕当前真人数据放宽解析合同，防止事后择源误读。

这并不能证明出版方MAT文件损坏：只能证明我们实现的两种MAT目录读取方式未能安全解释其结构。全部失败与事先冻结协议均保留，而非挑选“成功一次”冒充模型复验。

## 3. 科学级别与后续

| 门槛 | 真实结果 |
|---|---|
| 独立团队原作者来源真实固定版本 | 通过 |
| 完整出版方MD5/完整原始SHA256 | **通过 E1** |
| 原始MAT数据结构与合法字段地图 | **阻断** |
| 真正FE/AI/MI、四人组、20轮，从原数组重新计数 | 未执行 |
| 源行为上下限、同人跨session、角色正规化 | 未核验 |
| M0/M1/M2完整留出群组的真人预测 | **0条；无E2** |
| 真实样本二次独立复算、新招募E3 | 未成立 |

[详细机读来源证据收据](R098_2025_WANG_HILBE_ZHANG_FIRST_PARTY_ZENODO_MAT_E1_SOURCE_AUTHENTICATED_SCHEMA_BLOCKED_RECEIPT_2026-10-17.json)、[出版方元数据安全源码](r098_wang2025_4p_linear_zenodo_mat_publisher_MD5_structure_only.py)、[独立MAT5目录解析器](r098_phase_a5_mat5_tlv_metadata_only_parser.py)、24+25项synthetic与完整GitHub失败/通过记录均已归档。

**R099优先寻找真正可读、可验证源字节的独立真人CSV记录，具有session、actor、round、对手与行动，且≥20轮；不要将同一批受试者跨session重复当成独立人群，也不要将原作者实验设计说明当成原数据已复算。** R095和R096既有E2阳性与阴性结论保持不变。

**R098=SOURCE_AUTHENTICATED_SCHEMA_BLOCKED_BOUNDED（E1），PESEN v0.1=FROZEN。**
