# R066 E2：Larson–Lewis 2026 公开数据集固定 V1.0 文件审计协议

日期：2026-10-16。**在三个原始文件首次读取前冻结**。该步仍是数据来源和模型可识别性测量审计，不进行模型优化或因果推断。

## 元数据关口已经独立通过

先前 [Dataverse 目录协议](R066_E2_DATAVERSE_CATALOG_AVAILABILITY_2026-10-16.md) 与 GitHub Actions run 38862426339 成功核实哈佛数据仓库 `doi:10.7910/DVN/RAHSVM` 已发布 `V1.0`，release_time `2026-07-29T00:35:44Z`，公开许可 `CC0 1.0`，完整三文件目录：
- `Data_LarsonLewis_nws.tab`，datafile ID `14101729`，444658 字节，公开表格；
- `LL_SpecialIssue_Replication.R`，ID `14101728`，72914 字节，原作者 R 复现代码；
- `Uganda_Codebook_NWS_2026.docx`，ID `14101730`，30623 字节，原作者代码本。

## 必须通过的来源/解析门

1. 下载必须只访问 `https://dataverse.harvard.edu/api/access/datafile/<fixed-id>`，固定上述三个 ID。用标准库 HTTP GET，限制下载字节数及 20 秒单请求超时；不处理登录认证、不使用私人连接、不向仓库写原始个体行。哈佛 Dataverse 的 Tabular API 可能返回自动转换的 TSV 内容，因此以目录固定 ID、已发布版本、返回字节及运行时 SHA256 为证据；如果下载大小不同于元数据 declared filesize，明确 `SIZE_MISMATCH/FORMAT_CONVERSION`，保留实际大小与哈希，**不可自动判定字节一致**。
2. 原始 tab 要 UTF-8 严格解码、解析首行字段和其余行，记录**总行数、总列数、重复字段名、行宽错误数、空列名**。超过 10MB、2000 列或 100000 行须 fail closed。只输出已删敏的字段名及与 `attitude/baseline/endline/village/network/treatment` 相关的列名关键词匹配，**不输出任何原始 respondent ID/答案/网络边**。
3. 对作者 R 脚本仅解码和做源字节哈希，记录实际大小、行数、与问卷/网络相关的安全模式词（是否包含 `read.csv`, `read_dta`, `network`, `edge`, `attitude` 等），不提取原始个人数据或全文复刊。
4. 对 DOCX 用 ZIP/OOXML 完整性检查并统计 `word/document.xml` 中非空段落、表格数/文本节点数量；允许在报告中记录**关键词出现次数**，不转载问卷个人信息或整份说明书。
5. 事先将三文件目录及 V1.0 标识、发布日期、许可证作为固定基准记录，若目录元数据在实际文件读取前变化，记录 `VERSION_DRIFT` 不是 PASS。所有源内容仅用于临时 runner 内存，上传 artifact 仅包含代码生成的无个人识别的结构/散列统计。
6. 代码结构同时预留与完全非科学数据源下载错误的分离：403/404、超时、文本非 UTF8、字节数/列宽错误都不能伪造原数据 PASS；后继模型拟合仍须新协议，且必须明确网络真实边、冲击/干预和个体两波索引如何处理。

## 验收

- `SOURCE_SCHEMA_PASS`：三个文件内容确实读取、大小与 V1.0 目录固定元数据一致且格式检查通过；该 status 仅代表文件来源结构成功。
- `SOURCE_OR_SCHEMA_BLOCKED`：下载、字节与格式门任一失败。
- `MODEL_IDENTIFICATION_READY`：**本轮严禁设为 YES**。即使字段名匹配，仍须人工/codebook + 数据实际关联审查、模型状态观测和因果时序识别，不通过该门。
- 单元测试先行：确定性假数据散列、异常行宽/字段重复、字段脱敏、DOCX 非 ZIP、脚本关键字扫描与源大小异常拒绝；GitHub Actions 合成作业及真实数据作业分开。

`R066_REAL_SCHEMA_PROTOCOL_FROZEN=YES`
`R066_EMPIRICAL_SEVEN_MODEL_COMPARISON=NOT_APPLICABLE`
`R066_EMPIRICAL_THREE_MODEL_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
