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
