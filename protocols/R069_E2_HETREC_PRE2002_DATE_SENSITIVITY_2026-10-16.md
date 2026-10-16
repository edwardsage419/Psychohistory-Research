# R069 E2 原始正数时间戳的历史可行性敏感性试验

日期 2026-10-16。本协议在第一次重算 pre-2002 过滤代理统计前提交，与首轮时间字段失败、Rev-002 源核验互相独立，不可回写已归档结果。

Rev-002 真实 [CI 38874783610](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874783610)：GroupLens 原始 ZIP MD5 `296d61afe4e8632b173fc2dd3be20ce2`，SHA256 `6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c`，186,479 原始标签记录中 4 条为负，正时间 186,475 条；最早合法*正整数*时间被换算为 UTC **1979-04-30**。Last.fm 创始人在其 [2009 年公开信](https://blog.last.fm/2009/06/10/message-from-the-lastfm-founders-felix-rj-and-martin)中描述网站始于 2002 年，因此 **1979 的 Last.fm 标签时间不可能被直接当作网站真实标签时间**；这可能是时间转换或异常输入，但原因尚未恢复。

在不改变 Rev-002 正数规则的前提下，计算两个完全独立的匿名统计：
1. 审计全部有效正整数毫秒时间是否落在 `t < 2002-01-01T00:00:00Z`（选择全年 2002 之前作为**保守明显不可能窗口**，不把它当作真实成立日期）。输出这类原始标签数、来自几个不同 user-artist 最早可用标签以及全样本用户—艺人首个有效事件是否含此异常。
2. 将所有 `timestamp < 2002-01-01T00:00:00Z` 的正整数异常行作为**敏感性**从时间先行代理算法另一次副本中过滤，再重新计算首次用户—艺人标签数量与至少一个静态好友先行打标签的数量。输出严格的`original_rev002`与`sensitivity_excluding_pre2002` 聚合指标对比；**严禁**替代 Rev-002 初始结果或声称达到新的机制验证。
3. 原 ZIP 源必须再次 SHA256/MD5 双验证；4 条负整数继续单列，且只有 186,475 条正时间事件作为 Rev-002 基准；不裁掉 2002 以后可能的其它误差，也不逆推真实用户曝光时点。切勿输出用户名、艺术家编号、具体个人 1979 事件、个体时间线、好友边或小组结果。
4. 只有时间范围异常计数完整、两套固定代理重算都成功才标记 `SENSITIVITY_DESCRIPTIVE_COMPLETE`；其他状态 fail-closed。真实网络建立时间及真正首次收听日期缺失，因此真实 Watts/IC 机制识别始终 `BLOCKED_MEASUREMENT`，本实验只解决观察窗口日期可信性问题。

`R069_PRE2002_TEMPORAL_SENSITIVITY=FROZEN`
`R069_HETREC_FRIEND_EARLIER_TAG_CAUSAL_STATUS=NOT_ESTABLISHED`
`PESEN_v0.1=FROZEN`
