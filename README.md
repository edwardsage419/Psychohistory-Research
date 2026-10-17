# 心理史学 | Psychohistory Research

可检验的跨尺度计算社会科学研究档案。研究主轴为个体认知与学习、群体互动、制度环境以及有条件的长期社会变化。

## 当前归档覆盖（2026-10-15）

**R001 至 R064 共 64 轮均有历史研究 ZIP 对应材料归档。** 已恢复、校验并提交 ChatGPT 文件资料库中的全部 74 份历史 ZIP（按 SHA256 区分有 71 份不同内容），保留历史重复版本。

* **[74份原始 ZIP](archives/library-originals/)**：保持原文件名及内容，ZIP CRC PASS，Git SHA 已校验。
* **[逐轮对应清单](manifests/RECOVERY_STATUS_R001_R064.csv)**：R001、R003 在早期综合包中；R002 为 2026-10-15 补做；R004—R064 为正式编号包。
* **[每份文件 SHA256](manifests/LIBRARY_ORIGINAL_ZIPS_2026-10-15.csv)** 与 **[完整恢复审计](manifests/RECOVERY_AUDIT_2026-10-15.md)**。

归档完整表示当前能检索的 ZIP 文件已经保存，不能自动证明每轮研究的外部原始数据、科学有效性或所有散落非 ZIP 附件均已完整复现。PESEN v0.1 仍然冻结。

## 独立文档与源代码快照

从 ChatGPT Library 另行恢复 **163 份独立文件**（87份 Markdown、58份 Python、12份 JSON、5份 CSV、1份 TXT），合计原始字节 2,068,126。已保存为 [完整 ZIP 快照](archives/library-standalone/心理史学_独立文件原始快照_2026-10-15.zip)（845,358字节，SHA256: `0f57a02eda0cb111ca02e5a0d20bef2aca40c6f7f3bbc2cba3848edc64fbf12b`），并保留 [163份文件逐项 SHA256](manifests/STANDALONE_FILES_SHA256_2026-10-15.csv)。

最新增量主控台 [v5.0](docs/RESEARCH_CONTROL_v5.0_2026-10-16.md)（另保留 [v4.0 历史快照](docs/RESEARCH_CONTROL_v4.0_2026-10-15.md)）与 [R065 研究入口](protocols/R065_RESEARCH_GATE.md) 单独提供便于在线阅读。ZIP 中保留所有旧主控台版本、独立报告、程序与附表，包括可能重复出现在逐轮研究包中的文件。

## 已核验的重点研究结果

| 轮次 | 类型 | 当前证据 |
| :--- | :--- | :--- |
| R002 | 2026-10-15 追补的合成机制对照 | 人造数据、21 项本地测试通过；不能冒充历史已执行研究 |
| R063 | Najar et al. 2020 动态社会学习机制审计 | 固定作者源码和 Figure 6 来源核查、29 项本地测试通过；未完成原始逐试次 CSV 本地字节级重算 |
| R064 | Levy et al. 2025 独立观察学习回顾性分析 | GitHub 作者处理后 CSV 固定 blob 的连接器端实数值分析、16 项本地构造数据测试；本地原始 CSV 端到端重算待完成 |

R064 主要结局为高收益减低收益的受试者等权模仿率差 **+0.00583**，受试者 Bootstrap 95% 区间 **[-0.01103, +0.02288]**，跨零。此结果不可直接视为 R063 metaVS 或 PESEN 的独立机制检验。

## 目录说明

* `research/R002/`、`research/R063/`、`research/R064/`：逐轮可复现代码、研究报告、派生结果和各自的完整性校验记录。
* `archives/library-originals/`：74份从历史聊天文件资料库恢复的原始研究 ZIP，含编号轮次与早期基础模型包；`archives/` 根目录保留先前发布的3份 ZIP。每份原件 SHA256 见清单。
* `protocols/`：事前锁定方案及其适用条件（R064 锁定协议已从研究资料库提取入库）。
* `manifests/`：文件 SHA256、轮次归档状态与尚未闭合的证据门槛。
* `docs/`：研究治理、复现约束、历史研究主控台、年度计划、跨学科知识索引与候选模型目录。

## 复现和审慎使用

使用 Python 3.10 及以上版本，进入 `research/R002/`、`research/R063/` 或 `research/R064/` 后执行 `python -m unittest discover -p 'test_*.py' -v`。

R063 的部分精确非参数检验依赖 SciPy，缺少 SciPy 时程序会说明相应检验未执行。R064 的源数据必须先从原作者仓库取得，且 Git blob SHA 必须匹配，方能完成本地原始 CSV 复算。

本仓库不包含私人研究参与者数据，也不再分发两项外部研究的原始完整实验数据。外部来源、固定提交和 blob SHA 见研究报告。

**PESEN v0.1 保持冻结。** 当前数据不足以确定独立社会惩罚心理机制，也不足以支持普适历史预测定律。对新机制的吸收以预先确定的竞争性检验、外部数据和可复现性为准。

## 使用权与来源

本仓库用于公开研究存档、审阅和可追溯性。未单独声明的本仓库原创内容暂无明确开放源码授权；第三方论文、源码与数据遵循各自许可。参见 `docs/PUBLICATION_POLICY.md`。

## R065 新增研究阶段（2026-10-15）

已建立 [R065 关键试次与来源复核](research/R065/README.md)：从 Levy 等人固定 Git blob 读取 4,427,523 字节并重新核验 Git SHA1，筛选 226 人、1,808 次诊断选择。高收益减低收益模仿率差为 +0.004425，受试者 Bootstrap 95% 区间 [-0.03208, +0.04093]。关键试次的 M1 收益分层简化预测在回顾性留整人评估中略差于 M0；该项仅为探索性后续复核。新增可运行 Python 代码和 9 项通过的合成测试；本地完整真实 CSV 复算仍待完成。PESEN v0.1 继续冻结。

R001 至 R064 的历史 ZIP 归档状态见此前恢复审计。当前最新实质研究阶段为 R065 PHASE A，不将新增 R065 研究文件误记为历史 R065 正式 ZIP。

最新主控台：[v4.1 增量记录](docs/RESEARCH_CONTROL_v4.1_2026-10-15.md)；每阶段交付同步要求：[GitHub 同步规程](docs/RESEARCH_SYNC_WORKFLOW_2026-10-15.md)。

## R065 第二阶段：顺序与时间趋势（2026-10-15）

继续完成 [R065 Phase B 分块趋势与 counterbalance 审计](research/R065/R065_PHASE_B_ORDER_AUDIT.md)。226 人每人 8 次关键试次，前两个实验块平均模仿率 46.68%，最后两个 34.07%，前减后 +12.61 个百分点，受试者 Bootstrap 区间 +6.42 至 +18.81 个百分点。顺序分组为先高收益 121 人、先低收益 105 人，收益效应的组间差异区间跨零。全部属于已见结果上的回顾性分析。

本轮 [R065 复现程序与测试](research/R065/README.md) 共有 15 项本地构造数据单元测试实际通过，外部来源数据 Git blob 在连接器端核验成功；完整原始 CSV 的本地 Python 全字节重算仍受网络条件阻碍。PESEN v0.1 继续冻结，研究整体关口未关闭。

## R065 第三阶段：原作者模型状态重置审计

对七个模型的 [原作者固定源码](https://github.com/arielevy8/obs-learning-fishing/blob/fd5f435b5368b69916e7acc6a9991aa5f46b3ddb/model_fitting/objectives.py) 实读发现，模型统一在 day 23、45、67、89、111 重置学习状态；真人实验 8 个各 17 日的区块起点则是 day 18、35、52、69、86、103、120，两者没有重合。day 89 正是第六个关键选择，公开实现若逐字使用，会在该次选择前清空历史，令两动作的初始化预测等概率。有关结构反例、来源限定及待验证事项见 [R065 Phase C 审计](research/R065/R065_PHASE_C_RESET_AUDIT.md)，其机读数据位于 [R065 Phase C JSON](research/R065/R065_PHASE_C_RESET_RESULTS.json)。

截至本轮，R065 全部 **25 项本地人工样本与代码结构测试通过**，但完整原始行为文件与作者模型拟合的本地端到端重放尚未完成。公开源码差异对论文已发表模型拟合的实际影响仍为 UNKNOWN。PESEN v0.1 维持冻结。

## R065 第四阶段：回顾性关键试次预测比较（2026-10-16）

新增 [R065 Phase D 审计](research/R065/R065_PHASE_D_PREDICTION_AUDIT.md)及[完整派生数值](research/R065/R065_PHASE_D_PREDICTION_RESULTS.json)。在 226 名参与者、1,808 个关键选择的完整留整人评分中，统一概率 M0、收益分层 M1、实验块分层 M2、实验块与收益交叉 M3 的平均 Log loss 分别为 0.664810、0.665154、0.661563、0.663022。M2 试次时间分层的平均分数最好，但相对 M0 的受试者重抽样区间跨零。此次计算纠正并记录了初始草算中单行扣除导致同一参与者数据泄漏的问题；正式结果与 R065 Phase A 的 M0、M1 既有结果一致。

代码已提交 [严格 Git blob 约束的本地复现脚本](research/R065/r065_phase_d_loso.py)、[构造样本测试](research/R065/test_r065_phase_d_loso.py)及 [GitHub Actions 来源重算工作流](.github/workflows/r065-reproducibility.yml)。目前容器成功运行四项独立 synthetic 排除算法测试。原作者完整处理 CSV 本地获取仍受网络限制，GitHub Actions 作业成功状态尚未证实，不能声称完成本地真人数据复算。未来需要检查 CI 日志，并进一步比较原作者七模型状态重置规则对真实预测分数的影响。

研究总关口仍 OPEN，PESEN v0.1 冻结。

## R065 第五阶段：day 89 固定源码的初始预测损失界限（2026-10-16）

按照先行提交的 [Phase E 事后研究计划](protocols/R065_PHASE_E_DAY89_BOUND_2026-10-16.md)，检查所有七模型公开源码在第 89 轮重置学习状态的预测后果。226 名合格被试中当日 73 名选择了作者定义的直接模仿动作。两选项等概率预测 Log loss 0.69314718；按其他参与者同日观察值计算的 Beta(4,4) 留人基线 Log loss 0.63346543，平均差 0.05968175，20,000 次受试者重抽样描述性区间 [0.01513433,0.10422917]。

完整方法、严格来源与边界请阅读 [R065 Phase E 审计](research/R065/R065_PHASE_E_DAY89_AUDIT.md)和 [机读 JSON](research/R065/R065_PHASE_E_DAY89_RESULTS.json)。独立 [复算 Python 程序](research/R065/r065_phase_e_day89.py)与 [8 项本地通过的测试](research/R065/test_r065_phase_e_day89.py)已同步，程序和测试远端 Git blob 与本地执行字节一致。GitHub Actions 已添加 Phase E 来源校验，但 CI 成功证据尚未取得。

本阶段属事后、来源条件性的预测界限检查，不能替代作者七个认知模型的真实重新拟合，也不应修改 PESEN v0.1。整体研究关口依然 OPEN。

## R065 第六阶段：不依赖个人原始记录的统计证书

在不复制原作者第三方逐人数据的前提下，新建 [R065 Phase F 独立汇总量审计](research/R065/R065_PHASE_F_AGGREGATE_CERTIFICATE_AUDIT.md)，用第五阶段已公开的 226 名合格参与者、73 次 day89 直接模仿和 Beta(4,4) 平滑规则，精确重算历史平均 Log loss、Brier 及**条件性二项分布 bootstrap 95% 百分位区间**。程序确认 Phase E 当时的有限次模拟区间与精确分布计算一致；这只认证汇总算术，不认证原始来源或心理机制。

本地已实际运行 [9 项新测试](research/R065/test_r065_phase_f_aggregate_certificate.py)，均 PASS；[复算程序](research/R065/r065_phase_f_aggregate_certificate.py)和[结果 JSON](research/R065/R065_PHASE_F_AGGREGATE_RESULTS.json)已按本地 Git blob 原样提交并远端核验。仓库的 GitHub Actions 新增可独立运行的无外部数据 `aggregate-certificate` 任务，但尚无远端作业成功证明。

最新主控台见 [v4.6](docs/RESEARCH_CONTROL_v4.6_2026-10-16.md)。完整原始 CSV 的本地 Python 复算与原作者七个模型的真实对照重拟合仍待执行。PESEN v0.1 冻结。

## R065 第七阶段：匿名单元独立复算（2026-10-16）

从固定来源数据中提取八实验块×高低收益的 16 个聚合计数单元，保留 226 人、1,808 次关键选择及模仿总计 684 次的证据约束。使用 [独立 Python 复算程序](research/R065/r065_phase_g_cell_certificate.py) 完全脱离个人原始记录，重建 R065 Phase D 的 M2（按实验块）与 M3（按实验块×收益）对数损失及 Brier，数值与历史计算吻合，12 项本地测试通过。

进一步确认：在每个固定实验块中，收益标签与先高/先低序列组完全对应，故 M3 的交叉预测不能单独识别收益效应。参见 [Phase G 研究审计](research/R065/R065_PHASE_G_AUDIT.md)、[匿名聚合数据](research/R065/R065_PHASE_G_CELLS.json)和[本地重算结果](research/R065/R065_PHASE_G_RESULTS.json)。

最新控制台见 [v4.7](docs/RESEARCH_CONTROL_v4.7_2026-10-16.md)。GitHub Actions 离线作业已添加，但成功执行尚无可核实证据。R065 完整研究门保持 OPEN；PESEN v0.1 冻结。

## R065 第八阶段：固定原作者逐人试次上的 Model 3 敏感性

在作者原始逐人 CSV 的十份便利样本、共 542 次正式 `play` 选择中，固定 Model 3 与 β=5，只替换状态重置时间轴：原作者公开日期方案平均 NLL **1.417681470**，按实际实验区块边界重置的平均 NLL **1.529461786**。有 21 次自主选择预测概率受到影响。样本非随机，未重新拟合参数；这一有限结果说明“修正不对齐日期”不会自动改善具体模型的预测表现。

查看 [Phase H 研究报告](research/R065/R065_PHASE_H_AUDIT.md)、[聚合结果与来源 SHA](research/R065/R065_PHASE_H_RESULTS.json)、[Python 程序](research/R065/r065_phase_h_model3_reset.py)和[12 项实际通过的单元测试](research/R065/test_r065_phase_h_model3_reset.py)。原作者原始文件在 GitHub 连接器端实读，未在本仓库重新分发；本地 Python 使用完整原始样本的重放仍未执行，原作者七模型的 native 拟合亦未执行。工作流已增加独立来源重放配置，但成功执行记录尚无核验。

主控台现为 [v4.8](docs/RESEARCH_CONTROL_v4.8_2026-10-16.md)。R065 全研究门仍 OPEN；PESEN v0.1 保持 FROZEN。

## R065 第九阶段：调整 Model 3 β 后重置日期敏感性（2026-10-16）

固定十份原作者逐人实验文件、542 次 `play`，延续前阶段的两个状态重置方案。将先前固定 β=5 的损失比较扩展到 β∈[0,30] 的独立拟合和**留出整名参与者、其他九人拟合 β**的十折预测。作者时钟平均留人 NLL 约 **0.68635**、区块边界约 **0.69086**；对比 β=5 时平均 NLL 1.41768、1.52946，表明参数选择对预测效果影响非常大。

已提交 [Phase I 审计](research/R065/R065_PHASE_I_AUDIT.md)、[匿名计数及真实连接器侧十折结果](research/R065/R065_PHASE_I_RESULTS.json)、[Python 复算程序](research/R065/r065_phase_i_beta_profile.py)、[12 项本地通过测试](research/R065/test_r065_phase_i_beta_profile.py)和 [GitHub Actions 两类校验配置](.github/workflows/r065-phase-i.yml)。同时修正 Phase H 在极高 β 下的 Softmax 精度问题；本地两阶段共 25 项测试通过。

这仍属十人便利样本上的事后敏感性实验，不是论文全部七模型的 native 重新拟合或独立可推广预测证据。自动复算的 GitHub 作业是否成功尚无可核验记录。

最新 [主控台 v4.9](docs/RESEARCH_CONTROL_v4.9_2026-10-16.md)。PESEN v0.1 冻结；R065 整体科学验证仍 OPEN。

## R065 第十阶段：扩大到作者筛选合格的 24 名参与者（2026-10-16）

本轮首先锁定选样方法，再从原作者固定处理数据中的 226 名合格者按两种实验收益顺序各选 12 人，读取 24 份固定 Git blob 的原始实验文件，分析 1,327 次自主选择。比较作者源码与区块起始日两套重置时间轴，独立拟合 Model 3 的 β，并用其他 23 人拟合后预测留出的第 24 人。

24 折留人平均对数损失分别为 **0.67843771**（作者时钟）与 **0.67867746**（区块时钟），差异仅 **0.00023975**。24 人中 13 人在作者规则下得分较好，11 人在区块规则下得分较好。对照先前十人便利样本，本次差距显著缩小，仍不能据此宣称某套规则具有稳定优势。

已提交 [Phase J 研究报告](research/R065/R065_PHASE_J_SCREENED_24_AUDIT.md)、[匿名充分计数及来源哈希](research/R065/R065_PHASE_J_SCREENED_24_RESULTS.json)、[可复现的严格筛选与 24 折程序](research/R065/r065_phase_j_screened_replay.py)、[10 项已通过的本地测试](research/R065/test_r065_phase_j_screened_replay.py)及 [GitHub Actions 来源回放配置](.github/workflows/r065-phase-j.yml)。远端 CI 是否已运行成功，**仍未得到证据**。

研究主控台更新至 [v5.0](docs/RESEARCH_CONTROL_v5.0_2026-10-16.md)。原作者七个认知模型的完整 native 拟合未完成，R065 科学验证门仍开放，PESEN v0.1 保持冻结。

## R074 第二独立真人重复博弈外部复验（2026-10-17）

[正式 R074 研究目录](research/R074/README.md)已完成真实原作者来源校验、[外部模型评分前独立冻结协议](protocols/R074_DALBO_AUTHOR_INDEPENDENT_HUMAN_E3_TRANSFER_FREEZE_2026-10-17.md)、29项完全合成反例测试及**另一独立作者实验**的18个场次、15,338次个人合作选择完整留场次预测。[第一份 R074 E3 报告](research/R074/R074_REAL_EXTERNAL_HUMAN_E3_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-17.md)记录了 M3(本人及对手上轮选择) 对 M1(本人上轮选择) 的场次等权 Brier 差 **−0.022915**，18场中16场更好、2场更差；而 M4(双方两轮) 对 M3 的差 **+0.003171**，仅5场更好、13场更差。因而上一轮对手行动的额外条件预测性在独立真人实验中获得支持，更长记忆总会增进预测的假设被真实反例限制。所有未改善场次保留，不能解释为因果记忆或制度因果。

[19,308字节匿名原始宏评分归档](research/R074/R074_EXTERNAL_REAL_HUMAN_18_SESSION_E3_RESULTS.json)已由[独立 GitHub Actions SHA256 严格重算](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38988844437)确认；原始真人行与任何逐场ID均不存本仓库。R074 为有界 E3 结题（`CLOSED_BOUNDED`），当前拟合系数仍来自新实验自身其他场次，零样本数值参数迁移、心理因果机制与长时段历史外推均保持开放。PESEN v0.1 继续冻结。

## R075：第三独立原作者真人重复博弈的外部 E3 复验（2026-10-17）

[第三真人实验正式归档入口](research/R075/README.md)和[完整科学方法及负结果](research/R075/R075_REAL_THIRD_HUMAN_E3_RESULTS_AND_SCIENTIFIC_BOUNDARIES_2026-10-17.md)：恢复 Fudenberg、Rand、Dreber 2012 论文共同作者 David Rand 本人发布的可校验一手原始 ZIP（SHA256 `328346c3cf88a71a3d6cf574f7d6ba741dcea460f3926c16266f1784d3a699ef`），完成18原始实验场次、384场次内参与者身份槽、34446原始人类决定的完整字节和字段核验。在独立提交[冻结 E3 协议](protocols/R075_COAUTHOR_ORIGINAL_HUMAN_18_SESSION_E3_TRANSFER_FREEZE_2026-10-17.md)后执行七个严格未改动 R073 模型，36项纯合成检查与**26116个真人意向行动目标、18场完整留出评分**均通过真实 GitHub Actions。

第三实验结果：M3 双方上一轮相对 M1 本人上一轮场次等权 Brier `−0.029117`（**18/18场改善**）；M4 双方前两轮相对 M3 Brier `−0.012417`（**15/18场改善**），但零执行噪声处理的3场全部恶化。R074独立第二实验的 M4 净恶化继续保留，说明延长记忆的增量并不跨制度稳定。完整原始匿名数字结果 [R075 19,692字节 JSON](research/R075/R075_REAL_THIRD_HUMAN_18_SESSION_E3_RESULTS.json) SHA256 `eb74129bfd9af62678e9cacf910477854be694317d7b5d875e5ca33dc0f76174`，已由[独立第三次完整原作者数据重放CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38991027657)成功核验后永久Git归档，不保存任何原始人类决策行、真实场次标识或个体轨迹。

**R075 `CLOSED_BOUNDED`、A01至A06 PASS，独立第三真人 E3 通过；跨实验零样本数值参数迁移、社会反馈心理因果作用和宏观历史演化仍未证实。PESEN v0.1 继续冻结。**

## R076：R073 原始数值参数零样本迁移到另外两项真人实验（2026-10-17）

[正式R076研究包](research/R076/README.md)已经完成严格 `NO_TARGET_TRAINING_LABELS=TRUE` 的真实来源数值迁移：只在 R073 原始12场、18424个 t>=3 真人风险事件上拟合一次固定的七模型（M0–M6中M0–M4的源概率），再将不变的来源参数直接用于 R074 18场15338个决策与 R075 18场26116个意向行为。24项合成测试与[真实GitHub Actions](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38993686411)两个job success，且[第二次独立原始数据全字节重算和Git归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38993752496)同样success。

主要固定来源全部12场时，R074的 M3−M1 Brier `−0.023302`、M4−M3 `−0.002442`；R075分别为 `−0.028524`、`−0.012907`。另两套预定来源对照并列保留：R073固定同伴6场的参数应用到 R074 时 M4 相对 M3 **变差 +0.000823**，不能把记忆深度的获益当成普适性质。[所有三套donor×两目标真实匿名评分](research/R076/R076_RETROSPECTIVE_R073_SOURCE_ONLY_TO_R074_R075_REAL_HUMAN_RESULTS.json)共129126字节SHA256 `ecee82cf3686d6c03cef56fb84c84118b252b7c184b46dc45413e34f876a52da`。

**R076已`CLOSED_BOUNDED`、A01至A06 PASS，但两个目标此前已经被研究者查看过，所以本次属于回顾性跨研究数值迁移，尚不能声称是新的前瞻E3。** [冻结协议与局限](protocols/R076_RETROSPECTIVE_SOURCE_ONLY_ZERO_SHOT_CROSS_STUDY_TRANSFER_FREEZE_2026-10-17.md)及[科学结果报告](research/R076/R076_RETROSPECTIVE_SOURCE_ONLY_REAL_HUMAN_TRANSFER_RESULTS_2026-10-17.md)已同步。PESEN v0.1 继续冻结。

## R077：第四独立原作者真人实验上的固定数值模型零目标拟合验证（2026-10-17）

[正式R077研究包](research/R077/README.md)已完成另一作者 Drouvelis/Pearce 2025 公开 Zenodo [原始人类实验数据](https://zenodo.org/records/15462528) 的精确来源哈希验证：3,620次人类合作选择，260名场次内参与者、15个真实来源session、1,810次双人局轮，局内具有完整前两轮真实行动的1,040次共同下一步选择。唯一冻结 donor 为R073原作者12个session、18,424个训练目标；**不使用任何R077结果拟合或校准**，七模型、alpha=20和固定策略参照0.05均不变。第四研究论文在2025年已发表，此处只指我们七模型此前尚未对该真实人群评分，并非在真人参与前预注册的全新实验。

按照原始15场等权Brier，M0=0.224580、M1=0.151140、M2=0.155817、M3=0.120929、M4=0.119010、M5=0.177250、M6=0.512500。两项主要比较：**M3−M1=−0.030211（14场好/1场差）**；**M4−M3=−0.001919（8场好/7场差）**。多一轮历史的增量非常有限且不稳定，不能忽略7场反例及固定WSLS明显较差的反例。[完整科研结题报告](research/R077/R077_FOURTH_REAL_HUMAN_ZERO_SHOT_E3_FINAL_SCIENTIFIC_REPORT_2026-10-17.md)保留全部处理分层和log loss。

**来源门失败并未被改写：** Rev-001要求同一 `game` 永不换配对，真实源的一个处理130次重新分组，另有80个个人局不从t1完整连续采样，导致[两个首次真实作业严格拒绝、未产生任何人类模型得分](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995038132)。在首次真正真人评分之前，另行冻结[Rev-002 修订](protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md)，只用严格同局存在的t−1/t−2记录、保留所有重配对处理，不调参数；24项合成守卫和[首次成功真实评分](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995309336)均通过，[再次从原作者重下载并逐字节SHA复算、永久Git归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995401729)成功。[完整匿名结果9835字节](research/R077/R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json) SHA256 `8d8b8413e3e55cb5d856f34b873ee20c2ba470e04190bb8577f931d25ba509a4`，未存个人原始记录或逐场分数。

**R077 `CLOSED_BOUNDED`；第四独立作者真实人类数值转移有界通过；R077 Rev-001 原始资格门FAIL永久保留；未证明人类认知记忆因果与长期制度演化；PESEN v0.1继续冻结。**

## R078：个体预测相同与因果机制不同的数学反例、群体层差异（2026-10-17）

[正式 R078 E1 数学研究包](research/R078/README.md)建立两个结构竞争模型，单个参与者 `(X,对手上一行动O,本人本轮选择Y)` 的完整观测联合分布和Bayes最优Brier/log loss **完全相同**：加入O后的人工 Brier `0.21`，不加入O `0.25`，两模型都改善 `0.04`；但强制改变O的因果作用分别是 `0.4` 与 `0`。在明确额外的“模型A的组员O彼此独立、模型B同组共享潜在U”假设下，10人群体合作率的方差分别为 `0.025` 和 `0.061`。这证明预测增益不识别社会影响因果，而组级共同冲击结构在某些设计下具有区分价值；**这些是纯数学假设数字，不是已被四项真人实验验证的群体机制**。

[正式结构模型数学报告](research/R078/R078_EXACT_OBSERVATIONAL_CAUSAL_NONIDENTIFICATION_AND_CROSS_SCALE_REPORT_2026-10-17.md)、[独立结果执行前冻结的协议](protocols/R078_PREDICTION_CAUSALITY_CROSS_SCALE_EQUIVALENCE_FREEZE_2026-10-17.md)及[真实GitHub Actions 42项合成检查+精确两次运行归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996053069)均可复核。[2,463字节纯E1 JSON](research/R078/R078_EXACT_SYNTHETIC_OBSERVATIONAL_EQUIVALENCE_E1_RESULTS.json) SHA256 `7d13d3f238552b19be689b9cf841acc04cb7b8a535fd8639bce2cf13f2edb680`，完全没有读取人类行为原始行。R078 `CLOSED_BOUNDED`、A01–A06 PASS、仅E1，不新增真人E2/E3，不构成制度/历史因果发现。PESEN v0.1保持冻结。

## R079：真实作者实验中的动态双人网络配对、群体合作方差及随机重配对数学参照（2026-10-17）

[正式R079真人群体研究包](research/R079/README.md)在独立提交[冻结协议](protocols/R079_INDEPENDENT_HUMAN_DYAD_COVARIANCE_RANDOM_MATCHING_REFERENCE_FREEZE_2026-10-17.md)后，从 Andreozzi、Ploner、Saral (2020) [原作者GitHub实验资料](https://github.com/seyhunsaral/stabilitycondcoop)固定 Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9` 的425701字节CSV中实际读取1340次人类正式行为、134个场次内参与者身份槽、6个独立原始实验session、10轮、670对真正双方动作镜像互证的动态配对；计算该研究特有的真实0/50/100已实现转移 `y=action/100`，不将本项当作R073二元重复PD同一模型的E3复验。

按原始session等权，实际配对人类贡献的去均值交叉矩 `+0.033114`，数学上均匀随机重配对参考 `−0.006030`，**超额交叉矩 `+0.039144`（6/6真实场次都为正）**；双人组平均贡献的横截面方差实际 `0.080317`，重配对参考 `0.060745`。两处理各3场分层数值保留，前5轮平均贡献0.366692、后5轮0.290859，但所有结果均为**E2描述性组级二阶统计与固定个人选择的非因果匹配数学参考**，不能由此推断同伴因果效应、制度因果或百年历史动力学。

34项纯合成检查、真实网络配对身份互证、独立[原作者SHA逐字节复算GitHub Actions](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996643486)成功，首次合成测试误报失败仍保留；[3771字节匿名原始二阶矩结果](research/R079/R079_REAL_AUTHOR_HUMAN_DYAD_NETWORK_MOMENTS_E2_RESULTS.json) SHA256 `82efe8ad7bcc6c01ac10616676d84c5208ad9f6cc83670aa4c5b72f3860ff102` 已永久同步。[完整科研报告](research/R079/R079_REAL_HUMAN_NETWORK_DYAD_GROUP_MOMENT_REPORT_2026-10-17.md)与[结题验收](research/R079/R079_FINAL_ACCEPTANCE_STATUS.json)均可核验。R079 `CLOSED_BOUNDED`；未来64个真实网络的资料尚需原始文件、真人机器人角色和网络重连边界审计；PESEN v0.1继续冻结。

## R080：原作者完整64组真人–机器人时变网络合作与拓扑 E2 实证（2026-10-17）

[正式R080研究入口](research/R080/README.md)已完整实读 Shirado & Christakis (2020) [作者 Mendeley Data v1](https://doi.org/10.17632/t963ktp6ft.1) **全部64份原作者网络JSON、逐文件发布方官方SHA256、3R+3CSV元数据**，经 `players.is_bot` 区分1024个人类实验身份槽与独立机器人，重建每网30行为轮、31个真实网络快照，共1920个行为round、1984个真实图状态，30720个潜在人类行动槽中**27656次实际可观测C/D**（90.0%）。原作者各8网络的八种处理均保留，真64网络等权的真人合作率第1轮 `0.679803`、第30轮 `0.569070`，平均下降 `−0.110732`；但某些网络工程策略 `disengaged_mgmt_bots` 则 `0.6000→0.7936`（+19.4百分点），而 `engaged_mgmt_bots` `0.7014→0.3167`（−38.5百分点），反例同样完整归档。真实HH边网络均值由35.922增至52.719，但不能因多连边而因果解释合作变化。

**来源/门槛失败全部保存**：[第一次网络源节点资格失败](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998214433)因图快照会合法省略零度人类，后经全64源不评分校验、在**任何网络合作率结果出现前**独立冻结[Rev-002真实图零度节点规则](protocols/R080_PRE_FIRST_REAL_NETWORK_METRICS_GRAPH_ISOLATE_AMENDMENT_REV002_2026-10-17.md)，未改变人类人数、结果口径和八类处理；第一次独立CDN复查SHA不匹配亦拒绝存档并保留记录。45项合成[人机身份/整图保护测试与真正64网实数计算](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998549613)均成功，之后[独立再次下载并核对原作者所有SHA、结果逐字节同一且永久Git归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998839902)成功。

[11,745字节匿名E2真实结果JSON](research/R080/R080_FIRST_PARTY_64_HUMAN_NETWORKS_TOPOLOGY_E2_RESULTS.json) SHA256 `7b7d231d97a98c4b08e7d3658fa8e943bacd60aef1d8529754cd1f75179b99c8`，[最终科学报告](research/R080/R080_FULL_64_HUMAN_BOT_NETWORK_E2_SCIENTIFIC_FINAL_REPORT_2026-10-17.md)与[A01–A06结题验收](research/R080/R080_FINAL_ACCEPTANCE_STATUS.json)已全部同步。R080 `CLOSED_BOUNDED`仅是真人网络E2条件性描述，**没有**新E3个体预测、机器人社会影响因果识别或长时期历史预测；`PESEN v0.1`继续冻结。下一阶段独立检查原作者网络级随机分配、机器人节点语义与真人动作缺测。


## R081：64个原作者人机网络的全部真人缺测行动精确界限与实体语义审核（2026-10-17）

[R081正式研究入口](research/R081/README.md)已按照[新真人界限结果前的独立冻结协议](protocols/R081_AUTHOR_64_NETWORK_ASSIGNMENT_BOT_ENTITY_AND_MISSINGNESS_BOUNDS_FREEZE_2026-10-17.md)完成64/64份作者Mendeley v1网络JSON发布方SHA256严格来源验证，并在**25项合成测试全部成功后**两次独立完整执行真正人类行为缺测极端敏感性分析。[首次真实CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38999664896)和[独立SHA逐字节复算永久归档CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38999829725)均success，10,714字节匿名[结果JSON](research/R081/R081_FIRST_PARTY_ORIGINAL64_MISSING_HUMAN_ACTION_SHARP_BOUNDS_E2_RESULTS.json) SHA256 a6d7f84924eabc5389dc9b82f6de62ed73ce79a455eb6dba873af33cb81d1998。

全部64网络共30,720个每轮16人理论行动槽，真实可观察真人C/D为27,656，缺失3064。R080原观测首末合作下降11.07个百分点；如果每一缺失槽都可任意赋一项二元C/D，全部64网络等权完整名册合作变化**精确界限为下降20.2148至2.4414个百分点，始终为负**。原8类处理有4类严格下降、1类严格上升、3类在缺测极端补全下触零/跨零。首轮缺31槽、末轮缺151槽，覆盖率随时间减弱。单独网络中有21/64在自由补全下方向不定；第二实验248网络快照有一例机器人五节点各一真人连接结构的例外，均如实保留。

[正式科学报告](research/R081/R081_ALL64_AUTHOR_MISSINGNESS_BOT_ENTITY_AND_CAUSAL_ASSIGNMENT_SCIENTIFIC_REPORT_2026-10-17.md)和[六项验收](research/R081/R081_FINAL_ACCEPTANCE_STATUS.json)现已同步。R081研究证据级别仍为**真实来源、回顾性E2缺测敏感性**；论文所谓单一逻辑机器人与原始记录五个bot节点的映射、实验处理随机分配、人类动作缺测机制及第一/第二实验可交换性均仍待独立核验，因果推断门未开。**R081=CLOSED_BOUNDED，PESEN v0.1=FROZEN**。


## R082：原作者全部64真人网络的缺测轨迹与零度网络状态共现审计（2026-10-17）

[正式R082科研入口](research/R082/README.md)和[结果前方法协议](protocols/R082_ORIGINAL64_HUMAN_NONRESPONSE_GRAPH_ISOLATION_AND_ALLOCATION_SOURCE_FREEZE_2026-10-17.md)固定了六类真人行动可观测性轨迹、两种网络快照索引时间对齐及两种网络孤立口径。[首次原作者SHA全64网络分析CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39000527926)与[独立第二次严格SHA全64网络重新下载及原字节永久归档CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39000654904)均成功，各执行**28项纯合成测试**；完整八处理/64网络[匿名23,743字节原始数字结果](research/R082/R082_FIRST_PARTY_ORIGINAL64_HUMAN_NONRESPONSE_AND_NETWORK_ISOLATION_E2_RESULTS.json) SHA256 `9ba6caeb25b0f2c8e024c4ce53ff7377567cef14f175c4fb0036d22c5f3b6999` 获逐字节一致性核验。

全部1024原始真人名册身份槽中，**869**身份30轮均有C/D，**31**个30轮全无记录，**120**个有此前合作选择但末段持续缺测，**4**个间歇缺测后有返回；31个从无记录与120个持续末段缺测共解释3064个无C/D槽位中的**3048**个。原始网络快照第t+1索引对齐第t个行动列表项，缺测中的**3060/3064个**与真人图连接度0共现；另有5个真人行动虽图度0仍有C/D，以及4个有边却缺测，全部保留。采用另一快照索引、没有真人邻居但仍有机器人邻居的分层也同步保存。实验2来源五个机器人标记节点248个图快照中，有247个五条人机边，1个四条边（总机器人标记节点度数0的一次事件）。

**这为数据完整性与记录机制建立了可复算的强关联证据，未识别人际或机器人因果：**缺测/图节点状态可能由原实验平台的同一状态规则编码；原初图随机化和每轮重连机会随机化不独立证明机器人实验处理在原始网络之间随机分配。正式[科学结题报告](research/R082/R082_ORIGINAL64_HUMAN_NONRESPONSE_GRAPH_ASSOCIATION_AND_ALLOCATION_CAUSAL_GATE_FINAL_REPORT_2026-10-17.md)、[A01至A06验收](research/R082/R082_FINAL_ACCEPTANCE_STATUS.json)已归档。**R082=CLOSED_BOUNDED、真人原始来源E2、因果资格OPEN、PESEN v0.1=FROZEN**。


## R083：原作者真人“协调惩罚偏好”主实验与复验两队列的E2复算（2026-10-17）

本项转向新的条件性惩罚微观机制家族。已经以[冻结协议](protocols/R083_COORDINATED_PUNISHMENT_ORIGINAL_HUMAN_PAIRED_MAIN_REPLICATION_FREEZE_2026-10-17.md)（首次新R083真人结果前提交 `2f9e6ddfb56bc1a83cd3c6484ca7efe307ae6ac0`）锁定 Molleman et al. (2019) *Nature Human Behaviour* 原作者公开 GitHub [固定提交](https://github.com/LucasMolleman/NHB_CoordinatedPunishment/commit/42cba97300910988b7b7386379fa32492d35d8aa)上的完整 Stata 真人原始数据及作者 .do 脚本，两份各自的 Git blob 已经验证。作者原始全4320行，其中2880人次配对拥有本研究定义的 `punisher==1` 完整0/1行为策略记录。

[首次35项合成及真人SHA运行](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001261509)与[第二次独立原始字节重取、35合成及结果全文件 SHA 完全一致的归档](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001352142) 均SUCCESS。主实验1336配对在“他人惩罚”与“他人不惩罚”的自身惩罚选择差为**+4.416个百分点**，复验1544配对为**+2.785个百分点**，主实验四格1054/134/75/73与作者原始.do脚本既有值完全一致。结果符合两队列正向的先冻结机制方向门。关键负面分层：主实验原本无条件惩罚者差**−1.974个百分点**、复验该类为+3.017百分点，两个细分检验都未达到常见显著性标准，切勿扩大为任意个体都协调惩罚。

[完整科学报告及因果边界](research/R083/R083_REAL_AUTHOR_COORDINATED_PUNISHMENT_MAIN_REPLICATION_SCIENTIFIC_REPORT_2026-10-17.md)、[原作者SHA二次全字节匿名数字](research/R083/R083_ORIGINAL_HUMAN_COORDINATED_PUNISHMENT_MAIN_REPLICATION_E2_RESULTS.json)（6019字节SHA256 `a75638fbb3619667a077e1fa640bc1b3ca97dce062b2538c779eeac053e216ae`）与[六项正式结题](research/R083/R083_FINAL_ACCEPTANCE_STATUS.json)均在Git main。项目未上传任何原作者个人记录、逐行选择或原始Stata数据。原作者 `rerun` 主/复验样本是否与其他外部作者实验彻底独立、真实他人惩罚的因果作用、处罚制度演化与历史社会发展仍未验证；本项为**已发表原作者数据回顾性E2**，不冒称新招募受试者的E3。**R083=CLOSED_BOUNDED，PESEN v0.1=FROZEN**。


## R084：七实验室原作者OSF来源资格、二次失败复验及有界结题（2026-10-17）

[R084原作者来源门入口](research/R084/README.md)与[新结果前冻结协议](protocols/R084_MULTILAB_INSTITUTIONAL_SELECTION_SOURCE_GATE_FREEZE_2026-10-17.md)研究2023年 Lo Iacono 等发表于 PNAS Nexus 的七实验室惩罚制度选择复验，论文报告1008真人、84组、30轮和五个实验室满足全部预注册复验准则，Oxford/Warsaw未全部满足。以上都是**原论文事先已发表结果**。另据OSF自身公开Trove元数据找到原作者 `Replication Data` component `r7y9n`及 `Utrecht_sbj.csv` 文件ID `fjyg3` 的索引SHA256线索，**但原始文件字节从未实取核验**。

[真实官方OSF元数据访问run 39001728447](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001728447) 与[独立再次复验及永久归档run 39001798435](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001798435) 均执行通过26项合成安全测试；每次对10个真实OSF官方元数据路径的访问均返回**HTTP 503（10/10）**。因此**0份原始真人文件、0条原始行为行、0次真人统计结果**。两轮安全HTTP状态收据确实逐字节一致，共4185字节、SHA256 `3ebccaca8f6b631afeaa927aeadc677d896b8aa358ab498c3309c2542028e1ac`，作为[永久反面证据归档](research/R084/R084_2023_SEVEN_LAB_ORIGINAL_OSF_OFFICIAL_SOURCE_GATE_FAIL_CLOSED_E0_RESULTS.json)。

[科学报告](research/R084/R084_SEVEN_LAB_INSTITUTION_SELECTION_OSF_ORIGINAL_SOURCE_GATE_SCIENTIFIC_REPORT_2026-10-17.md)和[六门正式验收](research/R084/R084_FINAL_ACCEPTANCE_STATUS.json)完整区分行政性的 **R084=CLOSED_BOUNDED（仅来源资格失败审计）** 与科研的 **REAL_HUMAN_E2=OPEN / BLOCKED_OFFICIAL_OSF_SOURCE_503**；两个CI返回success只说明安全失败被准确记录，不证明OSF永久不可用、实验从未存在或本项目复算了已发表5/7结果。SI/SFI制度由个人自行选择，因果解释也未成立。后续优先换其他可获取的原作者真人制度/互动源，不让一个来源受阻无限延缓更多模型的独立研究；PESEN v0.1继续冻结。


## R085：不对称四人公共品实验的Zenodo原作者身份通过、MAT内部格式失败有界结题（2026-10-17）

[R085主报告入口](research/R085/README.md)、[原作者文件身份冻结协议](protocols/R085_AUTHOR_ASYMMETRIC_FOUR_PERSON_PGG_SOURCE_AND_SCHEMAS_FREEZE_2026-10-17.md)和[格式独立追加协议](protocols/R085_PHASE_B_ORIGINAL_MAT_FORMAT_NONBEHAVIORAL_INSPECTION_FREEZE_2026-10-17.md) 已按新真实证据出现前先行提交。固定原作者Wang/Hilbe/Zhang 2025 [Zenodo v2 16918146](https://zenodo.org/records/16918146)四人线性与阈值PGG两源文件，分别以原作者MD5原字节核验通过。**两文件MATLAB5结构经同一冻结SciPy读取器失败**，不据此伪造四人原始合作评价。

[首次真实及24synthetic run 39002422986](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002422986) → [第二次独立格式及34synthetic run 39002668337](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002668337) → [第三次34synthetic与相同发布方二原始文件MD5独立重复、永久归档run 39002819018](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002819018) 均顺利**执行来源失败收据**。第三次与第二次匿名来源失败收据字节严格相同： [1123字节安全结果](research/R085/R085_ORIGINAL_AUTHOR_TWO_MAT_VERIFIED_MD5_BUT_STRUCTURE_FAIL_SOURCE_RECEIPT.json) SHA256 `282d3beb52b30ad938cf0e89247a2316a2c40d118a51712543a42c9fd6a3bae8`。源码与全部24+10项纯合成有界检测均归档；没有原作者原始真人行入项目仓库。

[正式负结果与边界报告](research/R085/R085_ZENODO_ORIGINAL_FOUR_PERSON_PGG_AUTHOR_MD5_SCHEMA_SOURCE_GATE_REPORT_2026-10-17.md)和[A01至A06验收](research/R085/R085_FINAL_ACCEPTANCE_STATUS.json) 明确 **R085=CLOSED_BOUNDED（仅来源/格式资格审计），真正四人真人贡献E2仍然BLOCKED / OPEN，PESEN v0.1=FROZEN**。下一独立R086可检查同一作者已公开MD5的两人Excel实验（线性+阈值）或转向另一真正可运行来源；不无限扩大失败数据格式子问题。


## R086：原作者1104真人两人线性/阈值公共品的两session真实贡献E2（2026-10-17）

[正式R086科研入口](research/R086/README.md)、[来源评分前协议](protocols/R086_WANG_HILBE_ZHANG_TWO_PLAYER_PGG_ORIGINAL_XLSX_SOURCE_AND_OUTCOME_FREEZE_2026-10-17.md)和[新真人行为计分前冻结角色/贡献评分规则](protocols/R086_PHASE_B_TWO_PERSON_FULL_ORIGINAL_BEHAVIOUR_WITHIN_SESSION_FROZEN_SCORE_2026-10-17.md)均事先提交。固定Wang/Hilbe/Zhang 2025 [Zenodo v2原作者两Excel](https://zenodo.org/records/16918146) 的出版方MD5和一次完整源SHA256：[来源MD5+十工作表实体资格run39003094721](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003094721)安全合成及真实访问成功；[第一次真人贡献E2全计算run39003367675](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003367675)和[再次独立下载原始文件、两方真实结果完全同字节及永久Git归档run39003432643](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003432643)也都成功。53项合成检查每次通过。

**独立于R085四人MAT来源失败，R086取得550名线性+554名阈值真实参与者，每人两session本人行为，共45810次原始本人贡献数值实算。** 二人原始每名焦点参与者四行中，排除伙伴重复行为行；线性第1场22轮、第2场21轮，阈值两场各20轮。已执行两实验×五处理×两session共20条主比较，每条本人一人一权；线性AI贡献末减初分别 +5.0943/+2.2547（原单位），阈值AI −0.8654/−1.6442，部分条件两场反向；阈值FE 85/110、93/110本人首末贡献完全不变，所有这些**科学阴性/零证据**均永久保存，避免凭均值宣称多数人向同方向变化。

[全部20原始分层、逐轮匿名曲线与正式科学报告](research/R086/R086_ORIGINAL_TWO_PERSON_LINEAR_THRESHOLD_PGG_1104_HUMANS_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[双来源SHA严格复验85,566字节永久JSON](research/R086/R086_ORIGINAL_1104_HUMAN_TWO_PERSON_LINEAR_THRESHOLD_FIVE_ARM_E2_RESULTS.json)（SHA256 `600104f42f2b896646abe543cc6d8ab10450f1d30ed823d9feeeaf6d20a1628c`）及[A01-A06正式验收](research/R086/R086_FINAL_ACCEPTANCE_STATUS.json)已经同步main。**科学证据级别E2原作者真实贡献再运行，不能基于不同禀赋与组内相互作用宣称条件因果、更不能宣称新的E3或历史演变预测；正式R086=CLOSED_BOUNDED，PESEN v0.1=FROZEN。**


## R087：原作者134名真人十轮条件合作策略迁移实证E2（2026-10-17）

[正式R087科学研究包入口](research/R087/README.md)、[首次134名真人数据评估前冻结协议](protocols/R087_AUTHOR_CONDITIONAL_COOPERATION_134_HUMANS_ORIGINAL_GIT_SOURCE_BEHAVIOR_FREEZE_2026-10-17.md)（提交 `551cbb044201ffb7e83798118455199d9af68c81`）基于 Andreozzi/Ploner/Saral (2020) *Scientific Reports* 一手原作者 GitHub固定commit `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`，对原作者发布的完整 `subjects.csv`（Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`）和原作者生成脚本严格来源验证。6实验场次、134真人（NoCondInfo68；CondInfo66）、每人10次真实互动，共**1340人期行为**。原始z-Tree的六件文件到CSV的清洗链目前尚未独立重跑，不冒称完整源层复现。

[首次真实原作者Git SHA复算CI run39003772753](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003772753)与[第二次原始源完整重新下载、38项纯合成及真实人期精确重算永久归档39003815853](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003815853)均成功，结果**16,647字节**、SHA256 `e0663ea1d7829fb1c4ba51b134ca1276e9c16e6e0b3b3d321b343ee66c8e4bbe`逐字节相等。所有隐私ID/原始真人行为行都未存本仓库。

真人人类条件策略ccL、ccM、ccH的四分类中，**条件合作者C期1 87人→期10 46人；无条件完全不合作者D 35→79人**；首末**C→D 43人、D→C 4人**，全10期类别完全不变者仅50/134。实际行动均值**42.54→17.16**，条件策略高低合作响应跨度**54.10→24.25**。两信息处理均方向一致但仍属于同一项2020年已发表研究，不能据此断言信念无因果作用或2026年新增E3复验。[正式完整科研报告](research/R087/R087_ORIGINAL_134_HUMAN_CONDITIONAL_COOPERATION_STRATEGY_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[全十期/两信息处理匿名数值](research/R087/R087_FIRST_PARTY_134_HUMAN_10_PERIOD_CONDITIONAL_STRATEGY_TRANSITIONS_E2_RESULTS.json)、[六门最终验收](research/R087/R087_FINAL_ACCEPTANCE_STATUS.json)已永久归档。**R087=CLOSED_BOUNDED，真人原始作者回顾性E2，因果E3与长时段历史演化OPEN；PESEN v0.1=FROZEN。**


## R088：171个人类六人群体20轮全球合作的缺失锐界实证E2（2026-10-17）

[R088科研主入口](research/R088/README.md)基于另一原作者Pilgrim/Stewart/Raihani (2025-12/2026, *Scientific Reports*, [DOI 10.1038/s41598-025-30979-2](https://doi.org/10.1038/s41598-025-30979-2)) 对全球/本地多层阈值公共品实验进行原始真人 E2 独立回顾性复算。原始仓库 `chasmani/PUBLIC_social_identity_and_cooperation` 固定commit `8ce2c0cac4784485232aa96295f48ff147290b05`，原作者完整6人组源CSV Git blob `f902865203bdb465a505869b593eca432831b2fa`，连同作者排除及合作率R脚本逐件Git blob真实字节验证。**171个群组×6真人×20轮、三处理各57组，共1026原始真实受试者、3420组轮和20520行动机会。**

科研阴性链完整保留：先冻结[Phase A](protocols/R088_SIX_PERSON_MULTILEVEL_PUBLIC_GOODS_171_GROUP_ORIGINAL_SOURCE_E2_FREEZE_2026-10-17.md)，首次[真实run39011042473](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011042473)发现“每期行动均非空”的原假设失败；再冻结[Phase B](protocols/R088_PHASE_B_ORIGINAL_ACTION_FIELD_DIAGNOSTIC_FREEZE_2026-10-17.md)，[真实run39011243425](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011243425)核验**20,456项明确真实选择、64项空行为**（三处理19/26/19，期1缺失29、期20缺失0）；另冻结[Phase C缺失锐界算法](protocols/R088_PHASE_C_ORIGINAL171_MISSING_ACTION_SHARP_INTERVAL_SOURCE_FREEZE_2026-10-17.md)，从171组六人实际观察数和未观察数严格给global投资、四人及以上阈值达标的上下界，**没有删除受试者、没有把未知当不合作**。[首个真实171组全部评分run39011509370](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011509370)81项合成与真实作者来源成功；[第二次独立完整源取回、81synthetic及两个匿名报告逐字节Git归档run39011582787](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011582787)也通过。

在完整六人作者样本里，**GlobalOnly**全球投资率 **67.95—68.23%**、全球阈值达标率 **71.32—71.58%**；**Balanced**相应 **44.62—45.00%**、**42.98—43.51%**；**GlobalBoost**相应 **60.63—60.91%**、**64.39—64.56%**。无论64缺失如何，GlobalOnly−Balanced的全球投资比率差仍 **+22.95至+23.61个百分点**，GlobalBoost−Balanced仍 **+15.63至+16.29个百分点**；但三处理初末自身合作率均下降，分别必在约 −27.19至−24.85、−26.61至−24.27、−21.05至−17.25个百分点。负例：三处理中仍各有至少1/11/9个原始群组保证初末全球投入增加，不能声称每个小组都衰退。

[完整A01–A06科研正式报告](research/R088/R088_ORIGINAL_171_MULTILEVEL_PUBLIC_GOODS_GLOBAL_SHARP_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[原始真实171组缺失锐界结果](research/R088/R088_ORIGINAL171_GLOBAL_COOPERATION_64_MISSING_SHARP_BOUNDS_E2_RESULTS.json)（**65,424字节**、SHA256 `2b0f76fa8f7d1a42d2f91508c4acf52c0a7c0fc9523801ec1d9759559d8fb67e`）、[独立64缺失来源负证据](research/R088/R088_ORIGINAL20520_ACTION_LABEL_MISSINGNESS_E1_SOURCE_RECEIPT.json)（2144字节SHA256 `b52f6313f40beecdb761c5bb9b6013b318700c2e1c2f8f4d0a7682efee5edf18`）与[正式验收](research/R088/R088_FINAL_ACCEPTANCE_STATUS.json)全部保留。源身份核证、群体行为界限属于**原作者已发表E2回顾性再算**，区间是missing可行上下界**不是置信区间**，研究样本仅是原作者排除后完整组六人且不含被排除者，新的社会身份因果/群体政策因果/独立E3与长时段历史演化均未建立。**R088=CLOSED_BOUNDED；PESEN v0.1=FROZEN。**


## R089：171个六人群体完整留出5折，实验前身份与合作行动历史的下一轮预测E2（2026-10-17）

[R089正式完整科研包](research/R089/README.md)采用 [R088](research/R088/README.md) 经过原作者来源Git blob验证的171组×6真人×20轮完整组资料，先于任何R089新真人预测评分[冻结M0–M3模型、5折完整留出群体与64项行动缺失锐界评分](protocols/R089_171_GROUP_COMPLETE_HOLDOUT_HISTORY_AND_BASELINE_IDENTITY_PREDICTION_FREEZE_2026-10-17.md)（提交`8f303a8e7b4e2275f177d3e50aa903dd199d48b7`）。固定完整六人团体留出而非逐条行为随机分割；每条件57组独立分5折12、12、11、11、11，共171个原始群体仅留出一次、**3249个未来下一轮群体轮次实际预测**。实验前群体身份指标只允许`survey.1.player.DIFI_big_group_distance`；绝不使用游戏第5/10/15/20轮问卷与任何事后身份来预测过去轮次。原源64项缺失不当0或删组，对真实六人global人数所有可行值穷举平方误差锐界，预测器的历史输入中点也明确只是数值表示而非个人行为补全。

[最初synthetic函数名语法失败CI39012760897](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39012760897)留存，修复测试拼写后[首次40synthetic及真实171组5折预测CI39012803376](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39012803376)成功；[第二次完整原作者文件再次SHA读取、40synthetic及全部匿名结果逐字节重复和永久Git归档CI39012889699](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39012889699)success。

**真实原作者E2留出预测结果（平均六人群体全球投资比例平方误差识别界，越小越好）**：仅条件与同轮训练群体的 M0 **0.078922–0.079495**，留出群体自己上一轮选择的M1 **0.033694–0.034130**，M2固定半半混合 **0.037304–0.037651**，M3再加入实验前身份 **0.037316–0.037663**。针对同一个缺失不确定预测目标，M1相对M0改善有完全正的锐界 **+0.044918到+0.045671**，三实验处理方向均为正；**M3没有展现出在M2以外的额外预测改善**。重要的实证负例：三条件下M1的改善并非人人成立，Balanced有5/57完整组更差、GlobalBoost有24/57更差、GlobalOnly有25/57更差以及1组模糊，必须保留。

[正式科学报告](research/R089/R089_171_SIXPERSON_GROUP_FIVEFOLD_HISTORY_PREGAME_IDENTITY_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[20,052字节匿名全部5折/三处理得分与负例](research/R089/R089_ORIGINAL171_GROUP_FIVEFOLD_HISTORY_VS_PREGAME_IDENTITY_SHARP_E2_RESULTS.json)（SHA256 `9dda5e5fbf4abe2a9d9e7d2fb029e03eb81202c63f0e0af576b7e69882aea266`）与[A01–A06正式限定验收](research/R089/R089_FINAL_ACCEPTANCE_STATUS.json)都已同步。该发现是**同一原作者已发表实验内部严格留出群体后历史行为的预测信息**，不是新来源跨实验E3、不证明群体身份无因果效应或长时段历史变化。**R089=CLOSED_BOUNDED，PESEN v0.1=FROZEN**。下一项优先另找独立原作者、独立真实人群与明确实验场次/完整群体以检验该预测收益是否跨实验稳健。


## R090：独立原作者气候俱乐部30组六人历史预测迁移失败（真实E2负面证据，2026-10-17）

[R090正式科研主入口](research/R090/README.md)，来自另一原作者Antonioni/Sánchez/Cabrales的[Zenodo固定记录17610157](https://zenodo.org/records/17610157)。原作者真实CSV 419189字节、作者网页MD5 `56931608b717aea06105ad10a58ff937`、全文件SHA256 `ebc8831011a1a3b4893a80ae158d5129ed0f35e57a8092eba36c6a7b0cbd4282`，2700人轮×27源字段；经严格[Phase A源冻结](protocols/R090_INDEPENDENT_CLIMATE_CLUBS_REAL_GROUP_SOURCE_ELIGIBILITY_FREEZE_2026-10-17.md)首次真人[oTree轮字段不一致失败CI39013486584](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39013486584)后，另冻[Phase B时序结构方案](protocols/R090_PHASE_B_OTREE_TWO_ROUND_FIELDS_NONOUTCOME_AUDIT_FREEZE_2026-10-17.md)，[CI39013629744](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39013629744)证明真实实验轮来自`subsession.round_number=1..15`，技术`participant._round_number`均15，**180人、8场次、30个六人稳定群体×15轮**，T1/T2各8个完整组、T3/T4各7个完整组。首次失败永存，没有以伪造轮次提前计算合作效果。

[Phase C实际原始贡献计分前冻结](protocols/R090_PHASE_C_CROSS_AUTHOR_30_GROUP_15_ROUND_HISTORY_TRANSFER_FROZEN_SCORING_2026-10-17.md)，沿用R089三个冻结预测器结构但将源目标预定换为可比范围[0,1]的 `sum(本轮各原受试者贡献)/sum(本轮禀赋)`，每次留出完整原作者固定六人组全部15轮，训练其他同条件原始组、t2..15共**420个真实群组下一轮预测**。M0其他group同轮条件平均MSE **0.04888197**，M1自身上一轮group投入**0.05719792**（比M0**更差0.00831595**），M2原先固定二者各半 **0.04029091**（比M0改善**0.00859106**）。**R089历史上一轮M1的跨原作者直接正向迁移被真实阴性反驳**：M1在30群组13改善/17恶化；只有T1的M1改善，T2/T3/T4全部反向；M2在T3也负改善。R089同实验源自身的历史信息阳性仍是E2，**不同任务中迁移不支持普遍同一心理惯性规律**。

重要来源风险：该2700记录中**249次系统自动决策**（T1/2/3/4分别82、38、80、49），198次贡献超时，故新结果是**真人参与实验记录的贡献过程（含自动决策）**，不是每条人类主动选择的心理证据，尚未做预冻仅手动行动敏感性。二任务虽共享M0/M1/M2模型结构，但R089是六人是否投资global的离散比例、R090是连续禀赋加权贡献比例，非完全相同输出测量。无实验场次bootstrap置信区间、无因果政策效应、无新独立前瞻E3，更没有历史级长期预测。

[首次84项完全synthetic+真实原件420次预测CI39013984019](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39013984019) 和 [第二次完整Zenodo原始MD5+SHA重新下载、84synthetic重复、**7913字节匿名全文逐字节复核**CI39014046442](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39014046442)均SUCCESS，永久Git存档SHA256 `f7970b444588d0af7986a10056750400190d360d1533bb1d3dafffa9cce05182`：[完整原始新原作者群组匿名失败/部分成功结果](research/R090/R090_INDEPENDENT_AUTHOR_30GROUP_15ROUND_HISTORY_TRANSFER_M1_NEGATIVE_E2_RESULTS.json)、[正式科学报告](research/R090/R090_CLIMATE_CLUBS_CROSS_AUTHOR_GROUP_HISTORY_TRANSFER_NEGATIVE_E2_SCIENTIFIC_REPORT_2026-10-17.md)和[A01–A06机读验收](research/R090/R090_FINAL_ACCEPTANCE_STATUS.json)全部完成，负面实证同正面实证同等级归档。**R090=CLOSED_BOUNDED；跨作者E2确认M1未复现、M2池化上部分成功；PESEN v0.1=FROZEN**。下阶段优先检验真正独立、输出指标与R089更一致的真人多层公共品组实验，不为消除R090负结果而在已见数据上重新调模型。


## R091：独立Jonsson灾害四人公共品190组3610次留出预测的第三作者真人E2（2026-10-17）

[R091正式完整研究包](research/R091/README.md)，Jonsson & Jonsson (2025), *Cooperation in the face of disaster*, [PLOS ONE DOI 10.1371/journal.pone.0318891](https://doi.org/10.1371/journal.pone.0318891)。原作者官方[markusrobertjonsson/condcoop](https://github.com/markusrobertjonsson/condcoop) 固定commit `2a23fc3221e636c0119b1d1f1a9c4945bca83e85`；首次Git blob核验原著`Data_Main.xlsx` 571844字节、源SHA1 `499787e08242c44c32a469b5d72b206ccf2c73f0`、完整SHA256 `04d2ed5a59885cde2a1740f33b295a86bd374b80cd811d8ff84c88cded68a023`。作者主sheet `DiffTreatments` 经不看贡献的单独来源资格真实实跑核验：**760名真人、190个稳定4人群体、每组连续20轮、15,200真人动作行**，菲律宾111组/瑞典79组、两国×五条件10层最少12个组。另一`DiffProb`瑞典概率扩展sheet可能包含与主sheet重叠人员，因此**没有相加**；不能把论文宣称的884总人错误当本轮真实评分分母。

所有源合同在真人评分前分五阶段冻结：[A原始Git元数据](protocols/R091_JONSSON_DISASTER_PGG_ORIGINAL_XLSX_STRUCTURE_BEFORE_BEHAVIOR_2026-10-17.md)、[B群体成员和20轮](protocols/R091_PHASE_B_JONSSON_2025_MAIN_SHEET_4PERSON_GROUP_ROSTER_BEFORE_CONTRIBUTION_2026-10-17.md)、[B2只读source标签](protocols/R091_PHASE_B2_AUTHOR_COUNTRY_TREATMENT_SOURCE_LABELS_NONOUTCOME_FREEZE_2026-10-17.md)、[B3原作者Phils/10Prob/40Prob/40Impact/40Level正式安全映射](protocols/R091_PHASE_B3_AUTHOR_ORIGINAL_FIXED_COUNTRY_TREATMENT_MAP_BEFORE_ROSTER_RERUN_2026-10-17.md)、[C原数据贡献读取之前冻结190组M0/M1/M2全部LOOG评分](protocols/R091_PHASE_C_190_AUTHOR_4PLAYER_GROUP_COMPLETE_LOOG_M0_M1_M2_BEHAVIOR_SCORING_FREEZE_2026-10-17.md)。首次source-header私密泄露合成错误[CI39015518318](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015518318)在真人读取前阻止运行、首次source类别不一致[CI39015866343](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015866343)真实拒绝，均如实保留；先以官方源不看行为证明准确码本后才继续，新行为预测模型结构没有根据实证效果调整。

**新的真正第三原作者 E2 预测结果：**在每次完整留出一个原四人组全部20轮并使用同国×处理其它组训练后，t2..20共**190×19=3610个真正原组下一轮目标**。group贡献标准化为四人原始0..20货币贡献之和/80；M0其它训练组同国处理同轮均值MSE **0.03849598**，M1该组上一轮行为 **0.01920014**，M2预设二者各半 **0.01932837**。M1较M0误差平均改善**+0.01929585**，M2增益**+0.01916761**；全部两国和10个国家×处理源层的平均M1/M2改善均为正，**但190组中M1只在142组优于M0，48组反而更差**。

[真实首次完整原作者E2 run39016300977](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016300977)及[第二次独立真实整文件Git blob/SHA重新读取、100项合成重复与匿名结果完整字节复算永久归档run39016368841](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016368841)均SUCCESS，真实永久结果 **18471字节**，SHA256 `1657ee31c5df7640ea7a0943886900133e68f70c0f9c3ac900302d36191f723b`。[A01–A06正式科学报告](research/R091/R091_JONSSON_2025_190_FOURPERSON_GROUP_CROSS_AUTHOR_HISTORY_TRANSFER_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[100合成及精确真人真实数值匿名结果](research/R091/R091_INDEPENDENT_JONSSON_190_FOURPERSON_GROUP_3610_LOOG_M0_M1_M2_E2_RESULTS.json)、[正式机读验收](research/R091/R091_FINAL_ACCEPTANCE_STATUS.json)与原始源码均已同步。

**跨作者结论必须同时保留：**R089六人二元Global投资历史M1正向，R090六人连续贡献含249自动代作记录历史M1负向，R091四人连续贡献历史M1正向但有48组反例；三套预冻方法跨任务**不是同一行为结果，也不是完整实验E3复验**，不足以得出万能心理惯性或历史动力定律。**R091=CLOSED_BOUNDED，原始独立作者真人E2已界定，PESEN v0.1保持FROZEN。** R092优先相同二元行为/更同质跨实验复现，不在这190组已见样本上事后调优。


## R092：第四个独立原作者四人阈值公共品MAT格式来源认证（E1成功、E2阻断，2026-10-17）

[R092受限来源审计入口](research/R092/README.md)，[Wang、Hilbe、Zhang (2025) 官方Zenodo数据v2](https://zenodo.org/records/16918146) 四人阈值公共品原始文件`ThresholdPGG_4P_ExperimentalData.mat`，原作者正式MD5 `6036f73c2f758ab3aeed6dcf4f74585b`，完整源长**17,159字节**、SHA256 `76b02d921d02ad652cb952a71173e84b206135e4deb7bfc6235b9387738a6b05` 均实际从官方首方原件核验成功。作者记录276名受试者（FE76、AI100、MI100）、同人参加两个20轮场次且第二场重新配组，但当前研究**没有从真实MAT变量读取实际真人贡献、group/session或真实预测评分**。

三个相互预先冻结的来源关口保留失败：[A MAT变量形状](protocols/R092_WANG_HILBE_ZHANG_2025_ASYMMETRIC_THRESHOLD_4P_ORIGINAL_ZENODO_MAT_SOURCE_FREEZE_2026-10-17.md) [真实CI39016888560](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016888560)先19项synthetic全PASS，真实数据`scipy.io.whosmat`不可读取；[A2 HDF5结构替代](protocols/R092_PHASE_A2_ORIGINAL_PUBLISHER_MATLAB_V73_HDF5_METADATA_ONLY_FREEZE_2026-10-17.md) [CI39017000035](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017000035)34项synthetic全PASS，官方原件不符合预设HDF5结构；[A3严格只读文件类型安全信号](protocols/R092_PHASE_A3_ORIGINAL_THRESHOLD_MAT_RESTRICTED_FILE_SIGNATURE_DIAGNOSTIC_FREEZE_2026-10-17.md) [CI39017117283](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017117283) **47synthetic和真实原件文件源诊断全部success**，确定源文件**MATLAB 5文件头**、SciPy该源不兼容TypeError，但这不是作者数据损坏证明。所有协议都在对应实读前提交，没有一条原始个人动作/原群体ID落盘公开仓库。

[正式来源研究报告](research/R092/R092_ORIGINAL_THRESHOLD_4PERSON_PUBLISHED_SOURCE_FORMAT_ADMISSION_REPORT_2026-10-17.md)及[机读严谨验收](research/R092/R092_SOURCE_QUALIFICATION_FINAL_ACCEPTANCE_STATUS.json)明确**A03真实模型评分=BLOCKED，不是A01–A06全PASS**。R092状态`CLOSED_SOURCE_FORMAT_BLOCKED`，证据仅E1原件身份，不能将未知贡献同R089/R090/R091实际E2的正负结果比较，更不能标注实验室E3。后续可新冻结使用其它MATLAB5兼容读取工具，但优先转向能直接验证行为的其他独立实验，减少重复尝试同一数据源。**PESEN v0.1=FROZEN。**
