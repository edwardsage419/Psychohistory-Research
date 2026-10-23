# R258 最优控制（11-018，P2）

九个人工**三阶段、三离散状态、两动作、二元独立随机扰动**模型，**1728条完整原始x0/六bit结构source**，科研状态`CLOSED_BOUNDED_E1_FINITE_THREE_STAGE_STOCHASTIC_FEEDBACK_CONTROL`。严格人工E1，未复现真实人类/历史政策干预。

[事前冻结](../../protocols/R258_OPTIMAL_CONTROL_9_THREE_STEP_1728_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科研报告](R258_SCIENTIFIC_REPORT_2026-10-23.md) · [Fraction Bellman与全部512合法反馈策略穷举源码](r258_exact_finite_stochastic_control.py) · [1728原source CSV](R258_ALL_1728_ORIGINAL_THREESTEP_CONTROL_SOURCE_ATOMS.csv) · [九world完整价值函数与最优反馈JSON](R258_EXACT_RESULTS.json) · [SHA256机器凭证](R258_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界验收](R258_FINAL_ACCEPTANCE_STATUS.json)。

各期先看状态x_t再选u_t、随后才随机到达d_t；所有9world原source条件积分、Bellman最优价值与**独立完整512个非clairvoyant Markov反馈策略**最小值三路一致。8种预先固定open-loop行动序列不优于反馈；p=1/2、κ=τ=1、x0=1时反馈期望9/2 vs open-loop19/4，严格节省1/4；x0=2反馈47/4 vs open-loop95/8，节省1/8，但另一些world无严格改善。这些是有限数学期望不是政策效果。

[最终成功CI run39897521571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897521571)三个job成功，Python3.11和3.12各82项共164真实单测通过，完整原source/JSON/SHA机器人永久归档[50838d37](https://github.com/edwardsage419/Psychohistory-Research/commit/50838d3793de4274794e999fdb539b4801c48c86)。首次CI run39897405451仅档案审计CSV文本Fraction分母格式错误、overall失败，保留其可审计记录，只修数据类型转换后复验。新增真人E2/历史E3=0，R073/PESEN v0.1冻结。下项原11-019 Multi Objective Optimization（R259）。
