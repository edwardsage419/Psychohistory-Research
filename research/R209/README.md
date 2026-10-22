# R209 创新扩散两轮机制：正式有界人工E1补充研究结题

日期2026-10-22。**CLOSED_BOUNDED_E1_ARTIFICIAL_TWO_ROUND_ADOPTION**。

**目录映射重要校正：R209不是原239项目录中独立的`08-033`条目，因原目录08类止于08-031。** [目录核验与更正](../../docs/R_SERIES_CATALOG_MAPPING_CORRECTION_2026-10-22.md)。关联`04-005 Simple versus Complex Contagion`和`06-013 Bass Diffusion Model`但本R209采用的是自造的四节点同步两轮人工Bernoulli过程，并不意味着已经完成任一原论文全部公式/实证或原239目录的新增一项。本R209属**有界额外机制审计**。下一原239目录实际项目是`09-001 Randomized Controlled Experiment`，按当前R序号进入R210。

[冻结来源/评分协议](../../protocols/R209_ADOPTION_36_WORLDS_972_TRAIN_26244_INDEPENDENT_PRESCORE_FREEZE_2026-10-22.md) · [正式报告](R209_SCIENTIFIC_REPORT_2026-10-22.md) · [36世界精确JSON](R209_EXACT_RESULTS.json) · [972条原完整训练轨迹](R209_ALL_972_ORIGINAL_TRAIN_ADOPTION_TRAJECTORIES.csv) · [26244条独立重抽轨迹联合来源](R209_ALL_26244_INDEPENDENT_NEW_TRAJECTORY_PAIRS.csv) · [源SHA机器验收](R209_FINAL_MACHINE_ACCEPTANCE.json) · [事后正式科研验收与目录纠错收据](R209_FINAL_ACCEPTANCE_STATUS.json) · [原生标准库程序与42项测试](r209_exact_two_round_adoption.py)。

STAR/PATH/CYCLE三个人工无向四节点图，每图固定四个单一起始采用种子，三真实Bernoulli机制BASE/SIMPLE/COMPLEX，两轮同步吸收式采用，36个图×seed×机制世界。每世界27条确切全轨迹和27个真正独立未来路径，合计972个原训练和26244个两轨迹联合来源完整枚举，训练三候选选择只读第一条真实轨迹；对第二条全27轨迹真正来源各计算完整新轨迹logloss及末期新增2+事件Brier，精确Fraction Brier两算法和math.log/70位Decimal核验。

**主要科学反例**：STAR中心0种子，COMPLEX门槛≥2绝不触发，COMPLEX与BASE的全部27路径概率逐一精确相同，真COMPLEX训练识别概率0。CYCLE seed0真COMPLEX虽然与BASE分布不同，单条短训练轨迹选择正确模型概率仅81/1024，未来完整轨迹平均logloss3.412208反而差于固定BASE3.183998；同CYCLE seed0真实SIMPLE选择正确概率405/512，未来完整新轨迹logloss2.754991改善于固定BASE4.149421。不得把完整人工真概率分布误称真实社会行为数据。

[最终Actions run39735660871](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39735660871) Python3.11与3.12各42项、**84次测试通过**，第三生成972+26244完整真实人工来源与SHA并永久机器人[main提交c68e2542](https://github.com/edwardsage419/Psychohistory-Research/commit/c68e254217af9f7732990ac9e61f51cf6abe5e64)。报告透明记录首次CI语法错误和第二次第三归档job误导入Fraction的错误，以及最终三job成功。

仅人工E1，新增真人E2=0、真实历史E3=0，R073/PESEN v0.1继续冻结。下一**R210应研究实际目录09-001 Randomized Controlled Experiment**；全239目录逐项完成之后才统一分类再熔炼。
