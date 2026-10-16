# R072 结题后真实资料恢复：PLOS 2016 原始 XLSX 字节与匿名结构核验

日期：2026-10-16。**本成果确实通过两个真实来源 CI，但不构成真实信誉模型拟合。** 本报告只是对前次失败的安全源恢复及合规测量适用性重新评估。R072 既有 `CLOSED_BOUNDED` 的范围、E1 原始结果与首次来源失败记录不被替换；`E2_SOURCE_BYTE=PASS` 和 `E2_ANONYMOUS_SCHEMA=PASS` 必须与 `E2_REAL_MECHANISM=BLOCKED` 分开。

## 1. 原始失败的具体原因和最小修复

R072 初次仅从出版者/DOI 认可主机下载 [PLOS S8](https://doi.org/10.1371/journal.pone.0152076.s008)。[初次 run 38921163855](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38921163855) 的来源任务失败（13条安全测试 PASS），当时学术档案如实记为 `SOURCE_UNRESOLVED`。

之后核对真实 PLOS 出版者 S8 附件入口：其将请求重定向到 Google Cloud Storage 中 **PLOS 指定的 `plos-corpus-prod` 对象**，并带有出版权限的临时 `X-Goog-*` 签名。这揭示了最初仅允许 PLOS 域名跳转的源白名单过窄，而不是证明学术附件不存在。为防扩大攻击面，**在第二次实读源数据之前**另冻结[REV-002 限定对象路径/签名委托链协议](../../protocols/R072_E2_PLOS_SIGNED_ORIGIN_REDIRECT_RECOVERY_2026-10-16.md)，commit `ff00fd649d795401386bb9075925e6204c639556`，只允许 PLOS 自己的服务器跳转到确切 DOI `10.1371/journal.pone.0152076` 版本目录下的 `pone.0152076.s008.xlsx` 对象，检查 signed URL 格式、文件类型、ZIP限制和 CRC，不接受其他 bucket、路径或事先自行提供的存储 URL。工作流中从不记录签名 token。

[真实 REV-002 Actions run 38924258028](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38924258028) 两个 job均 `SUCCESS`，**22项**原点验证/对象白名单单元测试 PASS，真正取得原作者 XLSX 字节：**38,647 bytes**，**SHA256=`5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`**，OOXML容器完整。没有读取内部任何 human 表格值、也没有将原始数据存储在Git。

## 2. 先冻结新阶段才匿名检查真实工作簿

取得正确字节后，在**第一次解析真实 XLSX 工作簿内容前**另冻结[REV-003 原作者数据结构隐私协议](../../protocols/R072_E2_S8_ANONYMOUS_SCHEMA_DIAGNOSTIC_2026-10-16.md)，commit `83ad91f1c1f504e0a0720b16a944071ccdd0a85f`，锁定真实 SHA。使用只读 ZIP/XML，不输出原始字段名、工作表名称、任何成员身份/个人记录/个人特征、任何数据行/数据值，仅允许匿名表尺寸和预先指定的安全表头**关键词类别计数**。

[首次 REV-003 Actions run 38924768397](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38924768397) 因4个人工 OOXML 测试夹具问题而失败，真实源作业跳过；[第二次 run 38924890902](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38924890902) 又因人工 DTD 夹具的一条表头字符串索引缺失而失败；两次失败均可复核。仅修复**合成测试**而没有修改原作者源文件或解析程序；第三次 [GitHub Actions run 38924991302](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38924991302) **19 项全部安全测试 PASS、真实匿名表结构 job SUCCESS**。

原作者 38,647 bytes SHA 固定 Excel 实际诊断：

| 匿名结构字段 | 实读结果 | 含义限制 |
|---|---:|---|
| Sheet数量 | **1** | 未输出原作者给它起的 sheet 名 |
| Sheet 1 XML row 标签数量 | **199** | 不是经过作者纳排的真实参与者数/有效请求数 |
| Sheet 1 最高使用的列序号 | **10** | 不是10种经过模型识别的人类心理指标 |
| 非空单元格总数 | **1819** | 并不代表独立个体行动数量 |
| 按OOXML储存为numeric的单元格 | **1790** | 未读取/输出原始数字与含义 |
| 按OOXML储存为text的单元格 | **29** | 未读取/输出原始文本与可能的身份 |
| 从第1行字段文本检测的白名单类别 | `provider:1; reference:2; request:1; service:2` | 仅字段名关键词被检测，**不是**作者字段字典/真实行为测量 |

其余预先指定的 `treatment, condition, group, accept, response, profile, neutral, history, reputation, date` 等白名单类别命中数为0。**这绝不能证明原表没有接受行为/分组信息**；同一作者可能使用其它字段命名/代码/多列组合才定义这些概念。因此标 `CANDIDATE_NAME_ONLY_NOT_AUTHOR_DATA_DICTIONARY`，当前未知“哪一列是 serving-history 处理”“哪列是 yes/maybe/no 反应”等。

## 3. 与论文公开原始实验设计严格对照

作者 [van Apeldoorn & Schram (2016), *Indirect Reciprocity; A Field Experiment*, PLOS ONE 11(4):e0152076](https://doi.org/10.1371/journal.pone.0152076) 对 **189次**服务请求的随机 profile 类型分配发表了明确陈述：曾提供服务的服务档案组 **96**，中性资料组 **93**，请求对象具有在线可提供服务的状态且最近两周曾登录。真实实验是**2013年5月8–13日**向不同社区成员发送请求，随后在5月14日相关实验 profile 被网站删除；论文主要检验下游互惠，即对标注“曾帮助过第三人”的请求是否更多正面回应。这是作者**已发布的研究设计**，不是我们的真 Excel 统计结果。

**199个 XML 行标签与论文中189次请求并不构成有效记录数量矛盾的已证事实。** XML row标签可包括标题、超出分析范围的记录、公式格式或其他数据区块；当前未经作者数据字典、纳排规则及索引匹配，不能擅自假定“198条个人数据比189条多9条”或删除10行让数字匹配。另作者的随机二元历史资料操作不等同 R072 的 Image Scoring、Simple Standing、Stern Judging 三种逐笔信誉更新方式；即使能复现服务历史组与中性组的总体反应比例，也只能检验**不同的真实二元服务历史讯号问题**，无法一步证实原 R072 玩具模型的三条评价规则。

## 4. 截至本次科学状态

- `R072_S8_OFFICIAL_PUBLISHER_BYTES=PASS_SHA_PINNED`；
- `R072_S8_ANONYMOUS_WORKBOOK_STRUCTURE=PASS_PRIVACY_BOUND`；
- `R072_S8_ACTUAL_AUTHOR_CODEBOOK_AND_ROW_UNIVERSE=NOT_RECONSTRUCTED`；
- `R072_REAL_SERVING_HISTORY_RANDOMIZED_RESPONSE_TEST=NOT_PERFORMED`；
- `R072_REAL_IMAGE_STANDING_STERN_JUDGING=BLOCKED_EXPERIMENTAL_MEASUREMENT`；
- `R072_EXTERNAL_INDEPENDENT_E3=OPEN`；
- `R072_RESEARCH_ORIGINAL_CLOSURE=CLOSED_BOUNDED_UNCHANGED`；
- `PESEN_v0.1=FROZEN`。

下一步不是制造新的合成模型，而是**先从作者正文与所有公开列的实际编码核对实验纳排及处理/回应变量**，制定明确可重放、保护真实个人记录的分析协议，若通过再复验 189 个纳排数量和作者 Table1 的原始匿名分组计数。任何真实统计之前必须冻结解释，避免观察到方向后自选编码；原始人类数据保持 Git 外临时处理，Git 仅接纳足够匿名的核验摘要。
