# R072 REV008 真实人类原始数据：出版者编码字典独立恢复失败的正式审计

日期：2026-10-17。继承[R072 REV007八组匿名回应合计与作者 Table1精确配对](R072_E2_REV007_REAL_TABLE1_ANONYMOUS_GROUP_CHECKSUM_AND_SCIENTIFIC_BOUNDARY.md)，本次**不扩大原R072自制信誉机制模型**，只按来源伦理限制检查能否把原始第一列八个数字编码与“显示服务历史/中性”绑定。本研究为事后探索性**来源验证工作**，不是作者论文效果复现或模型实证外推。

## 实际使用的三种不同证据必须区分

1. **出版社论文的一手文字**。[van Apeldoorn & Schram (2016), PLOS ONE DOI 10.1371/journal.pone.0152076](https://doi.org/10.1371/journal.pone.0152076) 的 Methods 陈述：研究者制造八种性别×国籍×历史资料的匿名实验档案，为189名最近登录、公开表示能提供服务的社区成员随机派发一次服务请求，处理分为96次有历史、93次中性；Table1分别报告是否有回复与 yes/maybe/no 等回复类别。作者公布的研究效果属于**原作者**的科学报告，不代表R072复算过。
2. **真正独立取得的S8数据来源**。PLOS S8 DOI `10.1371/journal.pone.0152076.s008` 出版原始38647字节 SHA256 `5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`，此前已确认198物理非表头行由189numeric候选/9末尾非候选行组成；8个无名组大小和第二列编码1人数配对**恰等于**Table1公开八组 `(n,any-response)` 多集。但这是**看了89总回应之后的事后探索性检查**，不等于唯一源代码字典。
3. **本轮真正新观察**：从来源9条非候选行（不观察任何真人回应或结果变量）尝试直接提取能唯一识别八个匿名原值代码的 serving/neutral 含义；不利用Table1分组回应频率及作者效应方向。

## 独立协议、执行与真实阴性发现

[REV008 实验操作协议](../../protocols/R072_E2_S8_REV008_INDEPENDENT_LEGEND_CODEBOOK_BINDING_2026-10-17.md) 在首次对真实来源施加这组匹配规则前提交 GitHub `main`，冻结两条有限规则：(A) 同一真实注释字符串必须出现具有绑定符的明确源数字代码＋服务历史或中性语义；(B) 同一尾行不同单元格拥有独立合法数字代码＋明确、无冲突的 serving/neutral 单一类别。完整代码候选要求唯一覆盖真实**八个**profile数字编码，且两类各四个；部分、无关数字、范围猜测及根据论文已公布96/93补齐均拒绝。程序只输出本身的**匿名布尔**、是否有冲突/范围提示、证据状态和已验证源SHA，绝不输出任何原始档案代码、真人记录、尾注全文、社会身份、个体字符串或回应数据。

[首次Actions run 38930015652](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38930015652)：15个人工合成测试中14成功，一项测试误把“人类响应没有被泄露”这个字段**名称**误判为泄露了真实回应数据；真实来源job SKIPPED，保留完整FAIL历史。只修改失败测试对“不输出原始回应”的判断，不修改主解析模型和冻结规则。随后[真正成功的Actions run 38930145114](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38930145114) **15/15 PASS，真实 PLOS SHA固定原件任务 SUCCESS**，返回：

- `CANDIDATE_ROWS=189`、`NINE_NONCASE_NOTE_ROWS=9`，与此前独立源结果一致；
- `candidate_full_eight_codebook_exists=false`；
- `candidate_unique_serving_neutral_four_each=false`；
- `candidate_conflict_found=false`；
- `range_syntax_hint_present_not_adopted=false`；
- `status=BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK`。

**准确解释**：此有限的两类严格字典语法没有在原始S8的九条说明行找到全部八组数字代码与服务历史标签之间的**可重复独立映射**。不能声称从此证明原作者原始研究没有代码本（它也可能在作者未公开脚本、未检查过的其它资料或不同编码格式中）。本阶段保持未恢复状态，而不能靠试探8组已发表回应率将源代码人为分配至高效组/低效组。

[永久归档 CI run 38930303469](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38930303469) 第二次检验并将真实匿名输出SHA256 `cdc0ec4fe5f076d20f8981891afb42b767fb1735d7646842caac1afbb27d33ae`、1030字节结果永久存档 [R072_E2_PLOS_S8_INDEPENDENT_AUTHOR_CODEBOOK_REV008.json](R072_E2_PLOS_S8_INDEPENDENT_AUTHOR_CODEBOOK_REV008.json)。只有当档案 run `SUCCESS` 且本文件真实存在于 `main` 时，才可视永久存档真正完成。

## 不得跨越的科学门与下一工作取舍

- 原始人类真实行为**来源、行结构、匿名公开描述性分组人数×回应计数**：已取得、可核验，但REV007匹配属于事后探索性证据。
- 原S8的 numeric profile code 到**独立于回应结果**的服务历史/中性二元处理身份：**未建立**，这是最上游阻塞。
- 原 Table3 中96/93作为**真实个体派发过程的独立代码映射计数**：尚未由本项目自己独立核对，不能仅用8组大小拼凑。
- 作者Table2 的probit、yes/maybe/no差异、随机化推断与真正声誉社会心理机制：都**未复现**。
- R072数学模型里的IMAGE/STANDING/STERN三种每笔捐赠评价规范**没有在本真人现场实验中被随机操控**，即使原作者处理码全部恢复，也不能将其作为三规范的直接经验验证。
- E3独立新参与者群体 `OPEN`；PESEN v0.1 `FROZEN`；R072 `CLOSED_BOUNDED` 原研究不回写。

**研究资源建议（后续需要重新冻结）**：此阶段已经完成对同一S8九条注释的两次有界规则家族检查（REV006/REV008），若没有作者本人提供的可审计代码本或发布在仓库里的**来源独立**映射，不宜继续任意变换正则、枚举所有96/93组合、用已见真实回应效果优化规则。下一主线优先寻找**原作者直接记录数据字典的真人数据**，或使用已可恢复语义的R063原作者实证行为、R067真实 IPD 数据来对尚未被E2验证的抽象机制提出清晰问题，而不是继续把证据缺口拖进同一R编号。
