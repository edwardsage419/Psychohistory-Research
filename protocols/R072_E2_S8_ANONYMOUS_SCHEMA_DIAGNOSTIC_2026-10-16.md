# R072 后续真人原件：PLOS S8 XLSX 匿名工作簿结构与测量合同诊断（REV-003）

日期 2026-10-16。**在本阶段首次解析真实工作簿任何 sheet 内容前冻结**。独立于 [REV-002 字节恢复协议](R072_E2_PLOS_SIGNED_ORIGIN_REDIRECT_RECOVERY_2026-10-16.md)。REV-002 CI run `38924258028` 已确认原作者 PLOS 2016 S8 真实 XLSX byte length=38647，SHA256=`5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`，22项安全测试 PASS。**不因为首次成功取得文件就认为已证明任何人类行为模型**，也不改写 REV-001 失败 run `38921163855`。

## 真实源与精确重新获取条件

出版者 DOI `10.1371/journal.pone.0152076`，附录 S8 DOI `10.1371/journal.pone.0152076.s008`。每次工作流都必须先按 REV-002 的源入口签名委托链验证文件，原始 SHA256 **必须精确等于**上述已通过的不可变指纹。只使用 PLOS 内容发布链，不使用第三方上传或私人数据。ZIP大小、CRC、宏脚本/外链/ZipBomb上限沿用 REV-002 的验证函数。

## 本轮最小匿名表结构授权

以前研究阶段明确不读取 XLSX 单元格；**本独立新协议才允许第一次解析** workbook 的基本结构，但不允许输出任何逐人记录。使用受限且可复现的 OOXML 只读解析器（Python 标准库 ZIP/XML，无 VBA/外部公式执行，不改变文件），在内存中限读 `xl/workbook.xml`、`xl/_rels/workbook.xml.rels`、`xl/sharedStrings.xml`（如存在）和各张 `xl/worksheets/sheet*.xml`。只统计**最多20张工作表**的非空/数字/日期式/空单元格、列数量、含数据的行数量，及表头**去身份化**的语义关键词类别。严禁导出 sheet 标题、原始字段标题、个人、群体或 profile IDs、邮件、国籍/性别/国家、任何原始受访行、单元格值与响应向量；这些信息可以在原始出版物中找到，但不能无意复制至本项目 Git 历史。

只允许白名单语义词匹配（忽略大小写，不输出原词）：
`treatment, condition, group, request, accept, response, provider, profile, service, serving, neutral, history, reference, reputation, match, time, date, outcome, reciprocity, control`；
总结果每个类别仅布尔列是否存在 + 匹配列数量，不记录列号或原始可识别字符串；全表列数与行数作为计量元数据。若实际标题不同、不匹配，输出 `MAPPING_NOT_ESTABLISHED`，不以列名猜测创造作者变量。若 sheet 在第1行存在标题，允许读仅前2行的列类型供安全诊断，**不向外写任何文本**。列可含真人人口或可识别文本，但不得在工作流日志中输出，禁止 `print` 原始 XML、单元格或未清洗报错。超长、非安全路径、外部关系、不可解析XML、超过20张/200列/10000行的任意工作簿，状态 `SCHEMA_UNRESOLVED`，并保留旧真实原始哈希已验证的 E2 字节级状态。

### 强制核验

至少16个在**人工生成的假 XLSX**上执行的安全测试：有效 OOXML 基本结构、没有真实字段文本泄漏、标题未列在第一行导致 `MAPPING_UNESTABLISHED`、工作表数越界拒绝、成员路径越界拒绝、异常XML拒绝、sharedStrings表头只转匿名类别、真实示例外的自定义昵称/PII不产生输出、真实源 SHA 变动 Fail closed、禁止下钻人类个体行为。真实 CI 在全部测试成功后，才执行从 PLOS 取得原件、SHA固定，再运行只统计结构的匿名审计，返回唯一 SHA+sheet数+各sheet结构计数+白名单类别和 `HUMAN_R072_MECHANISM_FIT=NOT_PERFORMED`。原始资料不落盘于 repo。

本论文实际研究是**单次真实服务请求**的随机资料/服务历史 profile 信息差别，可能没有面向4人互动的按次 PUBLIC信誉更新，不保证同 R072 的固定策略/错误信号模型合约。**即使工作簿结构验证通过，也不代表达到 E2 机制识别**。可在未来预注册对作者真实下游互惠的简化二元响应复核，但必须先核对字段字典、授权、样本抽样设计和处理条件，不得直接把公开的189次请求当作本项目的189条有效独立回归样本。

`R072_S8_REV003_SCHEMA_PROTOCOL=FROZEN`
`R072_S8_ORIGINAL_SHA_LOCK=5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`
`R072_HUMAN_IMAGE_STANDING_STERN_FULL_MODEL=BLOCKED_MODEL_CONTRACT`
`PESEN_v0.1=FROZEN`
