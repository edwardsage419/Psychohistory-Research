# 心理史学 R257–R259：最优化、有限随机最优控制、多目标Pareto — 连续原R模型正式有界E1结题索引

日期2026-10-23（Asia/Taipei）。本索引对应正式原239模型候选目录中的连续三项：`11-017 Optimization Theory`（R257/P1）、`11-018 Optimal Control`（R258/P2）、`11-019 Multi Objective Optimization`（R259/P2）。所有研究均先单独提交并冻结预评分协议，随后开发原生Fraction精确源与第二独立数学验证路线，运行Python3.11/3.12加第三原source审计/机器SHA256永久GitHub bot归档三job，最后发布正式科学报告与有界验收状态。

**只有人工数学E1闭合**：本轮原source均是事前固定枚举的有理方案/初值/外生噪声类型，**不是**真人样本、历史行动/政策案例、外部实验复现或现实效用参数估计。R073与PESEN v0.1保持冻结，新真人E2=0、历史E3=0。用户既定研究顺序继续**先完成原R全部模型→统一归类→最后熔炼和开发原创体系**，个人决策系统暂缓。

## R257（11-017，P1）严格凸三角约束优化及非凸KKT不充分

[事前冻结协议](../protocols/R257_OPTIMIZATION_9_TRIANGLE_KKT_WORLDS_225_CANDIDATE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [全部225原候选source、代码与来源SHA导航](../research/R257/README.md) · [正式科学报告](../research/R257/R257_SCIENTIFIC_REPORT_2026-10-23.md) · [有界科研验收](../research/R257/R257_FINAL_ACCEPTANCE_STATUS.json) · [全部三job成功CI run39897185617](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897185617)。

九人工world，前八world在闭三角约束`x,y≥0,x+y≤C`下以严格凸二次目标`f=(x-a)²+(y-b)²`作投影；第九world Hessian=diag(−2,+2)为非凸明确反例。每world完整5×5=25固定原格点，**225人工源**，包括C=1时不可行10格点（均标注，不当最优可行解），每source设计质量1/25。格点穷举与独立三条边界面/内部连续解析投影两路严格区分，所有八严格凸world的唯一连续全局最优具有正定Hessian、Slater可行点和原始/对偶/互补/驻点四类KKT精确证书。INTERIOR_OFF_GRID连续最优(3/5,1/5)，目标0，但格点搜索最好1/80，不得将离散格点最小值冒充连续最优。非凸world满足全部KKT的驻点(1/2,1/2)成本0却非全局最优，解析实际下界−1/4由(0,1/2)达到，说明非凸KKT必要条件不自动变成充分条件。真实CI3job成功、Python3.11/3.12各82真实测试，**164次通过**，全部原CSV/JSON/SHA永久bot提交[e328edc4](https://github.com/edwardsage419/Psychohistory-Research/commit/e328edc4eff479b4453219e3b9c622f87968e4b8)。

## R258（11-018，P2）三阶段随机反馈最优控制与512合法策略

[事前冻结协议](../protocols/R258_OPTIMAL_CONTROL_9_THREE_STEP_1728_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [1728完整原noise初态来源和原生控制程序](../research/R258/README.md) · [正式科学报告与首次CI失败保存](../research/R258/R258_SCIENTIFIC_REPORT_2026-10-23.md) · [机器科研结题资格](../research/R258/R258_FINAL_ACCEPTANCE_STATUS.json) · [最终成功CI run39897521571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897521571)。

九个人工三步、三状态x∈{0,1,2}、二动作u∈{0,1}、二元随机d∈{0,1}、已冻结随机成本`x²+κu`与终端`τx3²`机制。每world3个设计初态×64个完整六bit公平外生shock，共192人工源，九world**1728完整结构类型**，每source结构权重1/192（同初态条件原bit权重1/64）。先观察x再行动u、最后实现当期d，严格禁止政策获知本期未来实现或全部未来噪声。第一数学路线Bellman自终端倒推并在全原source执行；**第二完全独立数学路线穷举2^(3×3)=512个合法确定性时间—状态Markov反馈策略**，每策略对八条未来噪声二元组合按正确Bernoulli路径权重算期望损失，与Bellman最优和所有原source积分逐world逐初态Fraction精确一致。八种固定开环行动序列均为合法反馈类子集，逐world得`V_feedback≤V_openloop`。在HALF_SHOCK_MEDIUM中x0=1，最佳反馈期望9/2，开环19/4，严格差1/4；x0=2，反馈47/4，开环95/8，差1/8；某些p/κ/τ下同值，不能无条件主张反馈总严格优越。首次[CI run39897405451](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897405451)两个版本模型数学job通过、第三审核将有理CSV文本错误传给Fraction(string,64)导致overall failure；保留失败记录，仅修审核转换，最终[run39897521571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897521571)三job success，Python3.11和3.12各82真实单测，**164次通过**，原CSV/JSON/SHA永久bot提交[50838d37](https://github.com/edwardsage419/Psychohistory-Research/commit/50838d3793de4274794e999fdb539b4801c48c86)。

## R259（11-019，P2）非支撑Pareto vs粗权重网格漏选

[事前冻结协议](../protocols/R259_MULTI_OBJECTIVE_9_FIVE_ACTION_WORLDS_225_WEIGHT_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [全部225决策—权重原source及源码](../research/R259/README.md) · [正式科学报告](../research/R259/R259_SCIENTIFIC_REPORT_2026-10-23.md) · [正式有界科研验收](../research/R259/R259_FINAL_ACCEPTANCE_STATUS.json) · [三job全部成功CI run39897791434](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897791434)。

九个双目标最小化人工世界，每world五离散决策×五固定权重{0,1/4,1/2,3/4,1}，**225完整原人工来源类型**，每source固定1/25设计权重。第一路线完整Pareto支配比较+五权重所有平手最优记录；第二独立解析路线**不凭格点权重推断连续权重是否支持**，对任意方案把全部竞争者的加权差异线性不等式与λ∈[0,1]求闭区间交，精确识别连续支持区间/空集并直接给有理见证。CONCAVE_THREE_UNSUPPORTED五方案全Pareto，却B/C/D在**任何**连续权重下都无法加权最优；ε约束f1≤2、min f2可恢复C=(2,3)。STRICTLY_CONVEX_DISCRETE_FRONT中的B受**真实连续权重区间[5/9,7/11]**支持，但五权重点全未命中；不可把有限格点遗漏误作理论non-supported。目标1成本数值×10保留同标签Pareto集合，但内部平手支持λ=1/11且当λ固定为1/4时，加权最优标签从原E变成A，因此**单位缩放≠固定名义权重具备相同目标权衡**。支配解和相同成本不同标签均留在完整原source内，不凭无标签成本集合恢复方案身份。CI三job success，Python3.11与3.12各82真实测试，**164次通过**，全部原CSV/JSON/SHA机器人永久commit[d7d85147](https://github.com/edwardsage419/Psychohistory-Research/commit/d7d85147b240aa4d83a87efefb1dfbdc2ec0ea44)。

## 本轮统一验收、跨域推断阻断与下一个模型

本轮连续三原目录模型：**3项正式有界E1研究；9×3=27个独立预评分冻结人工world；完整人工原source225+1728+225=2178类型；Python3.11/3.12真实通过测试164+164+164=492次；三条最终GitHub Actions run全部completed/success、共9个job success**。每项均有在开发前先提交的冻结协议、完整原source CSV、原生源程序、独立理论复算、SHA256及机器人永久main归档、报告和机器正式验收。另有R258第一次未完成原source归档的失败run及精确修复，不计入最终成功验收统计。所有原source仅在给定人造世界里有设计概率含义，**不是2178个独立真人/真实历史案例，也没有真实因果识别**。

R073/PESEN v0.1全部冻结，新增真人E2=0/真实历史E3=0。原目录下一条已核为**11-020 Robust Optimization（P2，拟R260）**，下一研究继续按原R进度推进；全部原R完成后统一归纳分类，最后跨模型熔炼。
