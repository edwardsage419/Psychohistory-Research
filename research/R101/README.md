# R101：2023年另一独立团队的真人逐轮选择伙伴公共品实验原始来源筛选

2026-10-17。**当前 Phase A：真实第一手DataverseNL目录元数据审核运行中，原始行为源字节/人物与对手身份/独立场次均尚未证实，实际真人模型新得分0。PESEN v0.1=FROZEN。**

独立作者 Stallen、Snijder、Gross、Hilbert、De Dreu 的2023年[*Nature Communications*原论文](https://doi.org/10.1038/s41467-023-42128-2)报告336名真人、八人群体、每轮双人配对、由系统分配或选择伙伴条件。论文公开数据位置[OSF CASQZ](https://doi.org/10.17605/OSF.IO/CASQZ)，另一作者机构UvA报告正式同论文数据集[DataverseNL DOI 10.34894/EYFM5L](https://doi.org/10.34894/EYFM5L)。**这些是论文和机构公开索引的出处事实，不等于本项目已独立读取任一个原始真人行为文件。**

优先真正DataverseNL以避开R097另一OSF数据源原API503的重试损耗。[Phase A官方来源元数据冻结](../../protocols/R101_PHASE_A_STALLEN_2023_DATAVERSENL_OFFICIAL_METADATA_ONLY_GATE_FREEZE_2026-10-17.md)只允许精确官方 `dataverse.nl` DOI API的文件目录，不访问任何actor/partner/round值。[纯标准库官方目录审计](r101_stallen_2023_original_DataverseNL_official_metadata_only.py)、15项纯synthetic和[GitHub工作流](../../.github/workflows/r101-2023-Stallen-DataverseNL-author-metadata-source-only.yml)均已经上传GitHub；真实来源成功或失败必须另将匿名机读收据归档。若目录确实开放，先固定官方fileID/文件大小/MD5与精确路径，再逐步验证Source actor/opponent/round/session独立性。

研究目标：检验个人历史之外当前及过往对手行动是否对下一轮选择仍提供**新增、独立留出预测价值**。R100已正式E1身份不能重建限定结题，不能带入R101的训练样本；R095阴性、R096固定与换伴异质、R099四人组历史正向仍并列保留。R073及PESEN模型保持既有冻结，不能因新样本结果事后选参。


## Phase A2实际原DataverseNL官方元数据目录通过（2026-10-17）

R101第一次源API真正执行返回`R101_OFFICIAL_DATASET_DOI_MISMATCH`（只是审核器只认API顶层DOI字段），[首次失败收据](R101_PHASE_A_LIVE_CI_OFFICIAL_METADATA_ONLY_RECEIPT.json)仍永久保存。再以官方Dataverse版本字段正式规范[独立冻结 A2 唯一DOI字段回退](../../protocols/R101_PHASE_A2_DATAVERSENL_LATESTVERSION_DATASET_PERSISTENT_ID_ONLY_COMPATIBILITY_FREEZE_2026-10-17.md)，把原CI改手工，额外3项synthetic，使后续真正DataverseNL源目录读取成功，[新的真实匿名来源收据](R101_PHASE_A2_LIVE_CI_OFFICIAL_METADATA_ONLY_RECEIPT.json)经[GitHub Actions机器人正式提交](https://github.com/edwardsage419/Psychohistory-Research/commit/6c3ac2ca24b22644f172033518d6643cb2ce6898)并经再读取验证。真实官方DOI确证、**9份ZIP原文件的目录元数据**、目录总登记43,631,177字节、0份CSV/TSV/TXT平铺、公开MD5字段0份。**真正ZIP原始字节尚未取回/核验、原人物/对手/实验场次身份尚未读取、真人评分0条。**

[Phase A2第一手科学报告与外推限制](R101_PHASE_A2_GENUINE_DATAVERSENL_9_ZIP_METADATA_ONLY_SCIENTIFIC_REPORT_2026-10-17.md) · [机读正式阶段状态](R101_PHASE_A2_CURRENT_STATUS.json)。**R101=IN_PROGRESS_OFFICIAL_DATASET_METADATA_CATALOG_VERIFIED，E0源目录成功，E1真实行为文件和E2模型均未成立，PESEN v0.1 FROZEN。** 下一步仅在另行预冻确切目标ZIP路径、大小及来源签发哈希后下载选择的一份，不批量下载9份或未经协议扫描真人贡献。


## Formal bounded source-transport conclusion after A3–A8 (2026-10-17)

The actual official DataverseNL [A3 nine-file inventory](R101_PHASE_A3_LIVE_CI_OFFICIAL_PUBLIC_ZIP_CATALOG_RECEIPT.json) identified `3. Raw data files.zip` public file ID **383977** and recorded **2,247,187 bytes**. Full provenance and selection are documented in the [A3 original catalog report](R101_PHASE_A3_OFFICIAL_NINE_ZIP_PUBLIC_FILE_SELECTION_SCIENTIFIC_REPORT_2026-10-17.md). The separately frozen [A4 actual download](R101_PHASE_A4_LIVE_CI_FIRSTPARTY_RAW_ZIP_SHA_DIRECTORY_RECEIPT.json) was rejected by the exact official URL host gate; [A5 first-party nofollow HTTP303](R101_PHASE_A5_LIVE_CI_REDIRECT_PREFLIGHT_RECEIPT.json) established the presigned SURF research storage delivery host `objectstore.surf.nl` with all signed URL values redacted. [A6 bounded one-hop true-download attempt](R101_PHASE_A6_LIVE_CI_ORIGINAL_SURF_DELIVERED_ZIP_SHA_DIRECTORY_RECEIPT.json) failed `R101_A6_ORIGINAL_SURF_PAYLOAD_FINAL_HOST_NOT_VERIFIED`. A separately frozen no-body [A7 actual response](R101_PHASE_A7_LIVE_CI_FINAL_HTTP_HEADER_DIAGNOSTIC_RECEIPT.json) genuinely confirmed HTTP200, one Dataverse 303, final SURF host, `application/zip`, and expected 2,247,187-byte header. The **single unchanged A8 replay** was pre-frozen and [again returned the same bounded source mismatch](R101_PHASE_A8_LIVE_CI_UNMODIFIED_ORIGINAL_ZIP_DOUBLE_SHA_REPLAY_RECEIPT.json). All real negative evidence remains permanent; auto transport retries stop here.

[Formal R101 scientific bounded conclusion](R101_FINAL_BOUNDED_SOURCE_TRANSPORT_NOT_E1_E2_REPORT_2026-10-17.md) · [Machine acceptance](R101_FINAL_ACCEPTANCE_STATUS.json). **R101=CLOSED_BOUNDED_SOURCE_TRANSPORT; first-party original DOI and file metadata plus SURF HTTP delivery chain are authenticated, raw ZIP full SHA E1=NOT_ESTABLISHED, verified human actor/opponent/session schema=NO, new human E2 scores=0, PESEN v0.1=FROZEN.** Continue to R102 new independent team with direct published small CSV and a verified original MD5; do not reclassify the original source access problem as model-negative evidence.
