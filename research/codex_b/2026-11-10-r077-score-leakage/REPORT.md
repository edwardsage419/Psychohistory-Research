# R077 合成评分验收：当前标签污染与错误 log loss 变异

2026-11-10。基线 main `e5f2baa7f6b13b1a2bf95f48ed49571f732e7611`，
独立分支 `codex-b/r077-score-leakage-20261110`。
原评分源码 Git blob `70889bd15c6fd943bdb07ab3ae1f60c943ebc538`；
冻结 R073 本体 blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a` 不变。

状态：两个实际源文件变异可绕过既有合成守卫，新增数值验收候选已执行。
**原评分器与新独立 oracle 一致；未发现原程序实际泄漏或历史真人结果错误。**

## 可执行反例

在临时副本中仅替换 R077 原 `score_with_frozen_source` 的一行：

```python
# original
pred=predict(model,row,fit)
# deliberately invalid mutation, synthetic sandbox ONLY
pred=(predict(model,row,fit)+row[4])/2
```

当前标签进入概率，但 R077 原24项测试仍全部 PASS（普通/-O 均如此）。
原测试验证传入 fit 对象不变、结果声明目标训练标签数为0，以及若干源码
字符串不存在；这些检查不能排除局部评分路径直接使用当前标签。此变异
不执行任何概率训练，所以“training count=0”本身甚至仍可成立，却不能
作为无目标信息污染的充分证据。

对于任意原预测 p 和二元标签 y，变异 p'=(p+y)/2 给出
`(p'-y)^2=(p-y)^2/4`。实际使用旧测试自身的完全虚构 `fake_fit/cases`，
M0 宏 Brier **17/75≈0.2266667** 降为 **17/300≈0.0566667**；
log loss 从 **0.64598066** 降为 **0.26765402**，声明目标训练数仍为0。
这是错误分数的最小反例，不是真人结果改进。

第二个实际变异把 `total_l+=logloss(row[-1],pred)` 改成
`total_l+=brier(row[-1],pred)`。旧24测试亦全部 PASS；旧虚构样例 M0
“log loss”错误变为0.2266667。检测控制将全局宏 Brier 改为按行数加权，
旧测试正确以断言失败拒绝。三类实际源文件变异均被新 gate 数值拒绝。
完整变异行、SHA256、命令、退出码及原始stdout/stderr见 `evidence/`。

## 独立数值验收与防护范围

`score_oracle.py` 不导入 R073/R077 的 predict、状态编码、损失或评分实现。
来源充分统计量计算概率时只索引四个过去动作；当前标签仅进入损失。
目标按32个五位事件格聚合，Brier 用 `Fraction` 精确求和，log loss 用
**70位 Decimal 自然对数**，然后先逐场平均、再跨场等权。
这与原逐行 float/math.log 路线不同；新算法为内部验证构造，不冒充原作者
算法，也不代表外部团队复现。

合成来源在16个历史状态各有4行，分别以 p0=1/4 和1/2 构造一致的非空
状态表；不是改变冻结超参数或从真人目标选参。目标包括四个大小为
32/3/5/2 的虚构场次、两处理、全部32事件及翻转标签的版本。
手算锚包括9/52、7/36、5/24的条件概率，p0=1/4下四场宏Brier=**1/3**，
以及合作比例13/24对应的独立对数均值。

新 gate 比较完整公开输出树：7模型的总体/两处理 Brier、log loss，6对
差值、全局/分处理胜平负数、分母、声明字段及精确类型。每次**150个叶
字段**；数值浮点比较绝对容差 **2e-12**，整数/bool/键集合严格相等。
缺失/多余字段、NaN/Inf、数字字符串、bool冒充0、非法来源统计与空输入
均被拒绝。旧输出键名 `scored_t3_human_events` 在此仅沿用原接口；本包
全部事件为人工生成，**没有真人模型评分**。

12项新增测试包括全部历史状态/两标签/两来源表的完整调用，以及
`p=(Brier(y=0)-Brier(y=1)+1)/2` 的标签对恒等式，可从数值检查固定
预测是否符合来源概率。原冻结 alpha=20、TFT/WSLS噪声1/20不变。

边界：这是固定合成语料上的评分回归/独立算术检查，不是对任意未来程序
均无泄漏的形式化证明。来源统计量真实性、伙伴/时间窗口提取、参与者
身份及现实场次独立性不由此检查。生产/CI尚未采用本独立 gate。
精确有理数的配对平局只在本合成语料上与原浮点结果验证一致；不推断任意
未知近零差值数据的符号稳定性。

## 实际执行记录

仓库根目录实际执行：

```bash
python -B -m unittest discover -s research/codex_b/2026-11-10-r077-score-leakage -p 'test_score_oracle.py' -v
python -B research/codex_b/2026-11-10-r077-score-leakage/replay.py --output research/codex_b/2026-11-10-r077-score-leakage/evidence/normal
python -O -B research/codex_b/2026-11-10-r077-score-leakage/replay.py --output research/codex_b/2026-11-10-r077-score-leakage/evidence/optimized
```

重放必须指定全新的输出目录（如 `/tmp/r077-review-new`）；复用路径在写入
之前拒绝，避免旧成功收据残留。各 `commands.json` 记录实际展开argv/cwd/
退出码；被清理的临时变异目录可由 replay 再生。输出末尾 summary 仅在全部
必需检查通过后写入。38个源码/协议/原档案指纹前后一致，历史文件还用
独立 Git blob 计算匹配 HEAD；同版本的 SHA256/字节数逐文件归档。

| 验证 | 普通 Python | Python -O |
|---|---:|---:|
| R073 原合成测试 | 23 PASS | 23 PASS |
| R077 原合成测试 | 24 PASS | 24 PASS |
| 新评分验收测试 | 12 PASS | 12 PASS |
| 当前标签污染的旧守卫 | 24仍PASS | 24仍PASS |
| Brier冒充log loss的旧守卫 | 24仍PASS | 24仍PASS |
| 按行数加权控制的旧守卫 | 断言失败 | 断言失败 |
| 新 gate 的三类实际变异 | 3/3拒绝，exit42 | 3/3拒绝，exit42 |

正向 **59个不同测试方法**，两模式 **118次正向执行，零失败/错误**。
独立数值契约每模式68次人工评分函数调用、**10,200个输出叶字段比较**，
这些内部字段比较不称为单元测试。变异套件另计，不混入正向通过数。
`red.log` 保留初始12方法在no-op骨架下9个断言失败/2个KeyError（含subtests）
的真实记录；`green-attempt.log` 为实现后12方法全部通过。

## 分轨、版本和科学边界

已刷新 main、13个开放PR、近期 R 交接及既有 R077 匿名宏/sign审计。
PR #13处理 R074/R075训练场次重复/遗漏，本包独立从main分支，不依赖或
重做其代码；既有R077归档sign数学复核与本人工评分测试不同。R272和
R333–R340生产验收继续留给已有轨道。未提交并行聊天活动不可观测。
待核队列154项（P0=27/P1=82/P2=45），正式净关闭0。

证据：**人工合成、非盲态程序变异验证 + 内部独立精确/高精度复算**。
独立真实数据预测、新真人E2/E3、外部团队复现均0。真人数据下载/评分、
原始身份/时间/伙伴关系重审、历史科学结论重新验收、全仓库测试和
Actions均 **NOT_RUN**。无计费API、购买资源、依赖安装或workflow dispatch；
账户账单/免费CI额度 **NOT_VERIFIED**。R073/PESEN v0.1冻结，Rev001历史
失败和Rev002语义修订保留，原程序、协议、真实宏结果完全不改。

审查记录在 `PROGRESS.md`；将发布仅含本目录增量的独立 draft PR，
提交和标题使用 `[skip ci]`，不自动合并。PR最终状态与URL见交付消息。
