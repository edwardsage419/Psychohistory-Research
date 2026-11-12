# Fresh-context只读复核（2026-11-12）

复核提交f04469d40407b383d4a19bbfc0d8d7400ae12e2a，对照main d4740c2c。
独立审查者未发现可执行正确性问题；只读审查，不是外部科研团队复现。

实际命令：

```sh
python3 -B research/codex_b/2026-11-12-r277-s73-native-replay/replay.py --output /tmp/r277-review-f04469d-native-20261112
```

exit0：15命令、30流、12来源、2逐字节相同产物、8坏文件拒绝；前7命令exit0，后8 exit1。
Python3.12.14、Node24.22.1。另inline Python核验exit0：归档及fresh两包各30成员，
全部长度/SHA256/Git blob匹配，2再生输出匹配冻结字节，8坏输入哈希可重建，领域错误
及stdout空匹配，3完整B摘要匹配。12来源及两份协议与base/head/冻结版本一致。
`git diff --check` exit0，审查前后工作区干净，仅6新增文件。

确认边界：CSV负例只覆盖append/delete行数；不声称通用schema安全。原R复制字段控制
不计有效新拒绝。保留协议Python与归档Node差异，不升级E1或正式验收。
没有执行无关数学、真人评分、网络、push、PR、CI或修改原始/A文件。
