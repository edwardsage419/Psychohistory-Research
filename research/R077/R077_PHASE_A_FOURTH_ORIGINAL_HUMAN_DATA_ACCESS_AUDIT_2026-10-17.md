> **保留的历史阶段快照，非R077当前状态。** 本报告准确记录2026-10-17最初OSF网页/API HTTP503与第四数据无法取得的阶段A事实。随后已找到 Drouvelis/Pearce 2025 的原作者Zenodo数据，核验15个原始场次，提交严格冻结并在首次模型结果前记录 Rev-001 资格门失败和 Rev-002 修订；最后真实七模型评分、SHA重算归档成功，R077已结题为 `CLOSED_BOUNDED`。见[当前研究入口](README.md)和[正式科学报告](R077_FOURTH_REAL_HUMAN_ZERO_SHOT_E3_FINAL_SCIENTIFIC_REPORT_2026-10-17.md)。旧文 `R077 E3=OPEN` 仅描述当时状态，不能当成当前状态。

# R077 Phase A：第四独立真人实验来源筛选及公开档案的真实可达性审计

日期：2026-10-17。**R077尚未得到第四份可核验的真人逐试次来源；阶段状态 `SOURCE_ACCESS_BLOCKED`，研究本身 `ACTIVE`，E3=`OPEN`**。本文件只记录官方网络入口的真实可达性，绝不把公开论文提供的研究结果当成新的M0-M6真人模型计算。

## 数据实验候选与严格前置门

在访问任何第四实验真实参与者行动数据及计算真实模型指标以前，已独立冻结 [R077来源和盲评分门](../../protocols/R077_FOURTH_INDEPENDENT_HUMAN_DATA_SOURCE_AND_BLIND_SCORE_GATE_2026-10-17.md)，commit `92453bd6f1a759bbe019d7b68207df57d2902ad1`。目前三项优先候选来自互不重叠的第四作者实验来源：

1. **C1 优先**：Barreda-Tarrazona, Jaramillo-Gutiérrez, Pavan, Sabater-Grande (2026)，*Exploiting the machine: Human cooperation with artificial agents in prisoner's dilemma*，Journal of Economic Psychology 116(2026),102925，DOI `10.1016/j.joep.2026.102925`。论文报告human-human实验对照及另外human-agent处理，repeated PD三次各10轮，作者资料已声明全部 Stata/z-Tree/原始行动托管 [OSF 4HTQ3](https://osf.io/4htq3/)。将来只有Human对Human条件、同一局内已看见历史才允许进入真实验证。**独立原始 session / participant / local C/D codebook 未验证**。
2. **C2 备用**：Kasberger、Martin、Normann、Werner (2026)，*Algorithmic cooperation: A comparison with human play in the infinitely repeated prisoner's dilemma*，Games and Economic Behavior 159,113–130, DOI `10.1016/j.geb.2026.06.001`。论文明确另外真正的240名真人实验，在2022-2023独立20/30人的场次收集，真实人类预先注册资料见 [OSF zcv6x](https://osf.io/zcv6x/)。**原文数据可用性是按需请求**，OSF注册入口可查不表示真实逐人行动CSV已经公开，必须先核验。
3. **C3 备用**：2019 Royal Society Open Science 论文 *Cooperation in the Prisoner's Dilemma: an experimental comparison between pure and mixed strategies*，作者声明资料见 [OSF p4dgz](https://osf.io/p4dgz/)。真实处理、场次标识、逐轮合作动作和配对结构尚未核验。

## 真实 GitHub Actions 执行与失败等级

代码 [r077_official_fourth_source_reachability.py](r077_official_fourth_source_reachability.py) 复用已通过合成反例安全测试的 R075 源URL探测器；实际 [R077 GitHub Actions run 38994025347](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994025347) 已分别向6个官方网页和公开OSF文件API探测，10项合成网络/ZIP隐私回归测试通过。**六个HTTP响应均503**：

| 候选 | 官方网页 | 官方文件API | 可读原始数据 |
|---|---|---|---|
| C1 OSF 4HTQ3 | HTTP 503 | HTTP 503 | UNKNOWN |
| C2 OSF zcv6x | HTTP 503 | HTTP 503 | UNKNOWN；且论文数据称按需索取 |
| C3 OSF p4dgz | HTTP 503 | HTTP 503 | UNKNOWN |

这是本次执行环境OSF端点访问受阻的**明确负证据**，不能推导“数据未发布”“论文有问题”“下载不存在”或“全部来源不可合法取得”。不能使用论文表格推造参与者序列，也不能把OSF网页可访问程度、合成测试成功当成真人来源已核验。

在此门之前以及本阶段中，R077 **没有下载任何第四项原始真人行、没有拟合任何第四项模型概率、没有计算或公布任何第四项E3 Brier/logloss、没有修改R073–R076的冻结公式**。前期R076使用的两个目标此前已被研究者看过，不能通过给既有数据重新分折充当真正全新E3。

## 下一次任务边界

继续尝试官方可下载的镜像、学会共享资料、原作者仓库或另一份完全独立的真实真人实验，**先确认原始逐试次来源字节和 session / partner / t / C-D方向 / 在 t-1 实际可见的历史反馈**，再单独提交不可调整的模型与评分协议，然后才能真实运行预定R073 source-only donor 在第四实验的条件预测；任何数据源无法提供 session，则可限定为源参数零样本预测但不能宣称严格的独立session校验。

`R077_PHASE_A=SOURCE_ACCESS_AUDITED_WITH_HTTP_503_BLOCKERS`
`R077_FOURTH_REAL_HUMAN_M0_TO_M6_SCORES=NONE`
`R077_E3=OPEN`
`R076_RETROSPECTIVE=NOT_EQUIVALENT_TO_FOURTH_STUDY`
`PESEN_v0.1=FROZEN`
