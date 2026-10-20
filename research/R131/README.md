# R131：演化博弈论——演化稳定、连续/离散局部稳定与有限种群漂变的四种不同问题

日期：2026-10-20（Asia/Taipei），原239候选目录 **P1 05-007 Evolutionary Game Theory**。

**科学验收状态**：CLOSED_BOUNDED_TAYLOR_JONKER_1978_ORIGINAL_ESS_DYNAMIC_NON_EQUIVALENCE_AND_PROJECT_FINITE_DRIFT。
**有界学习结题**：LEARNING_COMPLETE_BOUNDED_TAYLOR_JONKER_1978_EVOLUTIONARY_ESS_VS_DYNAMICS_AND_FINITE_DRIFT。
**新增真人E2=0，历史外部概率预测E3=0**。此前R129已研究原Maynard Smith–Price1973五策略模拟表，本轮不是重新运行原30,000次模拟，也没有修改冻结R073或PESEN v0.1。R132将专题研究复制子动力学的时间轨迹，R133将专题研究一般ESS，R131的两个原反例不能冒称已完成其余候选。

## 本轮真正直接阅读与核验的第一手源

Peter D. Taylor与Leo B. Jonker（1978），[*Evolutionarily Stable Strategies and Game Dynamics*](https://doi.org/10.1016/0025-5564(78)90077-9)，Mathematical Biosciences 40:145–156。从[第一作者自己发布的Queen's University学术出版物目录](https://sites.google.com/view/peter-taylor/biology/publications)点击1978条目，直接获取并[阅读正式原刊12页PDF](https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a5647942e33b89ab7af1/1697031525653/1978%2Bevolutionarily%2Bstable%2Bstrategies%2Band%2Bgame%2Bdynamics.pdf)。重点实际截图核对印刷p147/PDF2（ESS稀有入侵及Eq1）、p149/PDF4（Eq2连续更新和Eq3离散更新）、p150/PDF5（三策略循环矩阵ESS/连续稳定/离散不稳定）、p151/PDF6（另一个三策略连续稳定但非ESS的α参数）。与此前R129使用1973原作者模拟表不同，这篇1978的主要可复验成果是**定理、定义及具体数学反例**，不是新的人类或动物重复实验。

另核J. Maynard Smith（1974）[《The theory of games and the evolution of animal conflicts》DOI及出版社摘要](https://doi.org/10.1016/0022-5193(74)90110-6)，PubMed PMID4459582；本期没有取得或亲自逐页读完1974原刊，相关ESS通行定义可与[斯坦福哲学百科演化博弈专业条目](https://plato.sydney.edu.au/entries/game-evolutionary/)对照，但不要把二手解析写成1974一手全文已复验。

## 第一手公式和第一组原刊ESS/动态反例

原1978 p147 ESS定义：当前种群策略分布p、任意不同的入侵策略混合q、入侵份额μ，实际见到对手的混合环境 r=(1−μ)p+μq。如果对于**所有足够小的正μ**，原居民p取得的平均收益严格高于入侵者q，才满足原文ESS入侵防御定义。ESS不等于一个普通静态Nash点，也不等于所有更新机制下的动态吸引点。

原p149 Eq2连续时间更新：dot(x_i)=x_i[fitness_i−fitness_mean]；原Eq3离散世代：x_i_next=x_i(1+fitness_i)/(1+fitness_mean)。**离散原论文明确增加1作为出生乘数的基线**；本代码严格验证输入类型、1+fitness_i非负、总体分母严格正，不能将原作者公式偷偷替换为x_i×fitness_i/mean或任意位移。

原p150作者给 A=[[-ε,1,−1], [−1,−ε,1], [1,−1,−ε]]，任意ε>0可构成该思路的regular ESS。本项目事前冻结选ε=1/2以同时满足原离散出生乘数的非负边界，均衡p=(1/3,1/3,1/3)，三种现有纯策略对群体p均得−1/6。任意不同q的入侵收益相对居民之差**严格等于−(μ/2)Σ(q_i−1/3)²**，因此对所有q≠p与μ>0均小于0，严格ESS可用解析公式**普遍证明**而非只测试几个纯突变者。

对该完全相同的p和A，原连续更新的二维切平面Jacobian有trace=−1/3、det=13/36，连续局部严格稳定；原离散更新的Jacobian有trace=8/5、det=**28/25>1**，且特征值为一对复共轭，因此其模平方28/25>1、离散局部不稳定。该实例清楚说明**数学ESS与更新制度的局部吸引稳定性不能直接画等号**。本期只复现源原p150一个ε参数的局部稳定判据，不代替R132后续整个非线性复制子轨迹和时间步长理论。

## 第二组原刊严格反例：连续动态稳定仍不足以说明ESS

原p151另列A(α)=[[2,1,5],[5,α,0],[1,4,3]]；作者给出区间−8<α<8.5有内点、其中α<0为ESS而α<3连续动态严格稳定。项目锁定α=1，解原矩阵中三个纯类型收益相等得到**p=(15,11,9)/35**、每个纯类型对p的平均收益**86/35**。连续Jacobian严格Fraction：
[[-291/245,−60/49],[2013/1225,33/49]]，
迹 **−18/35<0**，行列式 **297/245>0**，因此局部严格稳定。

但是，突变者q=(0,0,1)（**完全选择第三种纯策略**）面对被其占比μ混入后的实际群体，其预期收益相对原p居民**精确高出3μ/35**；仅取μ=1/10即可得正数**3/350**。这一个明确合法的、任意正小μ都获优势的反例，已经足够否证p是ESS；本轮完全不需要凭有限网格枚举来猜测或统计ESS失败。**稳定的群体频率轨迹与没有潜在稀有策略能够入侵，属于不同可检验命题。**

上述两个原矩阵的**二维Jacobian每个有理数元素**都由两套相互独立算法交叉验证：严格手动解析求导，与三次多项式场使用两个有理数步长及Richardson恰好消除h²项得到的**精确**中心差商。p147的原文线性入侵差关系又在每边k/6、和为1的**28个三型格点**、每个3种纯变异者、3个入侵份额、两原矩阵上做**504个**“直接混合环境中各类型所有九对期望收益”与“独立常数＋μ二次型表达式”的Fraction恒等对照。504个是纯数学比较，不是504个受试者或模拟观测。

## 新的有限群体漂变反例明确为项目自设（不归原1978作者）

为了单独识别“策略不利”与“绝不可能扩散”之间的逻辑差别，项目另加**不是Taylor/Jonker1978原公式**的有限个体Moran式出生死亡游戏。N=5人，两种类型A/B，人工设A遇任意类型收益2、B遇任意类型收益1，并按**fitness=1+收益**得到A繁殖率3、B繁殖率2。居民A在此无限群体人工博弈中是严格纯ESS，而B遇到A严格不利。

有限群体模型每轮先根据当前N人出生能力按适应度抽一名复制，再等概率抽一名被替代；全部五人将来最终被仅有1名B变种替换的精确吸收概率仍为**16/211≈7.58%（非零）**，中性两型相同繁殖能力时一个变种概率为1/5=20%。原因是有选择偏差的随机过程仍可能出现概率虽低但连续幸运繁殖事件，**ESS不等于有限样本中其它类型胜出的概率为严格零**。程序对N=2..8的全部中性与反向选择例，以及每个内部人数状态的向上/向下/原位转移概率归一逐项核验。**该例不表示1978作者做过五人实验，也没有测任何现实社会群体的N、个体适应度或突变概率。**

## 真实自动化验收和全部正式文件

[GitHub Actions 39360828291](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39360828291) **completed success；63项真实unittest全部通过、0失败**，另独立再运行1978年两套原刊反例、504项源Eq1解析/直接公式对照与finite Moran模型N5=16/211、中性1/5案例，且由GitHub CI机器人实际生成并提交代码、测试、研究报告三份文件的SHA256机器[正式接受收据](R131_PHASE_A_1978_63_TEST_504_INVASION_SOURCE_FINITE_DRIFT_CI_ACCEPTANCE.json)，已从默认main真实回读。

- [计算前冻结研究协议](../../protocols/R131_TAYLOR_JONKER_1978_STATIC_ESS_DYNAMIC_COUNTEREXAMPLES_AND_FINITE_DRIFT_FREEZE_2026-10-20.md)
- [作者1978一手原刊数学与模型区别的完整科研报告](R131_TAYLOR_JONKER_1978_ORIGINAL_ESS_DYNAMIC_COUNTEREXAMPLES_AND_FINITE_DRIFT_SCIENTIFIC_REPORT_2026-10-20.md)
- [完整Python Fraction源码](r131_taylor_jonker_1978_evolutionary_game_exact.py)
- [63项真正的原刊和独立数学单元测试](test_r131_taylor_jonker_1978_evolutionary_game_exact.py)
- [机器CI运行与三文件SHA256证据](R131_PHASE_A_1978_63_TEST_504_INVASION_SOURCE_FINITE_DRIFT_CI_ACCEPTANCE.json)
- [正式研究科学范围、状态和不能推断的E2/E3](R131_FINAL_ACCEPTANCE_STATUS.json)

仅用Python3.11标准库复算：PYTHONPATH=research/R131 python -m unittest -v research/R131/test_r131_taylor_jonker_1978_evolutionary_game_exact.py。

**当前证据边界**：1978官方原刊数学公式与两个确切的源反例已严格复算、项目额外小有限种群数学漂变说明已执行；没有新的人类/动物原始行为记录、没有进化过程的实际人口抽样、没有任一真人E2预测分数或历史E3，也没有证明ESS一律不动态稳定或离散动力一定不能稳定——每个结论保留其原参数与更新制度。接下来仍按原R系列目录学习R132复制子动力学与R133更一般ESS，其后统一归类、最后熔炼；R073/PESEN v0.1冻结。
