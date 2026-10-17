# R097 限定来源研究报告：2017长期真人重复博弈的OSF原始文件目录不可访问

日期：2026-10-17。**`R097=SOURCE_ACCESS_BLOCKED_BOUNDED`、仅E0来源可用性阴性证据，绝非科学模型预测正/负复验。** 本研究不是完整科研模型验收，没有取得原人类实验的微观观测，也没有进行任何外部E2/E3。PESEN v0.1 FROZEN。

## 1. 筛选新的、真正不同实验团队的长期真人研究

**Andrew Mao、Lili Dworkin、Siddharth Suri、Duncan J. Watts**，2017 [*Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma*](https://doi.org/10.1038/ncomms13800)，*Nature Communications* 8:13800。原论文报告94名真人参与者，在20个工作日重复合作实验，每日20次十轮双人囚徒困境（即同一人至多400局、4000次原始轮次）。原作者明确提供[OSF研究数据](https://osf.io/64z8u/)与[TurkServer实验软件代码](https://github.com/TurkServer/long-run-cooperation)。

这个研究团队与R096 Montero-Porras等不同，而且时间尺度更长，是合适的独立队列候选；但是**实验参与者跨日重复出现**，不能把20日当20个新招募的独立实验参与者样本，更不能把400局作为400个互不相关的人群实验。每10轮固定伙伴、每局之间配对变化；玩家历史很可能同时跨同局和跨局，需要先以原行动字段严格厘清，否则留出单位不可靠。论文摘要和曲线只提供已发表结果，不能代替逐人逐轮真实行动。

## 2. A01源资格在访问数据前冻结

[前置单独提交的R097 Phase A协议](../../protocols/R097_MAO_DWORKIN_SURI_WATTS_2017_LONG_RUN_20_DAYS_ORIGINAL_OSF_SOURCE_ACCESS_GATE_2026-10-17.md)确立：只允许访问原作者指定OSF项目ID`64z8u`的公有元数据接口、原始文件目录；不下载或查看任何演员行动、日期/同组/相对伙伴身份证明、录像与个人属性；原行为若不可用即严格fail-closed。此阶段不冻结不可核实的实验模型目标，不为原作者假设虚构来源代码本。原作者公开软件[TurkServer/long-run-cooperation](https://github.com/TurkServer/long-run-cooperation)存有实验程序（Git树对象 `4d8ed83e7745e1ffe82ce9403064e3558fabfa6f`），**没有本项目核实可重放的原始人类记录**。

实际[GitHub Actions run 39024639047](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39024639047)：严格OSF主机/固定项目ID/文件扩展名匿名化/不能导出个人文件名/不能读人物轮行数等**23项纯synthetic全部PASS**。随后由GitHub Actions真实访问：
- `https://api.osf.io/v2/nodes/64z8u/` → **HTTP 503**
- `https://api.osf.io/v2/nodes/64z8u/files/osfstorage/?page%5Bsize%5D=100` → **HTTP 503**

GitHub真实来源job`failure`是预期的**资格拒绝**，不是效应阴性或程序合成失败。官网网页读取也出现过503；不能据此推论OSF永久不开放，不应猜测文件名、虚构认证源SHA/MD5或下载第三方未认证“替代”微观行为。

[完整机器可读不可访问收据](R097_MAO_2017_94_HUMANS_20DAY_OSF_ORIGINAL_SOURCE_ACCESS_E0_RECEIPT_2026-10-17.json)保留两次HTTP503，原source程序[r097_mao_2017_long_run_osf_original_20day_metadata_access_gate.py](r097_mao_2017_long_run_osf_original_20day_metadata_access_gate.py)，23项source安全[synthetic测试](test_r097_mao_2017_long_run_osf_original_20day_metadata_access_gate.py)，可完全独立检查本阶段E0“为何不能进入行为评分”。

## 3. 科学证据边界

| 门槛/评价 | 实证状态 |
|---|---|
| 论文与独立实验作者真实来源 | PASS（可引用论文） |
| 原实验软件Git仓库存在及源码树 | PASS（但未等同原始行为证据） |
| 原2017 OSF项目、文件目录真实访问 | **BLOCKED：两接口503** |
| 原人类行动源文件作者SHA、精确来源行/人/日/局/轮 | **NOT ESTABLISHED** |
| 原真人逐轮双侧行动、伙伴身份资格 | **NOT ESTABLISHED** |
| 严格完整留出真实实验/参与者单位 | **NOT ESTABLISHED** |
| M0/M1/M2冻结目标真实评分、阴阳结果 | **NOT PERFORMED（0条）** |
| 新实验人群E3、文化/历史长期因果 | **NOT ESTABLISHED** |

不能因2017论文发表了“有韧性的合作类型”等结论而在本项目自称复现实证；更不能因为源暂不可访问就报告某模型不如另一模型。此阶段科研价值仅在**排除不合格来源、防止跨日重复人物被当作独立场次，以及形成可重放的原始数据来源失败证据**。

## 4. 与已完成的E2结果不发生冲突

R095作者原数据真正8个不同实验室场次、96真人的t2二元行为M1对M0 **8/8独立场次负面**，R096不同作者FP/SP 12场次、188真人、100轮的M1对M0在FP **6/6正**、SP **3/6正3/6负**，SP初期为负而晚期转为正；这些证据均不会被R097未读到的数据改变。R097阶段不对这两项作形式上显著性检验，也不增添来源不明的正负“复验结论”。

## 5. 阶段验收与下一步

R097此候选源的**来源可行性研究已限定归档完成（E0）**，但**不**等同新一项成功真人行为模型结题。本阶段不是A01–A06六项完整科学验收PASS：只有搜索/来源先冻结、23synthetic核查与真实HTTP503负收据可验收；原来源、实际真人评分、两次真实源独立复算、E2独立实验推广均**未完成**。

**下一阶段R098优先重新筛选可读取真实原作者来源的另一实验团队长重复二元或群体合作行为**；至少真实场次ID、唯一参与者、逐轮行为、对象匹配/对手标识及完整来源MD5/SHA五关全部通过，才冻结M0/M1/M2与早/晚分段并进行实证；被试跨场次重现则必须分开说明“实验日留出”与“参与者留出”。禁止生成未经数据实际运行的数字或自称科研正式结题。

**`R097_SOURCE_CANDIDATE=CLOSED_E0_BLOCKED`; `R097_HUMAN_E2_NEW_RESULTS=NONE`; `PESEN_v0.1=FROZEN`。**
