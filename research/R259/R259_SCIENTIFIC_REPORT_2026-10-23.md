# R259 多目标优化：九人工有限方案世界、225完整原source与帕累托有效但不受加权支持的精确区分

日期2026-10-23（Asia/Taipei）；原239目录 `11-019 Multi Objective Optimization`（P2）。正式有界科研资格`CLOSED_BOUNDED_E1_DISCRETE_BIOBJECTIVE_PARETO_AND_WEIGHT_SUPPORT`。本研究全为九个已明示离散可行方案成本集的严格代数，**不是现实人类社会价值、制度多元偏好或真实经济成本的估计**。新真人E2/历史E3均0，R073与PESEN v0.1保持冻结。

## 一手文献与关键科学界限

Kaisa Miettinen, [*Nonlinear Multiobjective Optimization*, Springer](https://doi.org/10.1007/978-1-4615-5563-6)（1998），系统介绍多目标Pareto最优与加权标量化、约束法等。研究还参考数学优化研究中连续/离散可行集的“非支撑非支配解”术语，说明线性加权目标不保证能找到非凸部分的全部Pareto点。**本项的完整可行集仅每个world的5个独立方案，并非从无限或连续社会政策集抽样，无法证成现实Pareto前沿的曲率或制度政策偏好。**所有源独立先评分冻结：[九world全部双目标成本、五固定权重、225原source及完整解析支持区间协议](../../protocols/R259_MULTI_OBJECTIVE_9_FIVE_ACTION_WORLDS_225_WEIGHT_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，独立commit [e40857bc](https://github.com/edwardsage419/Psychohistory-Research/commit/e40857bc7fe4ea2040791042cbe24f3e902c9ba2)。

## 原source、Pareto偏序与连续权重法分离

每world冻结决策集合`D={A,B,C,D,E}`，每方案有明确两项人工有理成本`(f1,f2)`需要同时尽可能减小。冻结五个离散标量化权重`λ={0,1/4,1/2,3/4,1}`，综合成本`L_λ(d)=λf1(d)+(1−λ)f2(d)`。完整5方案×5权重=每world**25完整人工原结构source**，九world合计**225条原来源**，每个source设计质量1/25，非现实人群决策的概率模型。每条CSV保留两个原成本、权重、加权目标值、Pareto是否有效、是否某连续权重可支持和是否本冻结权重下取得**含全部平手的最优**。

原路线对每world的五个方案两两比较偏序：若方案j在两个目标都不高于i、至少一项严格低，则j支配i；没有其他方案支配才标记Pareto有效。**成本向量相同的不同方案标签不会互相严格支配**；也不能把相同的成本多重集合误认为相同标签的干预方案。针对所有冻结五权重点，从全部五方案真实加权值取最小，保存所有平手最优而非任意选一个可能隐藏内部Pareto方案的破平手记录。

**独立第二路线不依赖上述五个权重点对连续支持性下结论**。对任意方案i与其他四个j构造完全有理的一维半空间：
[
[(f_{1i}-f_{1j})-(f_{2i}-f_{2j})]lambda +(f_{2i}-f_{2j})le0.
]
将全部四个条件与`0≤λ≤1`精确区间求交，得到方案i在全部**连续允许权重**中可获全局最小加权成本的闭区间，可能为单点或空。对于每个非空区间，另取有理中点或singleton作为精确权重见证，对全部五方案重新算加权得分，确认确实最小。这既避免把“被五个格点漏选”误标成“无连续权重支持”，也避免把“只有有限格点支持”当作连续Pareto理论的完整验证。本项报告的支持允许端点λ=0/1；严格正权重与端点零权重的一般Pareto充分性需要另外区分，本冻结九机制被格点选中方案都是Pareto。

## 九模型完整集合和最重要反例

| 冻结world | Pareto有效方案标签 | 任何连续权重均不能支持的Pareto标签 | 连续可支持、但五个冻结权重全漏掉的方案 |
|---|---|---|---|
| LINEAR_FIVE_ALL_SUPPORTED | A,B,C,D,E | 无 | 无 |
| CONCAVE_THREE_UNSUPPORTED | A,B,C,D,E | B,C,D | 无 |
| DOMINATED_EXTRAS | A,C,E | 无 | 无 |
| OBJECTIVE1_MULTIPLY10 | A,B,C,D,E | 无 | B,C,D |
| DUPLICATE_TIE | A,B,C,D | 无 | 无 |
| STRICTLY_CONVEX_DISCRETE_FRONT | A,B,C,D,E | 无 | B |
| OBJECTIVE2_MULTIPLY10 | A,B,C,D,E | 无 | B,C,D |
| REVERSE_LABELS | A,B,C,D,E | 无 | 无 |
| LINEAR_COST2_STEEPER | A,B,C,D,E | 无 | B,C,D |

**真正的非支撑Pareto点：** CONCAVE_THREE_UNSUPPORTED将五个人工方案设置为A=(0,4)、B=(1,7/2)、C=(2,3)、D=(3,2)、E=(4,0)。两成本彼此权衡，任一方案都没有其他方案同时在两个目标上不高，故全五个都是Pareto有效。但这五点的中间B,C,D位于A/E直线下凸包边界的**上方**；对任一线性权重λ∈[0,1]都不可能比A/E更优，完整有理不等式交区均空，**五点Pareto有效不代表五点均可由加权求和选择**。对于明确不同的ε约束模型`min f2 subject to f1≤2`，可选A/B/C，其中f2分别4、7/2、3，严格选C=(2,3)；因此C虽加权非支撑，仍可通过ε约束方法找到。并不是加权优化器精度不足，而是标量化可表达方案范围本身的结构性差别。

**有限权重网格漏掉数学上确实可支持的方案：** STRICTLY_CONVEX_DISCRETE_FRONT五成本对为A=(0,4)、B=(1,9/4)、C=(2,1)、D=(3,1/4)、E=(4,0)，五点全部Pareto且连续权重都支持。解析区间对B是**[5/9,7/11]**，其内部每个λ都令B拥有适宜加权优势或端点平手，但冻结五点权重0、1/4、1/2、3/4、1都不在区间内，故完整有限网格遗漏B；λ=1/4选D、λ=1/2选C、λ=3/4选A。**“五点网格没见过B”与“无任何权重支持B”是两种完全不同的可检验命题**。本研究将连续支持区间单独证明，且不是依赖增加样本网格密度碰碰运气。

**目标单位变换改变名义权重的含义：** LINEAR_FIVE_ALL_SUPPORTED中五成本点(0,4),(1,3),(2,2),(3,1),(4,0)都有Pareto有效性，且λ=1/2五者完全平手。若仅将第一个目标的数值×10，仍在相同方案标签上Pareto集合完全不变，但令内部B/C/D受支持的连续唯一权重变为λ=1/11；冻结λ=1/4原世界选E，新的量纲世界却选A。若仅将第二目标×10，内部支持权重变为λ=10/11，同样未被五点网格命中。LINEAR_COST2_STEEPER中相应连续共同支持权重为λ=2/3，网格未命中。**正比例改变目标单位可以保留Pareto偏序，却改变给定数值λ所表达的目标取舍**。因此不应在尚未定义真实量纲、偏好与权重语义时使用“同一个λ”声称做了公平的政策比较。

**支配和相同成本标签是不同类型的失识别：** DOMINATED_EXTRAS中B=(1,5)被A=(0,4)支配，D=(5,1)被E=(4,0)支配，只有A/C/E有效；DUPLICATE_TIE中A、B目标完全相同(0,4)，两个不同标签在完整方案偏序中都不被严格支配，必须保留而不能把重复成本点自动删掉后宣称只剩一个干预方案。REVERSE_LABELS与LINEAR_FIVE_ALL_SUPPORTED拥有相同**五成本的多重集合**，但决定方案标签的赋值颠倒，因此若仅观察无标签目标成本集合，不能恢复真实方案身份。这只是明示人工标签非唯一，不是现实干预混淆的实证主张。

## 全部CI、SHA来源与科研结题资格

[原生Python Fraction Pareto与连续权重不等式半区间程序](r259_exact_multiobjective_pareto.py) · [九world完整225原方案/权重结构CSV](R259_ALL_225_ORIGINAL_DECISION_WEIGHT_SOURCE_ATOMS.csv) · [九world完整Pareto标签、连续支持区间、五权重全平手/ε约束JSON](R259_EXACT_RESULTS.json) · [原CSV/JSON SHA256机读凭证](R259_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39897791434](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897791434)总体completed/success、三个job全部success；Python3.11与3.12实际日志各`Ran 82 tests`、`OK`，**164次真实双版本单测通过**。第三独立source审计重建九world25个唯一方案×权重类型、每source1/25、所有格点加权值和包含平手的最优方案、原始双目标逐对Pareto偏序、**不调用五权重网格选择的连续λ区间独立解析求交**、CONCAVE三项真实unsupported与ε约束C、凸离散front的B区间[5/9,7/11]和格点遗漏、目标变换的帕累托不变性及λ=1/4决策反转、源CSV/JSON SHA256。实际日志`R259_ALL_225_ORIGINAL_PARETO_DECISION_WEIGHT_AND_CONTINUOUS_SUPPORT_WITNESSES_VERIFIED`、`R259_ALL_225_ORIGINAL_PARETO_SOURCES_PERMANENTLY_ARCHIVED`。完整原source、结果JSON及SHA机器凭证已机器人永久提交main [d7d85147](https://github.com/edwardsage419/Psychohistory-Research/commit/d7d85147b240aa4d83a87efefb1dfbdc2ec0ea44)。

原CSV SHA256 `a2d2547a067f042534424da2f7249a25686878458098dc617fc93efbca26b8b9`，结果JSON SHA256 `7dfaacad548278101836fb5db7624f2e872d147bfb9cea575d908ea9ad0d202f`。

本项科研资格`CLOSED_BOUNDED_E1_DISCRETE_BIOBJECTIVE_PARETO_AND_WEIGHT_SUPPORT`，未观察任何真实人类偏好/经济政策结果/历史决策，也不估计外部客观目标函数。新增真人E2与真实历史E3均0，R073/PESEN v0.1冻结。下一原目录`11-020 Robust Optimization`（拟R260，P2），仍遵守全部原R完成后再统一分类和模型熔炼。
