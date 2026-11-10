# R279 S75 原生命令行与归档字节复现

2026-11-10，Codex B。**已实际补齐 S75 报告所列的原生 Python/Node 复现证据；
本次未发现计算差异。** 历史科学验收文件保持原样，本报告不代替 ChatGPT 的正式验收。

## 为什么选择此工作包

R279 S75 的 R/B 报告、R 交接及 E109/E110 明确将归档 Python `--selftest` /
`--emit`、完整 CSV/JSON 字节再生、旧 B Node CLI 列为 NOT_RUN/OPEN。过去已有
V8 精确枚举、内部独立计数/方差核验及旧 B 持久化检查，本次不重新包装为新算法。
实际运行归档程序能减少一个明示的工程验收障碍，故选择此复现缺口。

优先复查过 R274 S70 时间隔离：v2 已修正历史自比较，并有配对 Y6 不变性及完整
来源公式门，未发现应重复实施的保护。读取 main 最近提交、20 个开放 PR 及范围；
A 的 R170 认证增量和队列工作与本包分开，未观察到 S75 原生复现 PR。
初始主线 `b3b3b9a1af020130e7c0e1a9cc0b58021be08e8e`；独立分支
`codex-b/r279-s75-native-replay-20261110`，只新增本目录。
范围快照及背景文件指纹见 `evidence/open-pr-scope.json`、`context-manifest.json`。
未宣称排除了不可见任务；待核154项仍P0=27/P1=82/P2=45，正式净关闭0。

## 归档程序原样执行

既有 Linux、Python **3.12.14**、Node **v24.22.1**、标准库，无安装依赖或网络调用。
`replay.py` 先读取并锁定10份原始输入/程序/协议的字节快照，核对固定 Git blobs
和当前提交；pins.json 的 SHA256 固定在程序中。程序、输入副本均在临时目录执行，
原研究目录不写入。复制只改变位置，执行代码字节不变，无数学生成逻辑重写。

实际命令入口（仓库根，输出目录必须全新）：

```bash
python -B research/codex_b/2026-11-10-r279-s75-native-replay/replay.py --output research/codex_b/2026-11-10-r279-s75-native-replay/evidence/normal
python -O -B research/codex_b/2026-11-10-r279-s75-native-replay/replay.py --output research/codex_b/2026-11-10-r279-s75-native-replay/evidence/optimized
```

两模式 exit0、`PASS_BOUNDED_NATIVE_CALIBRATION_REPLAY`。原 R279 `--test` 各
**84 个 unittest 方法**，共 **168 次正向执行**、0失败/错误。S75 `--selftest`
各一次，**不是额外 unittest 数量**；原 R279 `--emit`、S75 `--emit` 各一次。
旧 Python 的 `assert` 在 -O 下禁用，不能称这些内部断言仍有效。新入口的显式
版本/字节/跨文件/子进程检查和旧 Node B 门在两模式均实际运行。

所有子命令实际 argv、cwd、退出码、stdout/stderr 原始字节及 SHA256 见两模式
`commands.json` 和非空流文件。空流以0字节/哈希记录，不制造空日志文件。
一次占位入口的真实 RED 为 exit1/NOT_IMPLEMENTED，见 `pipeline-red.json`，其后
完整原生流水线 GREEN；这只是入口验收的 RED，不冒充历史科学回归失败。
首次探索误把 Node 参数反传，出现 JSON SyntaxError；随后按归档 CLI 的 CSV→JSON
顺序成功，未把调用错误当原程序缺陷；探索记录在 PROGRESS.md。

## 字节、分数字段与零质量来源

每模式五份完整输出逐字节相等：

| 原生输出 | 字节 | SHA256 |
| --- | ---: | --- |
| 原 R279 CSV | 18450 | c2c64e3a2bb4c5b1248663301ac50528e3762776ea3d4ef5ff2eeddf342edab0 |
| 原 R279 JSON | 5056 | 985764e4205d5673a0e2c7ca33f8e5589252ff6a5b5de39b617912773700da7f |
| 原机器收据 | 411 | 07642c79c2eef71788af72be2ccca432bb9413a306de989c8d244c4ac436ec7a |
| S75 CSV | 8420 | 359d23c7b2b88c3fc93ad6f1341134d91b445bafb7b9f431eb0254b1574c5349 |
| S75 JSON | 6638 | 784354f72050e850cc359e10d8e1d490d2731c9218d53f22631eb8225aa14466 |

机器收据与原 `--emit` stdout 对象一致，收据的两个 SHA256 重新计算一致。
原 R279 九世界人口 REL/RES/UNC/Brier 与 S75 的人口字段逐一对照，36/36 精确相等。
这是归档间的一致性链，不单凭相等推断数学正确。

数学/来源核验由**原作者归档的独立 B 门**承担：真实 Node CLI 对归档副本及本次
再生成副本各一次，共每模式2次，均返回 PASS/144行/9世界/99正质量来源。
它逐行核对概率、经验分解及 Brier，重算九世界人口值和加权摘要；算法信用归旧 B，
本包只提供原生执行和固定字节范围。99正质量+45零质量，零质量来源完整保留。

关键 Git blobs（10份完整 pins 及12份运行前后指纹在 pins.json / summary.json）：

- 原 R279 Python：`be073bc56afa68229fa643d0cb829cd6bc5b86fc`
- S75 Python：`d54ab6327ff0ba442a5611ae4a743451a353bffa`
- 旧 B JS：`03bceb6b6adf9728535df95840fe2d8994fc7198`
- S75 CSV：`4905c6df24a73d8a940b2442c44e91a83f4a0aab`
- S75 JSON：`6c47a52eb547901e7f9ed3d006eec35450735e24`

每模式9个实际坏输入均被旧 B CLI exit1、预期领域错误拒绝：等行数重复来源、
遗漏来源、逐行 REL=999、摘要 Brier=999、E2升为1、原 R279 标志 false、零质量
篡为1、删除全部45条零质量来源、E2的0改布尔false。前七类沿用历史V8审计范围，
并非新发现；后两项明确复核结构覆盖/类型边界。每次要求 stderr 出现对应领域错误，
拒绝将 SyntaxError/ReferenceError 或随机非零退出当作数学拒绝。
负控输入可由 `cases()` 确定性重建，哈希和错误流全部归档。

## 边界与交付

本包解决的是已记录的原生运行/字节再生证据缺失，不声称发现程序数值错误，也不
扩大旧 B 门的通用 JSON/schema 保证。入口只接受固定字节来源，不是任意外部收据
验证器；字节一致不能代替外部科学验证，元数据匹配不能恢复真实历史执行时序。
固定程序/快照中的边界已测，不承诺敌对并发写入、其他环境或生产系统的安全性。

证据分为：归档程序原样复算、旧内部独立 B 算法的原生重跑、故意篡改拒绝。
人工非盲态 E1，独立真实数据预测/新真人评分/E2/E3/外部团队复现均0。
R073/PESEN v0.1、冻结模型、参数、划分、指标、历史程序和结论均不改。
完整科学重新验收、其他平台/版本、全仓库测试、生产/CI接入均 NOT_RUN。
原 A raw-XLS 数据管道及许可问题不属于本包，没有执行或关闭。

没有付费 API、购买资源、依赖安装、workflow dispatch 或自动合并；实际账户账单
及免费 CI 额度 NOT_VERIFIED。发布前后 Actions 观察单列，空列表不算 CI PASS。
一次 fresh-context 工程审查、最终 main/PR 状态见 PROGRESS.md、HANDOFF.md。
