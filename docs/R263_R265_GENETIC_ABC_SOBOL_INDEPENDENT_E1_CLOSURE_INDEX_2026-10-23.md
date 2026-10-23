# 心理史学原R263–R265：遗传算法、拒绝式ABC、Sobol全局敏感度 — 连续研究E1正式结题与GitHub归档总索引

日期2026-10-23（Asia/Taipei）。原239候选模型目录按原顺序连续研究三项：11-023 Genetic Algorithms（R263/P2）、11-024 Approximate Bayesian Computation（R264/P2）、11-025 Sobol Global Sensitivity（R265/P1）。全部项目先向main提交冻结的预评分协议，再创建源代码/CI，经Python3.11与3.12双版本实际测试和第三来源审核并由机器人永久提交全部原CSV/计算JSON/源SHA256，最后发布单项科研报告、正式有界结题与此总索引。三个项目都只有人工数学E1，不是新增真实人类E2或真实历史E3；R073及PESEN v0.1保持冻结。原R模型全部完成前不开展统一模型归纳或熔炼。

## R263：九人工两名三bit个体一代遗传算法（11-023）

[事前冻结协议](../protocols/R263_GENETIC_ALGORITHMS_9_WORLDS_9216_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整9216原source及运行程序](../research/R263/README.md) · [正式科学报告](../research/R263/R263_SCIENTIFIC_REPORT_2026-10-23.md) · [机器有界科研验收](../research/R263/R263_FINAL_ACCEPTANCE_STATUS.json) · [全三job成功CI run39899578544](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899578544)。

九world每个由双亲各3原bit+交叉flag/切点2bit+定点突变触发2bit，即每world完整2¹⁰=1024原结构、九world**9216全部原source**，每条原质量1/1024。完整源逐项记录父代、交叉突变候选子代、精英或非精英最终两人、原先/最新最佳适应度和增加减少。第一源算法使用三bit组切片/翻转，第二独立算法按64组父本×16套算子事件，用三bit整数mask与XOR独立重建双幸存者**完整条件联合概率分布**，九world逐组全部Fraction一致。精英保留从父0/父1/子0/子1按最大适应度选前两，不可能单代损失原最佳；非精英CROSS_ONEMAX有80改善/80退化原source，MUTATE_ONEMAX有232改善/232退化，CROSS_MUTATE_ONEMAX有242改善/236退化，因变化幅度不同其**平均最佳适应度变化严格0**。ELITE_CROSS_MUTATE_ONEMAX有242改善、0退化、平均改善123/512；ELITE_CROSS_MUTATE_TRAP把000适应度定为4、111为3，平均改善53/128。仅人工单代，不证明长期全局收敛或现实人群生物/历史适应。三job success、Python3.11/3.12各82实际单测共**164通过**；全部原CSV/JSON/SHA由GitHub机器人永久commit[8de31843](https://github.com/edwardsage419/Psychohistory-Research/commit/8de31843bccdf8827dba91a6bd69186b618d12d0)。

## R264：九人工有限拒绝ABC、三先验参数、两bit观测（11-024）

[先行冻结参数和后验识别协议](../protocols/R264_ABC_9_WORLDS_432_THETA_SIMULATION_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [432完整先验/原随机数source及数学程序](../research/R264/README.md) · [正式科学报告](../research/R264/R264_SCIENTIFIC_REPORT_2026-10-23.md) · [机器有界验收](../research/R264/R264_FINAL_ACCEPTANCE_STATUS.json) · [最终成功CI run39899758034](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899758034)。

九world各有θ=0,1,2三个等概率先验参数、模拟Y1/Y2所需两个独立公平2bit随机源，完整3×16=48来源/world、九world**432原source**，每条质量1/48。目标人工观测Y=(1,0)。拒绝ABC按源模拟的三种距离：FULL_HAMMING/COUNT_SUM/FIRST_COMPONENT，分别ε=0,1,2，九world×九设置共**81组完整后验、接受率与总变差**由源模拟拒绝与另一条完全独立Bernoulli四可能结果解析计算逐Fraction一致。FULL_HAMMING ε0完全等于正确全向量Bayes；全部距离ε2，及COUNT/FIRST ε1，都无条件接收并退化回先验。COMPLEMENTARY_GRADIENT与REVERSED_COMPLEMENT在每θ下总数摘要K=Y1+Y2完整分布一致，两world COUNT ε0后验皆(5/14,2/7,5/14)，但完整数据Bayes分别(1/14,2/7,9/14)和(9/14,2/7,1/14)，TV各2/7。即使ε=0也不能弥补摘要已丢失Y1/Y2的身份信息；IID_GRADIENT中count足够则无该误差，必须区分模型依赖的充分性。**仅有限拒绝ABC，未复现Beaumont等2002的局部线性校正和真实遗传数据**。三job全部success，Python3.11/3.12各82真单测共**164通过**；原CSV/JSON/SHA机器人永久main commit[ce269471](https://github.com/edwardsage419/Psychohistory-Research/commit/ce26947160448c00cbeae80fb6c136be53dd3fe0)。

## R265：九人工四个独立二元输入Sobol敏感度（11-025）

[事前冻结全部15子集ANOVA与九world结果协议](../protocols/R265_SOBOL_9_FOUR_BINARY_INPUT_144_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [144全部原输入source与完整程序](../research/R265/README.md) · [正式科学报告](../research/R265/R265_SCIENTIFIC_REPORT_2026-10-23.md) · [机读有界E1资格](../research/R265/R265_FINAL_ACCEPTANCE_STATUS.json) · [最终成功CI run39900027884](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39900027884)。

九world×4个独立公平bit完整16输入配置/world，**144全部原人工source**、每source1/16。Y由九种冻结加权和、异或高阶交互、双/四输入AND门、平移放缩等函数生成。**原source Walsh/Fourier正交系数平方**直接给出全部非空子集方差分量`V_S`；另一独立理论路线按各子集固定输入计算`Var(E[Y|X_S])`，采用Möbius递推恢复同样15个`V_S`，9×15=**135个方差贡献**逐Fraction一致，总和精确等于原输出Var(Y)，四个一阶及总效应亦全部与独立补集条件式一致。PURE_FOUR_PARITY全部一阶0但全部总效应1，唯一四阶子集解释所有方差，揭示只看一阶会遗漏纯交互；AND_FOUR全部15子集指数各1/15，一阶各1/15、总效应各8/15；INTERACTION_PLUS_ADDITIVE一阶X1/X2为0但总效应各1/6。四个输入独立是**必要模型假设**，不能将这些值推广到真实相关心理变量或声称Saltelli 2010采样估计器已复算。三job success、Python3.11/3.12各82真实测试共**164通过**；全部原CSV/JSON/SHA机器人永久main commit[ad9bd248](https://github.com/edwardsage419/Psychohistory-Research/commit/ad9bd248106dfefdb353ae449bb381dd5429df87)。

## 统一验收与范围边界

**三项原R连续正式有界结题：3项、27个人工预评分冻结world、9216+432+144=9792个完整人工原source类型、164+164+164=492次真实Python双版本单测通过、3次最终GitHub Actions run全部completed/success、合计9个作业成功**。各项目都有独立源码、原完整CSV、冻结模型预评分协议、两条不同数学路线、结果JSON、机器SHA256凭证、科学报告和正式有界验收。**9792个结构类型不代表9792个真人/独立社会研究样本，不提供新的人类E2或历史E3外部证据**，不能将小样本穷举的数学一致性当作对不同实验和现实事件的验证。

R073、PESEN v0.1均继续冻结；真实E2=0，真实历史E3=0。原239目录下一项已核实`11-026 Monte Carlo Simulation`（P0，拟R266），其后`11-027 Latin Hypercube Sampling`（P1，拟R267）。遵循用户原顺序**先完成所有原R模型，再统一归纳分类，最后开始熔炼原创心理史学体系**，暂缓个人辅助决策体系具体开发。
