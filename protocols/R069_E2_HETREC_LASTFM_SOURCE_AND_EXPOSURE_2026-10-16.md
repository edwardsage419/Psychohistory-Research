# R069 E2：HetRec 2011 Last.fm 网络＋带时间戳标签行为的真实来源门

日期：2026-10-16。**首次取得 HetRec 原始 ZIP 并执行任何真实行为统计之前冻结**。继 R069 通过 Watts 阈值、独立级联、Bass 离散 E1 数学测试后，本关只做来源与可观测性审计，不拟合三个扩散模型、不宣布真实社交传染。此研究依《RESEARCH_ACCEPTANCE_STANDARD_V1》执行。

## 一手公开来源、复验身份及许可

GroupLens / UAM HetRec 2011 正式发布页 `https://grouplens.org/datasets/hetrec-2011/`，下载 `https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip`；公开数据集页描述 1892 名用户及约 92,800 条用户与艺人听歌记录；作者 README 定义 `user_friends.dat` 为 `userID,friendID` 的无向双向列示；`user_taggedartists-timestamps.dat` 为 `userID,artistID,tagID,timestamp`（Unix 毫秒），标签事件总计约 186,479。公开文献中为源 ZIP 标注 MD5 `296d61afe4e8632b173fc2dd3be20ce2`，其来源为 [DataRec 文档](https://www.datarechub.com/assets/pages/datasets/lastfm_2011/)，属**待执行的校验值**，不是已经验证真实字节。受限**非商业研究用途**；本研究不能将原始互动表、用户轨迹或 ID 发布至本仓库。

## 事先冻结的技术审计

使用 GitHub Actions 的临时 runner 直接下载 GroupLens 主站 ZIP；限制整个压缩包最多 15 MiB、每个展开成员 30 MiB，禁止路径穿越，限 20 个成员且压缩总解包不超过 60 MiB；验证精确 MD5 如不符立即 `FAIL_CLOSED_HASH`，不能通过其他镜像悄悄替换数据。只有 MD5 成功后，计算新 SHA256（精确源冻结供后续使用）。

必须找到 ZIP 中的官方 `readme.txt`、`user_friends.dat` 和 `user_taggedartists-timestamps.dat`，字段顺序如上，TSV 严格解析，任何来源字段行数与公开基线的差异均保留计数，不静默删行。检查：
1. 每个 `friend` 关系的人 ID 为正整数、无自环，分别计算原始有向列数、完全互反的无向对数、无对应反向关系的对数及用户覆盖。**不能**把缺少时间戳的好友网络伪装成事件发生前已存在的关系。
2. 每个标签事件包含正整数 `userID,artistID,tagID`，时间戳为正整数毫秒；计算真实记录数、唯一用户/艺人/标签数、最早/最晚事件日期（按 UTC、仅年月日）、重复完全相同行数、同一 user-artist 的重复次数以及同一 user-artist 首次观察标签事件数。
3. 计算有**用户好友关系且能在时间上配对观察的 tag 事件用户**数量。仅为了量测候选 E2 风险集，统计**全部有效 user-artist 首次标签行为**中，有多少在时间戳之前至少一位当前数据集中的好友给该艺人打过标签（`t_friend < t_user` 严格小于，平局不算先行）。把其称为 `retrospective_friend_precedent_proxy`，绝对不得称「确证的暴露」「采纳」「感染」「成功传播」。单个艺术家多个用户事件的时间相同可能人为发生；不输出任何 per-user 或 per-artist 计数。要求用按艺人排序时间＋基于仅先前时间的集合处理平局，不能依赖输入 CSV 行顺序。
4. 未被标签的用户对某艺人的真实风险集**不可观测**；音乐收听 `user_artists.dat` 也缺时间戳，单次打标签可能发生于多年听歌之后。当前好友网络关系建立时间未知。**不能**使用静态网络计算社会影响方向的因果参数，更不能把真实邻居数等于 adoption influence。
5. 仅存 zip SHA256、结构聚合、零/非零先行好友标签代理数量、来源版本/许可、匿名错误码；绝不输出真实用户 ID、艺术家 ID、标签文本、个体接触时序。

## 审计分支与授权范围

若原始 ZIP 无法下载、哈希不合、成员非法或 CSV 字段无法读取：状态 `SOURCE_UNRESOLVED` 或 `SOURCE_FAIL_CLOSED`，不得声称已开展真实 E2。若真实源和结构检查通过，最多 `E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS`；`E2_CAUSAL_INDEPENDENT_CASCADE_IDENTIFICATION=BLOCKED`、`E2_THRESHOLD_INFLUENCE_IDENTIFICATION=BLOCKED`，Bass 真实采纳时点也不可用。未来可仅在重新冻结匿名预测协议后讨论时间外推、时间分层及互为竞争基线；需要外部独立网络历史快照方可改变真正传播机制识别结论。

同时备选 Stanford SNAP Higgs 2012（`https://snap.stanford.edu/data/higgs-twitter.html`）具有配对匿名用户的关注网络与 retweet/mention/reply 时间，但这种**活动边不是独立级联成功机会或信息采纳**，且完整社交图超过千万条边；不为本次 HetRec 试验引入其超大原始文件。

`R069_E2_HETREC_PROTOCOL=FROZEN`
`R069_E2_TRUE_DIFFUSION_CAUSAL_MODEL_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
