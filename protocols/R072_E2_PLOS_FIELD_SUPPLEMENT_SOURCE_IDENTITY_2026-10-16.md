# R072 真实现场间接互惠资料 S8 来源字节门——首次下载前冻结

日期：2026-10-16。**在首次尝试自动下载真人原始 XLSX 附件字节之前冻结**。这个独立关口只检验出版社官方原始 XLSX 附件是否可达、字节哈希是否可固定、容器结构是否为有效 OOXML；绝不读取、筛选或发布任何个体回应、成员特征、请求内容、个人 profile、情绪/社会身份信息，**不输出任何数据表格单元**。本步骤上限为 `E2_PUBLISHED_HUMAN_SOURCE_BYTES_VERIFIED`，并不意味着 R072 合成模型获得真人 E2 参数校准。

出版社一手源：[PLOS ONE，*Indirect Reciprocity; A Field Experiment*，DOI 10.1371/journal.pone.0152076](https://doi.org/10.1371/journal.pone.0152076)。官网 Supporting Information 的 `S8 File. Raw Data. (XLSX)` DOI [10.1371/journal.pone.0152076.s008](https://doi.org/10.1371/journal.pone.0152076.s008)，文章附录显示作者使用在线社区请求，**189 个对象**被随机分配到实验 profile 请求处理（论文公布值，非本项目原数据复算），而非四人捐赠及完整实时公告。需要完整理解这项现场研究的伦理与再使用边界——其原参与者并不知道实验正在进行，作者有伦理审批与事后去偏差程序。公开 XLSX 下载不等于该文件自动具有任意形式再分发许可，源文件只在 GitHub Actions 临时内存读取。

首次按照以下固定优先级从官方域名获取单份 S8 内容，不从未知第三方源切换：1. `https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0152076.s008&type=supplementary`；2. `https://doi.org/10.1371/journal.pone.0152076.s008`。HTTP 30秒超时，每次最大 600KB；如果源请求被重定向仅允许 `doi.org`、`journals.plos.org` 和 `plos.org` 下域名；若任何最终 URL 不在出版者可控域，则 fail-closed。若源超过 600KB/HTML 禁止/不是标准 ZIP/无 `[Content_Types].xml`、`xl/workbook.xml`，或任何 zipfile CRC 校验失败，则 `SOURCE_UNRESOLVED`。ZIP 中超过 60 个成员、总解压宣称字节超过3MB、OOXML 含任何 `vbaProject` 或外部数据连接关键词者 fail-closed。**只报告原始 XLSX 的 SHA256、字节数、ZIP 成员总数**，以及官方 DOI/来源 URL；不读取任何 sheet 内容甚至 workbook 字段、成员 ID 或每行响应值。真数据统计、逐人行为量、模型预测和真实样本数保持 `UNKNOWN_NOT_READ`。

只提交经过上限/权限保护的 `source_bytes_audit.py`，至少10项合成恶意 ZIP/HTML/CSV 冒充/超过字节/CRC/外部 URL 判退测试与实际 Actions 下载；原始文件始终不写工作树、不上传归档，只存匿名 JSON 结构收据。如果来源失败，保留失败，不从纸面 “189份请求” 推断原始表确切有效记录数。通过仍需独立 E2 数据字典、合法权限、去标识处理、预注册真人任务规则对齐，才能进入真正模型校准。

`R072_S8_BYTE_PROVENANCE_PROTOCOL=FROZEN`；
`R072_EXACT_REAL_IMAGE_STANDING_STERN_LABELS=NOT_OBSERVED`；
`R072_REAL_HUMAN_BEHAVIOR_MODEL=NOT_FITTED`；
`PESEN_v0.1=FROZEN`。
