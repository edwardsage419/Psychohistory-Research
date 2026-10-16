# R069：网络集体行动的局部阈值、随机级联与宏观创新扩散

建立日期：2026-10-16。状态：**ACTIVE；E1 三机制数学基线 PASS；E2 真实网络与标签时间来源、先行关系代理 PASS_BOUNDED，但真实网络采纳与因果传播模型仍 BLOCKED_BY_MEASUREMENT；外部独立 E3 OPEN**。从 [R068 文化学习有限结题](../R068/R068_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)转向与短期选择明显不同的社会传播/技术制度采纳机制。

## 文献锚和冻结协议

[独立数学协议](../../protocols/R069_NETWORK_CASCADE_THREE_MECHANISMS_2026-10-16.md)已在首次测试结果出现前提交。四条经典文献线索：
- Granovetter (1978), *Threshold Models of Collective Behavior*, DOI [10.1086/226707](https://doi.org/10.1086/226707)；
- Watts (2002), *A simple model of global cascades on random networks*, DOI [10.1073/pnas.082090499](https://doi.org/10.1073/pnas.082090499)；
- Kempe, Kleinberg & Tardos (2003), *Maximizing the spread of influence through a social network*, DOI [10.1145/956750.956769](https://doi.org/10.1145/956750.956769)；
- Bass (1969), *A New Product Growth for Model Consumer Durables*, DOI [10.1287/mnsc.15.5.215](https://doi.org/10.1287/mnsc.15.5.215)。

本研究自己明确写出**六节点固定路径网络**，并不冒充复现 Watts 的随机大图临界相变、Kempe 的影响力优化理论证明或 Bass 的真实产品销量推断。

## 已真实完成的 E1

[纯 Python 三机制运行程序](r069_network_cascade_baselines.py) · [22 项数学边界测试](test_r069_network_cascade_baselines.py) · [机读结果](R069_E1_NETWORK_CASCADE_RESULTS.json)。[GitHub Actions run 38872162843](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38872162843) `completed/success`，22 tests OK。

固定 6 个节点的路径 `0−1−2−3−4−5`，初始仅节点 0 采纳：

| 机制 | 固定规则 | 结果 |
|---|---|---|
| Watts 同步局部阈值 | `φ=0.5`，邻居采纳比达到阈值即不可逆采纳 | 5 轮后 6/6 节点采纳 |
| 高阈值对照 | `φ=0.75` | 5 轮后仍只有 1/6 种子 |
| 独立级联 IC | 有向路径，每边单次 `β=0.5` 成功机会 | 精确穷举 32 种活边，最终采纳期望 **1.96875** 节点；每节点采纳概率 `[1,.5,.25,.125,.0625,.03125]` |
| Bass 宏观创新＋模仿 | `p=.03,q=.4,dt=1,x0=1/6` 离散 Euler | 第 1 步比例 `0.2472222`，第 5 步 `0.6807123` |

三种传播规则使用不同信息结构：局部阈值依赖邻居采纳比例，IC 依赖单次独立传播机会，Bass 是没有节点网络的总体采纳微分方程数值近似。因此不能仅按数字高低判定哪一个反映真实社会传播。

## 下一 E2 数据输入门

需要可合法复核的**节点间真实关系、起始种子、按时间的首次采纳/暴露、未观察或终止观察的风险集**。仅凭社交图和帖文转发不能直接说明感染、独立级联边传播或某个阈值导致采纳。应先冻结测量与匿名性/知识产权约束，然后校验至少两种机制在同一事件级时间数据上的可识别性与风险集，才可开展真人预测。

`R069_ACTIVE=YES`
`R069_E1=PASS`
`R069_E2_NETWORK_ADOPTION=OPEN`
`R069_E3=OPEN`
`PESEN_v0.1=FROZEN`


## 最新 E2：GroupLens HetRec 2011 真实社交网络、事件时间与测量拒绝（2026-10-16）

正式审计入口：[原始来源、异常处理和机制识别报告](R069_E2_HETREC_SOURCE_AND_IDENTIFICATION_AUDIT.md) · [不含人/艺人标识的机器可读结果](R069_E2_HETREC_REAL_SOURCE_AND_TIME_PROXY_RESULTS.json)。源为 GroupLens HetRec 2011 Last.fm 非商业研究数据，ZIP MD5 `296d61afe4e8632b173fc2dd3be20ce2`，SHA256 `6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c`。

真实原始文件经 GitHub Actions 下载校验：1892 匿名网络用户、12717 个双向好友关系，186479 条原始艺术家标签事件。严格原始验证发现 4 条**负时间戳**，按先行提交的修订协议仅从时间先后统计移除，保留首次 CI [38874370089 失败](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874370089)、[38874509818 诊断](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874509818) 和 [38874783610 修订通过](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874783610)。修订 7 项测试通过。正数时间仍有 1 条被解析为 1979 年，不可能是 2002 年以后出现的 Last.fm 标签；单独 [2002 年前敏感性协议](../../protocols/R069_E2_HETREC_PRE2002_DATE_SENSITIVITY_2026-10-16.md)与 [CI 38875206526](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38875206526) 成功，6 tests 通过（之前首次 CI 38875102015 因脚本命令行变量拼写失败并留存）。排除这一条异常后，独立代理计数稳定。

共 71063 组“用户—艺人**首次观察到标签**”，其中 11602 组存在现时好友对同艺人在严格更早时间的标签。排除 2002 年前明显异常事件，分母 71062、分子仍 11602。**这不是暴露、真正音乐采纳或社交影响的因果识别**。好友网络没有建交时间，用户首次听歌时间未被观察、可能在打标签前很久，未打标签用户—艺人完整风险集缺失。真实 Watts 阈值、IC 单次传播概率、Bass 真实首次采纳的 E2 识别保持 `BLOCKED_BY_MEASUREMENT`，不可从 11602 反推出传播参数。研究仍 ACTIVE，待寻找更加可信的时间变化边和真实传播/采纳事件；PESEN v0.1 仍 FROZEN。


## 最新真实 E2：SNAP Higgs 2012 活动时序及原始 RT 汇总逐边完整核验

本轮在一手 Stanford SNAP 2015-03-31 修订版数据上开展独立验证，源程序及前置协议见 [Higgs 完整 E2 审计](R069_E2_SNAP_HIGGS_TRUE_TEMPORAL_ACTIVITY_AND_PARITY_AUDIT.md) 与 [匿名结果 JSON](R069_E2_SNAP_HIGGS_ORIGINAL_SOURCE_AND_RT_PARITY_RESULTS.json)。[官方数据页](https://snap.stanford.edu/data/higgs-twitter.html)。两份原始 gzip 固定 SHA256，所有研究数据仅从官方 URL 在 Actions 临时 runner 下载，未发布匿名用户原始行为数据。

- [源读取 GitHub Actions 38876285461](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876285461)：18 项反例测试 PASS，真实活动 **563,069 条**：RT 354,930；MT 171,237；RE 36,902；2012-07-01 至 07-07 全部落在观察窗内。此事件为有方向的互动边，不等于论文的全部 985,590 条相关 tweet。
- 源文件 gzip SHA256 分别为 activity `901b199716a23b0fc0371705e3ae9941b5c9493277aec65456abc4988674ad79` 和 derived RT graph `4097edebd539043cfc62d9b4ba67676f79523f6dbe896d345fcc127dec3e936e`。
- [逐边交叉对照 GitHub Actions 38876563448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876563448)：13 项测试 PASS，**328,132 条唯一有向 RT 汇总边**严格等于全部 354,930 次原始 RT 活动逐对汇总，缺少的边=0、多出的边=0、权重差异=0。**这是同一观测来源两种表示的精确一致，不是两份独立可用作因果传播校准的人际网络**。
- 112,692 条真实 RT 事件的对象在严格更早时刻已有过 RT 活动，属于可信的**时间先行活动代理**，不是该消息/原帖的确切来源、有效暴露机会或外生因果传播。因此 IC 失败暴露风险集、Watts 真实决策阈值、事件发生时有效的社交好友关系均 `NOT_IDENTIFIED`；R069 E1 仅数学 PASS，E2 真实源及逐边一致性 PASS，**因果机制拟合仍 BLOCKED_BY_MEASUREMENT**。
- 上期 [HetRec Last.fm E2审计](R069_E2_HETREC_SOURCE_AND_IDENTIFICATION_AUDIT.md)及 4 条负时间戳/1 条明显不合理 1979 年正时间的失败历史不受本新独立源工作影响。两次 E2 数据源不可视为已证明机制，PESEN v0.1 保持冻结，R069 尚 `ACTIVE`。

**下一个关键门：** 真实源具有时间标记和关系方向，但 RT 汇总图来自**全观察期的目标行为本身**，不能作为训练时可见的传播图。若尝试做下一阶段留出预测，必须事前冻结严格时间切分、只由训练窗构造的暴露代理以及不需要外部社交边的新闻时间趋势基线，同时分离这种预测能力和真实 IC/阈值因果辨识。或者优先寻找包含历史合法有效关系与真正传播机会的独立数据。
