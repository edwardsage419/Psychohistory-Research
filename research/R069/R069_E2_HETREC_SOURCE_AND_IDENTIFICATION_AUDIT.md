# R069 E2 正式来源及可识别性审计：Last.fm 好友网络与带时间戳的音乐标签行为

日期：2026-10-16。科学证据地位：**E2 真实来源完整性、有限时间先行行为代理 PASS_BOUNDED**。三类扩散模型的**真实因果识别仍为 BLOCKED_BY_MEASUREMENT**，不对 R069 的完整 E2 模型拟合或 E3 外部验证作成功宣称。R069 主线状态继续 ACTIVE。

## 1. 第三方原始源，不是模拟数据

真实上游 [GroupLens / Universidad Autónoma de Madrid 的 HetRec 2011](https://grouplens.org/datasets/hetrec-2011/) 归档 `hetrec2011-lastfm-2k.zip`，原文 `README.txt` 授权**非商业使用**，不得再次发布个体数据表。本研究仅保留匿名元数据、计数、源哈希与纯标准库 Python 验证程序：

- 原始 ZIP `MD5=296d61afe4e8632b173fc2dd3be20ce2`，与公开 DataRec 外部 checksum 同一；
- 原始 ZIP `SHA256=6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c`，随后所有计算均要求精确这一哈希；
- `user_friends.dat`：**25,434** 条有向列示，完全互反，**12,717** 对唯一双向好友关系，涵盖 **1,892** 位匿名用户；
- `user_taggedartists-timestamps.dat`：**186,479** 条原始带时间戳标签事件；唯一标签用户 1,892、艺人 ID 12,523、标签代码 9,748。它不包含好友关系的建交时间及真正第一次听歌/采纳时间。

每一步均在 GitHub Actions 临时工作空间直接下载同一非商业原件、验证来源后只存匿名整库计数，不上传原始用户标识、艺人标识、好友边或时间线。

## 2. 两次真实反例和前置纠正

**首轮失败是必要保留的正式证据。**

1. [初始严格协议](../../protocols/R069_E2_HETREC_LASTFM_SOURCE_AND_EXPOSURE_2026-10-16.md)在首次数据处理前明确要求所有 ID/时间戳为正整数；[CI run 38874370089](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874370089) 真实源阶段 FAIL（`SOURCE_NONPOSITIVE_IDENTIFIERS_OR_TIMESTAMP`），12 个合成安全测试 PASS。不能因后来成功便把历史失败回写为 PASS。
2. [匿名来源诊断 run 38874509818](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874509818) 真正重新下载原 ZIP，原始 MD5/SHA256 固定，得到：好友表两字段均无非正数；186,479 条标签中 `userID/artistID/tagID` 均为正，仅 `timestamp` 有 **4 条负值**（没有零值/非整数）。
3. [独立 Rev-002 协议](../../protocols/R069_E2_HETREC_TIMESTAMP_SENTINEL_REV2_2026-10-16.md)在修订计算前提交，规定**只**从时间顺序算法排除原始 4 条负 timestamp 行，原 ZIP 不删改，186,475 条仍有正时间戳。[CI run 38874783610](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874783610) 两作业 `success`，7 tests PASS；源 SHA、25,434 好友表、186,479 原标签表及原始 4 条时间异常全部完整记账。
4. Rev-002 发现正数毫秒时间的 UTC 最早竟然是 **1979-04-30**，明显早于 [Last.fm 创始人描述的 2002 年平台起点](https://blog.last.fm/2009/06/10/message-from-the-lastfm-founders-felix-rj-and-martin)。根据[额外独立冻结的历史可行性协议](../../protocols/R069_E2_HETREC_PRE2002_DATE_SENSITIVITY_2026-10-16.md)开展保守 2002-01-01 界限敏感性分析。这一轮初次 CI [38875102015](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38875102015) 因研究程序 CLI 变量拼写问题 FAIL（安全测试 6 项 PASS）；代码在 commit `c2764b16ce969bfee869f7c314a6c93fab46d5fc` 明确修复，**不删除失败历史**；[第二次 CI 38875206526](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38875206526) 成功、6 tests PASS，发现仅 **1 条正整数时间事件**落在 2002 年前。此数据已向来历与准确性风险标注，不把负日期或 1979 日期伪装成网站真实事件。

## 3. 真实行为事实与有限代理结果

Rev-002 对严格正整数时间事件、同一用户—艺人组合只保留**首次观察到的标签时间**，**不是首次听歌**。针对每个首次标签，仅检验在已公开、但没有形成时间的好友图中，是否有现为好友者在**更早严格小于**时间戳，对同一艺人已有首次标签；同毫秒平局先评估后更新，不依赖 CSV 行顺序。研究记录：

| 量 | Rev-002 全正整数 | 排除 2002 年前异常的敏感性 |
|---|---:|---:|
| 可按正时间排序的原始标签行 | 186,475 | 186,474 |
| 用户—艺人首次观察标签组合 | 71,063 | 71,062 |
| 有静态好友严格更早标记同一艺人 | **11,602** | **11,602** |

全部 71,063 首次用户—艺人标签组合都来自至少具有一个目前静态好友的用户；其余 59,461 组无更早好友标记。至少一个好友更早标签的比率约为 **16.33%**，它只是**描述性静态好友—时间先行匹配率**。它不能估计比起没有好友时额外新增的标签概率；没有历史网络快照、无未观察到的首次听歌与所有未被标签艺术家的完整风险集，且共同兴趣同质性严重。敏感性只消除了一个明显不可能的过早正数时间事件，代理阳性总数未变；不意味着剩余 186,474 时间值全部经过外部真实性证实。

详细匿名 JSON [R069_E2_HETREC_REAL_SOURCE_AND_TIME_PROXY_RESULTS.json](R069_E2_HETREC_REAL_SOURCE_AND_TIME_PROXY_RESULTS.json)，代码 `r069_hetrec_lastfm_source_audit.py`、`r069_hetrec_nonpositive_diagnostic.py`、`r069_hetrec_source_rev002.py`、`r069_hetrec_pre2002_sensitivity.py` 与各自测试、原始 GitHub CI 全存档。

## 4. 是否有资格拟合 Watts、IC 或 Bass？

**结论：还没有。** 此数据的时间标签是网站上用户—艺人—文字标签事件，既不代表初次接触该艺人，也没有记载某条好友边在 t 以前是否存在，更没有对每个采纳机会观察成功/失败暴露。标准 IC 的一次尝试边传播概率、Watts 的采纳邻居比例与阈值、Bass 的新用户采纳时间都不能通过以上先行好友标签代理进行因果辨识。

后续若要继续做**纯预测**，可以另行冻结时间留出、与不含网络的时序流行度基线/标签个人偏好竞争的方案，使用**不可逆来源 SHA**，并将“当前静态社交图”作为严重可能发生时间泄漏的先验假设；不得从 11,602 的聚合事件计数直接计算阈值或 IC 感染率。更高等级 E2 真正传播检验必须寻找随时间可确认的好友边、初始种子和第一次有机会接触、第一次采纳的事件定义。

## 5. 当前验收状态

`R069_E1_THREE_DIFFUSION_MATH=PASS`（此前 22 项测试）；
`R069_HETREC_ORIGINAL_ZIP_INTEGRITY=PASS`；
`R069_HETREC_4_NEGATIVE_SOURCE_TIMES=RECORDED_AND_REV002_FILTERED`；
`R069_HETREC_1_PRE2002_ANOMALOUS_POSITIVE_TIME=RECORDED_SENSITIVITY`；
`R069_NONCAUSAL_FRIEND_PRECEDENT_PROXY=PASS_BOUNDED`；
`R069_REAL_THRESHOLD_AND_IC_IDENTIFICATION=BLOCKED_BY_MEASUREMENT`；
`R069_E3_NEW_COHORT=OPEN`；
`R069=ACTIVE`；
`PESEN_v0.1=FROZEN`。
