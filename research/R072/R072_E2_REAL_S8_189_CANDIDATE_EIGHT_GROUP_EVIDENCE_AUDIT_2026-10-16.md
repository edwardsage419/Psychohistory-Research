# R072 结题后 E2 来源进展：189条匿名候选、8组规模复核与处理标签尚未识别

日期：2026-10-16。**本报告使用真正取得且SHA固定的PLOS真人现场实验数据，形成了匿名源结构层证据，并完整保存未能证实的编码映射；不等于原作者人类实验影响的独立复验或R072自制IMAGE/STANDING/STERN模型的实证验证。**

## 来源和作者独立发表的标尺

van Apeldoorn & Schram (2016), *Indirect Reciprocity; A Field Experiment*, PLOS ONE 11(4):e0152076，完整官方论文 [https://doi.org/10.1371/journal.pone.0152076](https://doi.org/10.1371/journal.pone.0152076)。官方附录 S8 XLSX [https://doi.org/10.1371/journal.pone.0152076.s008](https://doi.org/10.1371/journal.pone.0152076.s008)。作者 Table 3 报告**189次服务请求**，其中服务历史档案96、中性档案93，八个性别×国家×服务历史实验档案接收的请求量分别为30、28、19、19、30、25、19、19。作者 Table 1 区分至少四种不同结局：任何回应、直接回答 yes、yes-or-maybe、明确 no；若不回信，它不等于“回信后说 no”，且没有依照出版物定义就不能把原工作簿任意数字当作这些结局。出版物报告有约47%收到任何回应，但本文下一步不应根据“数值恰好89/189≈47%”猜测源表中二元列的心理含义。作者原论文真正估计了人类服务历史档案的处理效果，本研究**迄今没有重算那些真实差异/标准误/随机化检验**。

本项目本轮所有读源任务继续锁定出版者 PLOS 自己签发的特定对象、仅内存使用的实际 XLSX原件：**38,647字节，SHA256 `5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`**。原 XLSX 未进入 GitHub、从未输出参与者账户/原字段名/单个回应值；对应当期正式[来源恢复/匿名结构报告](R072_E2_PLOS_S8_PUBLISHER_RECOVERY_AND_SCHEMA_AUDIT.md)。法律与伦理：出版的论文为CC-BY并附S8数据，但本研究不发布已收集人的逐个档案/原始请求记录，也不推断个人身份；论文中的真实受试者在当时未事前获悉其所收请求是实验。

## 阶段1：REV-004先不试图拟合或凑齐出版者的189

真正**在读任何工作簿的真实非表头值之前**先提交 [REV-004 匿名列域/客观行数协议](../../protocols/R072_E2_PLOS_S8_REV004_AUTHOR_ROW_UNIVERSE_AND_COLUMN_DOMAINS_2026-10-16.md)，原 protocol Git commit `a5045dd6e8c022b14613058477355b6989e8da80`。第一次真实[CI run 38926189750](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926189750) SUCCESS，**18项纯虚构测试PASS**，精确来源SHA校验后匿名读数如下：

- 1张表，物理199行标签中含1表头＋**198个非表头物理行**，全部198行至少有一个非空字段；
- 列1：198个非空格，其中**189为 numeric、9 为 text**，合计17种不同的匿名原值；
- 列2：**189**个 numeric，另外9行空缺，恰只有**2种不同 numeric 值**，且值在预先限定的二元0/1集合；
- 列5、6、7、8、10：各有189个 numeric、9行缺失；列3仅93个非空（89数值、4文本）。**不可在未经作者编码说明前将列3的89数值解释为答复人数或直接同意次数**；
- 全部10列均非空的真实非表头行只有 **89行**；若以“每行10列全填”当完整样本，会严重错漏未回应的人以及表格说明行。这些是客观结构数量，不是对人类合作效果的证据。
- 严格不按任何待观察的结果变量事后删行时，REV-004保持**`ROW_UNIVERSE_MISMATCH`**：198个非表头物理行不是论文189次请求。研究档案没有为了凑189把9行抹去。

该完整6,473字节匿名JSON来自真实CI结果SHA256 `2b1f26b3d615a393ada59b1b0f51c356f619467ecaae3bb6b4ce32b64611c7fa`，在[重放归档 run 38926470942](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926470942) 再次重算与固定哈希核验后，已永久进入[完整REV-004真实匿名汇总](R072_E2_PLOS_S8_ANONYMOUS_COLUMN_DOMAINS_REV004.json)。

## 阶段2：看到类型结构后另冻结 REV-005，只核8个匿名组规模

REV-004后才提出**事后探索性**“非表头行中若第一、二列均为数值格式，则作为候选请求记录，其他为格式不匹配行”的规则。此规则提交于[REV-005协议](../../protocols/R072_E2_S8_REV005_ANONYMOUS_BLOCK_COHORT_PARITY_2026-10-16.md)，commit `ff53f272ab5e13c15c1438a5b617057327c59f52`，之后才首次运行真实候选八分组。首轮[run 38926856955](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926856955)因**人工合成分段测试夹具**失败，真人数据工作流未执行，负结果保留；修复测试后 [run 38926940610](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926940610) **15测试PASS＋真正原件候选分组计数SUCCESS**。

获得确切匿名结果：

| 结构性核对 | 本项目实际算得 | 仍不能推断 |
|---|---:|---|
| 非表头全部物理行 | 198 | 不能机械丢弃任何9行 |
| 第一列和第二列均数值的“候选请求” | **189** | 尚未由作者代码字典确认189恰为全部有效实验样本 |
| 其它格式行 | **9** | 是否注释、说明/有效条件及作者原始纳排仍需确认 |
| 第一列候选numeric不同编码 | **8** | 未确认哪一码是服务历史、哪一码是中性 |
| 8组匿名编码对应规模排序 | **19、19、19、19、25、28、30、30** | 仅组规模多集与作者Table3一致，不等于8个真实实验身份标签一一对应 |
| 第2列候选numeric两种预定义代码 | **0:100，1:89** | 绝不直接称作89名回应者或任何制度服务历史处理组 |

源数据的这八个**匿名组规模**作为一个多集，完全匹配作者Table3的八个组规模排序；但这只是 **`STRUCTURAL_GROUP_SIZE_MULTISET_MATCH`**，不是服务历史与中性档案的96/93精确分配身份确认、更不是随处理而变的回应率结果。那189个候选数字行在原Excel物理顺序中连续，没有根据结果做分段拟合。

真实REV-005完整1,790字节匿名JSON SHA256 `2df9275477749e8f8ad6a91b890f705172b4d70b1fa617d3275253c618497086`，[归档CI run 38927095385](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38927095385)重复执行15项纯虚构测试和原始真实来源审计，成功将[全部正式匿名八分组结果](R072_E2_PLOS_S8_ANONYMOUS_PROFILE_BLOCK_PARITY_REV005.json)同步到 GitHub。**两份永久结果均由真正 PLOS 原件生成而非纸面汇总**。

## 阶段3：REV-006 对剩余9个非候选行查找内嵌字典

已在尚未读取这9个非候选行的具体文本前，另立[REV-006 匿名关键词字典门](../../protocols/R072_E2_S8_REV006_INTERNAL_CODEBOOK_LEGEND_DETECTION_2026-10-16.md)，commit `be4962eee341e697679c451e8aaa4af340a23158`。只允许对作者说明行的发表语义白名单扫描**存在/不存在**，不复制个体文字、用户名、原列名或逐人回答。[真实 CI run 38927407735](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38927407735) **12项合成安全测试PASS＋真人原件元数据任务SUCCESS**。9条非候选行**都排在189条候选之后**；汇总能检测到 female、male、israel、service、neutral、yes、maybe、no、reply等公开概念，但没有独立且明确的**数字代码=服务历史/中性组**双端赋值格式，因此不能补齐缺失的作者数据字典：`AUTHOR_CODEBOOK_STILL_NOT_RECOVERED`。

真实REV-006完整匿名元数据已由单独 GitHub归档机制保留；旧 REV-004 / REV-005 的方法和计数不会因后续发现而回改或伪称一开始知道9行说明性质。

## 截止这轮独立核验能证与不能证的断言

- `PLOS_REAL_ORIGINAL_SHA=PASS`；
- `S8_ROW_STRUCTURE=198_PHYSICAL_PLUS_1_HEADER`；
- `S8_POSTEXPLORATORY_CANDIDATE_ROWS=189`；
- `S8_PROFILE_GROUP_SIZE_MULTISET=EXACT_MATCH_TABLE3`；
- `S8_SERVICE_HISTORY_TREATMENT_CODE_MAPPING=NOT_RECOVERED`；
- `S8_96_93_SERVING_VS_NEUTRAL_IN_SOURCE=NOT_INDEPENDENTLY_REPLICATED`；
- `S8_89_ONES_BELONG_TO_WHICH_OUTCOME=UNVERIFIED`；
- `S8_REAL_TABLE1_RESPONSE_OR_YES_MAYBE_NO_EFFECTS=NOT_REPRODUCED`；
- `HUMAN_IMAGE_STANDING_STERN_JUDGING_MODEL_E2=NOT_IDENTIFIED`；
- `R072_ORIGINAL_CLOSED_BOUNDED=UNCHANGED`；
- `E3=OPEN`，`PESEN_v0.1=FROZEN`。

下一步如继续采用此作者资料，应首先恢复**具真实来源身份的作者编码字典及实验身份/服务历史编码**：可查论文的明确原文补充说明或作者公开分析代码；绝不凭“某种编码让结果正好支持论文结论”去倒找处理字段。只有跨过编码身份关，才新冻无需使用原始参与者标识、可重复的隐私安全 Table 3（96/93处理组）和 Table 1（不同回复分母）计数协议。若无代码本，应 `BLOCKED_AUTHOR_CODEBOOK` 并转向其他合法、编码清晰的E2真实资料，不得制造心理机制实证的成功。
