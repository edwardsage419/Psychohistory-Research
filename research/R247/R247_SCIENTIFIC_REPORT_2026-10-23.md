# R247 分支过程：九个人工二叉家族世界、2304完整结构来源与独立繁殖假设的有限反例

日期2026-10-23（Asia/Taipei）。原239目录 `11-007 Branching Processes`（P1）。科学资格 `CLOSED_BOUNDED_E1_EXACT_FINITE_GALTON_WATSON_AND_CORRELATED_FAMILY_SHOCKS`。所有结构完全人工，每世界只有一个始祖、三个后继代际、最多8个末代成员；不包含真实家庭、传染病传播链、文化史后裔或群体行为数据，新增真人E2/真实历史E3均0。

## 原著与边界

Galton–Watson过程经典定义见 Berkeley [*Branching Processes: Overview*](https://www.stat.berkeley.edu/users/mathsurv/branchfiles/branch/Overview.html) 及 Cambridge [*Probability, Chapter 14 Branching Processes*](https://www.statslab.cam.ac.uk/~jrn10/Lectures/p.pdf)。当每个活跃父节点的后代数都是独立同分布（IID）K，offspring PGF`f(s)=∑_k p_k s^k`，从单一始祖Z0=1出发，三代群体Z3的完整PGF是`f∘f∘f(s)`，均值为`(E K)^3`。本R只复算明确给定的有限三代概率分布及有界生存率，不把`P(Z3>0)`当作无限未来非灭绝概率，不用任何社会史例子断言“传播会持续”或“群体必然消失”。

[九world与八原bit完整事前冻结协议](../../protocols/R247_BRANCHING_9_WORLDS_2304_COMPLETE_EIGHT_BIT_FAMILY_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于Python代码、CI及原源正式计算独立提交 [2cdd09aa](https://github.com/edwardsage419/Psychohistory-Research/commit/2cdd09aa479b168c1072ce32f1fbea89f39c56e2)，锁定九结构、精确三代观察预测、相关parent反例及测试规则。

## 完整二叉树来源和独立二次验证

每world原外生`(U,B0,B1,B2,B3,B4,B5,B6)`是8独立公平二元变量，完备256种原bit模式，九world**2304条完整结构原来源**、每条1/256。B0关联始祖，B1/B2关联两个潜在第一代父节点，B3…B6关联四个潜在第二代父节点；固定索引树node0 children 1/2，node1 children 3/4，node2 children 5/6。父节点潜在后代数0则无孩子、1只左孩子、2左右孩子均有；末代Z3是所有存活第二代父节点繁殖出的子代总数，最多8。每原source保存U及B0..6、七个潜在父节点oracle offspring K、可见观测群体数量Y0..Y3、真实隐藏H0..H3，以及源概率。不活动潜在父节点的bit仍被完整保留，避免只记录存活者造成机械性的来源选择偏差。

第一路线逐256原bit通过完整潜在二叉树依次激活三代子节点，按来源精确Fraction积分得到全部可见四代人口路径联合、各代期望、P(Zn>0)与Z3完整分布。第二独立路线仅对真实满足每个父节点IID后代的五个world，和统计观察报告层与IID同分布的伪感测world，通过独立offspring PGF多项式复合`f∘f∘f`，不读取bit来源或树生成器，独立重算Z1/2/3所有整数值完整概率及`E Zn=(E K)^n`，逐格与完整来源分布相符。**三个明确相关的offspring世界禁止冒称IID Galton–Watson模型，故不将经典PGF用于其真实过程。**

## 九机制完整三代结果

| 冻结人工world | 潜在单父节点后代均值 | 实际可见E[Z3] | 实际可见P(Z3>0) | 数学含义 |
|---|---:|---:|---:|---|
| IID_FAIR_0_OR_2 | 1 | 1 | 39/128 | IID临界0或2子代，有限灭绝89/128 |
| IID_SUBCRITICAL_0_OR_1 | 1/2 | 1/8 | 1/8 | IID次临界，每代最多留下1 |
| IID_SUPERCRITICAL_1_OR_2 | 3/2 | 27/8 | 1 | IID超临界，因最低生育1而有限必存活 |
| DETERMINISTIC_ONE | 1 | 1 | 1 | 固定每代1，不能将均值等于1误认三代灭绝 |
| DETERMINISTIC_TWO | 2 | 8 | 1 | 固定每代倍增 |
| GLOBAL_SHARED_ENVIRONMENT | 1（单父边际） | 4 | 1/2 | 共同持久环境导致全树相关，IID均值公式不适用 |
| GENERATION_SHARED_SHOCK | 1（单父边际） | 1 | 1/8 | 同代父节点完全共振，有限生存不同于IID临界 |
| SIBLING_ANTICORRELATED_OFFSPRING | 1（单父边际） | 1 | 3/8 | 两个兄弟父节点子代数负相关 |
| STATIC_HIDDEN_TREE_SENSOR_ALIAS | 1（报告层） | 1 | 39/128 | 可见模拟IID，真实隐藏树只有初始始祖 |

**经典IID临界过程的三代灭绝概率。** IID_FAIR_0_OR_2中每活跃父节点都以1/2概率产生0个或2个后代，PGF`f(s)=(1+s²)/2`；完整树源和独立PGF两条路线都得到`P(Z3=0)=f(f(f(0)))=89/128`、三代存活`39/128`、`E Z3=1`。临界“均值1”不等于给定三代必存活，也不等于给定三代必灭绝；另DETERMINISTIC_ONE同样均值1但三代存活1，须留意后代分布形状与可用时间。

**隐含共同环境使单父边际均值误导整体增长。** GLOBAL_SHARED_ENVIRONMENT在U=0时所有潜在父节点K=0，U=1时所有K=2，因此任何单独潜在父节点的offspring边际都是0/2各半、均值1，看似和IID_FAIR完全一致。但全部家族共同受U支配，三代可见人数只有0或8，各1/2；所以`E Z3=4`、P(Z3>0)=1/2，明显不等于将IID机制误用后得到的均值1、生存39/128。**相同的单人后代边际不能替代父节点间独立性**。这种纯人工宏观共振不证明真实历史存在对应共同环境U。

**同样第三代均值，但有限生存率差别巨大。** GENERATION_SHARED_SHOCK每代各自选独立公用冲击，在该代所有潜在父节点上共享0或2子代；三代要全部维持正人口必须三个代际共同冲击全允许繁殖，概率1/8，且若成功末代有8人，因此`E Z3=8×1/8=1`。IID_FAIR的三代均值也为1，但有限生存率39/128更高；两模型均有相同单节点后代边际却不同完整家族概率分布。SIBLING_ANTICORRELATED_OFFSPRING则让潜在第一代左兄弟与右兄弟K互补为0/2或2/0，第二代父独立，在根成功繁殖(1/2)时必恰有两个第二代子女，其任一个繁殖下一代的概率3/4，因此三代生存率`(1/2)(3/4)=3/8`，第三代期望仍1。单单`E Z3=1`完全无法鉴别这些代际相依机制。

**报告树等价不证明真实传播。** IID_FAIR_0_OR_2和STATIC_HIDDEN_TREE_SENSOR_ALIAS对每条完全相同原八bit来源，全部可见Y0…Y3**逐来源完全相同**，联合分布、各代期望与有限生存全部一致。但后者oracle真实隐藏家族`H=(1,0,0,0)`，只有始祖，没有任何真实代际传播。该测量非识别只在报告器允许伪造一整棵家族树的人工情境成立；拥有独立验证的真实父子/传递链时不适用。绝不把此有限反例误称历史文化或疾病传播并不存在。

## 真实GitHub CI与来源审计闭合

[原生Python Fraction源码](r247_exact_finite_branching.py) · [全2304原人工八bit二叉树CSV](R247_ALL_2304_ORIGINAL_BINARY_TREE_FAMILY_SOURCES.csv) · [九world四代完整路径/PGF/生存率JSON](R247_EXACT_RESULTS.json) · [SHA256原来源验收收据](R247_FINAL_MACHINE_ACCEPTANCE.json)。

首次[CI run39892103900](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39892103900)两个模型test作业都success，但第三归档作业**failure**：独立检查脚本读取CSV列为字符串、误传`Fraction(CSV_string,256)`而触发`TypeError: both arguments should be Rational instances`。故首次run不得算结题，不曾把临时原源永久归档。仅在CI审计脚本中显式加`int(...)`转换，模型生成源码、冻结数据结构、概率值和PGF预测均未修改；修复提交[e11912a1](https://github.com/edwardsage419/Psychohistory-Research/commit/e11912a1c6a6cc7c35fd36c9b7599b565b8b661f)，保留首次失败供审阅。

修复后的[正式CI run39892184978](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39892184978)总体completed/success、3项作业均success；Python3.11和3.12真实日志各`Ran 84 tests`、`OK`，共**168次双版本测试通过**。第三来源审计实际核验九world×256完整唯一bit类型、源概率1/256、每源三代人数与可能值上限、全部四代观察概率归一、独立PGF的临界89/128灭绝和39/128存活、三相关世界的期望/生存精确反例、伪感测观察别名及CSV/JSON SHA。日志`R247_ALL_2304_BINARY_BRANCHING_SOURCE_FAMILIES_AND_INDEPENDENT_IID_PGF_VERIFIED`；机器人把全部原CSV/完整结果/机读SHA永久归档main提交[1f9220ca](https://github.com/edwardsage419/Psychohistory-Research/commit/1f9220ca1470aa0cf4376851132c0dae77550032)。

完整原CSV SHA256 `618bfdf1d597eec29d1fb116dc0d1a7c118bcf2efa13a6feccb8e36cbe72859d`，结果JSON SHA256 `6099a127a1ddebc59cf6394663b105fc97ddfbdae4d411b4093c0741aff918bd`。

本R只能按 `CLOSED_BOUNDED_E1_EXACT_FINITE_GALTON_WATSON_AND_CORRELATED_FAMILY_SHOCKS` 有界人工结题。未验证真实人类代际传染、组织影响传播、历史疾病扩散、真实父子依赖或长期灭绝预测；新增真人E2=0、真实历史E3=0。R073/PESEN v0.1保持冻结。下一原239目录11-008 Dynamical Systems Equilibria（拟R248）需从原目录复核。保持全部R之后归纳分类、最后原创熔炼。
