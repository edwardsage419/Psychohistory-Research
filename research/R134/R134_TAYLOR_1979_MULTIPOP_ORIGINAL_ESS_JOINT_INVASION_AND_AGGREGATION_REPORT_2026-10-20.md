# R134 科学报告：Taylor 1979 双群体原始ESS判据、联合入侵和聚合信息丢失

日期：2026-10-20。原目录 **P2 / 05-010 Multi Population Evolutionary Games**。状态：**有界科研结题，远端GitHub Actions两种Python环境实际完成全部测试。**

## 一手文献与审计范围

Peter D. Taylor (1979), *Evolutionarily Stable Strategies with Two Types of Player*, *Journal of Applied Probability* 16(1):76–83。原刊稳定引用 https://doi.org/10.2307/3213376，作者本人学术发表列表 https://sites.google.com/view/peter-taylor/biology/publications 中1979条目91的[原1979期刊PDF](https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a06fa3fe7456d63dd68d/1697030256664/1979%2Bevolutionarily%2Bstable%2Bstrategies%2Bwith%2Btwo%2Btypes%2Bof%2Bplayer.pdf)。**直接查看原始刊印p77（PDF索引2），p78（索引3），p79（索引4）**，确认原式(1)两群体同时稀有入侵、原式(2)(3)一阶/二阶收益条件、原式(4)跨类型块矩阵严格二次型以及原式(5)分群复制子方程。p79则核阅原作者另有**非线性**家长照料时间案例，其中原式(6)含等待时间依赖，**本期没有计算复现这套非线性家长案例**。论文直接研究理论博弈，不能当动物实际采样资料。

源1979对两类型 I、J 设适应度 F_i=(Ap+Bq)_i 和 G_j=(Cp+Dq)_j。A,D分别刻画同类依赖，B,C为跨类作用；两个群体各有独立策略分布p、q。原Eq5的纯策略频率连续更新：

dp_i/dt=p_i[F_i−pᵀF]，dq_j/dt=q_j[G_j−qᵀG]。

对于居民(p,q)与任意变化(r,s)的变异小群体，以共同稀有份额 ε 入侵，源Eq1的居民总适应度优势D(ε)等于 D0−εQ，其中

D0=(p−r)ᵀ(Ap+Bq)+(q−s)ᵀ(Cp+Dq)

Q=(r−p)ᵀ[A(r−p)+B(s−q)]+(s−q)ᵀ[C(r−p)+D(s−q)]。

一阶差D0>0或一阶平局D0=0且Q<0足以抵抗**指定**变异者。对所有(r,s)都要求成立才是原式ESS。项目代码直接计算源Eq1另一条路线，与展开式完全独立执行。

## 人工双群体联合失稳反例

所有矩阵与数值均为项目自行指定，**不是1979原作者家长照料资料**：

A=D=[[0,1],[1,0]]，B=C=[[2,0],[0,2]]；居民 p=q=(1/2,1/2)。各自保持另一群体分布不变时，任意单群体变异的二次型Q严格为 −2t²<0 或 −2s²<0，故原Eq1全方向单群体分别严格抗入侵。选双群体共同变异 r=s=(3/4,1/4)，D0=0、Q=1/4，D(ε)=−ε/4，所以任意正ε使居民落败。单群体变异同幅度Q=−1/8。

在完全相同的原Eq5动力学下，两人口第一策略份额(x,y)的局部Jacob矩阵为 [[−1/2,1],[1,−1/2]]，特征值精确 **1/2和−3/2**。若另一个人口被人为固定，各自一阶本地系数−1/2；但让两个群体同时响应时，一方向发散、一方向收敛，构成鞍点。此数学反例不同于R133单一人口三策略混合变异问题，也不证明任意多人口都不稳定。

## 人工纯跨群体零和周期与聚合不可辨识

设置源一般线性模型的A=D=0、B=[[1,-1],[-1,1]]、C=−Bᵀ。原Eq5化为两条一维耦合方程

dx/dt=2x(1−x)(2y−1)，dy/dt=−2y(1−y)(2x−1)。

在正内部，**H=x(1−x)y(1−y)为严格理论不变量**；对原场求导后两项解析恰好相消，程序全部有理点Fraction也精确为0。内部中心(x,y)=(1/2,1/2)，Jacobian [[0,1],[-1,0]]具有虚特征值±i，不能按吸引中心解释为稳定收敛。严格正H且位于内部的非临界等值线为守恒闭轨道；数学模型无噪声、无迁移或突变。

压缩观测 z=(x+y)/2 后，三个具有**同一 z=1/2**的初始状态分别为：

| (x,y) | H | dz/dt |
|---|---|---|
| (1/5,4/5) | 16/625 | +24/125 |
| (4/5,1/5) | 16/625 | −24/125 |
| (1/2,1/2) | 1/16 | 0 |

因此连**瞬时变化方向**都无法从单独z推断。这是固定模型与两群体的严格反例；不能在缺乏人口比例、不同类型行动语义、群体规模权重的情形下无条件推广任何现实群体。

## 有界枚举、独立检验及数值局限

严格数据链：从源77页先独立计算两个受扰动群体的实际适应度差D(ε)，另一份程序在固定居民状态直接计算线性项D0和二次型Q，二者独立核验。事前冻结的**81个自造矩阵配置**来自把上述self/cross四块各乘−1、0、1共3^4种；每组3×3组居民、4×4组变异者和3个入侵比例，共**34,992个源原式与独立展开结果逐条完全有理数相等**。还验证不同纯策略数量的2×3一般矩阵，以及源Eq5与不用通用矩阵程序的一维化简方程的多格点一致。

另外固定同一末期t=12、初始(x,y)=(0.2,0.8)的RK4数值计算如下。原连续理论H始终=16/625=0.0256，浮点输出与真不变量之差为：

| RK4网格数 | H数值减理论 |
|---:|---:|
|40|+7.380178163440138×10⁻⁶|
|80|+2.541428377189625×10⁻⁷|
|160|+9.260974990349391×10⁻⁹|
|320|+3.707657063312109×10⁻¹⁰|

此错误随步长减少而下降，不代表RK4是几何严格守恒方法，更不是1979原作者编写的原模拟软件。原论文的家长照料非线性表达、实际动物生活史、群体总量变化、个体异质性、参数现实校准均未复现。无真人/动物逐行E2预测及历史E3。

## 程序与研究归档

- 事前协议：[`protocols/R134_TAYLOR_1979_MULTIPOP_ESS_REPLICATOR_EXACT_PRESCORE_FREEZE_2026-10-20.md`](../../protocols/R134_TAYLOR_1979_MULTIPOP_ESS_REPLICATOR_EXACT_PRESCORE_FREEZE_2026-10-20.md)。
- 完整Python标准库独立源码及45项真正单测：[ZIP](R134_Taylor1979_source_and_45_tests.zip)。
- 机器可读固定结果：[`R134_PHASE_A_MATHEMATICAL_RESULTS.json`](R134_PHASE_A_MATHEMATICAL_RESULTS.json)。
- 研究结果与严格E2/E3边界：[`R134_FINAL_ACCEPTANCE_STATUS.json`](R134_FINAL_ACCEPTANCE_STATUS.json)。

代码直接调用：`python -m unittest discover -s . -p 'test_r134_taylor1979_two_population_exact.py' -v` 和 `python r134_taylor1979_two_population_exact.py`。

所有计算的科学证据资格限于真实阅读1979作者一手原式及自行构造理论反例。不会修改R073/PESEN v0.1，完整R系列学完后再归类和熔炼。

## 完成后的真实远端机器验收

[GitHub Actions 39371915556](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39371915556) 对原提交4bfcfb17b58536f508098e59ca9d2dd4f0a6ffd6执行完毕，conclusion success。job 118461452739（Python 3.12）与118461453142（Python 3.11）各实际运行**45项unittest全部通过，0失败，共90次独立执行**，源日志分别记录Ran 45 tests in 5.153s和6.972s。每一job均在执行前严格校验ZIP SHA256=302b05c9a6ffebe69063eabedb949ca6ef91ef17eb4c71d1b2a1f42c02d4e64b、项目源码SHA256=ddf3cca2a168641344b405a05212af46a6bce5c30f5badae766874cd9896e434、单元测试SHA256=c72f68d34ce03e189ba814829f783c421e0e97e5961fa408f65d373386fce5dd；两个job均再打印完整81组/34,992精确复算结果。详细结构化收据保存在[R134_PHASE_A_VERIFIED_45_TEST_34992_EXACT_CI_RECEIPT.json](R134_PHASE_A_VERIFIED_45_TEST_34992_EXACT_CI_RECEIPT.json)。科研证据仍然只有原论文理论重构与人工数学实验，无新增真人E2与历史E3。
