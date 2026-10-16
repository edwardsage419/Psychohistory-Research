# R066 E2：纵向网络—态度数据仓库可用性核查协议（检索前冻结）

日期：2026-10-16。研究身份：实证输入获取门，非意见动力学模型拟合或外部验证。沿用 `protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md`。

## 研究目标

核实 Larson–Lewis 2026 论文声称的 Harvard Dataverse 数据集 `doi:10.7910/DVN/RAHSVM` 是否具有**可公开解析的数据集目录、具体已发布版本、文件标识、非个人来源元数据和许可**。外部网络可能失败，因此必须区分：
- `PUBLIC_PUBLISHED_METADATA_VERIFIED`：公开 Harvard Dataverse API 返回 `status=OK`、版本已发布且明确列出文件。元数据可用不等于文件内容可用。
- `DRAFT_OR_RESTRICTED_METADATA`：明示草稿、禁访或数据存在但文件受限。
- `NOT_FOUND_OR_UNREGISTERED`：Dataverse API 明确 HTTP 404，且返回有效 API 结构/明确 NOT_FOUND；该结论只限查询时点，不断言永久不存在。
- `NETWORK_OR_UPSTREAM_UNRESOLVED`：DNS、TLS、超时、429、5xx 或其他无法判定响应。**不得将此项当作不存在**。
- `RESPONSE_SCHEMA_UNRESOLVED`：HTTP 成功但缺少足以验证的 API 元数据。

作为访问环境控制，使用已知 2016 Harvard Dataverse 公开数据集 `doi:10.7910/DVN/JIIICD`（Klar, *The Effect of Network Structure on Preference Formation*），验证同一 API 的可达性。此控制仅校准 Dataverse API 可达性，不代表 Klar 数据已经符合 R066 的重复个人态度+关系网络标准。

## 固定 HTTP/API 入口

标准数据集接口：`https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/RAHSVM` 和相同路径的 `doi:10.7910/DVN/JIIICD`。另仅记录 DOI landing `https://doi.org/10.7910/DVN/RAHSVM` 的 HTTP 状态及最终域名，**不**据跳转的非成功即断言未注册。请求使用标准库 `urllib.request`、Python 3.11、每次连接超时 20 秒、失败最多 1 次重试。只有 GET，无认证令牌、无表单提交、无邮件、无私人数据、无下载任何数据文件。

在元数据成功时输出：数据集 DOI、标题、最新版本主/次号、该版本发布时间、版本 release 状态、许可名/URL（如可见）、`dataFiles` 里每项的**文件名/格式/字节长度/公开或限制标记**。不得输出人员名字、邮箱、逐人数据或文件内容。为控制目录数量，最多 200 个文件的元数据，超过则标 `FILE_LIST_TRUNCATED`，不可判为完整清单。控制组只输出可达性、版本和文件数量。

## 明确的科学门槛

就算 `RAHSVM` 数据集存在且有文件，也必须在将来另冻协议后才可下载和审查列字段。可识别三模型所需最小字段是：可跨波关联的受试者匿名 ID、同一人的基线/末次态度量表、受试者间村内网络边、实验处理和时间点（对 DeGroot/FJ/HK 未修改的模型形式，还需提前规定冲击进入方式、缺失/失访与非实验网络形成的问题）。**元数据成功不构成测量/模型通过。**

优先来源顺序：真实论文及其数据 DOI；若受阻，保留第二公开数据来源作为候选，不立即将任何代理变量升级为“真实意见”。

## 证据与 CI

先提交协议、程序及合成 fail-closed 单元测试；再运行 GitHub Actions 真实查询，将匿名元数据审计 JSON 作为 artifact 和永久研究索引。失败或未明确发布必须写真实状态，禁止默许继续拟合。

`R066_DATAVERSE_DISCOVERY_PROTOCOL=FROZEN`
`R066_THREE_MODEL_REAL_DATA_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
