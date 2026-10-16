# R072：公共信誉、间接互惠与制度信号可信度

2026-10-16。**正式状态 `CLOSED_BOUNDED`**，已完整验证 **E1 合成固定策略信誉机制**；真实人类 S8 原件访问失败、行为/评判规则对齐未建立，真人 E2 `SOURCE_UNRESOLVED`，独立 E3 `OPEN`；**PESEN v0.1 `FROZEN`**。

主研究：四名抽象代理（ALLC始终帮助、ALLD始终拒绝、DISC见好声誉才帮助），三种公共道德评价规范 `IMAGE_SCORING / SIMPLE_STANDING / STERN_JUDGING` 与三种信息公告方式 `VERIFIED / FLIP_EVERY_FOURTH / NO_OBSERVATION`。受 Nowak–Sigmund 1998（DOI `10.1038/31225`）、Ohtsuki–Iwasa 2004（DOI `10.1016/j.jtbi.2004.06.005`）及 Kandori 1992（DOI `10.2307/2297925`）的理论启发，本研究自定义**有限四人固定策略模拟**，并未声称复算原论文 ESS、历史真人合作或间接互惠经济均衡。

## 完整 E1：实际运行并永久归档

[首次完整试验前冻结的E1协议](../../protocols/R072_REPUTATION_PUBLIC_SIGNAL_DONATION_E1_2026-10-16.md) commit `ee2b2145caa73b1273e1c07b96761b4f0e9fe2f4`；[可执行Python机制模型](r072_reputation_public_signals.py)、[30项测试](test_r072_reputation_public_signals.py)。

3^4=81策略向量×2^4=16初始二元声誉×3评判×3信息制度= **11,664个**独立合成状态，每状态全部12个有向捐赠次序执行2遍，共 **279,936** 个真实执行的代码交易。每次帮助捐赠者成本1/收者收益2，强制验收所有24次经济账务正确与时间先后无泄漏。

- [首次成功 E1 Actions run 38920131192](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38920131192) 实际运行全部11,664案例与30项数学/报告错误/完整宇宙测试，**SUCCESS**。
- [永久原始数学结果归档 run 38920307122](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38920307122) 二次真实重算，经 SHA256 `6137894586488cabcc684ae350e692ccd0c6c2a731d6e0787153197de3a8868a` 完整比对，已将 [45,784 字节全部 E1 结果+配对反例 JSON](R072_E1_FULL_11664_PUBLIC_REPUTATION_RESULTS.json) 永久提交 `main`。
- [完整数学发现、宏观均值掩盖微观变化和限制报告](R072_E1_REPUTATION_SIGNAL_FULL_ENUMERATION_AUDIT.md)。

同样1,296个策略/初始声誉条件等权时，IMAGE在三种报告制度下的总帮助率全为**50%**，但准确公告与每第四次虚假公告之间 **912/1296** 个逐配置实例帮助次数改变，说明**平均不变并不等于局部无影响**。STANDING准确公告下平均帮助率 **56.84%**，STERN准确公告 **54.17%**；在 NO_OBSERVATION 因声誉不更新，三种评判的真实帮助行动在全部配对初态**完全相同**。制度误报在本固定toy设计里对不同规范有相反平均方向，不能推广真实社会“误报有利”或声誉评级福利。

## 真实真人来源和失败门

已建立 [真实信誉行为研究候选及伦理/行为测量缺口](R072_E2_HUMAN_REPUTATION_EVIDENCE_SCOPE.md)。[PLOS ONE 2016 间接互惠现场实验](https://doi.org/10.1371/journal.pone.0152076) 官方文章确实提供 [S8 原始数据 XLSX](https://doi.org/10.1371/journal.pone.0152076.s008) 链接，但本项目以 [先冻结字节来源/隐私门](../../protocols/R072_E2_PLOS_FIELD_SUPPLEMENT_SOURCE_IDENTITY_2026-10-16.md) 尝试官方可靠路径时，[实际 Actions 38921163855](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38921163855) **13项合成来源安全测试 PASS、原始 XLSX 下载 job FAIL、整体工作流 FAILURE**。没有任何真实 XLSX SHA256、真实列名或可信独立行数；[匿名失败机读凭据](R072_E2_PLOS_FIELD_S8_SOURCE_ATTEMPT_RESULTS.json)已保存，未从第三方重新分发人类数据。论文作者报告的189个现场请求属于出版者内容，**不是本研究对源工作簿的原始行数核验**。

即使后来取得原始 XLSX，该人类现场实验不等于本研究指定的四人固定顺序捐赠与二元信誉公开规则，必须另制定伦理合规、数据结构及明确反事实识别合同。不得以论文结果替换自己的 E2，也不推断真人更倾向 STANDING 或 STERN。

## 限定结题与继续

[正式六门验收与有限结题报告](R072_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md) · [机读验收状态](R072_FINAL_ACCEPTANCE_STATUS.json) · [E2/E3/ESS 和长期文化演化开放问题](R072_POST_CLOSURE_OPEN_GATES.md)。

六门 PASS 指**已完成有限 E1 数学机制与真实来源失败证据的可复现科研归档**，并非真实间接互惠或跨尺度历史预测验证。下一步优先寻找**确能合法取得、可固定原始字节和精确暴露/帮助行为/声誉前序的真人来源**，避免项目长期只堆叠相同层次的合成机制。PESEN v0.1 不改。

## 2026-10-16 结题后新增证据：PLOS 原始 S8 文件安全恢复＋匿名结构（不修改 E1 结题）

原先 [真实附件首次来源门 38921163855](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38921163855) 下载失败，**历史记录原样保留**。重新核对 PLOS 下载入口发现其使用签名的 PLOS Google Cloud Storage 对象跳转；[REV-002 独立预冻安全协议](../../protocols/R072_E2_PLOS_SIGNED_ORIGIN_REDIRECT_RECOVERY_2026-10-16.md) 仅允许从 PLOS 正式入口跳转到指定 DOI 的 S8、时效合法签名 URL，并在 [GitHub Actions 38924258028](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38924258028) 中以 **22 tests PASS、真实原件任务 success** 恢复 **38,647 字节，SHA256 `5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`** 的官方 XLSX。

随后[REV-003 匿名结构事先冻结协议](../../protocols/R072_E2_S8_ANONYMOUS_SCHEMA_DIAGNOSTIC_2026-10-16.md)仅允许SHA固定源的工作簿结构与匿名表头类别。最初两次 CI 因合成测试夹具失败（run `38924768397`、`38924890902`），**原件结构还未读取**；修复测试后，[run 38924991302](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38924991302) **19 tests PASS、真实源结构作业 SUCCESS**。原始S8实际只有 **1张工作表、199个XML行标签、使用列至第10列，非空1819格（数字1790、文本29）**；只发现安全匿名表头关键词 `provider/reference/request/service`；**没有发表原始字段名称、参与者身份或任何人类响应行**。

详见[正式新增源恢复审计](R072_E2_PLOS_S8_PUBLISHER_RECOVERY_AND_SCHEMA_AUDIT.md)和[固定来源SHA及匿名机读结果](R072_E2_PLOS_S8_RECOVERY_AND_ANONYMOUS_SCHEMA_RESULTS.json)。PLOS作者报告**189次**服务请求（其中历史服务档案96，中性档案93），这与工作簿物理199个XML行标签不是同一种量；当前**尚未**核对作者样本纳排、具体处理编码、行为变量含义与真实统计。**后续 E2 来源字节验证/匿名结构门现为PASS，但E2人类信誉机制仍未获得识别；R072此前 `CLOSED_BOUNDED`、E1结果及历史失败未改变**。PESEN v0.1继续FROZEN。


## 2026-10-16 后续真人来源进一步实读：189候选记录、8个匿名组规模完全对应作者Table3（编码仍阻塞）

正式延续前两阶段 `S8_SOURCE_BYTES=PASS`、`ANONYMOUS_SCHEMA=PASS`，另立三次真实原件 E2 可适用性核验：

- [REV-004先验协议](../../protocols/R072_E2_PLOS_S8_REV004_AUTHOR_ROW_UNIVERSE_AND_COLUMN_DOMAINS_2026-10-16.md) → [CI38926189750](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926189750) **18测试PASS、真实原件数据结构检验成功**：除一行表头外有198物理行；第1列有189 numeric＋9 textual，第2列189个匿名二元numeric＋9空；**不**用作者报告189直接删除9行。随后[重算归档CI38926470942](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926470942)将[全部匿名列域结果](R072_E2_PLOS_S8_ANONYMOUS_COLUMN_DOMAINS_REV004.json)永久同步main。
- [REV-005另冻事后探索性结构拆分协议](../../protocols/R072_E2_S8_REV005_ANONYMOUS_BLOCK_COHORT_PARITY_2026-10-16.md)，首CI `38926856955`因**仅人工测试夹具失配**失败（历史保留）；修复后[CI38926940610](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38926940610) **15测试PASS、真实189候选numeric行＋9非候选行、8个匿名数值编码规模排序19/19/19/19/25/28/30/30**，与出版者Table3八个档案规模多集完全吻合。但“八种编码对应哪种性别×国家×服务历史”完全未独立解码。[成功归档CI38927095385](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38927095385)发布[匿名八组机读结果](R072_E2_PLOS_S8_ANONYMOUS_PROFILE_BLOCK_PARITY_REV005.json)。
- [REV-006字典来源侦查协议](../../protocols/R072_E2_S8_REV006_INTERNAL_CODEBOOK_LEGEND_DETECTION_2026-10-16.md) → [真实CI38927407735](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38927407735) **12合成保护测试PASS**，真正发现9个非候选行都在189候选记录之后，内含 `service/neutral/yes/maybe/no/reply` 等关键词，但**未证实数值标签与处理组的赋值关系**；[CI归档38927611260](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38927611260)保存[匿名关键词机读负证据](R072_E2_PLOS_S8_ANONYMOUS_FOOTER_LEGEND_REV006.json)。

[详细完整科研审计](R072_E2_REAL_S8_189_CANDIDATE_EIGHT_GROUP_EVIDENCE_AUDIT_2026-10-16.md) · [源层门禁机器状态](R072_POSTCLOSURE_REAL_E2_S8_189_ANONYMOUS_GATE_STATUS.json)。

**严禁误报：** 作者正文中的 `96 serving / 93 neutral` 是**出版者已发表事实**，项目只独立发现8个**未命名**组的数量完全对应；目前没有被权威验证的代码本指出哪4个匿名代码是 serving，亦没有绑定0/1或yes/maybe/no回应值。因此 `R072_TABLE3_SERVING96_NEUTRAL93_REPRODUCED=NO`，`R072_REAL_RESPONSE_EFFECT_FITTED=NO`，`R072_E2_REAL_IMAGE_STANDING_STERN_VERIFIED=NO`。要前进必须从可审计的作者原始说明或出版代码中找到独立编码映射，再另冻真人结果核验协议；绝不可选择看起来能得到更显著效果的映射。**R072 原`CLOSED_BOUNDED`、PESEN v0.1 FROZEN不变。**


## REV-007：PLOS 原始 S8 与作者 Table 1 的八组请求数×回应数精确匿名联合一致（2026-10-16）

在 REV004/005/006 已经核验来源 SHA、198个物理非表头行中的189个numeric候选行和8个匿名组大小多集的基础上，本次[REV-007 独立事后探索性冻结协议](../../protocols/R072_E2_S8_REV007_PUBLISHED_GROUP_RESPONSE_CHECKSUM_2026-10-16.md)事先指定**唯一**候选字段：第2列数字代码 `1` 作为“可能收到任何回复”的候选。因为前阶段已经观测该列共有89个`1`，而出版者论文 Table1已报告总回复89，本轮**不是未看数据前的独立确认性实验**。

[真实首次 Actions38928749514](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38928749514)：16个虚构隐私、损坏格式、分组联合计数反例测试 PASS，原作者 38,647 byte XLSX SHA固定真实计算 SUCCESS。八个不带原编码的 `(组请求数, 第二列数字1数量)` 按数目排序为 **(19,9), (19,10), (19,11), (19,12), (25,11), (28,14), (30,6), (30,16)**，**逐对完全等于**出版社 Table1八组 `(requests, any responses)` 多集，总请求189、代码1总数89。与只检验总计数的弱条件不同，合成对照证明即使总人数和总回复保持189/89，也可能存在组间分布不符的失败配置。将0/1取反产生100而非出版者89，也不匹配。

[独立真实结果归档 run38928909389](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38928909389) 二次计算并验证1,816字节匿名JSON SHA256 `3cd8a9baa0b881942e8c394ae7d547f419a6ea2348dab1b5bb3aa5c543b1f09a` 后永久存入 [REV007 真实来源匿名机读联合一致性结果](R072_E2_PLOS_S8_ANONYMOUS_TABLE1_PAIR_CHECKSUM_REV007.json)。[完整科研审计与循环论证风险](R072_E2_REV007_REAL_TABLE1_ANONYMOUS_GROUP_CHECKSUM_AND_SCIENTIFIC_BOUNDARY.md)；[新增机读科学状态](R072_POSTCLOSURE_S8_REV007_GROUP_RESPONSE_PARITY_STATUS.json)。

**最重要的证据边界：** 这**仅是八个匿名组的描述性数据与作者 Table1已发表结果精确吻合**；不等于原始编码字典已恢复，更不能用已发表的每组回复人数倒推出哪些原数值是 serving/neutral，然后再“检验”服务历史引起的效果，那样存在严重的 outcome→treatment 循环论证。作者处理分配96/93与 `yes/maybe/no` 原始编码仍未由**独立于结果**的材料绑定，原R072 IMAGE/STANDING/STERN 真人模型依然未受验证。R072`CLOSED_BOUNDED`、E3 OPEN、PESEN v0.1 FROZEN不变。
