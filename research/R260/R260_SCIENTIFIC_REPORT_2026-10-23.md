# R260 鲁棒优化：九人工双冲击预算不确定集、540全source与稳健极小最大损失/极小最大遗憾区别

日期2026-10-23（Asia/Taipei）。原239目录`11-020 Robust Optimization`（P2）。科研正式资格`CLOSED_BOUNDED_E1_FINITE_TWO_SHOCK_HARD_BUDGET_MINIMAX_AND_REGRET`。本项是完整人工两bit冲击及五个给定成本方案的有限决策演算，不是人类组织选项效用估计、真实极端天气或战争情景风险分布拟合；新增真人E2=0、历史E3=0，R073/PESEN v0.1继续冻结。

## 一手理论与刻意的简化
D. Bertsimas & M. Sim (2004), [*The Price of Robustness*, Operations Research 52(1), 35–53](https://doi.org/10.1287/opre.1030.0065)，研究优化方案为不确定性稳健性付出的代价和可调不确定性规模。**本文只做两个离散二元冲击、Γ∈{0,1,2}硬预算的有限集合UΓ，不复现一般连续不确定预算公式、违约概率上界或真实投资组合决策**。[九原参数世界、全部来源与验收数值预先冻结协议](../../protocols/R260_ROBUST_9_FOUR_SCENARIO_540_COMPLETE_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于代码和任何CI，由独立commit[e04a1601](https://github.com/edwardsage419/Psychohistory-Research/commit/e04a1601506367fb54f4f3db70a763f96f53102e)固定。

## 结构来源、信息集及两个不同的鲁棒目标

每个world设五个合法决定A/B/C/D/E、四种完全原二元冲击`00,01,10,11`、三种允许扰动预算Γ∈{0,1,2}。九world各5×4×3=60原source，**全部共540完整原结构source**，每source设计权重1/60；源包含**预算下被禁止的冲击**并显式标记eligible，不因其被禁止就在CSV中删除。硬预算`UΓ={(s1,s2):s1+s2≤Γ}`随着Γ增大严格嵌套，Γ=0只00、Γ=1包含00/01/10、Γ=2完整四种冲击。因此对**任何固定决策d**，`max_{s∈UΓ} c(d,s)`随Γ绝不下降，尽管单个情景损失c(d,s)本身不要求随冲击位数单调增加。

研究明确比较`min_d max_{s∈UΓ} c(d,s)`（最小最大损失）与`min_d max_{s∈UΓ}(c(d,s)−min_a c(a,s))`（最小最大遗憾）。后者中的`min_a c(a,s)`是**事后知道冲击的、不可提前实行的基准**，不能称实际决策者拥有事后最佳策略。另行定义一个**独立**风险中性模型：两冲击位独立公平，各原情景P=1/4，计算`min_d (1/4)Σ_s c(d,s)`，这一人工概率与Γ硬预算无逻辑必然关联；不把source设计质量1/60当真实冲击频率。

第一计算路线从全部60完整原source逐字读取原成本及预算准入标记求每个Γ的每个决策最坏损失、相对于每情景5个决策中事后最好的最大遗憾，以及所有同分最优决定集合。**独立第二路线不读取第一来源CSV生成器或其筛选计算函数**，直接从冻结成本表按两bit之和构造UΓ，逐decision形成epigraph上界证书及实际达到该上界的最坏情景见证；遗憾同样为所有允许情景构建上界与实际见证并求精确有理最小值。每个world×三个Γ全部直接源演算与独立epigraph路线严格同值，全部平手赢家保留。

## 九world的全参数Γ结果

以下每个“成本最优”列为`(最小最大成本,全部稳健赢家)`，遗憾列为`(最小最大遗憾,全部遗憾赢家)`：

| world | Γ0 成本/遗憾 | Γ1 成本/遗憾 | Γ2 成本/遗憾 |
|---|---|---|---|
| ALIGNED_DOMINANCE | (1,A)/(0,A) | (2,A)/(0,A) | (3,A)/(0,A) |
| HIDDEN_JOINT_TAIL | (0,A)/(0,A) | (0,A)/(0,A) | (3,C)/(3,B/C) |
| REGRET_VS_WORST | (0,A)/(0,A) | (0,A)/(0,A) | (4,C)/(2,B) |
| NONMONOTONE_SHOCK_COST | (2,B)/(0,B) | (2,B)/(2,A/B/C) | (2,B)/(2,A/B) |
| TWO_SHOCK_INTERACTION | (0,A)/(0,A) | (0,A)/(0,A) | (3,C)/(3,C) |
| ADDITIVE_COMMON_SHOCK | (0,A)/(0,A) | (2,A)/(0,A) | (3,A)/(0,A) |
| HIDDEN_TAIL_ALIAS | (0,A)/(0,A) | (0,A)/(0,A) | (0,A)/(0,A) |
| TIED_WORST_CASE | (0,A)/(0,A) | (1,B)/(1,A/B) | (2,A/C)/(1,A/B) |
| HEDGE_VS_NOMINAL | (0,A)/(0,A) | (3,C)/(2,B) | (3,C)/(2,B) |

**最坏损失与最坏遗憾的最优行动不一定一致。** REGRET_VS_WORST在Γ2下稳健成本选择C，因其所有冲击成本为4，故最坏损失=4；选择B在11情景损失5，最大成本5，因此不是最小最大成本解。但C在00/01/10三个情景各相对事后最佳行动A（成本0）损失4，最大遗憾=4；B这三情景成本2，相对事后最佳损失2，而11情景成本5对事后最佳C4遗憾1，最大遗憾只有2，因此**极小最大遗憾唯一选择B**。所谓“鲁棒最优”必须明示所优化的是损失、遗憾、风险约束还是别的函数。

**未被预算覆盖的情景不等于不存在风险。** HIDDEN_JOINT_TAIL与HIDDEN_TAIL_ALIAS在相同五方案上，对于Γ≤1全部三个被准入情景成本逐source完全一样。但未覆盖的11情景中前者A的成本12、后者A成本0，故一旦预算Γ=2：前者最小最大成本赢家C、最坏成本3；后者赢家A、最坏成本0。任何Γ≤1所要求的观察/结构验证都无法区分二者在未纳入的情景下的成本。该严格人工反例意味着不确定集合的**覆盖范围假设本身**影响选项稳健性；不等于现实事故发生概率得到验证。

**共同冲击损失、反单调成本与价格概念要分开。** ADDITIVE_COMMON_SHOCK对各行动仅叠加同一个情景损失，最坏成本从Γ0的0到Γ2的3，但赢家始终A、最大遗憾仍为0；“最坏绝对成本提高”不一定意味着最优方案变更。NONMONOTONE_SHOCK_COST中A成本(4,1,1,0)，两个冲击都来临反而使A成本低于无冲击时，仍严格满足随着可选情景集合扩大、固定行动最坏损失不降低的集合单调性。若用实际风险治理语义解释这个人为下降，就必须有额外机制数据，不能仅凭名称“冲击”推断成本一定增长。

**公平概率平均和硬预算完全不同。** HIDDEN_JOINT_TAIL在独立公平冲击下风险中性最小期望为3，A、B、C同值；但Γ2下最坏成本C单独最优3，Γ1下A最优0。REGRET_VS_WORST风险中性最优A（平均2），最坏成本最优C、遗憾最优B。公平冲击分布只是一项另行冻结的数学假设，不能把它误读为“真实未知风险会以1/4发生”。

## CI、完整来源及有界资格

[原生Fraction全源/最坏损失与遗憾程序](r260_exact_hard_budget_robust.py) · [九world540完整原source CSV](R260_ALL_540_ORIGINAL_SCENARIO_BUDGET_SOURCE_ATOMS.csv) · [全部硬预算全行动证书和平均成本JSON](R260_EXACT_RESULTS.json) · [CSV/JSON SHA256机器完整性凭证](R260_FINAL_MACHINE_ACCEPTANCE.json)。

初次[GitHub Actions run39898333104](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39898333104)两个版本数学测试成功，但第三来源审核中的一个本应保存研究结果的局部变量`r`被后续拆包为“整数预期遗憾r”，导致循环下一次读研究结构时TypeError，**首轮整体failure不能算永久归档**。仅修独立审计变量名为`expected_regret`，预冻结世界/原成本/两种独立算法与任何结果值未改；保留首轮失败历史与修复commit[5ebfe16b](https://github.com/edwardsage419/Psychohistory-Research/commit/5ebfe16b8c61d05515b9d474e4ff906d97d69e09)。

最终[GitHub Actions run39898498981](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39898498981)总体completed/success，三个job全部success，Python3.11和3.12实际各`Ran 81 tests`、`OK`，共**162次真实双版本单测通过**。第三独立审核逐world完整60决策×情景×预算source、每source1/60、Gamma准入、全部9×3鲁棒最优和遗憾赢家含平手、每action上界和实际最坏情景/最大遗憾情景见证、最小公平期望、Γ≤1观察同源别名而Γ2决策反转、CSV/JSON SHA，实际日志`R260_ALL_540_ORIGINAL_BUDGET_SCENARIO_AND_MINIMAX_REGRET_WITNESSES_VERIFIED`和`R260_ALL_540_ORIGINAL_HARD_BUDGET_SOURCES_PERMANENTLY_ARCHIVED`。全部完整原CSV、结果JSON及来源SHA已永久由GitHub bot提交main [f8b0b23d](https://github.com/edwardsage419/Psychohistory-Research/commit/f8b0b23d960d7e4fee9adbb6927289230228837e)。

原CSV SHA256 `4e3d057d5e80180e357bbe9206c0a20354fa1eca33cb96b0403b9294639cb467`；完整结果JSON SHA256 `b429cb687bcc6165ea3e22c9111327aeab19a22063f16c1bb5cf88fac143fd12`。

本R仅`CLOSED_BOUNDED_E1_FINITE_TWO_SHOCK_HARD_BUDGET_MINIMAX_AND_REGRET`，不能声称真实社会风险概率、后果成本或现实风险管理策略得到实证验证。新增真人E2=0/历史E3=0，R073和PESEN v0.1始终冻结。原目录下一项11-021 Mean Field Approximation（R261，P1），先完成全部R后统一归类及最终模型熔炼。
