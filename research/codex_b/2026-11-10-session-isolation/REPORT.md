# R074/R075 场次训练测试盲点：重复与遗漏 donor

2026-11-10。状态：已复现的合成工程验证缺口，新增独立核验候选；正式科学验收不变。
基线 main `e5f2baa7f6b13b1a2bf95f48ed49571f732e7611`；独立分支
`codex-b/session-isolation-mutation-20261110`。全部变异在临时副本发生。

## 发现与最小反例

R074 原 `fabricate()` 的三个训练候选场次复制相同的六条事件；R075 原
`toy()` 的两个/三个场次也复制相同的六条事件。将原 `fit_other_sessions`
中的事件读取从 `sessions[s]` 改为 `sessions[other[0]]`（R075 为
`sessions[training[0]]`），会重复首个合格 donor，遗漏其它 donor。
由于测试输入完全相同，p0、状态计数、训练目标数乃至整个模型输出仍相同：
原 R074 **20/20**、R075 **24/24** 测试全部通过。实际源文件变异行和
SHA256、真实子进程命令及 stdout/stderr 见
`evidence/{final-normal,final-optimized}/`。

这是可复现的测试假阴性（错误实现得到 PASS），不是发现原实现已在历史
真人数据上重复了场次。原训练代码实际使用 `sessions[s]`，本次未发现其
存在这种错误，也未重算真人分数。

`evidence/counterexample.json` 提供完全虚构的六场数据。固定留出 A_0，
A_1 与 A_2 各四行；将 A_2 误换成 A_1 后，两边训练行数仍为 **8**，
但两原训练器实测 p0 从 **3/8** 变为 **1/4**，M1 在 own_last=0 的
概率从 **17/48≈0.354167** 变为 **5/24≈0.208333**。
所以仅检查训练规模和模型数不足以保护这一有实际预测影响的错误。
原测试还包含 heldout-flip、同处理隔离和标签不参与当轮预测等有效保护，
不能把本缺口扩大描述为完全没有防泄漏。

## 独立方法与最小工程补充

新增 `fit_oracle.py` 不导入原研究代码：把每个五位二元事件编码到32格
列联表，对完整处理组表减去留出场次表，然后边缘化到 M1–M4 的状态空间。
这与原程序“先选 donor 再逐模型遍历事件”的顺序和实现不同。p0 与
alpha=20 平滑概率用 Python `Fraction` 精确运算，TFT/WSLS 固定噪声仍为
1/20。此算法由 Codex B 为内部工程检查构造，不冒充原作者算法。

`test_fit_oracle.py` 用手算的 3/8、完整四张状态表及 17/48 检查 oracle，
再用两种互不相同的合成场次设计（场次行数相等/不等，两个处理标签反转）
检查两个原训练器每折的全部充分统计量，以及全部32事件的七模型概率，
浮点比较绝对容差 **1e-15**。同时拒绝缺字段、多字段、计数 bool/float、
NaN/Inf、非法二元值、篡改状态计数、空折集合和损坏预测输出；保持留出
与异处理标签翻转不影响训练。
本 oracle 只验证提供的合成输入上的训练/预测行为，不能检测真实数据中
统计上无法区分的重复身份，也不声称验证了源文件资格、伙伴历史映射或
跨场次现实参与者身份。新 gate 尚未接入生产/CI，原冻结文件全保留。

## 实际执行与数量

在仓库根目录执行：

```bash
python -B -m unittest discover -s research/codex_b/2026-11-10-session-isolation -p 'test_fit_oracle.py' -v
python -B research/codex_b/2026-11-10-session-isolation/replay.py --output /tmp/codex-b-session-normal-new
python -O -B research/codex_b/2026-11-10-session-isolation/replay.py --output /tmp/codex-b-session-optimized-new
```

本轮实际 replay 的输出路径为
`research/codex_b/2026-11-10-session-isolation/evidence/final-normal` 与
`evidence/final-optimized`，目录必须不存在。完整展开的可执行 argv/cwd/退出码在
各自 `commands.json`；临时变异目录已自动清理，可由 replay 重新生成。
全部 Python 源在前后计算 Git blob 和 SHA256；历史源码 blob 与 HEAD 树
独立核对一致。`context-manifest.json` 固定协议、结果档案、队列和近期交接。

| 验证 | 普通 Python | Python -O |
|---|---:|---:|
| R073 原合成测试 | 23 PASS | 23 PASS |
| R074 原合成测试 | 20 PASS | 20 PASS |
| R075 原合成测试 | 24 PASS | 24 PASS |
| R077 原合成测试 | 24 PASS | 24 PASS |
| 新独立核验测试 | 12 PASS | 12 PASS |
| 重复 donor 变异上的旧测试 | R074 20、R075 24 仍 PASS | 同左 |
| 故意 heldout 泄漏控制上的旧测试 | 两者均断言失败、非导入错误 | 同左 |
| 新 gate 对两个研究×两种变异 | 4/4 拒绝，exit=42/FIT_MISMATCH | 4/4 拒绝 |

最终原始正向91项 + 新12项 = **103 个不同测试方法**，两种模式共 **206 次
正向测试执行，零失败/错误**。变异套件单独计数，不能并入正向通过数。
单次完整合成核验覆盖 **24折、5376次概率比较**，这些内部比较不称为单测。
`red.log` 保留未实现 oracle 骨架下10个方法的初始结果：9个断言失败、
2个 KeyError（含 subtest）；`green.log` 保留实现后初版10方法全通过。
初版 `normal/optimized` 日志保留，最终验证以 `final-*` 为准。
独立上下文审查发现新 gate 空输入可返回零折成功；先以
`review-red.log` 复现单一失败，再修复为明确拒绝，`review-green.log`
12方法通过。另补损坏 predictor 回归，刻意移除概率比较后7个子反例全部
断言失败（`predictor-guard-mutation.*`），证明新拒绝守卫的测试敏感性。

## 首轮范围核对与科研边界

已读 R073、R074、R075、R077 冻结协议、源码、合成守卫、归档结果和
失败边界。R073 的 t-1/t-2 窗口与同处理五场排除、R074 的同 match 历史和
两场训练、R075 的 file+subject+interaction 及噪声反馈语义、R077 的
Rev001 失败与 Rev002 实际连续历史/零目标拟合均保留。
未把 teacher forcing 的合法过去观察误判为未来泄漏。没有确认新的真实
时间泄漏，因此选择了场次重复/遗漏的有效测试缺口。

近期 ChatGPT 轨已完成 R074/R075 匿名宏汇总复核及 R077 sign 参考复核，
本工作不重复其算术结论；R272 和 R333–R340 强制生产验收仍由已有轨道
处理。开放 PR #1–#12 覆盖其它工程目标，范围快照归档；无法观察未提交的
并行聊天活动，不把拉取式范围核对称为原子锁。
待核 CSV 仍154项（P0=27/P1=82/P2=45），正式净关闭 **0**。

证据类别：**程序验证 + 内部独立精确算法复算，全部合成/非盲态**。
独立真实数据预测=0；新真人 E2/E3=0；外部团队复现=0。
真人源下载、真人模型新评分、身份重返排查、原始数据重复/遗漏审计：
**NOT_RUN**。历史科学结论的重新验收：**NOT_RUN**。全仓库测试和
GitHub Actions：**NOT_RUN**。未调用收费API、购买资源、安装依赖、
触发工作流或自动合并；账户账单/剩余免费CI额度 **NOT_VERIFIED**。
R073 和 PESEN v0.1 继续冻结。

审查与 PR：已完成一次 fresh-context 工程审查及上述修复验证，详细结果记入
`PROGRESS.md`。无未处理阻断项；修复后依靠失败回归与完整 scoped replay
验收，没有追加第二次审查。
仅提交本 Codex B 专用目录的增量 draft PR，标题/提交含 `[skip ci]`。
PR URL 与最终 head 以交付消息为准；未合并候选不记作 main 已采用。
