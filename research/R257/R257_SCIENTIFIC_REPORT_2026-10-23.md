# R257 最优化理论：九有理三角约束世界、225完整候选来源、凸KKT唯一全局最优与非凸不充分反例

日期2026-10-23（Asia/Taipei），原239候选目录 `11-017 Optimization Theory`（P1），有界科研资格 `CLOSED_BOUNDED_E1_STRICT_CONVEX_TRIANGLE_KKT_AND_NONCONVEX_COUNTEREXAMPLE`。所有数据来自可显式验证的人工二元变量/有理约束优化，不是现实社会效用估计、政策资源分配或人类实验。新增真人E2=0、真实历史E3=0；R073和PESEN v0.1保持冻结。

## 源文献、数学命题与证据边界

Stephen Boyd 与 Lieven Vandenberghe (2004), [*Convex Optimization*, Cambridge University Press](https://www.cambridge.org/highereducation/books/convex-optimization/17D2FAA54F641A2F62C7CCD01DFA97C4)，[作者原始教学网站](https://stanford.edu/~boyd/cvxbook/)，系统阐述凸优化和拉格朗日对偶/Karush–Kuhn–Tucker条件。本项对一个**有Slater严格内点、正定Hessian=2I**的有理二次函数特例构造和验算最优性证书，同时冻结一个**非凸时KKT不充分**的结构反例。绝不称KKT对所有非凸问题充分，亦不把25点人工格点最小值冒充连续约束域最小值。

[九world、固定225格点原来源和KKT验收的事前冻结协议](../../protocols/R257_OPTIMIZATION_9_TRIANGLE_KKT_WORLDS_225_CANDIDATE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先独立提交 [75b7f963](https://github.com/edwardsage419/Psychohistory-Research/commit/75b7f963eb850c9bc9e573d48877dab5f261a8ab)，再实现代码、CI和结果归档。九world均定义三角域`K_C={(x,y):x≥0,y≥0,x+y≤C}`，C=1或2。前8world统一严格凸平方损失`f=(x-a)²+(y-b)²`；第9world定义非凸`f=−(x−1/2)²+(y−1/2)²`且C=1。

原来源空间为每world 5×5=25有理点`G={0,1/4,1/2,3/4,1}²`，九world合计**225完整人工候选结构类型**、每source固定设计质量1/25。**C=1时25点中只有15点可行、10点不可行**；C=2时25点全可行。这些不可行source也全部完整归档并显式标注，不拿违反约束的低目标值伪装成更优可行解。原source中每行存(x,y)、容量、目标值、梯度、约束松弛、可行位和人工均匀设计质量。这里均匀质量只是完全枚举格点的设计权重，不是人群选择频率或现实试验概率。

## 独立连续投影、原格点搜索和KKT四类约束证书

第一条数学路线枚举25原格点并逐source求精确Fraction目标与梯度，过滤可行点后计算完整离散搜索最佳值及所有同分点，不能独立提供连续全域最优性证明。**独立第二条路线不依赖格点搜索来证明连续最优**，逐个求目标点(a,b)在三角形内部和三个边界面上解析投影：x轴`(clip(a,0,C),0)`、y轴`(0,clip(b,0,C))`、容量斜边`(t,C−t)`其中`t=clip((C+a−b)/2,0,C)`，目标点(a,b)若可行再加入。取有限组**解析边界/内部候选**中的精确最小值，因为正定Hessian及闭凸三角域保证唯一全局最优，且任意边面最小已被完整处理。

连续最优还必须给出可直接验算的拉格朗日乘子`λ,μx,μy`，同时严格满足：原域原始可行性`x,y≥0;x+y≤C`，对偶可行性`λ,μx,μy≥0`，补充松弛`λ(x+y−C)=0;μx x=μy y=0`，以及驻点`2(x−a)+λ−μx=0;2(y−b)+λ−μy=0`。全部八个严格凸world逐项验算无一失败；Slater点`(C/4,C/4)`严格满足全部不等式，KKT证书足以证实全局最优。**仅数值梯度为0不是此处全局最优的全部理由**，约束活跃面和凸性不可省略。

## 九冻结world精确结果

| 人工world | 唯一连续全局最优(x*,y*) | 最优目标值 | 原格点最优与连续差 |
|---|---|---:|---:|
| INTERIOR_OFF_GRID | (3/5,1/5) | 0 | 1/80 |
| BINDING_SUM_BOTH | (1/2,1/2) | 1/8 | 0 |
| LOWER_X_ACTIVE | (0,1/2) | 1/4 | 0 |
| LOWER_Y_ACTIVE | (1/2,0) | 1/4 | 0 |
| VERTEX_ORIGIN | (0,0) | 1/2 | 0 |
| VERTEX_RIGHT | (1,0) | 17/16 | 0 |
| VERTEX_UPPER | (0,1) | 17/16 | 0 |
| CAPACITY_TWO_SLACK | (3/4,3/4) | 0 | 0 |
| NONCONVEX_KKT_NOT_SUFFICIENT | (0,1/2) | −1/4 | 0 |

**网格最优与连续全域最优可严格不同。** INTERIOR_OFF_GRID的精确投影(a,b)=(3/5,1/5)本身严格处于连续C=1可行域内部，连续最优目标恰0，却不属于冻结25点网格。格点(1/2,1/4)目标为`(1/2−3/5)²+(1/4−1/5)²=1/100+1/400=1/80`，所有其他可行格点不更好。两路精确比较证明该格点搜索**存在1/80正目标差**。其他七个严格凸world的解析唯一最优恰好都在冻结格点中，原source网格最佳和连续全域最佳完全相等，差0。即使一个模型的网格搜索与连续最优一致，也须由独立连续证书而非有限枚举来证明。

**约束活跃与影子价格不能混同。** BINDING_SUM_BOTH目标(3/4,3/4)超过容量1，最优是(1/2,1/2)，容量约束乘子`λ=1/2`、两下界乘子0。VERTEX_RIGHT目标(2,1/4)、容量1，最优(1,0)，容量乘子`λ=2`且`μ_y=3/2`。CAPACITY_TWO_SLACK目标(3/4,3/4)、容量2，其最优(3/4,3/4)不接触斜边容量界，容量松弛1/2、λ=0。**同样出现某一非负行动结果，不表示其容量约束一定具有正影子价格**；乘子解释仅适用该已明示的优化模型和单位尺度。

**非凸时KKT驻点不是充分证书。** NONCONVEX_KKT_NOT_SUFFICIENT的Hessian为diag(−2,+2)。候选(1/2,1/2)在容量C=1边界上，梯度(0,0)，所有拉格朗日乘子取0满足原域/对偶/互补/驻点KKT；但它的目标f=0。另一个可行点(0,1/2)目标`−1/4<0`，故驻点不全局最优。这里甚至可**完整解析证明**全域最低−1/4：因为0≤x≤1，`−(x−1/2)²≥−1/4`，而`(y−1/2)²≥0`，因此所有可行f≥−1/4，(0,1/2)恰达到这一界。不能从此例推出对任意非凸问题KKT完全无用，只说明“满足必要条件 ⇒ 全局最优”不成立。

## 真实双版本CI、机器收据与可复现资料

[原生Fraction来源与独立投影/KKT代码](r257_exact_triangle_optimization.py) · [完整225格点原source CSV](R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv) · [九world完整解析结果及四类KKT证书JSON](R257_EXACT_RESULTS.json) · [原CSV/JSON SHA256机器验收凭证](R257_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39897185617](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897185617)总体completed/success、三jobs全部completed/success。Python3.11和3.12实际日志各`Ran 82 tests`、`OK`，合计**164次真实双版本单测通过**。第三独立archive作业逐world核查25个唯一格点、设计质量1/25、15/25可行数、全部可行梯度/目标、八凸world解析最优点和KKT各项、INTERIOR_OFF_GRID格点误差1/80、非凸KKT驻点和真实解析−1/4最优及全部原CSV/JSON SHA256；真实输出`R257_ALL_225_ORIGINAL_OPTIMIZATION_CANDIDATES_AND_STRICT_KKT_CERTIFICATES_VERIFIED`、`R257_ALL_225_ORIGINAL_OPTIMIZATION_CANDIDATES_PERMANENTLY_ARCHIVED`。全部原CSV、完整结果JSON和SHA机器收据已永久GitHub bot提交main [e328edc4](https://github.com/edwardsage419/Psychohistory-Research/commit/e328edc4eff479b4453219e3b9c622f87968e4b8)。

完整原CSV SHA256 `ac201d9b736f223e0a63b4d11d6a9891b4396f822c6a8b6eaba793a95f69cb5d`，结果JSON SHA256 `ab9aefc5626451d1ea2d0419b38d7cfc7abe12f12e891b3904926a8a22f7b87e`。

正式研究资格`CLOSED_BOUNDED_E1_STRICT_CONVEX_TRIANGLE_KKT_AND_NONCONVEX_COUNTEREXAMPLE`，只说明九个已定义人工有理目标与约束域的数学性质，不表明现实社会偏好、政治分配或组织预算优化问题具有同一效用函数/约束。新增真人E2、真实历史E3均0，R073及PESEN v0.1冻结。下一原目录11-018 Optimal Control（R258，P2），继续全部原R研究后分类与熔炼。
