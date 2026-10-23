# R256 排队理论（原11-016，P2）

九个明确的**有限4时格、容量2、每格至多一个到达与服务**人工队列world，每world9独立外生bit全512类型，共**4608完整人工原来源**，仅有界E1科研资格`CLOSED_BOUNDED_E1_FINITE_CAPACITY_TWO_FOUR_SLOT_QUEUE_AND_MARKOV_PATHS`。**不是连续时间Poisson到达/指数服务或无限容量M/M/1实证复算**。

[先行冻结](../../protocols/R256_QUEUE_9_FOUR_BIN_CAPACITY_TWO_WORLDS_4608_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告含首次失败CI](R256_SCIENTIFIC_REPORT_2026-10-23.md) · [Fraction原生队列/独立Markov核](r256_exact_finite_queue.py) · [4608原外生source CSV](R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_ATOMS.csv) · [九world全部队长路径及结果JSON](R256_EXACT_RESULTS.json) · [SHA256机器收据](R256_FINAL_MACHINE_ACCEPTANCE.json) · [正式科研验收](R256_FINAL_ACCEPTANCE_STATUS.json)。

保留4格需求与服务Bernoulli概率均1/2，仅改变“先服务后到达”与“先到达后可服务新任务”时，首格`P(Q1=1)`从1/2变成1/4。独立请求半率与固定隐藏U共同请求半率在单格边际相同，但`P(Q1=0,Q2=1)`前者1/4、后者0。所有4608完整源严格队列流守恒，全部81种四格队长路径与独立理论Markov核相等。虚拟报告器可模仿平衡队长完整路径而真实隐藏队列始终0，须外部真值验证。

[最终成功CI run39896631038](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896631038)三job成功，Python3.11/3.12各82真实单测、共164项通过，完整原source/JSON/SHA机器人永久归档[559ea6cf](https://github.com/edwardsage419/Psychohistory-Research/commit/559ea6cf3ee4de82c2822526dee5d04941f0372a)。首轮CI run39896586661因序列化map用法笔误失败，仅更正序列化后重新全部验收。新真人E2、真实历史E3均0，R073/PESEN v0.1冻结。下条11-017 Optimization Theory拟R257。
