# E109 R279 S75 与 Andreozzi 六会话有限推断治理审计

日期：2026-10-30 UTC。目标键：(operations,R279S75+Andreozzi2020,S75-freeze-fb5fbd79+author979abf87,six-session-inference-and-native-gates)。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。无修改 R、A、B、理论轨的历史文件、冻结协议或共享索引。

## 同步事实

基线 main HEAD d58803e66e6309ae14180c3e049e060061bffb7a。读取最近提交、12个开放 Codex PR 标题摘要、PR #1/#3 的实时 open 状态、R279 S75 R/B/A 报告、R轨交接、E108、统一验收标准 v1.0 及市场轨上轮记录。Codex PR #1 的 R257 S53 六类旧比较器假阳性仍为待审查证据，PR #3 严格检查器未合并。PR #2 同步协议也未合并，本轮按任务提示执行。

R279 S75 冻结提交 fb5fbd79c2589842d4b4ae27d59fe95f087cade4 到 B 报告提交 cc1581ad4fbfaec18b5af056673d05ea4ef8e7fc 的 GitHub compare 为 ahead=8, behind=0，冻结在结果之前。R279 S75 的9世界、144来源行、99正质量行及7个错误注入由R/B报告记录，V8非盲态收据检查已有通过。原生 Python 完整 CSV/JSON 字节再生与归档 B Node CLI 仍 OPEN；本轮没有运行这些命令。B报告提交的 commit statuses 为空，按 PR 触发过滤的关联 workflow runs 为空，无法据此宣称整个仓库所有 CI 都不存在，更不能写 CI PASS。

A轨新提交检查了 Andreozzi2020 六个公开 XLS 原始会话和 zTree 清洗链。原始 XLS 实际解析、zTree 运行、清洗 CSV 行级重建仍 NOT_RUN；已有813/1206的宽表历史滞后字段错误属于真人来源测量审计，尚无第二个独立真人实验的冻结预测复现。A轨说明原作者主分析脚本未直接读取该错误字段，不能将其直接归因于论文主回归失效。

## 新增有限样本治理计算：只有六个会话

作者原始论文 DOI https://doi.org/10.1038/s41598-020-70681-z ，记录134名参与者、6个实验会话，两个处理条件各3会话。原作者清洗代码从会话 globals 读取处理标签。现有已读论文说明每期随机配对和角色顺序；个体层处理随机分配机制尚未建立。

为量化独立会话数的约束，本轮独立用 Python 3.13.5 标准库 Fraction 和 itertools.combinations 计算一个**另行构造的人工反例**。六个会话等权结果固定为 [0,0,0,1,1,1]，假设恰有3会话随机分配至处理组，且20种三会话组合等可能。观测完全分离的均值差为1。枚举全部 C(6,3)=20 种标签分配，两侧绝对均值差至少1的组合恰好2个，人工双侧精确置换 p=2/20=1/10。其余差值为正负1/3。

这仅说明**在该假设和该人工结果下**，把134人或1340条重复观测当作独立随机分配单位会错误扩大有效独立信息。真实论文的处理分配是否随机、会话大小、处理效应及推断条件仍需原始证据；本人工 p 值不能引用为 Andreozzi 论文的实际显著性检验。原论文可能采用其他设计和层级建模，需逐项复算才能评价。

可复算命令（本轮已原生执行其同等计算）：

```python
from itertools import combinations
from fractions import Fraction
y = [0, 0, 0, 1, 1, 1]
stats = []
for a in combinations(range(6), 3):
    a = set(a)
    stats.append(Fraction(sum(y[i] for i in a), 3)
                 - Fraction(sum(y[i] for i in range(6) if i not in a), 3))
assert len(stats) == 20
assert sum(abs(x) >= 1 for x in stats) == 2
print(Fraction(2, 20))
```

新增治理问题 E109-01：SESSION_LEVEL_RANDOMIZATION_INFERENCE_NOT_ESTABLISHED。应先恢复会话分配机制和会话层原始数据，再选择适用的置换或层级推断；仅6个会话时避免使用普通个体独立标准误的未经核验显著性。

## 跨轨与证据边界

R279 原研究既有结题状态保持；S75人工非盲态E1，完整原生复算关口 OPEN。A轨已取得真实数据来源审计 E2，但新增真人样本外预测 E2=0，独立新研究总体 E3=0。R257 S53 原盲态 FAIL、R267 S63 评分前冻结时序 FAIL 保留。未见本轮所读目标路径发生跨轨覆盖；全仓库内容级逐文件扫描 NOT_RUN。

仓库 README 顶部仍以2026-10-21的R200为首条，不能将该导航顺序直接当作当前 R 系列进度；实时提交与交接显示 R279 S75。只登记导航滞后风险，避免覆盖他轨索引。

没有主动触发 Actions 或付费资源。GitHub 账单、免费额度、全仓库所有运行状态均未独立完整核验。

下一E110：核对 R279 S75 原生执行门是否被 R/B 后续关闭，并继续跟踪 Andreozzi 六会话处理分配和 raw XLS 到 CSV 的可复算证据。只有实际运行与字节核验才能关闭 OPEN。
