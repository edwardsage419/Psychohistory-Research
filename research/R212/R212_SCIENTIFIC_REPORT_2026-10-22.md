# R212 因果有向无环图（09-003）：六个人工SCM、44条完整外生来源、观察等价与干预差异

日期2026-10-22（Asia/Taipei）。原239目录真实编号 **09-003 Causal Directed Acyclic Graph（P0）**；正式科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_DAGS**。此处全部因果图与结构方程为事前固定的人工数学模型，不含任何真实真人E2或历史E3证据。

## 原始方法与冻结范围

Judea Pearl (1995), [Causal diagrams for empirical research](https://doi.org/10.1093/biomet/82.4.669), *Biometrika* 82(4):669–688，提供利用图结构与额外因果假设审阅观察关联、调整策略及因果可识别性的框架。本项另参考Pearl (2009), *Causality: Models, Reasoning, and Inference*, 2nd ed. Cambridge University Press。本项仅在六种固定≤4节点的人工DAG上做**精确有理数SCM外生来源枚举、两个do(T)干预、d-separation简单路径与条件概率审计**；未复现原作者的完整证明、一般DAG完整性算法、真实论文数据或任何现实因果机制。

[事前冻结的六模型、完整外生来源及88干预结局协议](../../protocols/R212_DAG_6_SCM_WORLDS_44_ORIGINAL_EXOGENOUS_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，提交[7dac2da5](https://github.com/edwardsage419/Psychohistory-Research/commit/7dac2da52bc40ad837280440a945e8d4d6e97fa6)，先于代码、CI与评分，不依结果改变图/方程、外生生成概率或因果比较目标。

## 人工来源：六DAG、44条完整独立外生原来源

二元处理T、二元结果Y；额外二元变量按各图固定。有独立Bernoulli(1/2)根变量及独立以四等概率槽j∈{0,1,2,3}生成的N=1{j=0}，使N发生概率1/4。CONFOUND、DIRECT、COMBINED、REVERSE_CAUSAL、MEDIATOR各**8条等概率真外生来源**，COLLIDER有**4条等概率真外生来源**，共**44条原外生来源**。每一来源记录完整人工观察变量、原外生变量、两种**同一外生状态下**执行`do(T=0)`及`do(T=1)`后的全图变量值和相应Y。全来源44×2=**88条同源反事实干预结局**，并不等于88次现实独立实验。

六固定因果图与结构方程：
* CONFOUND：`C→T,C→Y; T=C xor N, Y=C`。只有共同原因，T对Y无真实因果效应。
* DIRECT：`C→T,T→Y; T=C xor N, Y=T`。真实T→Y完全直接效应1。
* COMBINED：`C→T,C→Y,T→Y; T=C xor N, Y=T OR C`。观察差与真总干预效应不同。
* REVERSE_CAUSAL：`T→Y; T∼Bern(1/2), Y=T xor N`。只有直接因果箭头T→Y，完整二维观察(T,Y)分布却与CONFOUND相同。
* COLLIDER：`T→K←U→Y; T,U独立Bern(1/2), K=T OR U, Y=U`。在K=1分层选择时，打开不存在的T与U/Y关联路径。
* MEDIATOR：`T→M→Y; T∼Bern(1/2), M=T xor N, Y=M`。因果总效应完全通过处理后M传递，错误以M作后门条件会损失总效应。

外生来源每世界概率完整和为1，绝不把概率平均当作真实社会人口抽样概率。每条原数据有实际观察结果及两个同源干预真值；只有人工oracle能同时观察该同源反事实，实际现实数据没有这种权限。

## 六个世界的观察与干预结果

在每世界严格计算`E[Y|T=1]−E[Y|T=0]`及`E[Y|do(T=1)]−E[Y|do(T=0)]`。do效应采用两套Fraction途径独立核验：其一每条相同外生原来源上的结果差取平均，其二两个do干预分布的Y平均先分别积分再相减，两者全部六世界逐Fraction严格一致。

|人工SCM|观察差|真do总效应|附加固定审计|
|---|---:|---:|---|
|CONFOUND|1/2|**0**|观测预处理C的后门调整得0|
|DIRECT|1|**1**|预处理C调整仍为1|
|COMBINED|3/4|**1/2**|预处理C后门调整得1/2|
|REVERSE_CAUSAL|1/2|**1/2**|与CONFOUND观察(T,Y)四格概率完全一致|
|COLLIDER|0|**0**|只在K=1分层，条件观察差变−1/2|
|MEDIATOR|1/2|**1/2**|错误控制处理后M，条件化结果为0|

完整六个图的边列表、`(T,Y)`四格观察概率、do0/do1平均和每个调整步骤的分母支持信息见[主结果JSON](R212_EXACT_RESULTS.json)及[44条全外生来源CSV](R212_ALL_44_ORIGINAL_SCM_EXOGENOUS_SOURCES.csv)。

### 核心反例1：相同`P(T,Y)`，不同`P(Y|do(T))`

CONFOUND与REVERSE_CAUSAL在只观察T和Y时完全具有同一个人工二元联合分布：

|观察T,Y组合|实际概率，两模型逐Fraction一致|
|---|---:|
|T=0,Y=0|3/8|
|T=0,Y=1|1/8|
|T=1,Y=0|1/8|
|T=1,Y=1|3/8|

所以两世界观察差都为1/2，但在CONFOUND因果图中T只是共同原因C的结果，`do(T=1)`与`do(T=0)`都使Y总均值1/2，因果效应**0**；REVERSE_CAUSAL中Y受到T直接影响，do0平均1/4、do1平均3/4，真效应**1/2**。两个观察联合分布完全相同，**仅根据T,Y四格数据的观测相关不能识别T→Y的因果效果**。如果研究者额外观察到前一图的C并满足相应后门条件，信息权限改变；本研究**没有声称包含额外C的整个观察变量联合分布仍相同**。

### 核心反例2：已知前处理共同原因时有效调整有用

在CONFOUND，T和Y的普通相关来自`T←C→Y`路径；以观测到的处理前C分层，完整源两种处理均有非零观察概率，计算`Σ_c P(C=c){E[Y|T=1,C=c]−E[Y|T=0,C=c]}`精确得0。COMBINED图除该后门路径外还存在T→Y真因果路径，普通观察差3/4，调整后恢复真do效应1/2。DIRECT图不含C直接指向Y，调整C不会错误消除真实直接路径，恢复1。这三项仍是**人工图已知、充分测得共同原因、支持性与正确SCM**条件下的数学保证，不能承诺现实观测量已满足这些假设。

### 核心反例3：碰撞点条件化会创造虚假相关

COLLIDER原图`T→K←U→Y`，T与U独立，故T与Y在原人工总体上无条件观察差0，真do效应也0；在全部真来源的K=1条件子样本中，`E[Y|T=1,K=1]=1/2`，`E[Y|T=0,K=1]=1`，其差变为**−1/2**。对碰撞点K分层选择导致路径从原本关闭变成打开，不意味着新的干预因果效果。

这里还存在**正值性缺口**：T=1时K=T OR U总是1，因此`P(T=1,K=0)=0`；不能用缺支持数据冒充可以对K=0/1所有层做可识别的常规后门标准化。程序对此真实约束与d-separation路径开闭分别记录。

### 核心反例4：处理后的中介不能随意作为总效应调整量

MEDIATOR图`T→M→Y`，`M=T xor N`，`Y=M`。人工两态do结果Y均值分别1/4、3/4，真**总因果效应1/2**。但在每个固定M层里，Y由M确定、与T无关，`E[Y|T=1,M]−E[Y|T=0,M]=0`；错误把M视作处理前混杂变量再按P(M)平均，得到错误的**总效应0**。这其实与**控制直接路径的效应为0**一致，但它回答的并不是总效应问题。图的`T⊥Y|M`即使成立，也不足以许可把处理后中介纳入识别总效果的简单后门调整。

## 原生程序、真来源归档与CI

[原生Python程序与38项固定测试](r212_exact_causal_dags.py)独立计算六人工DAG全部原外生来源、实际观察与do干预、两个do效果积分表达式、前处理C后门标准化、碰撞K条件差、处理后M条件差。另以全部无向简单路径标注路径中间节点的碰撞/非碰撞属性，按给定条件变量及后代条件化检验六人工图的有限d-separation关系；图均独立核对无有向环。**这只是固定六个小图的算法审计，不是任意有向图上的一般d-separation因果识别结题。**

[GitHub Actions run39738558762](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39738558762)：Python3.11和3.12各**38测试，总76项全部通过**。第三作业确实生成六世界主结果、44条原来源CSV、88个do结局并核验概率、结构、数学与文件SHA，三job均success，真实原材料由机器人永久写回main提交[e9f92f91](https://github.com/edwardsage419/Psychohistory-Research/commit/e9f92f91dcc155075c6ae7564f14b16a0f1a03aa)。

* [冻结协议](../../protocols/R212_DAG_6_SCM_WORLDS_44_ORIGINAL_EXOGENOUS_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，先于评分提交。
* [完整六SCM机读结果](R212_EXACT_RESULTS.json)，SHA256 `d7e66092f7ea225e627c5c79729d30cc3deef29e4b70b1dd148e92b2d2dd469b`。
* [44条真外生来源与88组do结果](R212_ALL_44_ORIGINAL_SCM_EXOGENOUS_SOURCES.csv)，SHA256 `8fb3565ed2ed94320202587723220cbd3d6bc52c8855e484c875970ceeb65ebc`。
* [原始来源哈希、来源数及结构因果验收记录](R212_FINAL_MACHINE_ACCEPTANCE.json)。
* [事后科学正式结题机读收据](R212_FINAL_ACCEPTANCE_STATUS.json)。

**R212=CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_DAGS**。该结题仅限定于原目录09-003的一项人工因果机制学习，不证明存在任何真实心理、社会或历史中的因果方向。新增E2=0、历史E3=0，R073与PESEN v0.1继续冻结。下一真实原239目录 **09-004 Instrumental Variables（P1）**，研究编号拟R213。继续先完成全部原R模型、再统一分类、最后熔炼。
