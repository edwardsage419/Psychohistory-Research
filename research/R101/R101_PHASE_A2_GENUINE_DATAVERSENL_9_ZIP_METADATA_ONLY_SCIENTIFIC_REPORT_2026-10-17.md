# R101 独立作者2023实验的DataverseNL第一手文件目录元数据实际审计（Phase A2）

2026-10-17。**R101 Phase A2=OFFICIAL_PUBLISHER_METADATA_CATALOG_CONFIRMED_BOUNDED**，尚未下载真正原实验行为文件字节，**E1真实行为文件哈希认证尚未成立**，真人模型实际0次，PESEN v0.1冻结。

## 出版论文与双真实归档出处

Stallen、Snijder、Gross、Hilbert、De Dreu (2023), *Partner choice and cooperation in social dilemmas can increase resource inequality*, [Nature Communications 14:6432](https://doi.org/10.1038/s41467-023-42128-2)，论文报告336真人、八人群体、多轮双人合作与伙伴选择/分配两类原制度；出版方公开[OSF CASQZ](https://doi.org/10.17605/OSF.IO/CASQZ)。作者机构UvA还正式给出本论文数据的[DataverseNL DOI 10.34894/EYFM5L](https://doi.org/10.34894/EYFM5L)。**这些336人和实验层级来自论文报告，还未经R101原始游戏数据独立核实。**

## 真正官方元数据API与失败修订序列

先[冻结真正DataverseNL唯一 DOI API来源及严格匿名目录](../../protocols/R101_PHASE_A_STALLEN_2023_DATAVERSENL_OFFICIAL_METADATA_ONLY_GATE_FREEZE_2026-10-17.md)。15纯synthetic通过后首次真 API 得到 `R101_OFFICIAL_DATASET_DOI_MISMATCH` 并永久存入[首次失败收据](R101_PHASE_A_LIVE_CI_OFFICIAL_METADATA_ONLY_RECEIPT.json)。该错误源于原审核器只查询顶层 `data.persistentId`，而官方规范可能将正确 DOI 存在 `data.latestVersion.datasetPersistentId`。单独[事先冻结唯一规范版本字段兼容](../../protocols/R101_PHASE_A2_DATAVERSENL_LATESTVERSION_DATASET_PERSISTENT_ID_ONLY_COMPATIBILITY_FREEZE_2026-10-17.md)、保留第一次失败工作流、另添加三项纯synthetic并对原 API 再执行。

真实GitHub Actions官方JSON审计成功，把[真正 Phase A2匿名源目录收据](R101_PHASE_A2_LIVE_CI_OFFICIAL_METADATA_ONLY_RECEIPT.json)永久提交[Git 6c3ac2ca](https://github.com/edwardsage419/Psychohistory-Research/commit/6c3ac2ca24b22644f172033518d6643cb2ce6898)，本项目从main重新取得此收据并核验。在本次官方目录原数据：

| 官方源可验证元信息 | 真正结果 |
|---|---:|
| DOI | 10.34894/EYFM5L |
| 原文件目录记录数 | **9** |
| 目录全部文件格式 | **ZIP** |
| 九份文件总登记大小 | **43,631,177 bytes** |
| 目录公开独立MD5字段记录数 | **0** |
| 目录直接CSV/TSV/TXT文件 | **0** |
| 本阶段真实文件体下载 | **0 bytes** |
| 本阶段任何真实人行动或模型评分 | **0** |

从官方服务获得的9份ZIP文件元数据存在，只说明正式原来源目录和引用解析成功。**不能推断九份ZIP都包含真人逐回合行动，不能假定其中有真正独立session/actor/opponent ID，也不能说已经完成原始文件E1认证。** 每份fileID/名称暂不公开、也不进行批量下载与自动解压，因为ZIP内可能有代码、隐私与不符合研究需要的资料。

## 下一步

R101 Phase B前还需另先冻结**只读官方ZIP目录级元信息选择**：确定这九份ZIP的公开官方fileID、用途描述及精确大小，从作者公开说明选择真正游戏逐轮原数据所在一份，冻结独立源文件哈希与ZIP上限/安全路径/压缩炸弹保护，再进行真正文件体下载、完整字节MD5/SHA及CSV或其它游戏纪录的元数据-only身份审核。真实回合行为必须在人员/对手/同场配对/原实验室session真实来源字段和合法留出合同再冻结之后才读。无法证明source actor/opponent时立即有界阻断，避免复制R100误当行数独立性的失败。

本阶段**E0目录级真实认证成立，E1原始人类行为文件=NOT_ESTABLISHED，E2=0**。R095 8session阴性、R096 FP/SP异质和R099组历史阳性均保留；不得跨二元/连续指标直接合并。
