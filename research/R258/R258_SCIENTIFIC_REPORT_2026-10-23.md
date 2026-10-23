# R258 最优控制：九人工三阶段随机有限状态控制世界、1728完整原源与512合法反馈策略穷举

日期2026-10-23（Asia/Taipei）。原239候选目录`11-018 Optimal Control`（P2）；正式科研状态`CLOSED_BOUNDED_E1_FINITE_THREE_STAGE_STOCHASTIC_FEEDBACK_CONTROL`。本项所有来源、行动、误差和价值函数均为人工有理数学结构，不是真实政策干预、真实居民状态或历史社会行为样本；新增真人E2=0、历史E3=0。R073及PESEN v0.1保持冻结。

## 原始学术背景和前评分冻结

Richard Bellman (1957), [*Dynamic Programming*, Princeton University Press，Dover再版](https://store.doverpublications.com/products/9780486317199)，建立跨期最优性原理与递归求解多阶段决策的方法。本研究仅限三时格、三个离散状态、两个二元动作、一个先决策后实现的伯努利扰动。**不复现连续时间Hamiltonian/Pontryagin、连续动作LQR、长期稳态MDP或真实政策随机试验**。

[独立事前冻结九参数世界、全1728外生来源、512合法反馈策略穷举和完整指定数值](../../protocols/R258_OPTIMAL_CONTROL_9_THREE_STEP_1728_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于研究程序提交[62b3cff2](https://github.com/edwardsage419/Psychohistory-Research/commit/62b3cff2023ec7f4d0a35dbb408a6b24c8d6f5ae)。冻结后没有根据结果改变原随机扰动、动作集合、阶段成本或任何比较值。

## 原外生源、控制动作时序和基本递推

三个时点t=0,1,2。状态x∈{0,1,2}，动作u∈{0,1}，人工扰动d∈{0,1}，离散转移为
[
x_{t+1}=min(2,max(0,x_t+d_t-u_t)).
]
每阶段人工损失`c_t=x_t²+κ u_t`，终端损失`τx_3²`。决策者先观察(t,x_t)，**当期d_t及未来噪声尚未实现，决策绝不能读取它们**；动作可以在x=0时预防性取1，若出现到达d=1会在该格抵消。每world三个原初值x0=0,1,2分别与六个独立公平原位组成全部`3×2⁶=192`个完整原结构，九world总**1728原结构source**。每条完整结构设计质量1/192；给定初始状态后64个等概率外生源各具有条件概率1/64。全CSV逐source保存6个原随机bit、每格决策前状态、u、决策后实现的d、新状态、阶段与终端损失及严格有理总成本。设计初态不是从真实用户群体随机抽样。二bit均匀r=0..3以`r<4p`生成每格独立伯努利d，p只取0、1/4、1/2、3/4、1。

## 两条独立数学路线和信息约束

第一路线从终端`V_3(x)=τ x²`倒推Bellman最优方程：
[
V_t(x)=min_{uin{0,1}}igg[x^2+kappa u
+(1-p)V_{t+1}ig(mathrm{clip}(x-u)ig)
+pV_{t+1}ig(mathrm{clip}(x+1-u)ig)igg].
]
对每个t=0,1,2、x=0,1,2，完整保存9个最优反馈动作和每个时间层的价值；相同期望成本时固定选u=0。把这一明示策略在全部3初始值×64原外生bit上实际执行并严格Fraction积分，逐world每初态的路径成本期望恰等于V0(x0)，证明**决策时并未利用未来实际d的值**。

第二独立路线不读取第一递推、不调用源观察产生器和Bellman动作函数，另行穷举`2^(3×3)=512`个确定性、合法、只依(t,x)取动作的Markov反馈策略。对于每个策略与每个初态，列出全部8个可实现三扰动d序列，并用`Π_t p^{d_t}(1-p)^{1-d_t}`精确权重求完整期望成本，取512策略中的全局最小值。对九world每个原初态，这一独立且完整的策略最小值与Bellman V0及64原bit source积分**三条路线精确相同**。这里的512策略包括所有`t∈{0,1,2},x∈{0,1,2}`的事前状态反馈表，并**不包括可以预测当期或未来噪声的非法clairvoyant动作**。第三比较枚举全部`2³=8`个预先固定的开环动作序列，不允许随观察到的中间状态改变；因此开环策略集是反馈策略集的一个子集，理论上`V_feedback≤V_openloop`，全部九world三个初态逐项实测这一定义内不等式。

## 九参数世界的完整冻结结果

| 人工参数world | p,κ,τ | V0(x0=0,1,2) | 最佳开环期望成本(x0=0,1,2) |
|---|---|---|---|
| NO_SHOCK_EXPENSIVE | 0,2,1 | 0, 3, 9 | 0, 3, 9 |
| NO_SHOCK_CHEAP | 0,1/4,1 | 0, 5/4, 11/2 | 0, 5/4, 11/2 |
| HALF_SHOCK_LOW_ACTION | 1/2,1/4,1 | 3/4, 21/8, 77/8 | 3/4, 21/8, 77/8 |
| HALF_SHOCK_MEDIUM | 1/2,1,1 | 5/2, 9/2, 47/4 | 5/2, 19/4, 95/8 |
| HALF_SHOCK_HIGH | 1/2,4,1 | 35/8, 75/8, 16 | 35/8, 75/8, 16 |
| QUARTER_SHOCK_MEDIUM | 1/4,1,1 | 5/4, 13/4, 293/32 | 53/32, 117/32, 603/64 |
| THREEQUARTER_SHOCK_MEDIUM | 3/4,1,1 | 11/4, 45/8, 949/64 | 11/4, 367/64, 959/64 |
| ALWAYS_SHOCK_MEDIUM | 1,1,1 | 3, 7, 16 | 3, 7, 16 |
| HALF_SHOCK_NO_TERMINAL | 1/2,1,0 | 3/2, 7/2, 10 | 3/2, 15/4, 10 |

**反馈优势依赖当前状态与扰动分布，不普遍严格正。** HALF_SHOCK_MEDIUM的反馈表在三个时点均对x=0取u=0、x∈{1,2}取u=1，对x0=1的最优反馈期望成本9/2，相比最佳开环19/4减少1/4；对x0=2的反馈47/4相比开环95/8减少1/8；对x0=0两者都5/2。QUARTER_SHOCK_MEDIUM在x0=0期望成本从最佳开环53/32降至反馈5/4，精确节省13/32。NO_SHOCK、ALWAYS_SHOCK或低控制代价等world中，若某个固定控制序列已足以实现最优，则反馈和开环恰好同值，因此**“反馈严格优于开环”不是不加条件的全局命题**。

**更换终端成本可改变最后期策略。** HALF_SHOCK_NO_TERMINAL设置τ=0，优化的是前三个阶段状态和控制损失，不包含x3²终端处罚。在t=2的全部三个可见状态x=0/1/2中，反馈均选不行动u=0（κ=1），因为扰动后形成的新状态不再产生目标成本。若τ=1，部分t=2状态采取行动。这说明行动的最优性只在**明示的损失定义、阶段长度与时序**内成立；不能因此推断现实制度“不该在末期行动”，更不能与无限时域控制混同。

## CI失败审计、完整来源SHA与正式科研资格

[原生Fraction Bellman/512完整反馈穷举程序](r258_exact_finite_stochastic_control.py) · [九world全部1728完整原source CSV](R258_ALL_1728_ORIGINAL_THREESTEP_CONTROL_SOURCE_ATOMS.csv) · [每world三初态价值、9反馈动作/全部开环比较JSON](R258_EXACT_RESULTS.json) · [原CSV/JSON SHA256完整机读收据](R258_FINAL_MACHINE_ACCEPTANCE.json)。

初次[GitHub Actions run39897405451](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897405451)两个版本的模型科学测试均成功，但第三独立来源档案审核把CSV文本格式的有理路径成本传给`Fraction(string,64)`触发TypeError，故首次overall**failure不能算结题**。仅更改审计中的值转换为`Fraction(string)/64`，保留失败run及修复提交[5204bb6c](https://github.com/edwardsage419/Psychohistory-Research/commit/5204bb6cf9c9c1b6ddf4201de26c99441050f255)，九组模型、真实来源模拟/全部512策略和冻结数值未改。

最终[GitHub Actions run39897521571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897521571)总体completed/success，三个job全部success。Python3.11与3.12真实日志各`Ran 82 tests`、`OK`，合计**164次真实双版本测试通过**。第三独立审计重新核对九world×192完整原source，每world3初始状态各64个唯一六bit、1/192质量，九world全部Bellman V0及开环理论期望、全阶段无前瞻性状态转移、逐source成本、原source条件期望与V0匹配、8开环与512合法反馈证书、SHA256及零新增E2/E3；真实输出`R258_ALL_1728_ORIGINAL_BELLMAN_FEEDBACK_AND_512_LEGAL_POLICIES_VERIFIED`、`R258_ALL_1728_ORIGINAL_CONTROL_SOURCE_ATOMS_PERMANENTLY_ARCHIVED`。完整原CSV、结果JSON、机器SHA已机器人永久归档main提交[50838d37](https://github.com/edwardsage419/Psychohistory-Research/commit/50838d3793de4274794e999fdb539b4801c48c86)。

完整原CSV SHA256 `0af44af9bc97bd2cd8035e8437a58d420ac172cb6657eae969a50968f8be0f54`，结果JSON SHA256 `48951952d07ac2b610c3f884aa6e0c041b5a8ff6cca45154dd0a11a93916208e`。

最终科研资格仅`CLOSED_BOUNDED_E1_FINITE_THREE_STAGE_STOCHASTIC_FEEDBACK_CONTROL`。没有真实人类决策、组织干预、历史政策效果证据，也不代表具有真实可行性约束、价值偏好或干预成本估计。新增真人E2、真实历史E3为0，R073和PESEN v0.1冻结；下一原239候选目录11-019 Multi Objective Optimization（拟R259，P2），继续原R优先顺序。
