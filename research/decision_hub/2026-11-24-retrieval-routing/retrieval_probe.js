/* Research prototype, Node.js 18+. Run: node retrieval_probe.js. Fixed source excerpts and authored tags; synthetic development cases only. */
const docs=[
  {
    "id": "hard",
    "path": "research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md",
    "blob": "7cb8d5e3631dd17c0650cec06139d88b5bfcc700",
    "method": "c028_interval_feasibility@1.0.0",
    "tags": "底线 上限 下限 超过 不得 超预算 淘汰 能否接受 区间 硬约束",
    "aliases": "不能超|不能超过|最多|底线|上限|负担不起|不准|不得|超预算|至少",
    "raw": "# C028: Interval hard constraints and unknown feasibility (synthetic method card)\n\nDate: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN. Scope: personal decision workbench feasibility gate. Complements C004 hard-constraint example without altering its evidence status.\n\n## Decision question\nWhen a non-negotiable threshold is specified but an option's measured outcome is an interval, when may a workbench exclude, accept, or defer that option? An unknown outcome must not be silently converted to a safe point estimate.\n\n## Inputs and assumptions\nFinite options a; each user-confirmed lower-bound constraint j is x_j(a)>=L_j. For each option and constraint, evidence supports a closed interval [l_j(a),u_j(a)] with l<=u. Bounds are deterministic epistemic bounds, not calibrated probability intervals. Unknown or missing bounds are represented explicitly as UNKNOWN. For upper-bound constraints reverse inequalities. User sets thresholds and units. Each interval and threshold must share units, time horizon, population and scenario. Feasibility across all constraints uses conjunction.\n\n## Three-valued algorithm\nFor a lower-bound constraint: CERTAIN_PASS if l>=L; CERTAIN_FAIL if u<L; POSSIBLE otherwise (l<L<=u). An absent interval is UNKNOWN, distinct from POSSIBLE. For an option: REJECT if any constraint is CERTAIN_FAIL; ACCEPT only if every constraint is CERTAIN_PASS; otherwise UNRESOLVED. Report which constraint caused each status. A strict > threshold requires separate equality handling. No compensatory weighted score may override REJECT. Only ACCEPT options proceed to guaranteed-feasible ranking. UNRESOLVED may be explored in conditional scenarios but never labeled safe.\n\n## Worked synthetic example\nA and B are two hypothetical plans. User-confirmed minimum reserve is L=6 units. A has reserve [5,9], B has [6,7]. A is UNRESOLVED, B ACCEPT. A's nominal midpoint 7 exceeds B's midpoint 6.5, but a midpoint ranking that recommends A as certainly feasible violates the hard constraint gate. If a later valid measurement narrows A to [6.2,7], A becomes ACCEPT; if it narrows A to [4,5.9], A becomes REJECT. These are hypothetical inter"
  },
  {
    "id": "unobserved",
    "path": "research/decision_methods/C028_MANSKI_1990_UNOBSERVED_ALTERNATIVES_BOUNDS_2026-11-20.md",
    "blob": "a221a3a1e95ca3262a3574ab7685890f5f50d6d5",
    "method": null,
    "tags": "未选择 反事实 没选 结果 缺失 观察",
    "aliases": "没选|未选|当初|另一个选择|反事实|没走",
    "raw": "# C028 Manski (1990)：未选择方案的结果缺失与部分识别边界\n\n研究日期：2026-11-20（Asia/Singapore）。状态：PRIMARY_TEXT_BOUNDED / SYNTHETIC_ANALYTIC_EXAMPLE / SCIENTIFIC_ACCEPTANCE_PENDING。服务个人决策系统：决策后复盘、反事实解释、方案优劣声明的证据边界。本档为研究候选，非实现或科学验收。\n\n## 第一手资料和实际范围\n\nCharles F. Manski (1990), “Nonparametric Bounds on Treatment Effects,” American Economic Review 80(2), 319–323。公开原刊扫描：https://ipcid.org/evaluation/outros_temas/Manski%20-%20Nonparametric%20Bounds.pdf 。本轮实际读取原刊第319至323页的机器可读内容，重点核对第319页公式(1)、第320页公式(3)至(6)、第321页二元结果及第323页估计说明。公式(7)网页提取的括号存在排版丢失，故本档算例严格从清晰的公式(4)直接计算，未引用有歧义的排版。原刊扫描的文字提取不等于独立核验排版图像。\n\n作者研究群体中两个方案的潜在结果：每人只能观察实际接受方案的结果，未接受方案结果不可观察；当结果存在已知上下界时，能够给出平均效果的部分识别区间。依赖总体抽样、方案选择比例、已选方案条件均值以及结果界限。额外独立性或选择机制假设可能收窄区间，但需要分别论证。此研究的群体平均边界不得直接视为某个个人的精确反事实。\n\n## 独立合成计算\n\n设结果为0或1，A方案选择比例0.6，B方案选择比例0.4。观察到A组成功率0.7、B组成功率0.5。只假设潜在结果各在[0,1]，不假设随机分配、可忽略混杂或组间可交换。\n\nE[Y(A)] ∈ [0.6×0.7, 0.6×0.7+0.4] = [0.42,0.82]。\nE[Y(B)] ∈ [0.4×0.5, 0.4×0.5+0.6] = [0.20,0.80]。\n故群体平均效果 E[Y(B)−Y(A)] ∈ [0.20−0.82,0.80−0.42] = [−0.62,0.38]。\n\n观察组均值的直接差为0.5−0.7=−0.2。它位于上述区间内，但不能凭此宣称B造成20个百分点的成功率下降。区间跨越零，效果方向无法确认。此为代数教学构造，不是原论文实证复现，也不包含抽样置信区间。\n\n## 可执行候选解释与失效反例\n\n提问：实际选择了哪个方案？哪些结果真实观察到了？未选方案的结果来自何种独立证据？结果量纲是否有可信上下界？不同方案选择者是否具有不同基线条件？\n\n候选解释规则：决策复盘分别展示实际观察、未观察的反事实、外部估计和模型假设。缺少识别条件时，仅输出有证据支持的区间或UNKNOWN；跨零区间禁止自动断言因果方向。若使用观察组均值差，必须注明它是关联性比较。个人单次复盘不得把群体平均界限直接转成该人的个人因果效果。\n\n候选反例：A组60人成功42人，B组40人成功20人。系统若输出“选择B导致成功率降低20个百分点”，应拒绝因果结论，显示观测差−0.20和仅基于有界结果的效果区间[−0.62,0.38]，并说明未选方案结果缺失。\n\n竞争解释：自选择、既有能力差异、环境差异、未测混杂、结果记录缺失、方案定义变化。额外随机分配或条件可交换假设可能缩窄边界，但本轮没有验证。样本比例与均值是合成数值，实际统计不确定性和总体外推尚未评估。\n\n## 去重、执行与交接\n\n本轮检索仓库代码索引关键词“Manski”和“counterfactual bounds”未返回结果；此检索不足以证明全仓语义无重复。近期C023至C027主要覆盖概率预测评分及事后选择偏差，本档增加未观察反事实的因果识别边界。最新规程已读取，开放PR已检查。写入时不得覆盖并发文件，提交后需回读。\n\n原始论文指定内容审阅 COMPLETE；合成代数计算 COMPLETE；候选提问与反例 COMPLETE；全仓语义去重 PARTIAL；原始扫描逐图像核验 PARTIAL；程序测试、独立外部复算、真实数据验证、科学验收 NOT_RUN。\n\n模型轨：候选区间与UNKNOWN解释的适配，不擅自上线。数据轨：潜在结果、选择机制、外部数据可比性与抽样资格。独立验收轨：复核数值，检查跨零区间被误判为因果方向及个人外推反例。无收费API或CI。R073、PESEN v0.1及既有冻结协议保持不变。\n"
  },
  {
    "id": "pareto",
    "path": "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md",
    "blob": "0d04c633a26437ad6017946cd528c4dc68db3d83",
    "method": "pareto@1.0.0",
    "tags": "多目标 取舍 工资 时间 通勤 收入 生活质量 支配",
    "aliases": "工资|薪水|通勤|兼顾|收入|陪家人|两全|取舍",
    "raw": "# C004 动态效用权重、多目标偏序与鲁棒决策：候选测量方法\n\n研究日及检索日期：2026-10-27（Asia/Shanghai）。状态：METHOD_NOTE_BOUNDED。2026-10-27 首项实质增量。只研究候选方法、适用条件与验证清单。无个人健康、财务、关系等敏感资料，无产品开发。\n\n## 一、原始书目与阅读等级\n\n[A] Schwartz, Shalom H. (2012). “An Overview of the Schwartz Theory of Basic Values.” *Online Readings in Psychology and Culture* 2(1), DOI https://doi.org/10.9707/2307-0919.1116 。开放原刊 https://scholarworks.gvsu.edu/orpc/vol2/iss1/11/ ，完整原刊公开副本 https://www.rwlnetwork.org/media/66744/an_overview_of_the_schwartz_theory_of_basic_values.pdf 。直接审读价值相容与冲突、SVS与PVQ量表、价值优先次序的原文段落。原作是价值心理学，以下多目标优化为本项目方法推导。\n[B] Keeney, Ralph L. (1971). “Utility Independence and Preferences for Multiattributed Consequences.” *Operations Research* 19(4):875–893, DOI https://doi.org/10.1287/opre.19.4.875 。出版社原刊摘要 https://pubsonline.informs.org/doi/10.1287/opre.19.4.875 与作者机构书目 https://scholars.duke.edu/publication/1126388 已核，全文未审；可加效用需要检验偏好独立等条件。\n[B] Greco, Salvatore, Vincent Mousseau & Roman Słowiński (2008). “Ordinal Regression Revisited: Multiple Criteria Ranking Using a Set of Additive Value Functions.” *European Journal of Operational Research* 191(2):416–436, DOI https://doi.org/10.1016/j.ejor.2007.08.013 。原刊摘要 https://www.sciencedirect.com/science/article/pii/S0377221707008752 已核。作者2005年开放工作稿 https://www.lamsade.dauphine.fr/CahiersLAMSADE/CahiersLamsade240.pdf 检索到，但直接读取超时，不能标记全文审读。作者提出对所有相容价值函数成立的必要偏好与对至少一个相容函数成立的可能偏好。\n[B] Lahdelma, Risto, Joonas Hokkanen & Pekka Salminen (1998). “SMAA: Stochastic Multiobjective Acceptability Analysis.” *European Journal of Operational Research* 106(1):137–143, DOI https://doi.org/10.1016/S0377-2217(97)00163-X 。作者机构摘要 https://sal.aalto.fi/publications/abstracts/plah98.html 和大学书目 https://research.aalto.fi/en/publications/smaa-stochastic-multiobjective-acceptability-analysis/ 已核；全文未审。该方法在权重空间和输入不确定性下计算接受度，概率化权重空间本身需要正当化。\n[B] Strotz, R. H. (1955). “Myopia and Inconsistency in Dynamic Utility Maximization.” *Review of Economic Studies* 23(3):165–180, DOI https://doi.org/10.2307/2295722 。出版社书目 https://academic.oup.com/restud/article-abstract/23/3/165/1532695 已核，付费全文未读。动态不一致作为后续待审理论线索。\n所有来源均为非中文网站，检索日同上。A为直接原文指定章节，B为原刊摘要及书目。\n\n## 二、候选人生状态测量与主观价值约束\n\n候选维度：身体与现实条件、财务资源、精神体验、社会关系、能力成长、环境与自由度。每维需预先说明"
  },
  {
    "id": "regret",
    "path": "research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md",
    "blob": "a2588cfdd47e547a46a7ee8cde2644caf81198d9",
    "method": "C029@1.0.0",
    "tags": "情景 最坏 后悔 遗憾 最小最大 不知道概率",
    "aliases": "最坏|少吃亏|最少后悔|后悔值|不知道概率|哪种情况",
    "raw": "# C029: Scenario regret without invented probabilities (synthetic method card)\n\nDate: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Scope: personal decision workbench, conditional on user-confirmed hard-constraint feasibility. Independent acceptance NOT_RUN.\n\n## Decision gap and relation to existing work\nC028 handles feasibility with epistemic intervals; C004 discusses robust multiobjective preferences and uncertain weights. This card treats a different downstream question: when the user supplies mutually exclusive scenarios without justified probabilities, how can the workbench compare the cost of choosing a plan that turns out suboptimal? Do not assign probabilities or describe scenario regret as expected loss.\n\n## Inputs, assumptions, algorithm\nInputs: finite feasible options A, finite scenarios S, scenario-specific scalar utility u(a,s) on a single explicitly confirmed comparable scale, with higher better. Each scenario must have a defined time horizon and common utility normalization. User-confirmed hard constraints are evaluated before this method. The scenario list must not be presented as exhaustive unless evidence supports completeness.\n\nFor each scenario s compute M(s)=max over feasible b of u(b,s). Define regret r(a,s)=M(s)-u(a,s), and worst-case regret R(a)=max over s of r(a,s). Candidate minimax-regret choices minimize R(a); ties remain ties. Report the full regret matrix, worst scenario, scenario-wise best option, and every tie. Compare with maximin utility and a user-chosen reference option. Minimax regret is a descriptive decision rule conditional on the supplied scenario set, not a normative requirement or probabilistic forecast.\n\n## Fully worked synthetic case\nTwo equally plausible-looking but **unweighted** scenarios S1 and S2. Utilities: A=(8,2), B=(5,5), C=(2,8). In both scenarios the oracle maximum is 8. Regret vectors are A=(0,6), B=(3,3), C=(6,0). Worst-case regrets: A=6, B=3, C=6. Minimax regret selects B; maximin utility also selects B in this particular case, which does not establish their general equivalence.\n\nIf S1 were learned perfectly before an irrevocable decision, A would be chosen; if S2, C. Relative to commi"
  },
  {
    "id": "interval",
    "path": "research/decision_methods/C030_INTERVAL_BOUNDED_SCENARIO_REGRET_2026-11-20.md",
    "blob": "57301fb2a1dbda8e99510b44d6fcfb2e5f4a191e",
    "method": "C030@1.0.0",
    "tags": "区间 情景 收益范围 后悔值 上下界",
    "aliases": "收益范围|上下界|区间|大约在|之间",
    "raw": "# C030: Interval-bounded scenario regret without invented probabilities\n\nDate: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.\n\n## Decision gap and relationship\nC028 gates hard constraints and C029 ranks options with complete point-valued scenario utilities. This addendum covers scenario utilities available only as defensible intervals. It must not convert interval midpoints into observations or assign scenario probabilities. Only C028 ACCEPT options enter guaranteed-feasible comparison; UNRESOLVED options receive separate conditional analysis.\n\n## Inputs and assumptions\nFinite feasible options A and scenarios S. Each utility cell u(a,s) is known to lie in a closed interval [L(a,s),U(a,s)], L<=U, on one comparable user-confirmed scalar utility scale. All scenarios share a specified horizon. Bounds describe uncertainty, not confidence intervals or calibrated probabilities. At least one feasible joint realization of the intervals must exist. A rectangular uncertainty set (each cell can vary independently within its interval) is needed for *sharp* cellwise bounds below; if dependence is known, the formulas remain conservative bounds when the joint set is a nonempty subset of that rectangle.\n\nFor a realized utility table, regret r(a,s)=max_b u(b,s)-u(a,s) = max(0,max_{b != a}(u(b,s)-u(a,s))). The b != a exclusion is essential because a cannot outperform itself.\n\nFor each a,s define lower regret bound:\nr_low(a,s)=max(0,max_{b != a}(L(b,s)-U(a,s))).\nDefine upper regret bound:\nr_high(a,s)=max(0,max_{b != a}(U(b,s)-L(a,s))).\nFor a singleton option, both bounds are zero. For any consistent realization, r_low <= r <= r_high. Under independent rectangular uncertainty these bounds are sharp for the individual (a,s) cell. For the worst-scenario regret R(a)=max_s r(a,s), the enclosing interval is [max_s r_low(a,s), max_s r_high(a,s)]. Under rectangular independence these endpoints are sharp for each individual option, although different options' extreme values need not occur in the same realization.\n\nA cautious upper-bound rule chooses the option(s) with smallest max_s r_high(a,s), explicitly labeled *minimize worst-case regret"
  },
  {
    "id": "joint",
    "path": "research/decision_methods/C035_JOINT_HARD_CONSTRAINT_FEASIBILITY_COUNTEREXAMPLE_2026-11-23.md",
    "blob": "4f2c077e297a4b2733fa26309c99a510329ec6f4",
    "method": null,
    "tags": "共享预算 联合约束 总额 资源 合计 分配",
    "aliases": "共用|共享|加起来|合计|总额|同一笔|一起花",
    "raw": "# C035: Joint hard-constraint feasibility under coupled evidence (synthetic method card)\n\nDate: 2026-11-23. Scope: personal decision workbench feasibility gate. Status: ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.\n\n## Decision gap and relationship to existing work\nC028 tests each lower or upper bound separately and returns UNRESOLVED when every bound is individually possible but none is certain. This is a sound conservative three-valued gate. A known joint physical or budget identity can sometimes prove that all hard constraints cannot hold together even though each one separately could hold. This card is a narrow extension for a verified joint feasible set; it does not revise C028 or any frozen R result. Distinct from C034, which compares soft utility scores after feasibility filtering, and from causal transport parameter dependence.\n\n## Inputs and method\nGiven user-confirmed hard constraints g_j(z)>=0 and a defensible nonempty joint uncertainty set S of simultaneously possible states z, classify:\nCERTAIN_PASS iff every z in S satisfies every g_j(z)>=0;\nCERTAIN_FAIL iff there exists no z in S satisfying every g_j(z)>=0;\nUNRESOLVED otherwise.\nAn empty S due to contradictory measurements is EVIDENCE_CONFLICT, not CERTAIN_PASS or CERTAIN_FAIL. If S is missing or unsupported, return UNKNOWN. With linear constraints and linear coupling, use a linear-feasibility solver or exact rational elimination. Report the joint identity, evidence, units and a witness state when feasible. These are logical certificates conditional on S, not empirical probabilities.\n\n## Minimal exact counterexample\nTwo nonnegative resources x,y are jointly constrained by x+y=10, x in [4,6], y in [4,6]. The user requires x>=6 and y>=6. Individually, each interval [4,6] is POSSIBLE under C028, so C028 returns UNRESOLVED. Jointly, x>=6 and y>=6 imply x+y>=12, contradicting x+y=10. Thus CERTAIN_FAIL is mathematically established if the joint identity and both requirements are valid. This result can be verified by integer arithmetic; no numerical optimization is needed.\n\nFor a boundary check, replace the total with 12 while retaining x,y in [4,6]: the only joint state is x=y=6, so both requireme"
  },
  {
    "id": "adjust",
    "path": "research/decision_methods/C036_TWO_STAGE_ADJUSTABLE_FEASIBILITY_QUANTIFIER_BOUNDARY_2026-11-23.md",
    "blob": "d2438afcc93f8568cb3a0ef00285fa2f66b34f23",
    "method": null,
    "tags": "事前 事后 调配 观察 两阶段 资源",
    "aliases": "到时候再|看情况再|知道之后|事后调|临时调|先分配",
    "raw": "# C036: Two-stage adjustable feasibility and information timing (synthetic method card)\n\nDate: 2026-11-23. Status: ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.\n\n## Decision gap and de-duplication\nC035 classifies environmental states in a joint uncertainty set. When resource allocations are controlled by the decision maker, its universal-state CERTAIN_PASS test is not a substitute for existence of a feasible action. This card isolates the distinct decision-policy question: what can be committed before a scenario is observed, and what may be adjusted afterwards? It extends the previously documented C035 counterexample without modifying C035, C028, C034 or frozen R results.\n\n## Applicable decisions and inputs\nUse for budgets, time slots or staffing with future scenarios and conditional reassignment. Inputs: scenario set S and evidence; fixed budget B; precommitment action a in admissible set A; scenario-specific post-observation action x_s in X(a,s); per-scenario hard constraints g_j(x_s,s)>=0; maximum allowed reassignment k; observation time, action deadline and authority to reallocate. Record whether k is confirmed or hypothetical.\n\n## Three distinct queries\n(1) Existence for a known scenario: for a given s, does there exist x_s satisfying all constraints?\n(2) Fixed robust decision: does there exist a single a that satisfies constraints for every s?\n(3) Adjustable robust decision: does there exist an a such that for every s, an admissible x_s depending only on information observed by its action time satisfies constraints? A policy cannot depend on an unobserved future scenario. An unsupported scenario set or unknown adjustment authority yields UNKNOWN, not CERTAIN_PASS.\n\n## Exact synthetic example and reproducible arithmetic\nTwo accounts A and B share B=10 units. Scenario 1 requires final allocation (at least 7, at least 3); scenario 2 requires (at least 3, at least 7). With conservation, the only feasible final A allocations are 7 and 3 respectively. Let a be the initial A allocation, and k the maximum number of units transferred in one direction after observing the scenario. The adjustable constraints are |a-7|<=k and |a-3|<=k. Their intersection is none"
  },
  {
    "id": "voi",
    "path": "research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md",
    "blob": "bd494e2e1200a526dcb11d454e423ff9aebccd33",
    "method": null,
    "tags": "信息价值 调查 信号 成本 继续问 先打听",
    "aliases": "打听|调查|查清|再问|花钱了解|先问|获取消息",
    "raw": "# 不完全二元信号的信息价值：方法卡与验收准备\n\n日期：2026-11-20。职责：决策模型学习与接入。状态：合成解析算例 COMPLETE；独立程序复算 NOT_RUN；真实数据验证 NOT_RUN；科学验收 NOT_RUN。\n\n## 去重与目的\n承接既有 `ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md` 中完全信息 EVPI=2 的人工案例，增加有误差的信息信号，回答“花成本调查是否值得”。本卡是同一决策问题内的条件性计算方法，不提出跨问题通用信息价值排序，不修改既有研究结论。\n\n## 输入、假设与计算\n状态 S1、S2 先验概率各 0.5。行动 A 在两状态收益均为 6；B 在 S1 为 10、S2 为 0。效用线性且同单位。信号 +、− 满足 P(+|S1)=P(−|S2)=q，q∈[0.5,1]；信号到达前可自由等待，收到信号后可选择 A 或 B，无额外行为约束。q 为假设，不代表现实准确率。\n\n无信息时选择 A，期望效用 6。贝叶斯更新后 P(S1|+)=q，P(S1|−)=1−q。收到 + 时 B 的条件期望效用为 10q，只有 q>0.6 才严格胜过 A；收到 − 时 A 最优。两信号的边际概率各为 0.5。\n\n`EVSI(q)=max(0,5q−3)`，适用于上述 q 范围和完整设定。q=0.5 或 q=0.6 时 EVSI=0；q=0.8 时 EVSI=1；q=1 时 EVSI=2，等于既有完全信息 EVPI。成本 c 与效用同单位时净值为 `EVSI(q)−c`。q=0.8、c=0.5 时净值 +0.5；q=0.8、c=1.5 时净值 −0.5。成本或效用无法比较时净值 UNKNOWN。\n\n## 基线、反例、失效条件\n简单基线：不调查，直接选 A，效用 6。若信号准确率 q=0.55，调查结果不足以改变行动，EVSI=0。错误实现若将“准确率超过随机”直接判为“调查有正价值”，应失败。若系统把 EVPI=2 当作任意有噪声信号的价值，亦应失败。\n\n公式不适用于非对称混淆矩阵、改变先验、非线性效用、信息延迟、行动约束、调查本身产生效用或损失的情形；这些条件需要重新建模。没有可靠概率、信号质量与成本来源时只输出条件性情景，不提供真实个人事件的定量推荐。\n\n## 验收办法及接入建议\n独立验收轨：检查 q=0.5、0.6、0.8、1 四点及阈值两侧；验证 EVSI≥0、EVSI≤EVPI、随 q 非递减、成本单位不一致时 UNKNOWN；用显式枚举信号和行动独立复算解析值。数据轨：核查先验、信号混淆矩阵、调查成本、时限和数据来源。正式接入由另行授权的版本开发完成，系统须标注先验与准确率为假设或有来源的估计，保留“调查不改变行动”的结果。\n\n来源：Howard, R. A. (1966), Information Value Theory, IEEE Transactions on Systems Science and Cybernetics 2(1), 22–26，经典信息价值框架；本卡数值为独立设计的合成案例，并非该论文实验结果。相关跨问题排序限制见仓库 Abbas 与 Hazen（2024）研究卡。原始全文与推导核验状态 UNKNOWN，本卡仅证明上述有限模型的代数结论。\n\n归档后回读状态待记录。无个人资料，无付费 API，无 CI。R073、PESEN v0.1 与冻结协议保持不变。\n"
  },
  {
    "id": "timing",
    "path": "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md",
    "blob": "b0e07730d57bc096a607f967e124ff7c3e2b0da5",
    "method": "timing_investigation@1.0.0",
    "tags": "调查 截止 期限 等待 完成 时间 延误",
    "aliases": "来不及|截止|到期|最后期限|等消息|调查结束",
    "raw": "# 调查完成时间与真实状态相关时的截止期限决策：联合分布反例\n\n日期：2026-11-21。研究轨：决策模型学习与接入。状态：自构合成反例、解析枚举；独立验收与真实数据验证待执行。\n\n## 决策缺口、去重及适用问题\n接续 VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md 明确列出的“完成时间与状态相关时须使用联合分布”缺口。此前方法卡假定完成时间独立于状态及信号。本卡保持完成时间边际分布、信号准确率、成本和截止期限完全相同，单独改变完成时间与真实状态的依赖关系，检验“先调查还是立即行动”建议是否反转。仅用于有限状态、有限信号、有限完成时间、风险中性和明确可行集。\n\n## 输入、步骤、输出\n状态 S1/S2 各概率 1/2。立即 A 在两状态收益6，立即 B 在 S1 收益10、S2收益0。调查信号 Z∈{+,-}，P(+|S1)=9/10，P(-|S2)=7/10。调查成本 c=1/2。完成时间 D∈{0,1/2}，两点边际概率各1/2。B 仅在 D<1/3 可行，A 始终可行且收益6。假定 Z 与 D 在给定 S 后条件独立；调查完成时同时观察 D 和 Z，再选择行动。调查前不能观察 S。\n\n对每个 (d,z) 计算 J(a,d,z)=Σ_s P(s,d,z)u(a,s,d)。调查净期望收益 = Σ_{d,z} max_{a∈F(d)} J(a,d,z) - c。与立即行动基线 max(6,5)=6 比较。必须使用 P(S,D,Z)=P(S)P(D|S)P(Z|S)，不能将其替换为 P(D)P(S,Z)。\n\n## 精确合成反例\n两种世界均有 P(D=0)=1/2、P(D=1/2)=1/2，且相同 P(S)、P(Z|S)、收益、成本、期限。\n\n世界 E（有利状态较早）：P(D=0|S1)=4/5，P(D=0|S2)=1/5。早到正信号联合质量 P(S1,D=0,+)=9/25，P(S2,D=0,+)=3/100，正信号选 B 相对 A 的增量 10×9/25 - 6×39/100 = 63/50 = 1.26。早到负信号选 A；晚到只能 A。调查净收益 6+63/50-1/2=169/25=6.76；相对立即行动优势 19/25=+0.76。\n\n世界 L（有利状态较晚）：P(D=0|S1)=1/5，P(D=0|S2)=4/5。早到正信号联合质量 P(S1,D=0,+)=9/100，P(S2,D=0,+)=3/25，选 B 相对 A 的增量 9/10 - 6×21/100 = -9/25；早到负信号选 B 的增量也为负。调查后始终选 A，净收益 11/2=5.5；相对立即行动优势 -1/2。\n\n作为独立性对照，P(D=0|S1)=P(D=0|S2)=1/2 时，原卡截止期限结果为 -1/20=-0.05。\n\n因此，只知道完成时间边际分布和调查信号准确率，无法确定调查是否值得进行；相同边际信息可对应 +0.76 或 -0.50 的净优势。\n\n## 基线、假设、失效条件\n简单基线：立即选择 A，期望收益6。故意失配基线：假定 D 与 S 独立，得到 -0.05，可能错判世界 E。条件独立 Z ⟂ D | S 是明确假设；若信号质量也随完成时间变化，须直接提供完整联合分布。状态与时间的相关性须有实际证据；未知时只能列情景，不能根据边际分布宣称优势。成本、截止期限、行动后收益均为虚构，不能推断现实效应。\n\n## 验收与接入交接\n独立验收轨：以 Fraction 枚举两世界各8个 (S,D,Z) 联合事件，核查总概率=1、D 边际均为1/2、信号条件概率保持不变、世界 E 的 19/25、世界 L 的 -1/2、独立对照 -1/20；测试 D=1/3 严格期限边界、条件独立被破坏时拒绝沿用因式分解、无兜底动作时拒绝计算。数据轨：核查现实调查时长是否与结果或潜在状态相关，避免只收集平均时长。开发轨：候选输入为联合概率或有证据的条件概率、完成时间、信号质量、截止期限、成本；展示依赖假设与反转情景。正式接入需所有者单独授权。\n\n来源：本仓库 VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md 的明确未解边界；本卡是自构有限概率反例。未核对外部原始论文，未运行独立程序、CI或付费API，未做真实数据验证或科学验收。R073、PESEN v0.1及既有冻结协议保持原样。\n"
  },
  {
    "id": "sunk",
    "path": "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_PROSPECTIVE_CHOICE_BOUNDARY_2026-11-23.md",
    "blob": "26ca172dc0e4e89961dfe171c7bbcfccef9894ca",
    "method": null,
    "tags": "沉没成本 已付 不可退 未来 继续 放弃",
    "aliases": "已经花|已经付|退不了|拿不回|交了钱|不甘心",
    "raw": "> **科研去重纠错（2026-11-23）**：本档案与 2026-11-21 的 `ARKES_BLUMER_1985_SUNK_COST_FORWARD_DECISION_BOUNDARY_2026-11-21.md` 及 2026-11-22 的 `ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md` 在同一原始论文、沉没成本与未来增量比较、退款与违约金、技能积累、承诺价值、未知概率及最少追问方面实质重复。11月22日记录已审阅 Arkes 与 Blumer 原文第124至128页和第134至138页，证据阅读深度高于本档案的题头与摘要核查。本档案原先“新增候选规则”的归类有误，应改计为**既有方法的补充合成验收材料，新增独立理论方法数为0**。本档案第6项未选择方案不可观察、第8项证照资格、第9项不可逆安全风险可作为候选反例补充，仍未独立执行或验收。保留原文及历史陈述供审计；下方原有“搜索无结果”仅代表当时索引检索返回，不能据此推断仓库无同题研究。此纠错不改变原论文证据、既有冻结协议或科研验收等级。\n\n# 沉没成本与前瞻性选择：候选理论边界（2026-11-23）\n\n## 范围与来源\n研究目的：个人决策系统在用户已投入时间、金钱、声誉时，区分已经无法收回的投入与继续行动的真实增量后果。\n第一手来源：Hal R. Arkes and Catherine Blumer (1985), *The Psychology of Sunk Cost*, Organizational Behavior and Human Decision Processes 35(1), 124–140, DOI 10.1016/0749-5978(85)90049-4。2026-11-23 取得公开原文 PDF https://cognition.aau.at/bg/BA/Arkes%20%26%20Blumer%201985.pdf ，本轮核查原文题头及摘要；正文实验表格和统计推导尚未逐页审计。\n竞争理论来源：Richard Thaler (1980), *Toward a Positive Theory of Consumer Choice*, Journal of Economic Behavior & Organization 1(1), 39–60, DOI 10.1016/0167-2681(80)90051-7。核查原文题头及摘要 https://bear.warrington.ufl.edu/brenner/mar7588/Papers/thaler-jebo1980.pdf 。两者都讨论沉没成本；不能把这两份资料视作独立的现实个人决策效果验证。\n原论文摘要报告：剧院季票现场研究中，初始支付更多的消费者在后续六个月观看更多演出；问卷研究也观察到已投入成本影响继续投入和成功概率判断。该观察不直接识别每个消费者继续观看的真实效用，也不能推断每次继续行动都不理性。\n\n## 可执行候选规则\n触发：用户说「已经花了很多钱/时间，所以必须继续」，且选择是否继续尚未决定。\n先给出初步分析：将不可追回的历史投入单列为已发生事实；对“从现在起继续”与“从现在起停止或转向”比较新增成本、预期收益、真实退出费用、关系义务、学习价值和机会成本。只有会改变排序时追问：「从今天开始继续，还需要投入多少？如果停下，真正会失去什么？」\n允许用户明确确认情感、承诺与声誉价值，不能擅自设为零。未知收益与概率保持未知。过去投入可能是能力积累、合同权利或未来收益的证据，需单独核实其可转移或可兑现部分。\n候选解释：历史投入本身不会自动增加未来项目成功概率；新的能力、信息、网络或合同权利可能改变未来收益，必须单列。\n\n## 合成反例与验收准备（未运行）\n1. 历史已花100，未来继续需40，预期未来可兑现收益20，退出无费：历史100不应进入增量比较。\n2. 同题但退出需支付50的合法违约金：退出费用必须计入，不能机械劝退。\n3. 历史投入获得可转移技能：技能可影响继续及转向收益，不能一概视为损失。\n4. 用户重视守诺与关系：作为用户确认价值处理，不将其自动诊断为偏差。\n5. 项目未来收益概率未知：不能由历史花费估计成功率。\n6. 比较继续与停止时，双方均存在不可观测结果：禁止把未选方案记成真实结果。\n7. 只改历史成本数字，未来现金流、权利、约束与用户确认偏好完全相同：候选计算排序应保持不变。\n8. 时间投入可形成证照资格：应单独评估资格取得概率及剩余成本。\n9. 继续投入存在不可逆安全风险：先执行硬底线过滤。\n10. 用户拒绝补充数据：提供条件化建议，标记缺失项，不制造概率。\n\n## 竞争解释与局限\n可能存在损失厌恶、避免浪费、认知失调、对成功概率的事后合理化、承诺履行与真实转换成本等解释。单个观察无法区分这些机制。历史投入可能与未观测项目质量相关；“忽略沉没成本”不能作为忽略相关信息的理由。\n适用边界：供个人决策的候选问法与解释规则；尚无真实用户效用改善证据。研究与产品上线分离。\n\n## 去重与交接\n写前 main 68df8db210d028224929f32f5f3ce70c"
  }
];
const queries=[
  [
    "我最多只能花三千，哪个超预算就别考虑",
    [
      "hard"
    ]
  ],
  [
    "我每周上班不得超过四十小时",
    [
      "hard"
    ]
  ],
  [
    "当初没选另一份工作，现在能知道结果吗",
    [
      "unobserved"
    ]
  ],
  [
    "我没走另一条路，怎么知道它会不会更好",
    [
      "unobserved"
    ]
  ],
  [
    "一个工资高，一个通勤短，还想陪家人",
    [
      "pareto"
    ]
  ],
  [
    "收入和生活质量怎么取舍",
    [
      "pareto"
    ]
  ],
  [
    "不知道概率，想选最坏情况下少吃亏的",
    [
      "regret"
    ]
  ],
  [
    "各个情景的收益范围都不确定，后悔值怎么算",
    [
      "interval"
    ]
  ],
  [
    "两个培训共用同一笔预算，加起来不能超",
    [
      "joint",
      "hard"
    ]
  ],
  [
    "两个项目各自没超上限，但合计超了总额",
    [
      "joint",
      "hard"
    ]
  ],
  [
    "先分配资源，知道之后可以临时调整",
    [
      "adjust"
    ]
  ],
  [
    "到时候再看情况调配时间",
    [
      "adjust"
    ]
  ],
  [
    "要不要花钱了解一下再决定",
    [
      "voi"
    ]
  ],
  [
    "先问几个人，调查是否值得",
    [
      "voi"
    ]
  ],
  [
    "等消息可能来不及，报名截止前能决定吗",
    [
      "timing",
      "voi"
    ]
  ],
  [
    "调查结束时间可能超过最后期限",
    [
      "timing",
      "voi"
    ]
  ],
  [
    "已经花了钱退不了，要不要继续",
    [
      "sunk"
    ]
  ],
  [
    "交了钱拿不回，不甘心放弃",
    [
      "sunk"
    ]
  ],
  [
    "今天心情很差，为什么会这样",
    []
  ],
  [
    "帮我写一封感谢信",
    []
  ]
];
function experiment(docs,queries){
 const grams=s=>{const t=s.toLowerCase().replace(/[^\p{L}\p{N}]/gu,"");return Array.from({length:Math.max(0,t.length-1)},(_,i)=>t.slice(i,i+2))};
 const freq=s=>{const m={};for(const t of grams(s))m[t]=(m[t]||0)+1;return m};
 const corpus=docs.map(d=>({...d,tf:freq(d.raw),len:grams(d.raw).length}));
 const avg=corpus.reduce((s,d)=>s+d.len,0)/corpus.length;
 const df={};for(const d of corpus)for(const k of Object.keys(d.tf))df[k]=(df[k]||0)+1;
 function score(q,d){let s=0;for(const t of new Set(grams(q))){const f=d.tf[t]||0;if(!f)continue;const idf=Math.log(1+(corpus.length-df[t]+0.5)/(df[t]+0.5));s+=idf*f*2.2/(f+1.2*(.25+.75*d.len/avg))}return s}
 const modes=["raw","bm25","tag"];
 const rows=queries.map(([q,expected])=>({q,expected,...Object.fromEntries(modes.map(mode=>{
 const ranked=corpus.map(d=>{const lex=score(q,d);const matches=(q.match(new RegExp(d.aliases,"g"))||[]).length;const s=mode==="raw"?[...new Set(grams(q))].filter(t=>d.tf[t]).length:mode==="bm25"?lex:matches?100*matches+lex:0;return {id:d.id,score:s}}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));return [mode,ranked.slice(0,3).map(x=>x.id)]}))}));
 const stats=Object.fromEntries(modes.map(m=>{const pos=rows.filter(x=>x.expected.length);const neg=rows.filter(x=>!x.expected.length);return [m,{hit1:pos.filter(x=>x.expected.includes(x[m][0])).length,hit3:pos.filter(x=>x[m].some(i=>x.expected.includes(i))).length,recall3:pos.reduce((s,x)=>s+x[m].filter(i=>x.expected.includes(i)).length,0)/pos.reduce((s,x)=>s+x.expected.length,0),negative_nonempty:neg.filter(x=>x[m].length).length}]}));
 // Separate trusted registry identity, version, source identity and applicability states.
 const registry=new Map(docs.filter(d=>d.method).map(d=>[d.method,d]));
 function route(d,request){if(!d.method||!registry.has(d.method))return "RESEARCH_ONLY";const a=registry.get(d.method);if(a.path!==request.path||a.blob!==request.blob||request.method!==a.method)return "IDENTITY_MISMATCH";if(request.context!=="confirmed"||request.inputs!=="complete"||request.evidence!=="qualified")return "BLOCKED";return "ELIGIBLE_FOR_NATIVE_VALIDATOR"}
 const gates=[];for(const d of docs)for(const context of ["confirmed","unknown"])for(const inputs of ["complete","missing"])for(const evidence of ["qualified","unknown"])for(const version of ["exact","changed"]){const request={path:d.path,blob:d.blob,method:version==="exact"?d.method:(d.method||"candidate")+"@999",context,inputs,evidence};const status=route(d,request);const expect=!d.method?"RESEARCH_ONLY":version==="changed"?"IDENTITY_MISMATCH":context==="confirmed"&&inputs==="complete"&&evidence==="qualified"?"ELIGIBLE_FOR_NATIVE_VALIDATOR":"BLOCKED";if(status!==expect)throw Error("gate mismatch");gates.push({id:d.id,context,inputs,evidence,version,status})}
 const attacks=docs.filter(d=>d.method).flatMap(d=>["path","blob"].map(key=>{const req={path:d.path,blob:d.blob,method:d.method,context:"confirmed",inputs:"complete",evidence:"qualified",[key]:"forged"};const status=route(d,req);if(status!=="IDENTITY_MISMATCH")throw Error("identity mismatch");return {id:d.id,key,status}}));
 return {stats,rows,gate_cases:gates.length+attacks.length,gate_status:gates.reduce((m,x)=>(m[x.status]=(m[x.status]||0)+1,m),{}),identity_attacks:attacks,gate_rows:gates};
}
console.log(JSON.stringify(experiment(docs,queries),null,2));
