# Fresh-context只读复核

2026-11-12；审查63c20ef3fe68112de8db37e2d1efb6935a7f7787，对照d4740c2c。
未发现可执行问题。此为内部独立代码复核，不是外部科研团队复现。

实际执行：

```sh
python3 -B research/codex_b/2026-11-12-r275-s71-native-guards/replay.py --output /tmp/r275-review-20261112-unique
```

exit0：36命令、72流、原门-O 6错误接受、候选12拒绝。另独立archive verification
exit0：归档/fresh全部流哈希、退出码、baseline哈希、来源/输入身份、再生产物及2 AST
变异拒绝均核对。`git status --short`干净。

确认候选保留原18个条件、公式、数据及其余AST，修复有真实优化模式拒绝价值。
没有证据证明历史默认模式数值错误；没有科学等级提升；未接入生产。
原冻结B在-O仍失败，须A另行接入。仅覆盖6负例类别，非全部18 guard独立负例。
未跨环境、科学重验、真人评分、CI、网络或修改原始来源。
