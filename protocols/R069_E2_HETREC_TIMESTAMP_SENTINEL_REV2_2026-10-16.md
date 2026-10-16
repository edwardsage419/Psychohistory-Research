# R069 E2 HetRec 原始负时间戳的版本化纠正协议 Rev-002

日期 2026-10-16。**本协议在修正版本第一次计算真实用户—艺人好友先行标签代理前冻结。** 保留初版研究协议 `R069_E2_HETREC_LASTFM_SOURCE_AND_EXPOSURE_2026-10-16.md` 和初版失败的 GitHub Actions [run 38874370089](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874370089)：原始有效时间字段假设被真实源反例推翻，不得事后改写原失败为成功。

独立诊断脚本 `r069_hetrec_nonpositive_diagnostic.py`，[run 38874509818](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38874509818) 完成真实下载和源字节核验，并给出纯匿名异常计数：

- 原始 GroupLens ZIP URL `https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip`；
- 真实原始 ZIP `MD5=296d61afe4e8632b173fc2dd3be20ce2` 与此前公开值一致；
- 真实 ZIP **SHA256** `6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c`；
- `user_friends.dat` 25,434 行，两列均无非正整数；
- `user_taggedartists-timestamps.dat` 186,479 行，其中 **仅 timestamp 有 4 条负整数**，userID/artistID/tagID 全部为正整数，无 timestamp=0，也没有非整数。这 4 条在计算先后顺序前明确记为 `INVALID_TEMPORAL_ORDERING_ROWS=4`，源行总数始终记为 186,479，**仅 186,475 行可用于时间顺序候选分析**。

## 修正规则

1. 重下 GroupLens 官方 ZIP，先核验原始 ZIP 的精确 MD5 和新公布 SHA256，校验 Zip 安全和 `readme.txt`、两 TSV 完整性。原始 archive 永不更改。
2. 网络好友表 25,434 行全部严格校验原始格式，单条边不删改，原始有向表中成对互反及无自环；任何异常 fail-closed。标签 TSV 全表 186,479 行，`userID,artistID,tagID` 均严格正整数且 `timestamp` 必须为合法整数；遇到 timestamp<0 仅计数、不投入时间模型。遇到 timestamp=0 或其它未授权非法字段则立即 fail-closed。**负时间戳数量必须恰好为 4，否则 SOURCE_DRIFT**。绝不尝试把负数转换为真实日期。
3. 净事件 186,475；使用同一 `proxy_early_friend_tag` 函数按艺人排序，对每个用户—艺人首次可用标签，统计是否存在静态好友在**严格更早**时间对同一艺人有首次标签。相同毫秒同时出现不算先行。原始 ZIP SHA 校验先于全部测量。输出总人数/总事件/代理阳性、网络互反性等匿名聚合，不输出源行或用户艺人 ID。
4. 这里研究的是**第一次观察到的艺人标签**，不等于第一次听歌、更不等于艺术家真实采纳；好友网络无建立时间，观察到某好友更早标签不等于该用户有机会看到该行为，也不能确定信息传播方向。以后若要预注册条件预测，必须重新标注时序、训练时间窗口、静态好友网络偷看未来的局限和好友随机对照；此 Rev-002 不授权真实阈值/IC 参数拟合。
5. 对 Rev-002 附至少 6 项合成控制：四条负时间戳只剔除用于时间统计、超过四条失败、零时间失败、改动源 SHA 失败、平时间标记不计为先行、好友关系互反。CI 通过只可表述 `E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS_BOUNDED`，初版失败状态仍独立存在。

`R069_E2_REV002_CORRECTION=FROZEN_BEFORE_RECOMPUTATION`
`R069_INVALID_ORIGINAL_TAG_TIMESTAMPS=4`
`R069_TRUE_SOCIAL_CONTAGION_CAUSAL_INFERENCE=NOT_ESTABLISHED`
`PESEN_v0.1=FROZEN`
