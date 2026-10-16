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
