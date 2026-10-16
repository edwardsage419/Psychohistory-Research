# R072：PLOS S8 官方委托云存储跳转恢复协议（REV-002）

日期：2026-10-16；**在本轮首次尝试读取 S8 原始文件、计算原始 SHA256 之前冻结**。本协议与 [REV-001 官方域名白名单源门](R072_E2_PLOS_FIELD_SUPPLEMENT_SOURCE_IDENTITY_2026-10-16.md) 分开保存。REV-001 [CI 38921163855](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38921163855) 真实来源任务 FAIL、安全测试13 PASS，`SOURCE_UNRESOLVED` **继续是真实历史**，绝不删改或事后声称成功。

## 新外部证据与精确安全修订

本轮直接查看 PLOS 出版者 [S8 附件入口](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0152076.s008&type=supplementary)，观察其实际返回 **HTTP redirect 到有时效签名的 Google Cloud Storage URL**；该URL的主机 `storage.googleapis.com`，路径必须以 `/plos-corpus-prod/10.1371/journal.pone.0152076/` 开始，末尾的文件必须是 `pone.0152076.s008.xlsx`；中间可出现纯数字的出版版本目录。PLOS 官网原始文章 DOI `10.1371/journal.pone.0152076`，S8 DOI `10.1371/journal.pone.0152076.s008`。**PLOS签名云存储是其原始附件发布链的一部分**，但不能据此允许任意 Google 存储对象当真数据来源。

只向 PLOS 域名发起初始请求 `https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0152076.s008&type=supplementary`；严格 `HTTPS`；批准相同出版者辖域 `plos.org` / `*.plos.org` / `doi.org` 的跳转，或由 PLOS 官方响应签发的临时 `https://storage.googleapis.com/plos-corpus-prod/10.1371/journal.pone.0152076/<integer>/pone.0152076.s008.xlsx`，要求 query 含 `X-Goog-Algorithm=GOOG4-RSA-SHA256`、非空签名、Credential、Date、Expires，且签名有效期值在1..86400秒。**只有实际由 PLOS/DOI 返回的HTTP跳转才允许进入这条云存储路径，不许单独把陌生用户提供的Google URL作为新来源**。返回后必须精确检查实际最终 URL 仍是批准的 PLOS 委托路径；禁止任何额外不同主机、非指定 bucket、路径 traversal、非指定 XLSX 文件和 HTTP 降级。对这个单个指定对象不使用全域签名 URL 白名单。

从可信源读取最多 **600,000原始字节**、30s超时；必须为有效 ZIP/XLSX 容器且包含 `[Content_Types].xml`、`xl/workbook.xml`，至多60成员/≤3MB解压宣称总量、无宏或外部连接、所有 ZIP CRC 校验通过。无意读取任何真人记录或工作簿内容、姓名、组号、文本、回应值，**仅输出 SHA256、原始字节数、ZIP成员数、来源为 publisher-direct / publisher-delegated-GCS**，不记录/传播带时效认证签名的 URL、Credential 等任何 token。原附件字节仅存于 CI 进程内存，从未写入Git或工件。

在第一次实际重试前新增至少**16个合成URL/ZIP安全测试**，尤其证明：`storage.googleapis.com` 的 PLOS 路径若没有签名/不是 S8/冒名 bucket/存在路径注入/非出版者直接发出的跳转时 FAIL；相同域名其它 PLOS 论文的文件亦 FAIL；不把受限访问错误页面判为 XLSX；对非公开行不做输出。若 HTTP 或 ZIP 真实性失败，真实作业失败、独立匿名失败收据归档且原修订不倒退。成功最高仅 `E2_PLOS_S8_SOURCE_BYTES_VERIFIED`，**绝不**等于 `R072_E2_HUMAN_REPUTATION_MODEL_PASS`。

## 新发现相对于 R072 既有结题的地位

[R072 正式结题](../research/R072/R072_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md) 仍为 `CLOSED_BOUNDED`；本轮是**后续独立源获取修订任务**，不得改写“前版源任务失败”的历史。独立的真人数据行为字典、再利用伦理边界、真正公开信誉的事前可见性、实验分配及保密审查仍需要新协议和证据。真人论文只描述189次现场请求，不等于被试学习了 R072 的 IMAGE/STANDING/STERN 三规则或实验存在三种信息错误处理。E2机制 `BLOCKED_MODEL_CONTRACT`，E3 `OPEN`，PESEN v0.1 `FROZEN`。

`R072_S8_REV002_PROTOCOL=FROZEN_BEFORE_NEW_DOWNLOAD`
`R072_S8_OLD_FAILURE=HISTORICAL_UNCHANGED`
`R072_REV002_SCOPE=BYTE_PROVENANCE_ONLY`
