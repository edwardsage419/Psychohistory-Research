# R101 Phase A2：Dataverse原API DOI字段版本兼容单项修订（零行为）

日期：2026-10-17。原先已永久归档的[R101首次真实元数据fail-closed](../research/R101/R101_PHASE_A_LIVE_CI_OFFICIAL_METADATA_ONLY_RECEIPT.json)仅报固定`R101_OFFICIAL_DATASET_DOI_MISMATCH`，不得删除覆盖。该错误来自原程序**只**读取`data.persistentId`，而[Dataverse官方API文档](https://guides.dataverse.org/en/6.10.1/api/native-api.html)说明版本元数据可能于`data.latestVersion.datasetPersistentId`返回规范永久DOI。因此冻结**唯一字段容错**：先读取`data.persistentId`；字段缺失时才允许回退至`data.latestVersion.datasetPersistentId`，并且必须仍与确切`doi:10.34894/EYFM5L`大小写折叠完全相等。两字段同时有值且冲突时安全拒绝。该修订不改变官方HTTPS host、唯一源API、文件目录不读具体行为、MD5/大小类型校验、匿名报告、失败即拒绝及PESEN v0.1冻结。

原R101工作流先改为仅手工运行以保护首次失败收据。随后单独提交兼容源函数及synthetic中三种测试：仅旧字段正确、仅version字段正确、两字段相冲突应拒绝。独立新CI工作流将生成新路径`research/R101/R101_PHASE_A2_LIVE_CI_OFFICIAL_METADATA_ONLY_RECEIPT.json`，**不能覆盖历史第一失败**。即使真实官方元数据目录通过，仍属E0元信息资格，不等于任何真正原CSV字节哈希E1，更不等于真人行为预测E2。原作者论文报告336人、八人群体仍保留“出版设计数字，尚未由本项目数据源独立核实”限定。

本研究若出现新独立错误，保存真实异常码并按额外固定证据关口决策，不允许暗中改成宽松来源路径。
