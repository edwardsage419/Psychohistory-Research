# E013 R174 聚合观测与独立第一期事件审计

日期：2026-10-26，Asia/Singapore。轨道：E 只读科研治理。前置 main HEAD：7b2cb547f1e0a30ae802e0d0b0634c341a7f2b02。状态：COMPLETE_BOUNDED_RECEIPT_AUDIT。已核对 E004 至 E012 与当日 R174、TH047、A 数据侦察增量。本轮仅在 operations 新增问题登记，不修改 R、B、A、TH、market、F 或任何冻结协议。无主动新增费用，无 CI 启动。

## 1. 最新研究轨和冻结顺序

GitHub main 读到 HEAD 7b2cb547f1e0a30ae802e0d0b0634c341a7f2b02，最近 R174 第三方法冻结提交 f8e0d58b3124e2232e8df704ececde6cb3c3aa38，主程序提交 39e839189bdedd40766143d0028adda22f14ab04，B 独立事件程序提交 68952e882befd5e423c310254af7e403bcae5521，B 报告提交 cc14e17f9e0d294f9843b9e7e120995e37a6afe4。GitHub compare 确认冻结提交到主程序提交 ahead=1, behind=0。原 R174 于 2026-10-21 已有结果，故此次冻结属于原评分之后的追加研究，不能写成原始研究的全局盲法预注册。

固定原始结果 research/R174/R174_EXACT_RESULTS.json 当前 Git blob 为 084a6783cdf495e5fb06390a481e38c1efe396b6，与第三方法收据和 B 收据的 source_git_blob_sha1 一致。追加冻结协议 Git blob 为 21db327e8316fcf9c515009a135a8aea5d276be8。

## 2. 实际执行的独立收据结构和精确有理数检查

读取第三方法机器收据及 B 独立事件枚举收据。本轮以独立 JavaScript 对收据字段执行 364 项结构与聚合断言，检查每期三观察层的8组计数、等价类数、唯一世界数、累计计数及界限，0失败。另对24组 I 与 D 配对、4个时点，采用 BigInt 交叉相乘比较精确有理数，执行 192 项单调性检查，0失败。总计556项有界检查通过。

第三方法收据给出 t1 三观察层均为 63 个等价类、54 个唯一世界，t2 至 t4 均为 69 个等价类、66 个唯一世界。96个配对时点中，O2 相对 O1 的 TV 严格提高53次，O3 相对 O2 严格提高46次，O3 相对 O1 严格提高60次，三层完全相同36次。本轮独立重算这些计数并确认各层 TV 满足 O1≤O2≤O3。

path 图 seed1，强度1/4，t1 的 I/D TV 分别为 O1=9/64、O2=15/64、O3=1/4；star 图中心 seed0 的全部三档强度、四个时点和三观察层均为0。该结果只支持指定有限候选网格中的分布辨识与观测损失比较。等价类数相同不能解释为增加观测信息毫无价值。

B 轨收据报告72个世界、72×16=1152个第一期全状态精确比较、72×5=360个第一期采纳人数精确比较、错误0；负对照变异在 path seed1 的纯创新强度1/4产生 TV=1/4。此为 B 原有程序的机器收据，本轮核查其计数与字段一致性，未重新执行 B 独立硬币枚举，也未重算原始72×5个马尔可夫概率向量。t2 至 t4 尚缺第三条完全独立的逐时概率构造路径。

## 3. CI、来源及证据等级

直接查询 GitHub Actions runs?head_sha=39e839189bdedd40766143d0028adda22f14ab04 与 head_sha=68952e882befd5e423c310254af7e403bcae5521，均返回 total_count=0。仅能认定这两项指定 SHA 未查询到对应运行，不可声称远端 CI 成功或整个仓库没有其他运行。没有启动 Actions。

R174 原始72个人工世界及追加观察计算均为内部 E1。没有新增真人 E2、历史 E3、独立外部团队复现。独立实现路径与事前盲法独立复验需要分别标记。

A 轨新增 HATCH 2026 来源资格门，官方论文声称 5990 条国家技术序列、130种技术、228个国家；官方 CSV 原始字节、精确许可证及逐节点接触网络尚未核验，不能据此判定 R174 获得 E3，也不能用作 R073 的真人重复博弈数据。TH047 是理论审计提交，不计为新的 R 系列实证验收。

## 4. 未关闭问题登记

E013-01 HIGH OPEN：R174 t2 至 t4 第三独立逐时概率复核缺口，当前仅能声称第一期 B 算法路径独立。
E013-02 HIGH OPEN：有限网格中等价类数一致，同时 TV 与单次可区分性差异明显，报告必须分开写严格等价和有限样本区分力。
E013-03 MEDIUM OPEN：本轮追加协议冻结于原 R174 评分之后，不能标为原研究预评分盲法。
E013-04 MEDIUM OPEN：指定新增主程序与 B 程序提交无关联 Actions 运行，不得沿用原 R174 CI。
E013-05 HIGH OPEN：HATCH 原始数据字节、许可证、网络暴露及机制标签未闭合，历史验证暂缓。
E013-06 HIGH OPEN：沿用 E009 的 R170 全状态跨路线比较缺口、R136 冻结负对照事件及原始239模型索引154项待核，均未在本轮重算，不能标记关闭。
E013-07 MEDIUM OPEN：本轮只审计指定 R174 文件及近期提交，尚未全仓穷举文件重名、全部冻结协议与全部研究轨 CI。GitHub 免费额度与账户整体账单未独立核验。

本周 F002 已完成，无重复专题；新的衍生统计权限问题留待 F003。研究顺序继续完整 R 系列，再系统归纳，最后模型熔炼。

## 5. 可核对来源

1. https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R174_COARSENED_OBSERVATION_EQUIVALENCE_THIRD_METHOD_FREEZE_2026-10-26.md
2. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R174_COARSENED_OBSERVATION_THIRD_METHOD_EXACT_RECEIPT_2026-10-26.json
3. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R174_COARSENED_OBSERVATION_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R174_INDEPENDENT_EVENT_ENUMERATION_EXACT_RECEIPT_2026-10-26.json
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/HATCH_2026_NATIONAL_TECH_DIFFUSION_ZENODO_SOURCE_GATE_2026-10-26.md
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E012_R173_POSTSCORE_LOSO_INFLUENCE_AND_CI_SCOPE_READONLY_2026-10-26.md

下一次 E 优先检查 R175 新增冻结顺序、原始输入、机器收据和 CI 范围；若 R175 未出现，追踪 R170 与 R136 未关闭问题。只读审计优先，避免重复或覆盖。
